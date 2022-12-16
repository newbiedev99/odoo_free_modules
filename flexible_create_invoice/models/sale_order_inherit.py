from odoo import models, fields, api, _
from odoo.exceptions import AccessError
from itertools import groupby
from markupsafe import Markup

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_delivery_order_return(self):
        """ Look for the delivery order return document
            return the source document, product id and quantity done
            
            :return: {'WH/OUT/00017': [('4893-1', 2.0), ('7483-2', 10.0)]}
                    'DOReturnName' : [('product_id', quantity_done)]
            :return: {} if no data
        """
        do_return = {}
        for order in self:
            for delivery_id in order.picking_ids:
                if delivery_id.origin.startswith('Return of ') and delivery_id.state == 'done':
                    key = delivery_id.origin.replace('Return of ', '')
                    if key not in do_return.keys():
                        do_return[key] = []
                    for move_id in delivery_id.move_ids_without_package:
                        product_id = '%s-%s' % (move_id.unique_line, move_id.product_id.id)
                        item = (product_id, move_id.quantity_done)
                        do_return[key].append(item)
        return do_return

    def _prepare_invoice_line_do(self, delivery_ids):
        """
            Looking for product id and quantity done
            
            :param delivery_ids: id of delivery order
            :return: {'3782-1': 6.0} if have data
            :return: {} if no data
        """
        delivery_ids = self.env['stock.picking'].browse(delivery_ids)
        do_returns = self._get_delivery_order_return()
        data = {}
        for delivery_id in delivery_ids:
            for move_id in delivery_id.move_ids_without_package:
                key = '%s-%s' % (move_id.unique_line, move_id.product_id.id)
                if key in data.keys():
                    data[key] += move_id.quantity_done
                else:
                    data[key] = move_id.quantity_done
            if do_returns and delivery_id.name in do_returns.keys(): # Check if Name of Delivery Order in do_returns
                for do_return in do_returns[delivery_id.name]:
                    data[do_return[0]] -= do_return[1] # Reducing the quantity done
        # a = 'a'
        # if a == 'a':
        #     raise AccessError('Maintenance ... ^_^')
        return data

    def _prepare_invoice(self):
        """
            Add the Delivery Order Number to the Customer Invoice
        """
        res = super(SaleOrder, self)._prepare_invoice()
        delivery_ids = self._context.get('delivery_ids', [])
        res['delivery_ids'] = [(6, 0, delivery_ids)]
        return res

    def _create_invoices(self, grouped=False, final=False, date=None):
        if not self.env['account.move'].check_access_rights('create', False):
            try:
                self.check_access_rights('write')
                self.check_access_rule('write')
            except AccessError:
                return self.env['account.move']

        create_from_do = self._context.get('create_from_do', False)
        delivery_ids = self._context.get('delivery_ids', [])
        if create_from_do: # 1) Create invoices with DO.
            data = self._prepare_invoice_line_do(delivery_ids)
            invoice_vals_list = []
            invoice_item_sequence = 0 # Incremental sequencing to keep the lines order on the invoice.
            for order in self:
                order = order.with_company(order.company_id)
                current_section_vals = None
                down_payments = order.env['sale.order.line']

                invoice_vals = order._prepare_invoice()
                invoiceable_lines = order._get_invoiceable_lines(final)

                if not any(not line.display_type for line in invoiceable_lines):
                    continue

                invoice_line_vals = []
                down_payment_section_added = False
                for line in invoiceable_lines:
                    if not down_payment_section_added and line.is_downpayment:
                        # Create a dedicated section for the down payments
                        # (put at the end of the invoiceable_lines)
                        invoice_line_vals.append(
                            (0, 0, order._prepare_down_payment_section_line(
                                sequence=invoice_item_sequence
                            )),
                        )
                        down_payment_section_added = True
                        invoice_item_sequence += 1

                    key = '%s-%s' % (line.unique_line, line.product_id.id)
                    if not line.is_downpayment and key in data.keys():
                        quantity_do = data[key]
                        invoice_line_vals.append(
                            (0, 0, line._prepare_invoice_line_do(
                                sequence=invoice_item_sequence,
                                quantity_do=quantity_do
                            )),
                        )
                        invoice_item_sequence += 1

                invoice_vals['invoice_line_ids'] += invoice_line_vals
                invoice_vals_list.append(invoice_vals)

            if not invoice_vals_list:
                raise self._nothing_to_invoice_error()

            # 2) Manage 'grouped' parameter: group by (partner_id, currency_id).
            if not grouped:
                new_invoice_vals_list = []
                invoice_grouping_keys = self._get_invoice_grouping_keys()
                invoice_vals_list = sorted(
                    invoice_vals_list,
                    key=lambda x: [
                        x.get(grouping_key) for grouping_key in invoice_grouping_keys
                    ]
                )
                for grouping_keys, invoices in groupby(invoice_vals_list, key=lambda x: [x.get(grouping_key) for grouping_key in invoice_grouping_keys]):
                    origins = set()
                    payment_refs = set()
                    refs = set()
                    ref_invoice_vals = None
                    for invoice_vals in invoices:
                        if not ref_invoice_vals:
                            ref_invoice_vals = invoice_vals
                        else:
                            ref_invoice_vals['invoice_line_ids'] += invoice_vals['invoice_line_ids']
                        origins.add(invoice_vals['invoice_origin'])
                        payment_refs.add(invoice_vals['payment_reference'])
                        refs.add(invoice_vals['ref'])
                    ref_invoice_vals.update({
                        'ref': ', '.join(refs)[:2000],
                        'invoice_origin': ', '.join(origins),
                        'payment_reference': len(payment_refs) == 1 and payment_refs.pop() or False,
                    })
                    new_invoice_vals_list.append(ref_invoice_vals)
                invoice_vals_list = new_invoice_vals_list
            if len(invoice_vals_list) < len(self):
                SaleOrderLine = self.env['sale.order.line']
                for invoice in invoice_vals_list:
                    sequence = 1
                    for line in invoice['invoice_line_ids']:
                        line[2]['sequence'] = SaleOrderLine._get_invoice_line_sequence(new=sequence, old=line[2]['sequence'])
                        sequence += 1
            moves = self.env['account.move'].sudo().with_context(default_move_type='out_invoice').create(invoice_vals_list)
            if final:
                moves.sudo().filtered(lambda m: m.amount_total < 0).action_switch_invoice_into_refund_credit_note()
            for move in moves:
                move.message_post_with_view('mail.message_origin_link',
                    values={'self': move, 'origin': move.line_ids.mapped('sale_line_ids.order_id')},
                    subtype_id=self.env.ref('mail.mt_note').id
                )
            return moves
        else: # 1) Create invoices with SO.
            return super(SaleOrder, self)._create_invoices(grouped=grouped, final=final, date=date)
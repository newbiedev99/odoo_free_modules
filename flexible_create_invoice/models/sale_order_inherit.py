from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError
from odoo.tools import float_is_zero
from itertools import groupby

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
            if delivery_id.final_number in do_returns.keys(): # Check if Name of Delivery Order in do_returns
                for do_return in do_returns[delivery_id.final_number]:
                    data[do_return[0]] -= do_return[1] # Reducing the quantity done
        return data

    def _prepare_invoice(self):
        """
            Add the Delivery Order Number to the Customer Invoice
        """
        res = super(SaleOrder, self)._prepare_invoice()
        delivery_ids = self._context.get('delivery_ids', [])
        res['delivery_ids'] = [(6, 0, delivery_ids)]
        return res

    def _create_invoices(self, grouped=False, final=False):
        """
        Create the invoice associated to the SO.
        :param grouped: if True, invoices are grouped by SO id. If False, invoices are grouped by
                        (partner_invoice_id, currency)
        :param final: if True, refunds will be generated if necessary
        :returns: list of created invoices
        """
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')

        # 1) Create invoices.
        create_from_do = self._context.get('create_from_do', False)
        delivery_ids = self._context.get('delivery_ids', [])
        if create_from_do: # 1) Create invoices with DO.
            data = self._prepare_invoice_line_do(delivery_ids)

            invoice_vals_list = []
            for order in self:
                pending_section = None

                # Invoice values.
                invoice_vals = order._prepare_invoice()

                # Invoice line values (keep only necessary sections).
                for line in order.order_line:
                    if line.display_type == 'line_section':
                        pending_section = line
                        continue
                    if float_is_zero(line.qty_to_invoice, precision_digits=precision):
                        continue
                    if line.qty_to_invoice > 0 or (line.qty_to_invoice < 0 and final):
                        if pending_section:
                            invoice_vals['invoice_line_ids'].append((0, 0, pending_section._prepare_invoice_line()))
                            pending_section = None
                        key = '%s-%s' % (line.unique_line, line.product_id.id)
                        if line.is_downpayment and final:
                            invoice_vals['invoice_line_ids'].append((0, 0, line._prepare_invoice_line()))
                        if not line.is_downpayment and key in data.keys():
                            quantity_do = data[key]
                            invoice_vals['invoice_line_ids'].append(
                                (0, 0, line._prepare_invoice_line_do(
                                    quantity_do=quantity_do
                                )),
                            )

                if not invoice_vals['invoice_line_ids']:
                    raise UserError(_('There is no invoiceable line. If a product has a Delivered quantities invoicing policy, please make sure that a quantity has been delivered.'))

                invoice_vals_list.append(invoice_vals)

            if not invoice_vals_list:
                raise UserError(_(
                    'There is no invoiceable line. If a product has a Delivered quantities invoicing policy, please make sure that a quantity has been delivered.'))

            # 2) Manage 'grouped' parameter: group by (partner_id, currency_id).
            if not grouped:
                new_invoice_vals_list = []
                for grouping_keys, invoices in groupby(invoice_vals_list, key=lambda x: (x.get('partner_id'), x.get('currency_id'))):
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
                        payment_refs.add(invoice_vals['invoice_payment_ref'])
                        refs.add(invoice_vals['ref'])
                    ref_invoice_vals.update({
                        'ref': ', '.join(refs),
                        'invoice_origin': ', '.join(origins),
                        'invoice_payment_ref': len(payment_refs) == 1 and payment_refs.pop() or False,
                    })
                    new_invoice_vals_list.append(ref_invoice_vals)
                invoice_vals_list = new_invoice_vals_list

            # 3) Create invoices.
            moves = self.env['account.move'].with_context(default_type='out_invoice').create(invoice_vals_list)
            # 4) Some moves might actually be refunds: convert them if the total amount is negative
            # We do this after the moves have been created since we need taxes, etc. to know if the total
            # is actually negative or not
            if final:
                moves.filtered(lambda m: m.amount_total < 0).action_switch_invoice_into_refund_credit_note()
            for move in moves:
                move.message_post_with_view('mail.message_origin_link',
                    values={'self': move, 'origin': move.line_ids.mapped('sale_line_ids.order_id')},
                    subtype_id=self.env.ref('mail.mt_note').id
                )
            return moves
        else: # 2) Create invoices with SO.
            return super(SaleOrder, self)._create_invoices(grouped=grouped, final=final)
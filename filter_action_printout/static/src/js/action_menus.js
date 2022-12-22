odoo.define('filter_action_printout.ActionMenus', function(require) {
    'use strict';

    const { patch } = require('web.utils');
    const ActionMenus = require('web.ActionMenus');
    
    patch(ActionMenus.prototype, 'filter_action_printout.ActionMenus', {
        async _getFilterPrint(props, activeIds) {
            /**
             * Return 
             *  id of action_report which has the same code_filter as in context
             *  or all id in current action_report
             */
            var code_filter = props.context.default_code_filter;
            if (code_filter){
                var model = 'ir.actions.report';
                // Use an empty array to search for all the records
                var domain = [['id', 'in', activeIds], ['code_filter', 'in', code_filter]];
                // Use an empty array to read all the fields of the records
                var fields = ['id'];
                var buttonPrint = await this.rpc({
                    model: model,
                    method: 'search_read',
                    args: [domain, fields],
                });
                buttonPrint = buttonPrint.map(button => button.id);
                return buttonPrint;
            }
            return activeIds;
        },
        async _setPrintItems(props) {
            const printActions = props.items.print || [];
            const printIds = printActions.map(action => action.id) // Get id in current action_report
            const filterIds = await this._getFilterPrint(props, printIds);
            const printItems = [];
            printActions.forEach(action => {
                if (filterIds.includes(action.id)){
                    printItems.push({ action, description: action.name, key: action.id })
                }
            });
            // const printItems = printActions.map(
            //     action => ({ action, description: action.name, key: action.id })
            // );
            return printItems;
        }
    });
});
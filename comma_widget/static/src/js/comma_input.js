odoo.define('number_widget.DirectComma', function (require) {
    "use strict";

    var core = require('web.core');
    var QWeb = core.qweb;
    var _lt = core._lt;
    var basic_fields = require('web.basic_fields');
    var FieldFloat = basic_fields.FieldFloat;
    var FieldMonetary = basic_fields.FieldMonetary;
    var FieldInteger = basic_fields.FieldInteger;
    var field_registry = require('web.field_registry');

    var FloatDirectComma = FieldFloat.extend({
        descriptions: _lt('Float Direct Comma'),
        events: {
            keyup: '_onKeyUp',
            focusout: '_onFocusOut',
        },
        _onKeyUp: function(e){
            var val = e.target.value;
            val = val.replace(/[^0-9\.]/g, '') // Remove char except digit and .
            var front = val.split('.')[0].replace(/\B(?=(\d{3})+(?!\d))/gm, ',');
            var back = val.match(/\./g) ? '.' + val.split('.')[1].replace(',', '') : '';
            e.target.value = front + back;
        },
        _onFocusOut: function(e){
            var input = ''
            if (e.target.value){
                input = e.target.value.split(',').join('')
            }
            this._setValue(input);
        },
    });

    var IntegerDirectComma = FieldInteger.extend({
        descriptions: _lt('Integer Direct Comma'),
        events: {
            keyup: '_onKeyUp',
            focusout: '_onFocusOut',
        },
        _onKeyUp: function(e){
            var val = e.target.value;
            if (val.length > 1){
                val = val.replace(/^0*/g, '') // Remove 0 in front
            }
            val = val.replace(/[^0-9]/g, '') // Remove char except digit and .
            var front = val.split('.')[0].replace(/\B(?=(\d{3})+(?!\d))/gm, ',');
            e.target.value = front;
        },
        _onFocusOut: function(e){
            var input = ''
            if (e.target.value){
                input = e.target.value.split(',').join('')
            }
            this._setValue(input);
        },
    });

    var MonetaryDirectComma = FieldMonetary.extend({
        descriptions: _lt('Monetary Direct Comma'),
        events: {
            keyup: '_onKeyUp',
            focusout: '_onFocusOut',
        },
        _onKeyUp: function(e){
            var val = e.target.value;
            val = val.replace(/[^0-9\.]/g, '') // Remove char except digit and .
            var front = val.split('.')[0].replace(/\B(?=(\d{3})+(?!\d))/gm, ',');
            var back = val.match(/\./g) ? '.' + val.split('.')[1].replace(',', '') : '';
            e.target.value = front + back;
        },
        _onFocusOut: function(e){
            var input = ''
            if (e.target.value){
                input = e.target.value.split(',').join('')
            }
            this._setValue(input);
        },
    });

    field_registry
        .add('integer_direct_comma', IntegerDirectComma)
        .add('float_direct_comma', FloatDirectComma)
        .add('monetary_direct_comma', MonetaryDirectComma)

    return {
        IntegerDirectComma: IntegerDirectComma,
        FloatDirectComma: FloatDirectComma,
        MonetaryDirectComma: MonetaryDirectComma,
    };

});
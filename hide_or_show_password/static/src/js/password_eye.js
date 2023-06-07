odoo.define('hide_or_show_password.password_eye', function(require) {
    'use strict';
    
    var basic_fields = require('web.basic_fields');
    var InputField = basic_fields.InputField;
    const { patch } = require('web.utils');
    var core = require('web.core');
    var qweb = core.qweb;

    InputField.include({
        _renderEdit: function () {
            this._prepareInput(this.$el);
            if (this.nodeOptions.show_or_hide) {
                if ($(this.$el).length && this.nodeOptions.isPassword){
                    var element = this.$el;
                    var self = this
                    $(document).ready(function(e){
                        var span = $('<span/>').addClass('o_field_translate btn btn-link')
                        var icon = $('<i/>').addClass('fa fa-eye')
                        if ($(element).hasClass('o_field_translate')) {
                            $(element).addClass('o_password_eye')
                            $(span).addClass('o_field_translate_with_button_password_eye')
                        }
                        $(span).append(icon)
                        $(element).after(span)
                        
                        $(icon).click(function(e){
                            if($(element).attr('type') == 'password'){
                                $(icon).removeClass('fa-eye').addClass('fa-eye-slash');
                                $(element).attr('type', 'text')
                            }else{
                                $(icon).removeClass('fa-eye-slash').addClass('fa-eye');
                                $(element).attr('type', 'password')
                            }
                        })
                    })
                }
            }
        },
        _renderReadonly: function () {
            this.$el.text(this._formatValue(this.value));
            if (this.nodeOptions.show_or_hide) {
                if ($(this.$el).length && this.nodeOptions.isPassword){
                    var element = this.$el;
                    var self = this
                    $(document).ready(function(e){
                        var span = $('<span/>').addClass('o_field_translate btn btn-link')
                        var icon = $('<i/>').addClass('fa fa-eye')
                        $(element).attr('style', 'width: 100%; padding-right: 25px')
                        $(span).attr('style', 'margin-left: -35px')
                        $(span).append(icon)
                        $(element).after(span)
                        
                        $(icon).click(function(e){
                            if($(icon).hasClass('fa-eye')){
                                $(icon).removeClass('fa-eye').addClass('fa-eye-slash');
                                $(element).text(self.value);
                            }else{
                                $(icon).removeClass('fa-eye-slash').addClass('fa-eye');
                                $(element).text(self._formatValue(self.value));
                            }
                        })
                    })
                }
            }
        },
    });

});
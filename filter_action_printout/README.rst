Filter Action Printout
=======================

Filter printout actions for visible and invisible.


Installation
============

To install this module, you need to:

go to apps, 
    - install Filter Action Printout


Usage
=====

- Depends this module in your module
- Enter the value of code_filter in ir.actions.report
    Exception 1 :
        .. code-block:: xml
            <record id="id_your_ir_actions_report" model="ir.actions.report">
                <field name="name">Your Report Name</field>
                <field name="model">model.name</field>
                <field name="report_type">qweb-pdf</field>
                <field name="code_filter">your-code</field>
            </record>
    Exception 2 :
        - Go to the report form to be filtered
        - Edit value of field Code Filter
- Add value of action window context with 
    .. code-block:: xml
        default_code_filter: ['code', 'code', 'etc']
- If you don't want the filter/all print action to appear, don't add default_code_filter in the context.


Bug Tracker
===========

If you spotted any issue, help us smashing it by providing a detailed and welcomed feedback here.
contact us for support or help with technical issues. <mailto:newbiedev99@gmail.com>


Credits
=======

Don't forget to give stars and comments in this module


Author
======

Newbie Dev <http://agvenmuharisrifqi.github.io>


Maintainer
==========

Newbie Dev

This module is maintained by the Newbie Dev.

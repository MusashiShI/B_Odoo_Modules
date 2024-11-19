# -*- coding: utf-8 -*-
{
    'name': "odoo_proec",

    'summary': """ Can add servers of proeq and show the status """,

    'description': """
        See the status of proeq servers
    """,

    'author': "Jose Beselga",
    'website': "http://www.beselgamodules.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Services',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
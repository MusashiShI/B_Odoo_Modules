# -*- coding: utf-8 -*-
{
    'name': "Odoo Proeq Monitoring",
    'author': "Jose Beselga - ERPGAP SYSADM JUNIOR",
    'license': "LGPL-3",
    'version': '0.1',
    'category': 'Services',

    'summary': """ Can add servers of proeq and show the status """,

    'description': """
        See the status of proeq servers
    """,


    'website': "http://www.beselgamodules.com",




    'depends': ['base'],


    'data': [

        'views/views.xml',
        'views/templates.xml',
    ],

    'demo': [
        'demo/demo.xml',
    ],
}
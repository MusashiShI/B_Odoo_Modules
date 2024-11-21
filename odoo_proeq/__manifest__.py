# -*- coding: utf-8 -*-
from uaclient.api.u.pro.services.dependencies.v1 import dependencies

{
    "name": "Odoo Proeq Monitoring",
    "author": "Jose Beselga - ERPGAP SYSADM JUNIOR",
    "license": "LGPL-3",
    "version": '0.1',
    "category": "Services",

    'depends': ['base', 'mail'],

    "data": [
        "security/ir.model.access.csv",
        "views/menuview.xml",
        "views/metrics.xml",
        "views/reports.xml",
        "views/menu.xml"

    ]
}
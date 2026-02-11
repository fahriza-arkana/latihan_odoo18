# -*- coding: utf-8 -*-
{
    'name': "Arie Putra Library",

    'summary': "Modul Perpustakaan",

    'description': "Ini Modul Perpustakaan",

    'author': "prasmul-eli",
    'website': "https://prasmul-eli.co/id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/report_paperformat.xml',
        'report/library_book_report_action.xml',
        'report/library_book_report_template.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/library_book_views.xml',
        'views/library_category_views.xml',
        'views/library_author_views.xml',
        'views/res_partner_views.xml',
      
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}


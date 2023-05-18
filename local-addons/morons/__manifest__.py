# -*- coding: utf-8 -*-
{
    'name': "MORONS",

    'summary': """
        Translation Project Management for MercTrans""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Joe Tang",
    'website': "https://merctrans.vn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'project', 'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/project.xml',
        'views/templates.xml',
        'data/languages.xml',
        'data/currencies.xml',
        'data/email_template.xml',
        'data/company_data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

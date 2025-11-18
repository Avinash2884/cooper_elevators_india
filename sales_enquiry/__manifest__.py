

{
    'name': "Sales Enquiry",
    'version': '1.0.0',
    'depends': ['base','crm','sale_management','product','mail'],
    'author': "Unisas ITBusiness Solutions Private Limited",
    'category': 'Sales/CRM',
    'summary': "Manage and track sales enquiries with quantity and pricing details",
    'description': """
        Sales Enquiry Management
        ========================
        This module extends CRM and Sales functionalities to manage enquiries, track lift quantities,
        and integrate with price lists and quotations.
    """,
    'data': [
        'security/ir.model.access.csv',
        'data/price_list_sequence.xml',
        'data/lift_type_data.xml',
        'data/lift_type_data_two.xml',
        'views/crm_inherit_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}


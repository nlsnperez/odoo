{
    'name': 'Estate',
    'version': '1.0',
    'license': 'LGPL-3',
    'category': 'Sales',
    'summary': 'Módulo de gestión inmobiliaria',
    'description': """
        Módulo para gestionar propiedades inmobiliarias
    """,
    'author': 'Nelson Pérez',
    'website': 'google.com',
    'depends': ['base'],
    'data': [
        'views/estate_property_offer_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus_views.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
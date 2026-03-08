{
    'name': 'Clinica veterinaria',
    'version': '1.0',
    'license': 'LGPL-3',
    'category': 'Healthcare',
    'summary': 'Módulo de gestión para citas veterinarias',
    'description': """
        Módulo creado para gestionar las citas de una clínica veterinaria.
        Optimizado para:
        - Gestión de pacientes (mascotas).
        - Gestión de veterinarios.
        - Gestión de citas.
    """,
    'author': 'Nelson Pérez',
    'website': '',
    'depends': ['base'],
    'data': [
        'views/veterinary_appointment_view.xml',
        'views/veterinary_patient_view.xml',
        'views/res_partner_view.xml',
        'views/veterinary_clinic_menus_view.xml',
        'security/ir.model.access.csv',
        ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
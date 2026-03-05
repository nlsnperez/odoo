from odoo import models, fields, api

class UsersInherit(models.Model):
    #Señalar qué modulo se está heredando
    _inherit = 'res.users'
    
    property_ids = fields.One2many(
        'estate.property', #Modelo relacionado
        'salesperson_id', #Campo inverso en 'estate.property'
        string = 'Available Properties',
        domain = [('state', '=', 'new')]        
    )
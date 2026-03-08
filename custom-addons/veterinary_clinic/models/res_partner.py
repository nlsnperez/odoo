from odoo import models, fields, api

class PartnersInherit(models.Model):
    #Señalar qué modulo se está heredando
    _inherit = 'res.partner'
    
    patient_ids = fields.One2many('veterinary.patient', 'owner_id', string='Mascotas del cliente')
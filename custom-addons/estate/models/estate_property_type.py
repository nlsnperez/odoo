from odoo import models, fields

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "name"
    
    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer('Sequence', default=1)
        
    _sql_constraints = [
        ('check_type_name', 'UNIQUE(name)', 'The name of the property type must be unique.')
    ]
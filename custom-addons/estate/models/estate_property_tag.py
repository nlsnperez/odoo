from odoo import models, fields

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"
    
    name = fields.Char(required=True)
    color = fields.Integer()
    
    _sql_constraints = [
        ('check_tag_name', 'UNIQUE(name)', 'The name of the tag must be unique.')
    ]
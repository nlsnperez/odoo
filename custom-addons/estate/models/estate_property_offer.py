from dateutil.relativedelta import relativedelta

from odoo import api, models, fields
from datetime import timedelta

class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    
    price = fields.Float()
    status = fields.Selection(selection=[
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], copy=False, default='refused')
    partner_id = fields.Many2one('res.partner', string='Partner',required=True)
    property_id = fields.Many2one('estate.property', string='Property',required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse="_inverse_date_deadline")
    
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                date = offer.create_date.date()
            else:
                date = fields.Date.today()
                
            offer.date_deadline = date + relativedelta(days=offer.validity)
    
    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date:
                date = offer.create_date.date()
            else:
                date = fields.Date.today()
                
            offer.validity = (offer.date_deadline - date).days
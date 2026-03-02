from dateutil.relativedelta import relativedelta

from odoo import api, models, fields
from datetime import timedelta

from odoo.exceptions import UserError

class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"
    
    price = fields.Float()
    status = fields.Selection(selection=[
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner',required=True)
    property_id = fields.Many2one('estate.property', string='Property',required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse="_inverse_date_deadline")
    
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price >= 0)', 'The price of and offer should be greater than 0.')
    ]
    
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                date = record.create_date.date()
            else:
                date = fields.Date.today()
                
            record.date_deadline = date + relativedelta(days=record.validity)
            
    @api.model
    def create(self, vals):
        # Check if there are existing offers
        if vals.get("property_id") and vals.get("price"):
            #Store the property in a variable
            prop = self.env["estate.property"].browse(vals["property_id"])
            
            # We check if the offer is higher than the existing offers
            if prop.offers_ids:
                #store the highest price of an offer in a variable
                max_offer = max(prop.mapped("offers_ids.price"))
                #compare the new offer price with the highest price stored
                if vals["price"] <= max_offer:
                    #raise an error if offer price is lower than or equal to the highest price
                    raise UserError(f"The offer must be higher than {max_offer}")
            
            #change the property status to "offer_received"    
            prop.state = "offer_received"
        
        #return created record
        return super().create(vals)
    
    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                date = record.date_deadline
            else:
                date = fields.Date.today()
                
            record.validity = (record.date_deadline - date).days
    
    def action_accept(self):
        for record in self:
            if record.property_id.state == 'sold':
                raise UserError('The property is already sold.')
            elif record.status == 'accepted':
                raise UserError('The offer is already accepted.')
            else:
                record.status = 'accepted'
                record.property_id.write({
                    'buyer_id': record.partner_id.id,
                    'selling_price': record.price,
            })
                
    def action_cancel(self):
        for record in self:
            if record.status == 'refused':
                raise UserError('The offer is already refused.')
            else:
                record.status = 'refused'
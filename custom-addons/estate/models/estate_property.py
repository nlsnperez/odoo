from odoo import api, models, fields
from odoo.exceptions import UserError


class Property(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"
    
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
            string='Orientation',
            selection=[('north', 'North'),
                       ('south', 'South'),
                       ('east', 'East'),
                       ('west', 'West')],
            default='north'
        )
    active = fields.Boolean(default=False)
    state = fields.Selection(
        string='Status',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        copy=False,       
    )
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offers_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Float(compute='_compute_total_area')
    best_price = fields.Float(compute='_compute_best_price')
    
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price of property should be greater than 0.'),
        ('check_selling_price', 'CHECK(selling_price > 0)', 'The selling price of property should be greater than 0.'),
    ]
    
    #Método para calcular el área total
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
            
    #Método para calcular el mejor precio
    @api.depends('offers_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offers_ids:
                #Mapeo de los registros para determinar el valor más alto
                record.best_price = max(record.offers_ids.mapped('price'))
            else:
                #Si no hay registros, retorna 0.0
                record.best_price = 0.0
                
    @api.onchange('garden')
    def onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False
            
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            percentage = record.expected_price * 0.9
            if record.selling_price:
                if record.selling_price < percentage:
                    raise UserError('The selling price cannot be less than 90% of the expected price.')
                
    @api.ondelete(at_uninstall=False)
    def _unlink_if_property_state(self):
        for record in self:
            if record.state != 'new' and record.state != 'canceled':
                raise UserError('Cannot delete property unless is in "New" or "Canceled" state.')
            
    def action_cancel(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError('The property is already canceled.')
            elif record.state == 'sold':
                raise UserError('The property is already sold.')
            else:
                record.state = 'canceled'
    
    def action_sold(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('The property is already sold.')
            elif record.state == 'canceled':
                raise UserError('You cannot sell a canceled property.')
            else:
                record.state = 'sold'
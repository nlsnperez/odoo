from odoo import models, fields, api

class Property(models.Model):
    _inherit = 'estate.property'
    
    def action_sold(self):
        res = super().action_sold()
        
        for property in self:
            #Checkear si la propiedad cuenta con un comprador
            if property.buyer_id and property.selling_price:
                
                #Líneas de las facturas
                invoice_lines = [
                    (0, 0, {
                        'name': f'6% of the selling price',
                        'quantity': '1',
                        'price_unit': property.selling_price * 0.06
                    }),
                    (0, 0, {
                        'name': f'Administrative fees',
                        'quantity': '1',
                        'price_unit': 100
                    })
                ]
                
                #Diccionario de valores
                invoice_vals = {
                    'partner_id': property.buyer_id.id,
                    'move_type': 'out_invoice',
                    'invoice_date': fields.Date.today(),
                    'invoice_line_ids': invoice_lines
                }
                
                invoice = self.env['account.move'].create(invoice_vals)         
        
            print(f'Propiedad {self.name} marcada como vendida exitosamente')
        
        return res
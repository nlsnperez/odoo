from odoo import api, models, fields

class VeterinaryAppointment(models.Model):
    _name = 'veterinary.appointment'
    _description = 'Veterniary Appointment'
    
    # CAMPOS DE REFERENCIA
    name = fields.Char(string='Referencia', default='Nueva cita', readonly=True)
    active = fields.Boolean(string='Activo', default=True)
    priority = fields.Selection(string='Prioridad', selection=[
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high', 'Alta'),
        ('emergency', 'Emergencia')
    ], default='low')
    
    # CAMPOS DE RELACIONES
    patient_id = fields.Many2one('veterinary.patient', string='Paciente', required=True)
    owner_id = fields.Many2one('res.partner', string='Dueño', related='patient_id.owner_id', store=True)
    veterinarian_id = fields.Many2one('res.users', string='Veterinario')
    
    # CAMPOS DE FECHAS
    appointment_date = fields.Date(string='Fecha de la cita', required=True)
    appointment_time = fields.Float(string='Hora de la cita', required=True)
    duration = fields.Float(string='Duración (horas)', default=1.5, readonly=True)
    end_time = fields.Float(string='Hora de finalización', compute='_compute_end_time', store=True)
    
    #CAMPOS DE ESTADO
    state = fields.Selection(string='Estado', selection=[
        ('scheduled', 'Programada'),
        ('confirmed', 'Confirmada'),
        ('in_progress', 'En progreso'),
        ('completed', 'Completada'),
        ('cancelled', 'Cancelada'),
    ])
    cancelled_by_id = fields.Many2one('res.users', string='Cancelado por', default=lambda self: self.env.user)
    cancelled_date = fields.Date(string='Fecha de cancelación')
        
    @api.depends('appointment_time')
    def _compute_end_time(self):
        for record in self:
            if record.appointment_time:
                record.end_time = record.appointment_time + 1.5
            else:
                record.end_time = 0
    
        
    
    
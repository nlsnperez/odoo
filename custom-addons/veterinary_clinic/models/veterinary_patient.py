from odoo import api, models, fields

class VeterinaryPatient(models.Model):
    _name = 'veterinary.patient'
    _description = 'Veterinary Patient'
    
    # CAMPOS GENERALES
    name = fields.Char(string='Nombre del paciente', required=True)    
    species = fields.Selection(string = 'Especie', selection=[
        ('dog', 'Perro'),
        ('cat', 'Gato'),
        ('bunny', 'Conejo'),
        ('fish', 'Pez'),
        ('hamster', 'Hámster'),
        ('bird', 'Pájaro'),
        ('lizard', 'Lagarto'),
        ('other', 'Otra')
    ], required=True)    
    breed = fields.Char(string='Raza')    
    color = fields.Char(string='Pelaje')    
    gender = fields.Selection(string='Género', selection=[
        ('male', 'Macho'),
        ('female', 'Hembra'),
        ('unknown', 'Desconocido'),
    ], required=True)
    
    #CAMPOS DE EDAD
    birth_date = fields.Date(string = 'Fecha de nacimiento')
    age = fields.Integer(string='Edad', compute='_compute_patient_age', store=True)
    death_date = fields.Date(string='Fecha de defunción')
    is_deceased = fields.Boolean(string='Fallecido')
    
    #CAMPOS DE PESO
    weight = fields.Float(string='Peso (kg)')
    #RECORDATORIO: AGREGAR UN CAMPO PARA VISUALIZAR LOS CAMBIOS DE PESO
    
    #CAMPOS DE CONTACTO
    is_stray = fields.Boolean(string='Es callejero')
    owner_id = fields.Many2one('res.partner', string='Dueño')
    veterinarian_id = fields.Many2one('res.users', string='Veterinario asignado')
    
    @api.depends('birth_date')
    #Método para calcular la edad del paciente
    def _compute_patient_age(self):
        #Iterar sobre los registros
        for record in self:
            #Verificar que la fecha esté definida
            if record.birth_date:
                #Calcular la edad
                age = fields.Date.today().year - record.birth_date.year
                #Asignar la edad al campo correspondiente
                record.age = age
            else:
                record.age = 0
            
    
    
    
    
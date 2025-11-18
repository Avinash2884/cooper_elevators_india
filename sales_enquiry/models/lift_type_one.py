from odoo import models, fields, api , _

class LiftType(models.Model):
    _name = 'lift.type'
    _description = 'Lift Type'

    name = fields.Char(string="Lift Type", required=True)
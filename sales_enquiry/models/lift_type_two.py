from odoo import models, fields, api , _

class LiftTypeTwo(models.Model):
    _name = 'lift.type.two'
    _description = 'Lift Type II'

    name = fields.Char(string="Lift Type II", required=True)
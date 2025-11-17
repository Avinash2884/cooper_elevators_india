from odoo import models, fields

class QuotationTemplateCrm(models.Model):
    _name = "quotation.template.crm"
    _description = "Quotation Template CRM"

    section_heading = fields.Char("Section Heading")

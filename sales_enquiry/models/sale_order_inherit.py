from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    crm_template_id = fields.Many2one(
        "quotation.template.crm",
        string="Quotation Template"
    )

    def _confirmation_error_message(self):
        """Override to allow confirmation even if no product is set."""
        self.ensure_one()
        # Skip all validation checks
        return False

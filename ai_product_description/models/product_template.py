from odoo import models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def action_generate_ai_description(self):
        """Open wizard to generate AI description"""
        self.ensure_one()

        return {
            'name': 'Generate Description with AI',
            'type': 'ir.actions.act_window',
            'res_model': 'generate.description.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_product_id': self.id,
            }
        }

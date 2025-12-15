from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class GenerateDescriptionWizard(models.TransientModel):
    _name = 'generate.description.wizard'
    _description = 'Generate Product Description with AI'

    product_id = fields.Many2one(
        'product.template',
        string='Product',
        required=True,
        readonly=True
    )

    template_type = fields.Selection(
        [
            ('brief', 'Brief (50 words)'),
            ('standard', 'Standard (100 words)'),
            ('detailed', 'Detailed (200 words)'),
        ],
        string='Template',
        default='standard',
        required=True,
        help='Select the length and style of the description'
    )

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('generating', 'Generating...'),
            ('generated', 'Generated'),
            ('error', 'Error'),
        ],
        string='State',
        default='draft',
        required=True
    )

    generated_description = fields.Html(
        string='Generated Description',
        help='AI-generated product description. You can edit it before saving.'
    )

    error_message = fields.Text(
        string='Error Message',
        readonly=True
    )

    token_usage = fields.Char(
        string='Token Usage',
        readonly=True,
        help='Number of tokens used for this generation'
    )

    @api.model
    def default_get(self, fields_list):
        """Set default values when wizard opens"""
        res = super().default_get(fields_list)

        # Get active product from context
        active_id = self.env.context.get('active_id')
        if active_id:
            res['product_id'] = active_id

        return res

    def action_generate(self):
        """Generate description using OpenAI"""
        self.ensure_one()

        # Update state to generating
        self.write({
            'state': 'generating',
            'error_message': False,
            'generated_description': '<p class="text-muted"><i class="fa fa-spinner fa-spin"/> Generating description with AI...</p>',
        })

        # Force commit to show the loading state
        self.env.cr.commit()

        try:
            # Get OpenAI service
            openai_service = self.env['openai.service']

            # Generate description
            result = openai_service.generate_description(
                self.product_id,
                self.template_type
            )

            if result['success']:
                # Format the description as HTML
                description_html = f"<p>{result['description']}</p>"

                # Format token usage
                usage = result.get('usage', {})
                token_info = f"Tokens used: {usage.get('total_tokens', 0)} (Prompt: {usage.get('prompt_tokens', 0)}, Completion: {usage.get('completion_tokens', 0)})"

                self.write({
                    'state': 'generated',
                    'generated_description': description_html,
                    'token_usage': token_info,
                    'error_message': False,
                })

                _logger.info(f"Successfully generated description for product {self.product_id.name}")

            else:
                # Handle error
                self.write({
                    'state': 'error',
                    'error_message': result.get('error', 'Unknown error occurred'),
                    'generated_description': False,
                })

                _logger.error(f"Failed to generate description: {result.get('error')}")

        except Exception as e:
            _logger.error(f"Unexpected error in wizard: {str(e)}", exc_info=True)
            self.write({
                'state': 'error',
                'error_message': str(e),
                'generated_description': False,
            })

        # Return action to refresh the wizard
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'generate.description.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
            'context': self.env.context,
        }

    def action_regenerate(self):
        """Regenerate description with same or different template"""
        return self.action_generate()

    def action_use_description(self):
        """Save the generated description to the product"""
        self.ensure_one()

        if not self.generated_description:
            raise UserError(_('No description generated yet. Please generate one first.'))

        # Update product description
        self.product_id.write({
            'description_sale': self.generated_description
        })

        _logger.info(f"Description saved to product {self.product_id.name}")

        # Show success notification
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success!'),
                'message': _('Product description has been updated successfully.'),
                'type': 'success',
                'sticky': False,
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }

    def action_cancel(self):
        """Close wizard without saving"""
        return {'type': 'ir.actions.act_window_close'}

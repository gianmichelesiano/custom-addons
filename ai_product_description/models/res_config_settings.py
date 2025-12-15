from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    openai_api_key = fields.Char(
        string='OpenAI API Key',
        config_parameter='ai_product_description.openai_api_key',
        help='Your OpenAI API key. Get one at https://platform.openai.com/api-keys'
    )

    openai_model = fields.Selection(
        [
            ('gpt-4o-mini', 'GPT-4o Mini (Recommended - Fast & Cheap)'),
            ('gpt-4o', 'GPT-4o (More Accurate, More Expensive)'),
            ('gpt-3.5-turbo', 'GPT-3.5 Turbo (Legacy)'),
        ],
        string='OpenAI Model',
        default='gpt-4o-mini',
        config_parameter='ai_product_description.openai_model',
        help='Select the AI model to use for generation'
    )

    openai_temperature = fields.Float(
        string='Creativity Level',
        default=0.7,
        config_parameter='ai_product_description.openai_temperature',
        help='0.0 = More focused and deterministic, 1.0 = More creative and varied (Range: 0-1)'
    )

    openai_max_tokens = fields.Integer(
        string='Max Tokens',
        default=500,
        config_parameter='ai_product_description.openai_max_tokens',
        help='Maximum length of generated descriptions (higher = longer but more expensive)'
    )

    def action_test_openai_connection(self):
        """Test the OpenAI API connection"""
        self.ensure_one()

        if not self.openai_api_key:
            raise UserError(_('Please enter your OpenAI API key first.'))

        try:
            import openai

            # Configure OpenAI client
            client = openai.OpenAI(api_key=self.openai_api_key)

            # Test with a simple completion
            response = client.chat.completions.create(
                model=self.openai_model or 'gpt-4o-mini',
                messages=[
                    {"role": "user", "content": "Say 'Connection successful' if you can read this."}
                ],
                max_tokens=10,
                temperature=0.1
            )

            if response.choices:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _('Success!'),
                        'message': _('OpenAI API connection successful! Your API key is working correctly.'),
                        'type': 'success',
                        'sticky': False,
                    }
                }
            else:
                raise UserError(_('Unexpected response from OpenAI API.'))

        except ImportError:
            raise UserError(_(
                'OpenAI Python package is not installed.\n'
                'Please install it using: pip install openai'
            ))
        except openai.AuthenticationError:
            raise UserError(_(
                'Authentication failed. Please check your API key.\n'
                'Get your API key at: https://platform.openai.com/api-keys'
            ))
        except openai.RateLimitError:
            raise UserError(_(
                'Rate limit exceeded. Please check your OpenAI account quota.\n'
                'Visit: https://platform.openai.com/account/billing'
            ))
        except openai.APIConnectionError:
            raise UserError(_(
                'Could not connect to OpenAI API. Please check your internet connection.'
            ))
        except Exception as e:
            _logger.error(f"OpenAI API test failed: {str(e)}")
            raise UserError(_(
                'Failed to connect to OpenAI API.\n'
                'Error: %s'
            ) % str(e))

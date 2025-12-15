from odoo import models, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class OpenAIService(models.AbstractModel):
    """Service for OpenAI API integration"""
    _name = 'openai.service'
    _description = 'OpenAI Service'

    # Template definitions
    TEMPLATES = {
        'brief': {
            'name': 'Brief (50 words)',
            'max_words': 50,
            'style': 'concise and punchy',
            'description': 'Short and impactful description, perfect for product listings'
        },
        'standard': {
            'name': 'Standard (100 words)',
            'max_words': 100,
            'style': 'balanced and informative',
            'description': 'Balanced description with key features and benefits'
        },
        'detailed': {
            'name': 'Detailed (200 words)',
            'max_words': 200,
            'style': 'comprehensive and persuasive',
            'description': 'Comprehensive description with full details and storytelling'
        }
    }

    def _get_api_credentials(self):
        """Get OpenAI API credentials from settings"""
        IrConfigParameter = self.env['ir.config_parameter'].sudo()

        api_key = IrConfigParameter.get_param('ai_product_description.openai_api_key')
        model = IrConfigParameter.get_param('ai_product_description.openai_model', 'gpt-4o-mini')
        temperature = float(IrConfigParameter.get_param('ai_product_description.openai_temperature', '0.7'))
        max_tokens = int(IrConfigParameter.get_param('ai_product_description.openai_max_tokens', '500'))

        if not api_key:
            raise UserError(_(
                'OpenAI API key not configured.\n\n'
                'Please go to Settings → General Settings → AI Product Description '
                'and configure your API key.'
            ))

        return {
            'api_key': api_key,
            'model': model,
            'temperature': temperature,
            'max_tokens': max_tokens,
        }

    def _build_prompt(self, product, template_key='standard'):
        """Build the prompt for OpenAI based on product data and template"""
        template = self.TEMPLATES.get(template_key, self.TEMPLATES['standard'])

        # Collect product information
        product_info = {
            'name': product.name or 'Unknown Product',
            'category': product.categ_id.complete_name if product.categ_id else 'No category',
            'sale_price': product.list_price,
            'currency': product.currency_id.name if product.currency_id else 'EUR',
            'attributes': self._get_product_attributes(product),
            'existing_description': product.description_sale or '',
        }

        # Build the prompt
        prompt = f"""You are an expert e-commerce copywriter. Generate a product description with these requirements:

Product Information:
- Name: {product_info['name']}
- Category: {product_info['category']}
- Price: {product_info['sale_price']} {product_info['currency']}
{f"- Attributes: {product_info['attributes']}" if product_info['attributes'] else ""}

Requirements:
- Length: Approximately {template['max_words']} words
- Style: {template['style']}
- Tone: Professional, engaging, and persuasive
- Format: Clean paragraph(s), no special characters or markdown
- Focus: Highlight key features, benefits, and value proposition
- SEO: Include relevant keywords naturally

{f"Current description (use as reference but create new content): {product_info['existing_description'][:200]}" if product_info['existing_description'] else ""}

Generate only the product description text, without any preamble or explanation."""

        return prompt

    def _get_product_attributes(self, product):
        """Extract product attributes as a readable string"""
        attributes = []

        if hasattr(product, 'product_template_attribute_value_ids'):
            for attr_value in product.product_template_attribute_value_ids:
                attributes.append(f"{attr_value.attribute_id.name}: {attr_value.name}")

        return ', '.join(attributes) if attributes else ''

    def generate_description(self, product, template_key='standard'):
        """
        Generate product description using OpenAI API

        Args:
            product: product.template record
            template_key: str ('brief', 'standard', or 'detailed')

        Returns:
            dict: {
                'success': bool,
                'description': str,
                'error': str (if success=False),
                'usage': dict (token usage info)
            }
        """
        try:
            # Import OpenAI
            try:
                import openai
            except ImportError:
                return {
                    'success': False,
                    'error': _(
                        'OpenAI Python package not installed.\n'
                        'Please install it: pip install openai'
                    ),
                    'description': '',
                }

            # Get credentials
            credentials = self._get_api_credentials()

            # Build prompt
            prompt = self._build_prompt(product, template_key)

            _logger.info(f"Generating description for product '{product.name}' using template '{template_key}'")

            # Call OpenAI API
            client = openai.OpenAI(api_key=credentials['api_key'])

            response = client.chat.completions.create(
                model=credentials['model'],
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert e-commerce copywriter specializing in product descriptions."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=credentials['temperature'],
                max_tokens=credentials['max_tokens'],
            )

            # Extract the generated description
            if response.choices and len(response.choices) > 0:
                description = response.choices[0].message.content.strip()

                # Get usage information
                usage = {
                    'prompt_tokens': response.usage.prompt_tokens if response.usage else 0,
                    'completion_tokens': response.usage.completion_tokens if response.usage else 0,
                    'total_tokens': response.usage.total_tokens if response.usage else 0,
                }

                _logger.info(
                    f"Successfully generated description for '{product.name}'. "
                    f"Tokens used: {usage['total_tokens']}"
                )

                return {
                    'success': True,
                    'description': description,
                    'error': '',
                    'usage': usage,
                }
            else:
                return {
                    'success': False,
                    'error': _('OpenAI returned an empty response.'),
                    'description': '',
                }

        except openai.AuthenticationError:
            _logger.error("OpenAI authentication failed")
            return {
                'success': False,
                'error': _(
                    'Authentication failed. Please check your API key in Settings.\n'
                    'Go to: Settings → General Settings → AI Product Description'
                ),
                'description': '',
            }

        except openai.RateLimitError:
            _logger.error("OpenAI rate limit exceeded")
            return {
                'success': False,
                'error': _(
                    'Rate limit exceeded. Your OpenAI account has reached its quota.\n'
                    'Please check your billing at: https://platform.openai.com/account/billing'
                ),
                'description': '',
            }

        except openai.APIConnectionError:
            _logger.error("OpenAI API connection error")
            return {
                'success': False,
                'error': _(
                    'Could not connect to OpenAI API. Please check your internet connection.'
                ),
                'description': '',
            }

        except openai.APIError as e:
            _logger.error(f"OpenAI API error: {str(e)}")
            return {
                'success': False,
                'error': _('OpenAI API error: %s') % str(e),
                'description': '',
            }

        except Exception as e:
            _logger.error(f"Unexpected error generating description: {str(e)}", exc_info=True)
            return {
                'success': False,
                'error': _('Unexpected error: %s') % str(e),
                'description': '',
            }

    def get_available_templates(self):
        """Return list of available templates"""
        return [
            {
                'key': key,
                'name': template['name'],
                'description': template['description'],
            }
            for key, template in self.TEMPLATES.items()
        ]

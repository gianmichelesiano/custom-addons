{
    'name': 'AI Product Description Generator',
    'version': '19.0.1.0.0',
    'category': 'Sales/E-commerce',
    'summary': 'Generate professional product descriptions using AI (OpenAI GPT)',
    'description': """
AI Product Description Generator
=================================

Automatically generate professional product descriptions using OpenAI's GPT models.

Key Features:
-------------
* One-click AI description generation
* 3 predefined templates (Brief, Standard, Detailed)
* Preview and edit before saving
* Secure API key configuration
* Error handling and user feedback
* Works with existing product data

Perfect for:
-----------
* E-commerce stores with many products
* Saving time on content creation
* Maintaining consistent product descriptions
* Improving SEO with quality content

Requirements:
------------
* OpenAI API key (Bring Your Own Key - BYOK)
* Active internet connection

Cost: ~€0.02 per description (paid directly to OpenAI)
    """,
    'author': 'Gianmichele Siano',
    'website': 'https://github.com/bandigare',
    'license': 'LGPL-3',
    'price': 29.00,
    'currency': 'EUR',

    'depends': [
        'base',
        'product',
        'sale_management',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/product_template_views.xml',
        'wizard/generate_description_wizard_views.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'ai_product_description/static/src/css/styles.css',
        ],
    },

    'images': [
        'static/description/icon.png',
        'static/description/main_screenshot.png',
        'static/description/config_screenshot.png',
        'static/description/wizard_screenshot.png',
    ],

    'external_dependencies': {
        'python': ['openai'],
    },

    'installable': True,
    'application': False,
    'auto_install': False,
}

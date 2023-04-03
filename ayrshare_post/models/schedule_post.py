# -*- coding: utf-8 -*-

from odoo import models, fields, api

class schedule_post(models.Model):
    _name = 'schedule.post'
    _description = 'Schedule Post'
    _inherit = ['mail.thread', 'mail.activity.mixin']


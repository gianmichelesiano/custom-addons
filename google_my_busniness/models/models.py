# -*- coding: utf-8 -*-

from odoo import models, fields, api


class google_my_busniness(models.Model):
    _name = 'google_my_busniness.google_my_busniness'
    _description = 'Google My Business'

    displayName = fields.Char(string='Display Name')
    transale_comment = fields.Text(string='Translated Comment')
    orignal_comment = fields.Text(string='Original Comment')
    createTime = fields.Datetime(string='Created On', default=fields.Datetime.now)
    updateTime = fields.Datetime(string='Last Updated On', default=fields.Datetime.now)
    name = fields.Char(string='Name')
    google_my_business_id = fields.Char(string='Google My Business ID')



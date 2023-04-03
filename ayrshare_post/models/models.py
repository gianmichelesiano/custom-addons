# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ayrshare_post(models.Model):
    _name = 'ayrshare.post'
    _description = 'Ayrsharce Post'

    title = fields.Char(string='Title')
    image = fields.Binary(string='Image')
    description = fields.Text(string='Description')
    platform = fields.Selection([('facebook', 'Facebook'), ('instagram', 'Instagram')])


    def action_test_button(self):
        print("capocchia")
    
    
    def action_test_button_sec(self):
        print("capocchia2222")


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
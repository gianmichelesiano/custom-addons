# -*- coding: utf-8 -*-

from odoo import models, fields, api


class google_my_busniness(models.Model):
    _name = 'google_my_busniness.google_my_busniness'
    _description = 'Google My Business'

    displayName = fields.Char(string='Display Name')
    transale_comment = fields.Text(string='Translated Comment')
    orignal_comment = fields.Text(string='Original Comment')
    createTime = fields.Text(string='Created On')
    updateTime = fields.Text(string='Last Updated On')
    name = fields.Char(string='Name')
    google_my_business_id = fields.Char(string='Google My Business ID')


    @api.model_create_multi
    def create(self, vals):
        res = super().create(vals)
        print(res)
        if res:
            for item in res:
                reply_vals = {
                     #'google_business_id': res.id,
                    'displayName': item.displayName,
                    'transale_comment': item.transale_comment,
                    'orignal_comment': item.orignal_comment,
                    'createTime': item.createTime,
                    'updateTime': item.updateTime,
                    'google_my_business_id': item.google_my_business_id,
                    # copiare le informazioni necessarie dal record `GoogleBusiness` al record `GoogleBusinessReply`
                }
                self.env['google_my_busniness.google_my_busniness_reply'].create(reply_vals)
        return res



class google_my_busniness_reply(models.Model):
    _name = 'google_my_busniness.google_my_busniness_reply'
    _description = 'Google My Business replay'

    displayName = fields.Char(string='Display Name')
    transale_comment = fields.Text(string='Translated Comment')
    orignal_comment = fields.Text(string='Original Comment')
    createTime = fields.Text(string='Created On')
    updateTime = fields.Text(string='Last Updated On')
    name = fields.Char(string='Name')
    google_my_business_id = fields.Char(string='Google My Business ID')
from odoo import models, fields, api
from ..controllers.ayrshare_service import AyrshareService


class ayrshare_latest(models.Model):
    _name = 'ayrshare_latest.ayrshare_latest'
    _description = 'Ayrshare'

    text = fields.Char(string='Post Text')
    media = fields.Binary(string='Post Media')
    platforms = fields.Selection([('facebook', 'Facebook'), ('twitter', 'Twitter')], string='Post Platforms')

    

    def action_test_button(self):
        print("capocchia")

    def publish_post(self):
        # Crea una nuova istanza del servizio AyrshareService
        ayrshare_service = AyrshareService()

        # Invia la richiesta di pubblicazione del post per ogni record selezionato
        for post in self:
            response = ayrshare_service.publish_post(post.text, post.media, post.platforms)
            # Gestisci la risposta delle API di Ayrshare come necessario

        # Aggiorna il record del post per indicare che è stato pubblicato
        self.write({'published': True})
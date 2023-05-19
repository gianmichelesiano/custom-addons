import requests
import json


class AyrshareService():
    def __init__(self):
        self.base_url = 'https://api.ayrshare.com'
        self.headers = {'Authorization': 'Bearer your_api_key_here'}

    def publish_post(self, post_text, post_media, post_platforms):
        # Live API Key
        headers = {'Content-Type': 'application/json', 
                'Authorization': 'Bearer X9QAWER-X8MM9R4-QR1M6YS-VZSMYDW'}
        
        payload = {
            "post": post_text,
            "platforms": ["facebook"],
            "mediaUrls": ["https://img.ayrshare.com/012/gb.jpg"],
        }

        # Effettua la richiesta POST alle API di Ayrshare per pubblicare il post
        r = requests.post('https://app.ayrshare.com/api/post', 
            json=payload, 
            headers=headers)

        print(r.text)
        print("postResult")
        return True
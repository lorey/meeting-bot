import requests

import config


class Hubspot(object):
    api_key = None

    def __init__(self, api_key):
        self.api_key = api_key

    def find_cantact_by_email(self, email):
        r = requests.get('https://api.hubapi.com/contacts/v1/contact/email/%s/profile?hapikey=%s' % (email, self.api_key))
        print(r.json())

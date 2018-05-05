import requests


class Hubspot(object):
    api_key = None

    def __init__(self, api_key):
        self.api_key = api_key

    def find_contact_by_email(self, email):
        endpoint = 'https://api.hubapi.com/contacts/v1/contact/email/%s/profile?hapikey=%s'
        r = requests.get(endpoint % (email, self.api_key))
        return r.json()

    def push_note(self, email, note):
        contact = self.find_contact_by_email(email)

        if contact['status'] == 'error':
            raise RuntimeError('Contact not found: %s' % contact)

        endpoint = 'https://api.hubapi.com/engagements/v1/engagements?hapikey=%s' % self.api_key

        data = {
            "engagement": {
                "active": True,
                # "ownerId": 1,
                "type": "NOTE",
                # "timestamp": 1409172644778
            },
            "associations": {
                "contactIds": [contact['vid']],
                "companyIds": [],
                "dealIds": [],
                "ownerIds": [],
            },
            "metadata": {
                "body": note,
            }
        }

        response = requests.post(endpoint, json=data)
        return response.json()

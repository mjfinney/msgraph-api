import json

import requests

from msgraph.constants import GRAPH_URL, GRAPH_VERSION, LOGIN_URL, LOGIN_VERSION, LOGIN_ENDPOINTS, GRAPH_ENDPOINTS


class Sharepoint(object):

    def __init__(self, client):
        self.client = client
        self.site = None

    def getSitesList(self):
        sitesList = []
        endpoint = self.client.getEndpoint('list_sites')
        response = requests.get(endpoint)
        if response.ok:
            data = json.loads(response.text)
            for site in data.get('value'):
                sitesList.append(SharepointSite(**site))

        return sitesList

class SharepointSite(object):

    def __init__(self, **kwargs):
        self.siteId = kwargs.get('id')
        self.name = kwargs.get('name')
        self.displayName = kwargs.get('displayName')
        self.description = kwargs.get('description')
        self.webUrl = kwargs.get('webUrl')
        self.lastModifiedDateTime = kwargs.get('lastModifiedDateTime')
        self.createdDateTime = kwargs.get('createdDateTime')

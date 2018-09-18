import json

import requests

from msgraph.constants import GRAPH_URL, GRAPH_VERSION, LOGIN_URL, LOGIN_VERSION, LOGIN_ENDPOINTS, GRAPH_ENDPOINTS


class Client(object):

    def __init__(self, appId, tenant, secret):
        self.appId = appId
        self.tenant = tenant
        self.secret = secret

    def getEndpoint(self, path):
        endpoint = GRAPH_ENDPOINTS.get(path)
        if endpoint:
            endpoint = GRAPH_URL + endpoint
            endpoint = endpoint.format(tenant=self.tenant, version=GRAPH_VERSION)
        else:
            endpoint = LOGIN_ENDPOINTS.get(path)
            if endpoint:
                endpoint = LOGIN_URL + endpoint
                endpoint = endpoint.format(tenant=self.tenant, version=LOGIN_VERSION)
        return endpoint

    def getToken(self, grant_type='client_credentials', scope='https://graph.microsoft.com/.default'):
        data = {'client_id': self.appId,
                'scope': scope,
                'client_secret': self.secret,
                'grant_type': grant_type,
                }
        response = requests.post(self.getEndpoint('token'), data)
        if response.ok:
            return json.loads(response.text)
        else:
            return None

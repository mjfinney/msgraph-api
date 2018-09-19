from datetime import datetime, timedelta
import json

import requests

from msgraph.constants import GRAPH_URL, GRAPH_VERSION, LOGIN_URL, LOGIN_VERSION, LOGIN_ENDPOINTS, GRAPH_ENDPOINTS


class Client(object):

    def __init__(self, appId, tenant, secret):
        self.appId = appId
        self.tenant = tenant
        self.secret = secret

    def getEndpoint(self, path, **kwargs):
        endpoint = GRAPH_ENDPOINTS.get(path)
        if endpoint:
            endpoint = GRAPH_URL + endpoint
            endpoint = endpoint.format(tenant=self.tenant, version=GRAPH_VERSION, **kwargs)
        else:
            endpoint = LOGIN_ENDPOINTS.get(path)
            if endpoint:
                endpoint = LOGIN_URL + endpoint
                endpoint = endpoint.format(tenant=self.tenant, version=LOGIN_VERSION, **kwargs)
        return endpoint

    def getResponse(self, path, data):
        pass

    def getToken(self, grant_type='client_credentials', scope='https://graph.microsoft.com/.default'):
        data = {'client_id': self.appId,
                'scope': scope,
                'client_secret': self.secret,
                'grant_type': grant_type,
                }
        response = requests.post(self.getEndpoint('token'), data)
        if response.ok:
            return Token(response.text)
        else:
            return None

class Token(object):

    def __init__(self, data):
        self.data = data
        data_dict = json.loads(data)
        self.token_type = data_dict.get('token_type')
        self.expires_in = data_dict.get('expires_in')
        self.access_token = data_dict.get('access_token')
        self.expire_date = datetime.now() + timedelta(seconds=self.expires_in)

    @property
    def expired(self):
        return self.expire_date < datetime.now()

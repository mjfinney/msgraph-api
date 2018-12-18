from datetime import datetime, timedelta
import json

import requests

from msgraph.constants import GRAPH_URL, GRAPH_VERSION, LOGIN_URL, LOGIN_VERSION, LOGIN_ENDPOINTS, GRAPH_ENDPOINTS


class Client(object):

    def __init__(self, appId, tenant, secret, token=None):
        self.appId = appId
        self.tenant = tenant
        self.secret = secret
        self.token = token

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

    def getResponse(self, endpoint, **kwargs):
        if (self.token == None) or (datetime.now() > self.token.expire_date):
            self.token = self.getToken()
        headers = {'Authorization': self.token.token_type + ' ' + self.token.access_token}

        extra_headers = kwargs.get('headers', {})
        method = kwargs.get('method', 'GET')
        if extra_headers:
            if method == 'PUT' and not extra_headers.get('Content-Type'):
                extra_headers['Content-Type'] = 'application/json'
            headers.update(extra_headers)
        if method == 'PUT':
            return requests.put(self.getEndpoint(endpoint, **kwargs),
                        headers=headers,
                        data=kwargs.get('data', ''))
        if endpoint == 'next':
            return requests.get(kwargs.get('url'), headers=headers)

        return requests.get(self.getEndpoint(endpoint, **kwargs),
                            headers=headers)

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

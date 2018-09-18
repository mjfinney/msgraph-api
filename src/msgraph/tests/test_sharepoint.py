import json

from mock import Mock, patch
import requests_mock

from msgraph.client import Client


def test_client_getToken():

    appId = '535fb089-9ff3-47b6-9bfb-4f1264799865'
    tenant = 'testTenant'
    secret = 'qWgdYAmab0YSkuL1qKv5bPX'

    client = Client(appId, tenant, secret)

    shouldBe = 'https://login.microsoftonline.com/testTenant/oauth2/v2.0/token'
    assert client.getEndpoint('token') == shouldBe

    shouldBe = 'https://login.microsoftonline.com/testTenant/adminconsent'
    assert client.getEndpoint('adminConsent') == shouldBe

@requests_mock.Mocker()
def test_getting_token(m):

    appId = '535fb089-9ff3-47b6-9bfb-4f1264799865'
    tenant = 'testTenant'
    secret = 'qWgdYAmab0YSkuL1qKv5bPX'

    client = Client(appId, tenant, secret)

    responseData = {"token_type": "Bearer",
                    "expires_in": 3599,
                    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Ik1uQ19WWmNBVGZNNXBP..."
                    }
    responseJson = json.dumps(responseData)
    m.post(client.getEndpoint('token'), text=responseJson) 

    token = client.getToken()

    assert token == responseData

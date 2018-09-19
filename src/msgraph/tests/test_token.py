from datetime import datetime
import json

from mock import Mock, patch
import requests_mock

from msgraph.client import Client


def test_client_getEndpoint():

    appId = '535fb089-9ff3-47b6-9bfb-4f1264799865'
    tenant = 'M365x214355.sharepoint.com'
    secret = 'qWgdYAmab0YSkuL1qKv5bPX'
    siteId = "m365x214355.sharepoint.com,f66f0635-cbc1-4695-8c25-d76c20b5f883,73429943-801a-48bd-9ab9-b57b0b4e4f27"
    client = Client(appId, tenant, secret)

    shouldBe = 'https://login.microsoftonline.com/M365x214355.sharepoint.com/oauth2/v2.0/token'
    assert client.getEndpoint('token') == shouldBe

    shouldBe = 'https://login.microsoftonline.com/M365x214355.sharepoint.com/adminconsent'
    assert client.getEndpoint('adminConsent') == shouldBe

    shouldBe = 'https://login.microsoftonline.com/M365x214355.sharepoint.com/adminconsent'
    shouldBe = 'https://graph.microsoft.com/v1.0/sites/' + siteId
    assert client.getEndpoint('site_by_id', siteId=siteId) == shouldBe

@requests_mock.Mocker()
def test_getToken(m):

    appId = '535fb089-9ff3-47b6-9bfb-4f1264799865'
    tenant = 'M365x214355.sharepoint.com'
    secret = 'qWgdYAmab0YSkuL1qKv5bPX'

    client = Client(appId, tenant, secret)

    responseData = {"token_type": "Bearer",
                    "expires_in": 3599,
                    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Ik1uQ19WWmNBVGZNNXBP..."
                    }
    responseJson = json.dumps(responseData)
    m.post(client.getEndpoint('token'), text=responseJson) 

    token = client.getToken()

    assert token.token_type == responseData.get('token_type')
    assert token.expires_in == responseData.get('expires_in')
    assert token.access_token == responseData.get('access_token')
    assert token.expired == False

    token.expire_date = datetime.now()
    assert token.expired == True

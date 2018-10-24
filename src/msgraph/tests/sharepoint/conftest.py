import json

import pytest

from msgraph.client import Client, Token
from msgraph.sharepoint import Sharepoint

@pytest.fixture(scope="module")
def sharepoint():
    appId = '535fb089-9ff3-47b6-9bfb-4f1264799865'
    tenant = 'M365x214355.sharepoint.com'
    secret = 'qWgdYAmab0YSkuL1qKv5bPX'
    token_data = {'token_type': 'Bearer',
                  'expires_in': 3600,
                  'access_token': '123456'}
    token = Token(json.dumps(token_data))
    client = Client(appId, tenant, secret, token=token)

    return Sharepoint(client)

@pytest.fixture(scope="module")
def site_data():

    responseData = {"@odata.context": "https://graph.microsoft.com/v1.0/$metadata#sites/$entity",
                    "createdDateTime": "2017-07-31T16:29:12Z",
                    "description": "",
                    "id": "m365x214355.sharepoint.com,f66f0635-cbc1-4695-8c25-d76c20b5f883,73429943-801a-48bd-9ab9-b57b0b4e4f27",
                    "lastModifiedDateTime": "2018-09-03T03:40:16Z",
                    "name": "MarketingDocuments",
                    "webUrl": "https://m365x214355.sharepoint.com/sites/contoso/Departments/SM/MarketingDocuments",
                    "displayName": "Marketing Documents",
                    "parentReference": {}
                    }
    return responseData, json.dumps(responseData)

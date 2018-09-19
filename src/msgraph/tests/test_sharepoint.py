import json

from mock import Mock, patch
import requests_mock

from msgraph.client import Client
from msgraph.sharepoint import Sharepoint


@requests_mock.Mocker()
def test_getSitesList(m):

    appId = '535fb089-9ff3-47b6-9bfb-4f1264799865'
    tenant = 'M365x214355.sharepoint.com'
    secret = 'qWgdYAmab0YSkuL1qKv5bPX'

    client = Client(appId, tenant, secret)

    responseData = {"@odata.context": "https://graph.microsoft.com/v1.0/$metadata#sites",
                    "value": [
                       {"createdDateTime": "2017-09-15T01:11:50Z",
                        "description": "Let's capture our thoughts in this subsite blog.",
                        "id": "m365x214355.sharepoint.com,5a58bb09-1fba-41c1-8125-69da264370a0,5e9767b8-95bc-4bd1-aeb0-d6598e566ec0",
                        "lastModifiedDateTime": "0001-01-01T08:00:00Z",
                        "name": "internalblogs",
                        "webUrl": "https://m365x214355.sharepoint.com/internalblogs",
                        "displayName": "Internal blog"
                       }
                    ]}

    responseJson = json.dumps(responseData)

    m.get(client.getEndpoint('list_sites'), text=responseJson)

    sharepoint = Sharepoint(client)
    sites = sharepoint.getSitesList()

    assert sites[0].siteId == responseData['value'][0]['id']
    assert sites[0].name == responseData['value'][0]['name']
    assert sites[0].displayName == responseData['value'][0]['displayName']
    assert sites[0].description == responseData['value'][0]['description']
    assert sites[0].webUrl == responseData['value'][0]['webUrl']
    assert sites[0].lastModifiedDateTime == responseData['value'][0]['lastModifiedDateTime']
    assert sites[0].createdDateTime == responseData['value'][0]['createdDateTime']

@requests_mock.Mocker()
def test_getSiteById(m):

    appId = '535fb089-9ff3-47b6-9bfb-4f1264799865'
    tenant = 'M365x214355.sharepoint.com'
    secret = 'qWgdYAmab0YSkuL1qKv5bPX'

    client = Client(appId, tenant, secret)

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

    responseJson = json.dumps(responseData)

    m.get(client.getEndpoint('site_by_id', siteId=responseData['id']), text=responseJson)

    sharepoint = Sharepoint(client)
    site = sharepoint.getSiteById(responseData['id'])

    assert site.siteId == responseData['id']
    assert site.name == responseData['name']
    assert site.displayName == responseData['displayName']
    assert site.description == responseData['description']
    assert site.webUrl == responseData['webUrl']
    assert site.lastModifiedDateTime == responseData['lastModifiedDateTime']
    assert site.createdDateTime == responseData['createdDateTime']

@requests_mock.Mocker()
def test_getSiteByPath(m):

    appId = '535fb089-9ff3-47b6-9bfb-4f1264799865'
    tenant = 'M365x214355.sharepoint.com'
    secret = 'qWgdYAmab0YSkuL1qKv5bPX'

    client = Client(appId, tenant, secret)

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

    responseJson = json.dumps(responseData)

    path='contoso/Departments/SM/MarketingDocuments'

    m.get(client.getEndpoint('site_by_path', sitePath=path), text=responseJson)

    sharepoint = Sharepoint(client)
    site = sharepoint.getSiteByPath(path)

    assert site.siteId == responseData['id']
    assert site.name == responseData['name']
    assert site.displayName == responseData['displayName']
    assert site.description == responseData['description']
    assert site.webUrl == responseData['webUrl']
    assert site.lastModifiedDateTime == responseData['lastModifiedDateTime']
    assert site.createdDateTime == responseData['createdDateTime']

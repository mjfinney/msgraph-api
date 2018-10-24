import json

import requests_mock


class TestSharepointSites(object):

    def test_getSitesList(self, sharepoint):
    
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
    
        with requests_mock.Mocker() as m:
            m.get(sharepoint.client.getEndpoint('list_sites'), text=responseJson)
            sites = sharepoint.getSitesList()
            site = next(sites)
    
        assert site.siteId == responseData['value'][0]['id']
        assert site.name == responseData['value'][0]['name']
        assert site.displayName == responseData['value'][0]['displayName']
        assert site.description == responseData['value'][0]['description']
        assert site.webUrl == responseData['value'][0]['webUrl']
        assert site.lastModifiedDateTime == responseData['value'][0]['lastModifiedDateTime']
        assert site.createdDateTime == responseData['value'][0]['createdDateTime']
    
    def test_getSiteById(self, sharepoint, site_data):
    
        responseData = site_data[0]
        responseJson = site_data[1]
    
        with requests_mock.Mocker() as m:
            m.get(sharepoint.client.getEndpoint('site_by_id', siteId=responseData['id']), text=responseJson)
    
            site = sharepoint.getSiteById(responseData['id'])
    
        assert site.siteId == responseData['id']
        assert site.name == responseData['name']
        assert site.displayName == responseData['displayName']
        assert site.description == responseData['description']
        assert site.webUrl == responseData['webUrl']
        assert site.lastModifiedDateTime == responseData['lastModifiedDateTime']
        assert site.createdDateTime == responseData['createdDateTime']
    
    def test_getSiteByPath(self, sharepoint, site_data):
        responseData = site_data[0]
        responseJson = site_data[1]
    
        path='contoso/Departments/SM/MarketingDocuments'
    
        with requests_mock.Mocker() as m:
            m.get(sharepoint.client.getEndpoint('site_by_path',
                                                sitePath=path),
                  text=responseJson)
    
            site = sharepoint.getSiteByPath(path)
    
        assert site.siteId == responseData['id']
        assert site.name == responseData['name']
        assert site.displayName == responseData['displayName']
        assert site.description == responseData['description']
        assert site.webUrl == responseData['webUrl']
        assert site.lastModifiedDateTime == responseData['lastModifiedDateTime']
        assert site.createdDateTime == responseData['createdDateTime']

import json

import requests_mock

from msgraph.client import Client
from msgraph.sharepoint import Sharepoint

class TestSharepointColumns(object):
    def test_getLists(self, sharepoint, site_data):
    
        responseData = site_data[0]
        responseJson = site_data[1]
        siteId = responseData['id']

        with open('./src/msgraph/tests/data/lists.json') as f:
            text = f.read()
            response_lists = json.loads(text)
    
        with requests_mock.Mocker() as m:
            m.get(sharepoint.client.getEndpoint('site_by_id',
                                                siteId=siteId),
                  text=responseJson)
        

            m.get(sharepoint.client.getEndpoint('list_lists',
                                                siteId=siteId),
                  text=text)
    
    
            site = sharepoint.getSiteById(siteId)
            lists = site.getLists()
    
        assert len(lists) ==  len(response_lists.get('value'))
    
    def test_getListById(self, sharepoint, site_data):

        responseData = site_data[0]
        responseJson = site_data[1]
        listId = '71c37c1b-521b-4a02-ad97-be467b796f0b'
        siteId = responseData['id']

        with open('./src/msgraph/tests/data/single_list.json') as f:
            text = f.read()
            response_lists = json.loads(text)

        with requests_mock.Mocker() as m:
            m.get(sharepoint.client.getEndpoint('site_by_id',
                                                siteId=siteId),
                  text=responseJson)
            m.get(sharepoint.client.getEndpoint('list_by_id',
                                                siteId=siteId,
                                                listId=listId),
                  text=text)

            site = sharepoint.getSiteById(siteId)
            l = site.getListById(listId)
    
        assert l.displayName == "Documents"

    def test_getItems(self, sharepoint, site_data):
        responseData = site_data[0]
        responseJson = site_data[1]
        listId = '71c37c1b-521b-4a02-ad97-be467b796f0b'
        siteId = responseData['id']

        with open('./src/msgraph/tests/data/list_items.json') as f:
            text = f.read()
            response_items = json.loads(text)['value']

        with open('./src/msgraph/tests/data/single_list.json') as f:
            text_list = f.read()
            response_list = json.loads(text)

        with requests_mock.Mocker() as m:
            m.get(sharepoint.client.getEndpoint('site_by_id',
                                                siteId=siteId),
                  text=responseJson)
            m.get(sharepoint.client.getEndpoint('list_by_id',
                                                siteId=siteId,
                                                listId=listId),
                  text=text_list)
            m.get(sharepoint.client.getEndpoint('list_items_with_values',
                                                siteId=siteId,
                                                listId=listId),
                  text=text)

            site = sharepoint.getSiteById(siteId)
            l = site.getListById(listId)
            items = l.getItems()
    
        print items
        assert items[0].fields['Title'] == response_items[0]['fields']['Title']

#def test_createListItem():
#    assert False
#
#def test_getListColumns():
#    assert False

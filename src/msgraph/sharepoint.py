import json

import requests

from msgraph.constants import GRAPH_URL, GRAPH_VERSION, LOGIN_URL, LOGIN_VERSION, LOGIN_ENDPOINTS, GRAPH_ENDPOINTS


class Sharepoint(object):

    def __init__(self, client):
        self.client = client
        self.site = None

    def getSitesList(self):
        nextpage = 1
        while nextpage != None:
            if nextpage == 1:
                response = self.client.getResponse('list_sites')
            else:
                response = self.client.getResponse('next', url=nextpage)
            if response.ok:
                data = json.loads(response.text)
                for site in data.get('value'):
                    yield SharepointSite(client=self.client, **site)
                nextpage = data.get('@odata.nextLink')
            else:
                nextpage = None

    def getSiteById(self, siteId):
        response = self.client.getResponse('site_by_id', siteId=siteId)
        if response.ok:
            data = json.loads(response.text)
            return SharepointSite(client=self.client, **data)
        return None

    def getSiteByPath(self, sitePath):
        response = self.client.getResponse('site_by_path', sitePath=sitePath)
        if response.ok:
            data = json.loads(response.text)
            return SharepointSite(client=self.client, **data)
        return None


class SharepointSite(object):

    def __init__(self, client, **kwargs):
        self.client = client
        self.siteId = kwargs.get('id')
        self.name = kwargs.get('name')
        self.displayName = kwargs.get('displayName')
        self.description = kwargs.get('description')
        self.webUrl = kwargs.get('webUrl')
        self.lastModifiedDateTime = kwargs.get('lastModifiedDateTime')
        self.createdDateTime = kwargs.get('createdDateTime')

    def getLists(self):
        listsList = []
        response = self.client.getResponse('list_lists', siteId=self.siteId)
        if response.ok:
            data = json.loads(response.text)
            for l in data.get('value'):
                listsList.append(SharepointList(self, **l))

        return listsList

    def getListById(self, listId):
        response = self.client.getResponse('list_by_id',
                                           siteId=self.siteId,
                                           listId=listId)
        l = {}
        if response.ok:
            l = SharepointList(self, **json.loads(response.text))

        return l


class SharepointList(object):

    def __init__(self, site, **kwargs):
        self.site = site
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.displayName = kwargs.get('displayName')
        self.description = kwargs.get('description')
        self.webUrl = kwargs.get('webUrl')
        self.lastModifiedDateTime = kwargs.get('lastModifiedDateTime')
        self.createdDateTime = kwargs.get('createdDateTime')

    def getColumns(self):
        pass

    def selectColumnClass(self, column):
        choices = {'boolean': SharepointBooleanColumn,
                   'choice': SharepointChoiceColumn,
                   'dateTime': SharepointDateTimeColumn,
                   'lookup': SharepointLookupColumn,
                   'number': SharepointNumberColumn,
                   'personOrGroup': SharepointPersonOrGroupColumn,
                   'text': SharepointTextColumn,
                }
        for k,v in choices.items():
            if column.get('k'):
                return v
        return SharepointColumn

    def getItems(self, listId):
        response = self.site.client.getResponse('list_items_with_values',
                                           siteId=self.site.siteId,
                                           listId=listId)
        items = []
        if response.ok:
            data = json.loads(response.text)
            for item in data.get('value'):
                items.append(SharepointItem(**item))
        return items


class SharepointItem(object):

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.displayName = kwargs.get('displayName')
        self.description = kwargs.get('description')
        self.webUrl = kwargs.get('webUrl')
        self.lastModifiedDateTime = kwargs.get('lastModifiedDateTime')
        self.createdDateTime = kwargs.get('createdDateTime')
        self.fields = kwargs.get('fields')


class SharepointColumn(object):

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.description = kwargs.get('description')
        self.columnGroup = kwargs.get('columnGroup')
        self.name = kwargs.get('name')
        self.displayName = kwargs.get('displayName')
        self.defaultValue = kwargs.get('defaultValue')
        self.hidden = kwargs.get('hidden')
        self.readOnly = kwargs.get('readOnly')
        self.required = kwargs.get('required')
        self._type_properties = {}

    @property
    def type_properties(self):
        return self._type_properties

    @type_properties.setter
    def type_properties(self, value):
        if not isinstance(value, dict):
            raise ValueError("type_properties must be a dictionary")
        self._type_properties = value


class SharepointBooleanColumn(SharepointColumn):
    pass


class SharepointCalculatedColumn(SharepointColumn):
    pass


class SharepointChoiceColumn(SharepointColumn):

    def __init__(self, **kwargs):
        self.type_properties(self.kwargs.get('choice', {}))


class SharepointCurrencyColumn(SharepointColumn):
    pass


class SharepointDateTimeColumn(SharepointColumn):

    def __init__(self, **kwargs):
        self.type_properties(self.kwargs.get('dateTime', {}))


class SharepointLookupColumn(SharepointColumn):

    def __init__(self, **kwargs):
        self.type_properties(self.kwargs.get('lookup', {}))


class SharepointNumberColumn(SharepointColumn):

    def __init__(self, **kwargs):
        self.type_properties(self.kwargs.get('number', {}))


class SharepointPersonOrGroupColumn(SharepointColumn):

    def __init__(self, **kwargs):
        self.type_properties(self.kwargs.get('personOrGroup', {}))


class SharepointTextColumn(SharepointColumn):

    def __init__(self, **kwargs):
        self.type_properties(self.kwargs.get('text', {}))

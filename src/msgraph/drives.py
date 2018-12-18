import json

import requests

from msgraph.constants import GRAPH_URL, GRAPH_VERSION, LOGIN_URL, LOGIN_VERSION, LOGIN_ENDPOINTS, GRAPH_ENDPOINTS

class Drive(object):
    
    def __init__(self, client, **kwargs):
        self.client = client
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')
        self.webUrl = kwargs.get('webUrl')
        self.lastModifiedDateTime = kwargs.get('lastModifiedDateTime')
        self.createdDateTime = kwargs.get('createdDateTime')
        self.driveType = kwargs.get('driveType')
        self.quota = kwargs.get('quota')

    def upload(self, filename, data, location="root:"):
        headers = {'Content-Type': 'application/xml'}
        response = self.client.getResponse('upload_file',
                                           method='PUT',
                                           driveId=self.id,
                                           filename=filename,
                                           data=data,
                                           location=location)
        return response


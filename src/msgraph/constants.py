GRAPH_URL = 'https://graph.microsoft.com/{version}/'
GRAPH_VERSION = 'v1.0'
LOGIN_URL ='https://login.microsoftonline.com/'
LOGIN_VERSION = 'v2.0'

LOGIN_ENDPOINTS = {'adminConsent': '{tenant}/adminconsent',
                   'token': '{tenant}/oauth2/{version}/token',
                   }
GRAPH_ENDPOINTS = {'sites_root': '',
                   'list_sites': 'sites?search=*',
                   'site_by_id': 'sites/{siteId}',
                   'site_by_path': 'sites/{tenant}:/sites/{sitePath}',
                   'list_lists': 'sites/{siteId}/lists',
                   'list_by_id': 'sites/{siteId}/lists/{listId}',
                   'list_columns': 'sites/{siteId}/lists/{listId}/columns',
                   'list_items': 'sites/{siteId}/lists/{listId}/items',
                   'list_items_with_values': 'sites/{siteId}/lists/{listId}/items/?expand=fields',
                   'list_item': 'sites/{siteId}/lists/{listId}/items/{itemId}',
                   'list_drives': 'sites/{siteId}/drives',
                   'upload_file': 'drives/{driveId}/items/{location}/{filename}:/content',
                   'upload_session': 'drives/{driveId}/items/{location}/createUploadSession',
                   }

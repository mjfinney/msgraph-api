GRAPH_URL = 'https://graph.microsoft.com/{version}/'
GRAPH_VERSION = 'v1.0'
LOGIN_URL ='https://login.microsoftonline.com/'
LOGIN_VERSION = 'v2.0'

LOGIN_ENDPOINTS = {'adminConsent': '{tenant}/adminconsent',
                   'token': '{tenant}/oauth2/{version}/token',
                   }
GRAPH_ENDPOINTS = {'sites_root': '',
                   }

from dataclasses import dataclass
from typing import List
from apiclient.discovery import Resource

@dataclass
class DriveService:
    service: Resource
    
    def files_in_folder( self, folder_id ):
        response = self.service.files().list(
            q = f'"{folder_id}" in parents',
            orderBy = 'name',
            fields = 'files/id,files/name,files/webViewLink',
        ).execute()
        return response['files']

    # def retrieve_file( self, file_id ):
    
    def get_file( self, file_id ):
        response = self.service.files().get( 
            fileId = file_id, 
            fields = 'id,name,mimeType,trashed,parents,webViewLink'
        ).execute()
        return DriveFile( **response )

@dataclass
class DriveFile:
    id: str
    name: str
    mimeType: str
    trashed: bool
    # driveId: str
    parents: List[str]
    webViewLink: str
    # permissions: List[str]

def build_drive_service( client_secrets, SCOPES ):
    from apiclient.discovery import build
    http_creds = authenticate( client_secrets, SCOPES )
    service = build('drive', 'v3', http=http_creds)
    return DriveService( service = service )

    
def authenticate( client_secrets, SCOPES ):
    """
        returns http credentials object
    """
    from oauth2client import client, file, tools
    import requests
    import json
    from httplib2 import Http

    with open('client_secrets.json','w') as f:
        json.dump(client_secrets, f)

    store = file.Storage('credentials.json')

    # start the authentication flow
    flags = tools.argparser.parse_args(args=['--noauth_local_webserver'])
    flow = client.flow_from_clientsecrets('client_secrets.json', SCOPES)
    creds = tools.run_flow(flow, store, flags)

    # Validate token
    validation_endpoint = 'https://www.googleapis.com/oauth2/v3/tokeninfo'
    validation_params = { 'access_token' : creds.access_token }
    v = requests.get(validation_endpoint, validation_params)
    if v.json()['aud']:
        print ("Valid. Expires in {} s".format(v.json()['expires_in']))
    
    return creds.authorize(Http())

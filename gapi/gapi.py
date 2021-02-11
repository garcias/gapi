
def authenticate( client_secrets, SCOPES ):
    """
        returns http credentials object
    """
    from oauth2client import client, file, tools
    import requests
    import json
    from apiclient.discovery import build
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

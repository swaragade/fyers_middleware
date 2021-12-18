from os import environ
from fyers_api import accessToken

class AuthorizeMe:

    def auth():
        session=accessToken.SessionModel(client_id=environ.get('APP_ID'),
        secret_key=environ.get('SECRET'),redirect_uri='http://localhost:5000/saveAuth', 
        response_type='code', grant_type='authorization_code')
        authUrl = session.generate_authcode()
        #print("Authenticate with this URL from browser=",authUrl)
        return {'session' : session, 'authurl' :authUrl}

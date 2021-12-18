from flask import Flask, request,redirect, jsonify
from os import environ

from AuthorizeMe import AuthorizeMe

# fyers
from fyers_api import fyersModel

from Util import Util

## app code

app = Flask(__name__)

#https://www.tradingview.com/blog/en/introducing-variables-in-alerts-14880/
#https://github.com/FyersDev/fyers-api-sample-code/blob/sample_v2/python/getAccessToken.py
#https://myapi.fyers.in/docs/
#http://localhost:5000/?s=ok&code=200&auth_code=TDemIV8pkj3TU&state=None

#GET /?s=ok&code=200&auth_code=LCJ1dWlkIjoiZmI0MQk3qLWhi-kTDemIV8pkj3TU
# &state=None HTTP/1.1" 200 -
@app.route('/saveAuth', methods=['GET', 'POST']) 
def auth_details_receiver():
    status = request.args.get('s', default = 'error', type = str)
    statuscode = request.args.get('code', default = 409, type = int)
    #print('status =',status)
    #print('statuscode =',statuscode)
    #print('auth =',request.args.get('auth_code', type = str))
    if status == 'ok' and statuscode == 200:
        auth_code = request.args.get('auth_code', type = str)
        if auth_code:
            environ["AUTH_CODE"] = auth_code
            session.set_token(auth_code)
            response = session.generate_token()
            access_token = response["access_token"]
            environ["ACCESS_TOKEN"] = access_token
            Util.writeEnvVar('ACCESS_TOKEN',access_token)
        else:
            app.logger.error('AUTH CODE MISSING')
       
    return "<h1>Authentication Sucessful</h1>"

@app.route('/login', methods=['GET']) 
def getToken():
    # this will redirect you to fyers login
    # once you login, it will redirect u again to this middleware 
    # and save the auth_code given by the fyers
    auth_details = AuthorizeMe.auth()
    global session 
    session = auth_details['session']
    return redirect(auth_details['authurl'], code=302)

@app.route('/', methods=['GET']) 
def getDetails():
    global fyers
    fyers = fyersModel.FyersModel(client_id=environ.get('APP_ID'), token=environ.get('ACCESS_TOKEN'),is_async = True,log_path="/Users/swaragade/Documents/WorkSpaces/PyApi")
    print('profile==',fyers.get_profile())
    return 'ok'

# main driver function
if __name__ == '__main__':
    app.run(debug=True,port=5000)
    
    


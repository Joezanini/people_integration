from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

clientId = 'C75f2e7449fca7397c9e37e7edd21a062e05929b52973356f9e03c02ce48bb6f2'
clientSecret = '891bdcbef0aa9ff96a4d279edefa3992f32cf7c24ac1d62d785acb2206a1eba9'
redirectUri = 'http://127.0.0.1:5000/callback'

def get_user_info(bearer_token):
    url = 'https://webexapis.com/v1/people/me'
    headers = {
        'Authorization': 'Bearer ' + bearer_token,
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)
    response_json = response.json()

    if response.status_code == 200:
        user_info = response_json
        return user_info
    else:
        error_message = response_json.get('message', 'Failed to get user info')
        raise Exception(error_message)

def get_access_token(code):
    url = 'https://webexapis.com/v1/access_token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': 'authorization_code',
        'client_id': clientId,
        'client_secret': clientSecret,
        'code': code,
        'redirect_uri': redirectUri
    }

    response = requests.post(url, headers=headers, data=data)
    response_json = response.json()
    
    if response.status_code == 200:
        access_token = response_json.get('access_token')
        return access_token
    else:
        error_message = response_json.get('error_description', 'Failed to get access token')
        raise Exception(error_message)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/callback')
def callback():
    # Handle the redirect from the authorization server
    state = request.args.get('state')
    if state == 'abc123' :
        code = request.args.get('code')
        print('user information : ', get_user_info(get_access_token(code)))
    # Do something with the authorization code
    
    # Redirect the user back to the homepage
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

    #https://webexapis.com/v1/people/me
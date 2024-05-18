from botocore.exceptions import ClientError
from flask import Flask, render_template, request, redirect
from aws_util import create_boto_session, get_user_pool_id, get_cognito_client_id
import json
app = Flask(__name__)
app.session_token = None
app.user_full_name = None
app.user_email = None

def clear_auth_details():
    app.session_token = None
    app.user_full_name = None
    app.user_email = None

def create_user_account(session, params):
    client = session.client('cognito-idp')
    user_pool_id = get_user_pool_id(client)

    # Create the new user if the User Pool ID was found
    try:
        if user_pool_id:
            response = client.admin_create_user(
                UserPoolId=user_pool_id,
                Username=params['email'],
                TemporaryPassword=params['password'],
                UserAttributes=[
                    {'Name': 'email', 'Value': params['email']},
                    {'Name': 'given_name', 'Value': params['firstName']},
                    {'Name': 'family_name', 'Value': params['lastName']}
                ],
            )
    except client.exceptions.UsernameExistsException:
        return "UsernameExists"
    return "Ok"

def authenticate_credentials(session, params):
    client = session.client('cognito-idp')

    user_pool_id = get_user_pool_id(client)
    client_id = get_cognito_client_id(client, user_pool_id)
    try:
        # Call the admin_initiate_auth method with the user's email and password
        response = client.initiate_auth(
            ClientId=client_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': params['email'],
                'PASSWORD': params['password']
            }
        )
        app.session_token = response['Session']
        user_attributes = json.loads(response['ChallengeParameters']['userAttributes'])
        app.user_full_name = user_attributes['given_name'] + ' ' + user_attributes['family_name']
        app.user_email = user_attributes['email']
    except Exception as e:
        raise e
    return "Ok"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registration')
def registration():
    return render_template('registration_page.html')

@app.route('/user-profile')
def user_profile():
    if app.session_token:
        return render_template('profile_page.html', data={'name': app.user_full_name})
    else:
        return redirect('/')

@app.route('/create-new-user', methods=['POST'])
def create_new_user():

    params = {
        'firstName': request.form.get('firstName'),
        'lastName': request.form.get('lastName'),
        'email': request.form.get('email'),
        'password': request.form.get('password'),
    }
    response = create_user_account(app.boto_session, params)
    return response

@app.route('/authenticate', methods=['POST'])
def authenticate():
    params = {
        'email': request.form.get('email'),
        'password': request.form.get('password'),
    }
    response = authenticate_credentials(app.boto_session, params)
    return response

@app.route('/logout', methods=['POST'])
def logout():
    clear_auth_details()
    return render_template('index.html')

if __name__ == '__main__':
    clear_auth_details()
    app.boto_session = create_boto_session()
    app.run(debug=True)
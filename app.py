from flask import Flask, render_template, request
from aws_util import create_boto_session, get_user_pool_id, get_cognito_client_id

app = Flask(__name__)

def create_user_account(session):
    client = session.client('cognito-idp')
    user_pool_id = get_user_pool_id(client)

    # TODO - add params and parse them
    # Create the new user if the User Pool ID was found
    if user_pool_id:
        response = client.admin_create_user(
            UserPoolId=user_pool_id,
            Username='email@domain.com',
            TemporaryPassword='password!',
            UserAttributes=[
                {'Name': 'email', 'Value': 'email@domain.com'},
                {'Name': 'given_name', 'Value': 'First'},
                {'Name': 'family_name', 'Value': 'Last'}
            ],
        )

def authenticate_credentials(session, params):
    client = session.client('cognito-idp')

    user_pool_id = get_user_pool_id(client)
    client_id = get_cognito_client_id(client, user_pool_id)
    # TODO - add params and parse them

    try:
        # Call the admin_initiate_auth method with the user's email and password
        response = client.initiate_auth(
            # UserPoolId=user_pool_id,
            ClientId=client_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': 'jdoe6@gmail.com',
                'PASSWORD': 'passWord100!'
            }
        )
    except Exception as e:
        raise e

boto_session = create_boto_session()
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registration-page')
def registration():
    return render_template('registration_page.html')

@app.route('/create-new-user', methods=['POST'])
def create_new_user():
    create_user_account(boto_session)
    return '200'

@app.route('/authenticate', methods=['POST'])
def authenticate():
    params = []
    try:
        authenticate_credentials(boto_session, params)
        return 'SUCCESS'
    except Exception as e:
        return 'INVALID USERNAME OR PASSWORD'


if __name__ == '__main__':
    app.run(debug=True)
import boto3
import config
import os

def create_boto_session():
    """ Make sure ACCESS_KEY_ID, and SECRET_ACCESS_KEY environment variables are exported"""
    access_key_id = os.environ['AWS_ACCESS_KEY_ID']
    secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
    region = "us-east-1"

    session = boto3.Session(
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        region_name=region
    )
    return session

def create_cognito_user_pool(stack_name, template_file, session):
    cloudformation = session.client('cloudformation')

    with open(template_file, 'r') as file:
        template_body = file.read()

    response = cloudformation.create_stack(
        StackName=stack_name,
        TemplateBody=template_body,
        Capabilities=['CAPABILITY_NAMED_IAM']
    )

    return response

def get_user_pool_id(client):
    # client = session.client('cognito-idp')
    user_pool_name = config.USER_POOL_NAME
    response = client.list_user_pools(MaxResults=60)
    for user_pool in response['UserPools']:
        if user_pool['Name'] == user_pool_name:
            return user_pool['Id']
    return None

def get_cognito_client_id(client, user_pool_id):
    response = client.list_user_pool_clients(
        UserPoolId=user_pool_id
    )

    client_ids = [client['ClientId'] for client in response['UserPoolClients']]

    return client_ids[0]

def disable_force_password_change(session):
    client = session.client('cognito-idp')
    user_pool_id = get_user_pool_id(session)

    client.update_user_pool(
        UserPoolId=user_pool_id,
        AdminCreateUserConfig={
            'AllowAdminCreateUserOnly': False,
        }
    )

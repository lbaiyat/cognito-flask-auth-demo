import config

from aws_util import (
    create_boto_session,
    create_cognito_user_pool,
)

if __name__ == '__main__':
    stack_name = config.CLOUDFORMATION_STACK_NAME
    template_file = 'app-cognito.yaml'
    session = create_boto_session()
    response = create_cognito_user_pool(stack_name, template_file, session)
    print("Stack creation initiated. Stack ID:", response['StackId'])

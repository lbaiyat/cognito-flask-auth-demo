import config

from aws_util import (
    create_boto_session,
    create_cognito_user_pool_stack,
    delete_cognito_user_pool_stack
)
import argparse

template_file = 'app-cognito.yaml'

def create_cognito_user_pool():
    stack_name = config.CLOUDFORMATION_STACK_NAME
    session = create_boto_session()
    response = create_cognito_user_pool_stack(stack_name, template_file, session)
    print("Stack creation initiated. Stack ID:", response['StackId'])

def delete_cognito_user_pool():
    stack_name = config.CLOUDFORMATION_STACK_NAME
    session = create_boto_session()
    response = delete_cognito_user_pool_stack(stack_name, session)
    print("Stack deletion initiated. Stack Name:", stack_name)

def get_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', help='Please specify create or delete')

    create_parser = subparsers.add_parser('create', help='Create cognito user pool')
    create_parser.set_defaults(func=create_cognito_user_pool)

    delete_parser = subparsers.add_parser('delete', help='Delete cognito user pool')
    delete_parser.set_defaults(func=delete_cognito_user_pool)

    return parser


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func()
    else:
        parser.print_help()

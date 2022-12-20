import boto3
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session

load_dotenv()

AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')


# Create a AWS Cognito client in the 'eu-west-1' region
cognito_client = boto3.client(
    'cognito-idp',
    region_name='eu-west-3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

class DBSessionContext(object):
    def __init__(self, db: Session):
        self.db = db


class AppService(DBSessionContext):
    pass


class AppCRUD(DBSessionContext):
    pass


def get_cognito_user_pool():
    # Set the pagination variables
    pagination_token = None
    users = []

    # Loop until all users have been retrieved
    while True:
        
        # Get the next batch of users
        if pagination_token:
            response = cognito_client.list_users(UserPoolId="eu-west-3_EdcmRTUbN", PaginationToken=pagination_token)
        else:
            response = cognito_client.list_users(UserPoolId="eu-west-3_EdcmRTUbN")

        # Add the users to the list
        users.extend(response['Users'])

        # Check if there are more users
        if 'PaginationToken' in response:
            pagination_token = response['PaginationToken']
        else:
            break

    return users

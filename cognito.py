import os
import hashlib
import hmac
import base64
import boto3

from botocore.exceptions import ClientError

from dotenv import load_dotenv

load_dotenv()

app_client_id = os.getenv('COGNITO_APP_CLIENT_ID')
app_client_secret = os.getenv('COGNITO_APP_CLIENT_SECRET')
cognito_user_pool_id = os.getenv('COGNITO_USER_POOL_ID')
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')


def calculate_cognito_secret_hash(username, client_id, client_secret):
    message = username + client_id
    key = hmac.new(str(client_secret).encode(
        'utf-8'), msg=str(message).encode('utf-8'), digestmod=hashlib.sha256).digest()
    return base64.b64encode(key).decode()


secret_hash = calculate_cognito_secret_hash(
    'ligton.ribeiro@gmail.com', app_client_id, app_client_secret)

session = boto3.Session()


cognito_client = boto3.client(
    'cognito-idp',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=os.getenv('AWS_REGION')
)


def create_user_cognito(email, password, name):
    user = cognito_client.sign_up(
        ClientId=app_client_id,
        SecretHash=secret_hash,
        Username=email,
        Password=password,
        UserAttributes=[
            {
                'Name': 'name',
                'Value': name
            }
        ]
    )

    return user


def admin_create_user(email, name):
    response = cognito_client.admin_create_user(
        UserPoolId=cognito_user_pool_id,
        Username=email,
        UserAttributes=[
            {
                'Name': 'name',
                'Value': name
            }
        ],
    )
    return response


# def admin_initiate_auth(email, password):
#     response = cognito_client.admin_initiate_auth(
#         UserPoolId=cognito_user_pool_id,
#         ClientId=app_client_id,
#         AuthFlow='USER_PASSWORD_AUTH',
#         AuthParameters={
#             'email': email,
#             'password': password
#         }
#     )
#     return response


def confirm_signup_user(email, confirmation_code):
    confirm_user = cognito_client.confirm_sign_up(
        ClientId=app_client_id,
        SecretHash=secret_hash,
        Username=email,
        ConfirmationCode=confirmation_code,
    )

    return confirm_user


def signin_cognito(email, password):
    secret_hash = calculate_cognito_secret_hash(
        email, app_client_id, app_client_secret)

    try:
        response = cognito_client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password,
                'SECRET_HASH': secret_hash
            },
            ClientId=app_client_id
        )

        access_token = response['AuthenticationResult']['AccessToken']
        refresh_token = response['AuthenticationResult']['RefreshToken']
        token_type = response['AuthenticationResult']['TokenType']

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': token_type
        }
    except ClientError as e:
        if e.response['Error']['Code'] == 'NotAuthorizedException':
            return 'Incorrect username or password'


def respond_auth_challenge(email, new_password, session_token):
    secret_hash = calculate_cognito_secret_hash(
        email, app_client_id, app_client_secret
    )
    response = cognito_client.respond_to_auth_challenge(
        ClientId=app_client_id,
        ChallengeName='NEW_PASSWORD_REQUIRED',
        ChallengeResponses={
            'NEW_PASSWORD': new_password,
            'USERNAME': email,
            'SECRET_HASH': secret_hash
        },
        Session=session_token
    )
    return response


def forgot_password(email):
    response = cognito_client.forgot_password(
        ClientId=app_client_id,
        SecretHash=secret_hash,
        Username=email
    )
    return response


def confirm_forgot_password(email, confirmation_code, password):
    response = cognito_client.confirm_forgot_password(
        ClientId=app_client_id,
        SecretHash=secret_hash,
        Username=email,
        ConfirmationCode=confirmation_code,
        Password=password
    )

    return response


if __name__ == '__main__':
    # cognito_user = create_user_cognito('ligtonappdeveloper@gmail.com',
    #                                    'Lu@nny12', 'Wellington Ribeiro')
    # print(cognito_user)

    # confirm_signup_user('ligtonappdeveloper@gmail.com', '624471')

    print(signin_cognito('wellington.ribeiro.menezes00@aluno.ifce.edu.br', 'Lu@nny12'))

    # print(forgot_password('ligton.ribeiro@gmail.com'))

    # print(confirm_forgot_password(
    #     'ligton.ribeiro@gmail.com', '853098', 'Lu@nMarx27'))

    # print(admin_create_user(
    #     'wellington.ribeiro.menezes00@aluno.ifce.edu.br', 'Wellington R de Menezes'))
    # session_token = 'AYABeNaveicb7_8Y-VwM97MelnEAHQABAAdTZXJ2aWNlABBDb2duaXRvVXNlclBvb2xzAAEAB2F3cy1rbXMAS2Fybjphd3M6a21zOnVzLWVhc3QtMTo3NDU2MjM0Njc1NTU6a2V5L2IxNTVhZmNhLWJmMjktNGVlZC1hZmQ4LWE5ZTA5MzY1M2RiZQC4AQIBAHgDHnKSW2nDRJSDSLf55TGFyX5On_wV32whMfiMxuCEIAFEDhqkKZIMM8R9twgPflDEAAAAfjB8BgkqhkiG9w0BBwagbzBtAgEAMGgGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMaGuYr_c3JtVoRDVUAgEQgDv7SJJOjc_aQ6-VyZ9viLKnOeMTvsyH7-sbSrWGgtGEP-LgpXl83QrXSyPa6XI-a50PEMZSLMU2QY-c9wIAAAAADAAAEAAAAAAAAAAAAAAAAAAgIc0VO1EU_nBiHlGANR7c_____wAAAAEAAAAAAAAAAAAAAAEAAADVJT4Z1QM2KaC2tdPwH1gY0AGapSJ2JLq4WItl3UIi4aIJRLWUinfvQd4yAaFs05w_Z1cLPdqsKV3_WVigHx7bbSDr2i0uY6fSFU9g31TolTX24trzzKcO_aQsY64yIFOcqxfOY0I0q-t_UR2igqKWWiKZmxruuNGaNwMGApkhk-OmU7-XfovwIqfGWASpLuBKFg_ncCTqKtwzjcD4YM8pIDqvTD3D6OB-mn_N7-SeA-XDoYTfGzNp9JGpUR8dT05BOBLsNrJik0m5HbAry-4fOEADqM3oxUYtEzwIPkmkDRe3vNBhLg'

    # print(respond_auth_challenge(
    #     'wellington.ribeiro.menezes00@aluno.ifce.edu.br', 'Lu@nny12', session_token))

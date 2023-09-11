import os
import requests

from dotenv import load_dotenv

load_dotenv()

JWK = dict[str, str,]
JWKS = dict[str, list[JWK]]


def get_jwks() -> JWKS:
    return requests.get(
        f"https://cognito-idp.{os.getenv('AWS_REGION')}.amazonaws.com/"
        f"{os.getenv('COGNITO_USER_POOL_ID')}/.well-known/jwks.json"
    ).json()

import os
import requests

from dotenv import load_dotenv

from fastapi import Depends, HTTPException
from starlette.status import HTTP_403_FORBIDDEN

from app.utils.JWTBearer import JWKS, JWTBearer, JWTAuthorizationCredentials

load_dotenv()

jwks = JWKS.model_validate(
    requests.get(
        f"https://cognito-idp.{os.getenv('AWS_REGION')}.amazonaws.com/"
        f"{os.getenv('COGNITO_USER_POOL_ID')}/.well-known/jwks.json"
    ).json()
)

AuthenticatedUser = JWTBearer(jwks)


async def get_current_user(
        credentials: JWTAuthorizationCredentials = Depends(AuthenticatedUser)
) -> str:
    try:
        return credentials.claims['username']
    except KeyError:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN,
                            detail='Username missing')

from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from jwt import PyJWKClient

from books_api.auth.schemes import oauth_2_scheme


async def account_access_token(access_token: Annotated[str, Depends(oauth_2_scheme)]):
    url = (
        "https://accounts.paircoded.com/realms/paircoded/protocol/openid-connect/certs"
    )
    jwks_client = PyJWKClient(url)

    try:
        signing_key = jwks_client.get_signing_key_from_jwt(access_token)
        data = jwt.decode(
            access_token,
            signing_key.key,
            algorithms=["RS256"],
            audience="account",
            options={"verify_exp": True},
        )
        return data
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Not authenticated")

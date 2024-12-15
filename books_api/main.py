from typing import Union, Annotated

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2AuthorizationCodeBearer


from jwt import PyJWKClient
import jwt
app = FastAPI()


origins = [
    "https://books-api.paircoded.com",
    "https://books.paircoded.com",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


oauth_2_scheme = OAuth2AuthorizationCodeBearer(
    tokenUrl="https://accounts.paircoded.com/realms/paircoded/protocol/openid-connect/token",
    authorizationUrl="https://accounts.paircoded.com/realms/paircoded/protocol/openid-connect/auth",
    refreshUrl="https://accounts.paircoded.com/realms/paircoded/protocol/openid-connect/token",
)


async def valid_access_token(
    access_token: Annotated[str, Depends(oauth_2_scheme)]
):
    url = "https://accounts.paircoded.com/realms/paircoded/protocol/openid-connect/certs"
    jwks_client = PyJWKClient(url)

    try:
        signing_key = jwks_client.get_signing_key_from_jwt(access_token)
        data = jwt.decode(
            access_token,
            signing_key.key,
            algorithms=["RS256"],
            audience="api",
            options={"verify_exp": True},
        )
        return data
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Not authenticated")



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}", dependencies=[Depends(valid_access_token)])
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


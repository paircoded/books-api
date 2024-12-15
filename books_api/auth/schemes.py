from fastapi.security import OAuth2AuthorizationCodeBearer

oauth_2_scheme = OAuth2AuthorizationCodeBearer(
    tokenUrl="https://accounts.paircoded.com/realms/paircoded/protocol/openid-connect/token",
    authorizationUrl="https://accounts.paircoded.com/realms/paircoded/protocol/openid-connect/auth",
    refreshUrl="https://accounts.paircoded.com/realms/paircoded/protocol/openid-connect/token",
)

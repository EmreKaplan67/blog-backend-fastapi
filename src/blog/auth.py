import os
import jwt 

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWKClient

from dotenv import load_dotenv

load_dotenv()

SUPABASE_PROJECT_URL = os.getenv("SUPABASE_PROJECT_URL")
ADMIN_USER_ID = os.getenv("ADMIN_USER_ID")

if not SUPABASE_PROJECT_URL:
    raise RuntimeError("SUPABASE_PROJECT_URL is not set in the environment variables.")

if not ADMIN_USER_ID:
    raise RuntimeError("ADMIN_USER_ID is not set in the environment variables.")

security = HTTPBearer()

jwks_url = f"{SUPABASE_PROJECT_URL}/auth/v1/.well-known/jwks.json"
jwk_client = PyJWKClient(jwks_url)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        signing_key = jwk_client.get_signing_key_from_jwt(token)
        
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["ES256"],
            audience="authenticated",
            issuer=f"{SUPABASE_PROJECT_URL}/auth/v1",
        )

    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload

def require_admin(user = Depends(get_current_user)):
    if user.get("sub") != ADMIN_USER_ID:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return user
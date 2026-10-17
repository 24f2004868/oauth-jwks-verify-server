
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import jwt

app = FastAPI()

ISSUER = "https://idp.exam.local"
AUDIENCE = "t ds-mx3er0ig.apps.exam.local".replace(" ", "")

PUBLIC_KEY = """PASTE THE COMPLETE ASSIGNED RSA PUBLIC KEY HERE"""

class TokenRequest(BaseModel):
    token: str

@app.post("/verify")
def verify_token(request: TokenRequest):
    try:
        claims = jwt.decode(
            request.token,
            PUBLIC_KEY,
            algorithms=["RS256"],
            issuer=ISSUER,
            audience=AUDIENCE
        )

        return {
            "valid": True,
            "email": claims.get("email"),
            "sub": claims.get("sub"),
            "aud": claims.get("aud")
        }

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401,
            detail={"valid": False}
        )

import time, traceback
from jose import jwt


JWT_SECRET = ""
JWT_ALGORITHM = "RS256"

def decodeJWT(token: str) -> dict:
    try:
        #decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        decoded_token = jwt.decode(token, key=None, algorithms=[JWT_ALGORITHM], options={"verify_signature":False})
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except:
        traceback.print_exc()
        return {}
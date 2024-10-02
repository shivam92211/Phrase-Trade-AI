from fastapi import Header
from src.config.settings import env


# gets the user data from the session token
# the user data will be restrored from session cache for the RAM using session id
async def verify_bearer(authorization: str = Header(...)):
    try:
        bearer_token = authorization.split(" ")[1] if authorization else ""
        print(
            "bearer_token: ",
            bearer_token,
            env.AI_BEARER_TOKEN,
            bearer_token == env.AI_BEARER_TOKEN,
        )
        return bearer_token == env.AI_BEARER_TOKEN
    except Exception as e:
        print("Exception: ", e)
        return False

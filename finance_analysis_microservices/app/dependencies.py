from fastapi import Header, HTTPException

API_KEY = "5e884898da28047151d0e56f8dc6292773603d0d"

def verify_api_key(authorization: str = Header(...)):
    if authorization != f"ApiKey {API_KEY}":
        raise HTTPException(status_code=403, detail="Invalid API Key")
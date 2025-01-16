from fastapi import Header, HTTPException

# Установленный API-ключ
API_KEY = "5e884898da28047151d0e56f8dc6292773603d0d"

# Функция для проверки API-ключа
def verify_api_key(authorization: str = Header(None)):  # Указываем None по умолчанию
    if authorization != f"ApiKey {API_KEY}":
        raise HTTPException(status_code=403, detail="Invalid API Key")
import pytest
from httpx import AsyncClient
from app.main import app

# Тестируем успешный запрос с корректным ключом
@pytest.mark.asyncio
async def test_valid_api_key():
    headers = {"Authorization": "ApiKey 5e884898da28047151d0e56f8dc6292773603d0d"}
    async with AsyncClient(base_url="http://127.0.0.1:8000", headers=headers) as client:
        response = await client.get("/statistics")
        assert response.status_code == 200

# Тестируем запрос без ключа
@pytest.mark.asyncio
async def test_missing_api_key():
    async with AsyncClient(base_url="http://127.0.0.1:8000") as client:
        response = await client.get("/statistics")  # Без заголовка Authorization
        assert response.status_code == 403  # Ожидается 403 Forbidden


# Тестируем запрос с неправильным ключом
@pytest.mark.asyncio
async def test_invalid_api_key():
    headers = {"Authorization": "ApiKey invalid_key"}
    async with AsyncClient(base_url="http://127.0.0.1:8000", headers=headers) as client:  # Убрали `app`
        response = await client.get("/statistics")
        assert response.status_code == 403  # Ожидается 403 Forbidden из-за некорректного API-ключа
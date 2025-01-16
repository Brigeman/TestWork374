import pytest
from httpx import AsyncClient
from app.models import Transaction

@pytest.mark.asyncio
async def test_create_transaction(api_key_header):
    async with AsyncClient(base_url="http://127.0.0.1:8000") as client:
        response = await client.post(
            "/transactions",
            json={
                "transaction_id": "123456",
                "user_id": "user_001",
                "amount": 150.50,
                "currency": "USD",
                "timestamp": "2024-12-12T12:00:00"
            },
            headers=api_key_header
        )
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_invalid_transaction_data():
    headers = {"Authorization": "ApiKey 5e884898da28047151d0e56f8dc6292773603d0d"}  # Корректный API-ключ
    async with AsyncClient(base_url="http://127.0.0.1:8000", headers=headers) as client:
        response = await client.post("/transactions", json={
            "transaction_id": "",  # Неверный ID
            "user_id": "user_001",
            "amount": "not_a_number",  # Неверный формат
            "currency": "USD",
            "timestamp": "invalid_date"  # Неверная дата
        })
        assert response.status_code == 422  # Ожидаем 422 Unprocessable Entity

@pytest.mark.asyncio
async def test_get_statistics(test_db):
    db = test_db
    db.add_all([
        Transaction(transaction_id="1", user_id="user1", amount=1000, currency="USD", timestamp="2025-01-16T10:00:00"),
        Transaction(transaction_id="2", user_id="user2", amount=500, currency="USD", timestamp="2025-01-16T11:00:00"),
        Transaction(transaction_id="3", user_id="user3", amount=200, currency="USD", timestamp="2025-01-16T12:00:00"),
    ])
    db.commit()

    headers = {"Authorization": "ApiKey 5e884898da28047151d0e56f8dc6292773603d0d"}
    async with AsyncClient(base_url="http://127.0.0.1:8000", headers=headers) as client:
        response = await client.get("/statistics")
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_transactions():
    headers = {"Authorization": "ApiKey 5e884898da28047151d0e56f8dc6292773603d0d"}
    async with AsyncClient(base_url="http://127.0.0.1:8000", headers=headers) as client:
        response = await client.delete("/transactions")
        assert response.status_code == 200  # Ожидается успешный статус
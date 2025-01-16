import pytest
from httpx import AsyncClient
from app.models import Transaction

@pytest.mark.asyncio
async def test_create_transaction():
    """Тест создания транзакции."""
    async with AsyncClient(base_url="http://127.0.0.1:8000") as client:
        response = await client.post("/transactions", json={
            "transaction_id": "123456",
            "user_id": "user_001",
            "amount": 150.5,
            "currency": "USD",
            "timestamp": "2025-01-16T14:00:00"
        })
        assert response.status_code == 200
        assert response.json() == {"message": "Transaction received", "transaction_id": "123456"}

@pytest.mark.asyncio
async def test_get_statistics(test_db):
    """Тест получения статистики."""
    db = test_db
    db.add_all([
        Transaction(transaction_id="1", user_id="user1", amount=1000, currency="USD", timestamp="2025-01-16T10:00:00"),
        Transaction(transaction_id="2", user_id="user2", amount=500, currency="USD", timestamp="2025-01-16T11:00:00"),
        Transaction(transaction_id="3", user_id="user3", amount=200, currency="USD", timestamp="2025-01-16T12:00:00"),
    ])
    db.commit()

    async with AsyncClient(base_url="http://127.0.0.1:8000") as client:
        response = await client.get("/statistics")
        assert response.status_code == 200
        assert response.json() == {
            "total_transactions": 3,
            "average_transaction_amount": 566.67,
            "top_transactions": [
                {"transaction_id": "1", "amount": 1000},
                {"transaction_id": "2", "amount": 500},
                {"transaction_id": "3", "amount": 200}
            ]
        }

@pytest.mark.asyncio
async def test_delete_transactions():
    """Тест удаления всех транзакций."""
    async with AsyncClient(base_url="http://127.0.0.1:8000") as client:
        # Добавляем транзакцию
        response = await client.post("/transactions", json={
            "transaction_id": "123456",
            "user_id": "user_001",
            "amount": 150.5,
            "currency": "USD",
            "timestamp": "2025-01-16T14:00:00"
        })
        assert response.status_code == 200

        # Удаляем все транзакции
        response = await client.delete("/transactions")
        assert response.status_code == 200
        assert response.json() == {"message": "All transactions have been deleted"}

        # Проверяем, что транзакции удалены
        response = await client.get("/statistics")
        assert response.status_code == 200
        assert response.json() == {
            "total_transactions": 0,
            "average_transaction_amount": 0.0,
            "top_transactions": []
        }
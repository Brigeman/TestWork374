from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi.responses import JSONResponse
from app.security import verify_api_key  # Проверка API-ключа
from app.config import SessionLocal
from app.models import Transaction
from app.schemas import TransactionCreate
from app.services.tasks import update_statistics
from app.cache import get_cached_statistics, cache_statistics, redis_client  # Кэширование

router = APIRouter()

# Dependency для подключения к базе
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/transactions", dependencies=[Depends(verify_api_key)])
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    # Проверяем уникальность transaction_id
    if db.query(Transaction).filter(Transaction.transaction_id == transaction.transaction_id).first():
        raise HTTPException(status_code=400, detail="Transaction ID already exists")

    # Создаём новую транзакцию
    new_transaction = Transaction(
        transaction_id=transaction.transaction_id,
        user_id=transaction.user_id,
        amount=transaction.amount,
        currency=transaction.currency,
        timestamp=transaction.timestamp,
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    # Отправляем задачу в очередь Celery
    update_statistics.delay(transaction.dict())

    return {"message": "Transaction received", "transaction_id": new_transaction.transaction_id}

@router.get("/statistics", dependencies=[Depends(verify_api_key)])
def get_statistics(db: Session = Depends(get_db)):
    # Проверяем наличие статистики в кэше
    cached_stats = get_cached_statistics()
    if cached_stats:
        return cached_stats

    # Вычисляем статистику из базы данных
    total_transactions = db.query(func.count(Transaction.id)).scalar()
    average_transaction_amount = db.query(func.avg(Transaction.amount)).scalar()
    top_transactions = (
        db.query(Transaction.transaction_id, Transaction.amount)
        .order_by(Transaction.amount.desc())
        .limit(3)
        .all()
    )

    stats = {
        "total_transactions": total_transactions or 0,
        "average_transaction_amount": round(average_transaction_amount or 0, 2),
        "top_transactions": [
            {"transaction_id": t.transaction_id, "amount": t.amount}
            for t in top_transactions
        ]
    }

    # Сохраняем статистику в кэш
    cache_statistics(stats)
    return stats

@router.delete("/transactions", dependencies=[Depends(verify_api_key)])
def delete_all_transactions(db: Session = Depends(get_db)):
    # Удаляем все транзакции из базы данных
    db.query(Transaction).delete()
    db.commit()

    # Очищаем кэш
    redis_client.delete("statistics")
    return {"message": "All transactions have been deleted"}
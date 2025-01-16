from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.config import SessionLocal
from app.models import Transaction
from app.schemas import TransactionCreate

router = APIRouter()

# Dependency для подключения к базе
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/transactions")
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    # Проверяем уникальность transaction_id
    if db.query(Transaction).filter(Transaction.transaction_id == transaction.transaction_id).first():
        raise HTTPException(status_code=400, detail="Transaction ID already exists")

    # Создаём объект транзакции
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

    # Здесь можно добавить Celery задачу для обработки статистики

    return {"message": "Transaction received", "transaction_id": new_transaction.transaction_id}
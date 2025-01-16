from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import func
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

@router.get("/statistics")
def get_statistics(db: Session = Depends(get_db)):
    # Общее количество транзакций
    total_transactions = db.query(func.count(Transaction.id)).scalar()

    # Средняя сумма транзакций
    average_transaction_amount = db.query(func.avg(Transaction.amount)).scalar()

    # Топ-3 самых крупных транзакций
    top_transactions = (
        db.query(Transaction.transaction_id, Transaction.amount)
        .order_by(Transaction.amount.desc())
        .limit(3)
        .all()
    )

    # Формируем ответ
    return JSONResponse({
        "total_transactions": total_transactions or 0,
        "average_transaction_amount": round(average_transaction_amount or 0, 2),
        "top_transactions": [
            {"transaction_id": t.transaction_id, "amount": t.amount}
            for t in top_transactions
        ]
    })

@router.delete("/transactions")
def delete_all_transactions(db: Session = Depends(get_db)):
    # Удаляем все транзакции
    db.query(Transaction).delete()
    db.commit()

    # Здесь можно добавить логику очистки кеша, если требуется

    return {"message": "All transactions have been deleted"}
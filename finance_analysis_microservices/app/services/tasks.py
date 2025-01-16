from celery import Celery

celery = Celery(
    __name__,
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)

@celery.task
def update_statistics(transaction_data):
    print(f"Обновляю статистику для транзакции: {transaction_data}")
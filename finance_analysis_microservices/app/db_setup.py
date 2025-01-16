import sys
import os

# Добавляем корневую папку проекта в путь до модулей
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from app.config import Base, engine
from app.models import Transaction

# Создание таблиц
def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
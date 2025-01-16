import pytest
from app.config import Base, engine, SessionLocal
from sqlalchemy.orm import Session

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown_db():
    """Очистка и подготовка базы данных перед каждым тестом."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def test_db() -> Session:
    """Фикстура для предоставления сессии базы данных."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def api_key_header():
    return {"Authorization": "ApiKey 5e884898da28047151d0e56f8dc6292773603d0d"}
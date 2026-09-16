import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = 'sqlite:///:memory:' # база в оперативной памяти
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread':False}, poolclass=StaticPool) # соединение из разных потоков
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine) # создание таблиц

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db # тестовая сессия заместо реальной

client = TestClient(app)


def test_register_user():
    response = client.post('/register', json={
        "email": "testuser@example.com",
        "password": "testpass123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data['email'] == 'testuser@example.com'
    assert 'id' in data
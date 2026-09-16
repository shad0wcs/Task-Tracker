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


def test_login_user():
    client.post('/register', json={
        "email": "testuser1@example.com",
        "password": "testpass1123"
    })
    response = client.post('/login', json={
        "email": "testuser1@example.com",
        "password": "testpass1123" 
    })
    assert response.status_code == 200
    data = response.json()
    assert 'access_token' in data


def test_login_wrong_password():
    client.post('/register', json={
        "email": "testuser_wrongpassword@example.com",
        "password": "password"
    })
    response = client.post('/login', json={
        "email": "testuser_wrongpassword@example.com",
        "password": "wrong_password" 
    })
    assert response.status_code == 401


def test_create_task():
    client.post('/register', json={
        "email": "createtask@example.com",
        "password": "testpass1123"
    })
    login_response = client.post('/login', json={
        "email": "createtask@example.com",
        "password": "testpass1123" 
    })
    token = login_response.json()['access_token']

    response = client.post('/tasks', 
        json={'title': 'Test Task'},
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 200
    data = response.json()
    assert data['title'] == 'Test Task'
    
import os
os.environ["VERITABANI_ADI"] = "test_envanter.db"

import pytest
from fastapi.testclient import TestClient
from main import app
from database import veritabani_hazirla

@pytest.fixture(scope="session", autouse=True)
def temiz_veritabani():
    if os.path.exists("test_envanter.db"):
        os.remove("test_envanter.db")
    veritabani_hazirla()

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def auth_token(client):
    client.post("/kayit", json={
        "kullanici_adi": "test_kullanici_yeni",
        "sifre": "test123"
    })
    response = client.post("/giris", json={
        "kullanici_adi": "test_kullanici_yeni",
        "sifre": "test123"
    })
    return response.json()["access_token"]
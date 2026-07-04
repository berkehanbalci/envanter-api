import uuid
from fastapi.testclient import TestClient
from main import app


def test_ana_sayfa(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"mesaj": "Envanter API çalışıyor!"}

def test_olmayan_urun_404(client):
    response = client.get("/urunler/99999")
    assert response.status_code == 404

def test_kategori_ekle(client, auth_token):
    import uuid
    benzersiz_ad = f"test-kategori-{uuid.uuid4()}"
    response = client.post(
        "/kategoriler",
        json={"ad": benzersiz_ad},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert response.json()["mesaj"] == f"{benzersiz_ad} eklendi!"
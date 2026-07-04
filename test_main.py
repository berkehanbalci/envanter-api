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

def test_upsert_stok_artirma(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    client.post("/kategoriler", json={"ad": "test-gida"}, headers=headers)
    
    client.post("/urunler", json={
        "ad": "test-su", "fiyat": 10, "stok": 100, "kategori_adi": "test-gida"
    }, headers=headers)
    
    response = client.post("/urunler", json={
        "ad": "test-su", "fiyat": 10, "stok": 50, "kategori_adi": "test-gida"
    }, headers=headers)
    
    assert response.status_code == 200
    assert "150" in response.json()["mesaj"]

def test_farkli_fiyat_ayri_kayit(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    client.post("/kategoriler", json={"ad": "test-gida2"}, headers=headers)
    client.post("/urunler", json={
        "ad": "test-ekmek", "fiyat": 8, "stok": 100, "kategori_adi": "test-gida2"
    }, headers=headers)
    
    response = client.post("/urunler", json={
        "ad": "test-ekmek", "fiyat": 15, "stok": 30, "kategori_adi": "test-gida2"
    }, headers=headers)
    
    assert response.status_code == 200
    assert "eklendi" in response.json()["mesaj"]



def test_kategori_silme_urun_varsa_engellenir(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    client.post("/kategoriler", json={"ad": "test-elektronik"}, headers=headers)
    
    client.post("/urunler", json={
        "ad": "test-telefon", "fiyat": 5000, "stok": 10, "kategori_adi": "test-elektronik"
    }, headers=headers)
    
    kategoriler = client.get("/kategoriler").json()
    kategori_id = next(k["id"] for k in kategoriler if k["ad"] == "test-elektronik")
    
    response = client.delete(f"/kategoriler/{kategori_id}", headers=headers)
    
    assert response.status_code == 409

def test_put_atomiklik(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    client.post("/kategoriler", json={"ad": "test-kirtasiye"}, headers=headers)
    client.post("/urunler", json={
        "ad": "test-kalem", "fiyat": 5, "stok": 100, "kategori_adi": "test-kirtasiye"
    }, headers=headers)
    
    urunler = client.get("/urunler").json()
    urun_id = next(u["id"] for u in urunler if u["ad"] == "test-kalem")
    
    response = client.put(f"/urunler/{urun_id}", json={
        "ad": "degismis-isim", "fiyat": 999, "stok": 1, "kategori_adi": "olmayan-kategori"
    }, headers=headers)
    
    assert response.status_code == 404
    
    kontrol = client.get(f"/urunler/{urun_id}").json()
    assert kontrol["ad"] == "test-kalem"
    assert kontrol["fiyat"] == 5
    assert kontrol["stok"] == 100

def test_urun_silme(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    client.post("/kategoriler", json={"ad": "test-silme-kategori"}, headers=headers)
    client.post("/urunler", json={
        "ad": "test-silinecek-urun", "fiyat": 20, "stok": 5, "kategori_adi": "test-silme-kategori"
    }, headers=headers)
    
    urunler = client.get("/urunler").json()
    urun_id = next(u["id"] for u in urunler if u["ad"] == "test-silinecek-urun")
    
    response = client.delete(f"/urunler/{urun_id}", headers=headers)
    assert response.status_code == 200
    
    kontrol = client.get(f"/urunler/{urun_id}")
    assert kontrol.status_code == 404
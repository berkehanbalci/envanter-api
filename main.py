import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Urun(BaseModel):
    ad: str 
    fiyat: float
    stok: int

@app.get("/")
def ana_sayfa():
    return {"mesaj": "Envanter API çalışıyor!"}

@app.get("/urunler")
def urunleri_getir():
    baglanti = sqlite3.connect("envanter.db")
    imlec = baglanti.cursor()
    imlec.execute("SELECT id, ad, fiyat, stok FROM urunler")
    satirlar = imlec.fetchall()
    baglanti.close()

    urunler = []
    for satir in satirlar:
        urun = {
            "id": satir[0],
            "ad": satir[1],
            "fiyat": satir[2],
            "stok": satir[3]
        }
        urunler.append(urun)
    return urunler   

@app.post("/urunler")
def urun_ekle(urun: Urun):
    baglanti = sqlite3.connect("envanter.db")
    imlec = baglanti.cursor()
    imlec.execute(
        "INSERT INTO urunler (ad, fiyat, stok)  VALUES (?, ?, ?)",
        (urun.ad, urun.fiyat, urun.stok)
    ) 
    baglanti.commit()
    baglanti.close()
    return{"mesaj": f"{urun.ad} eklendi!"}

@app.delete("/urunler/{urun_id}")
def urun_sil(urun_id: int):
    baglanti = sqlite3.connect("envanter.db")
    imlec = baglanti.cursor()
    imlec.execute("DELETE FROM urunler WHERE id = ?", (urun_id,))
    baglanti.commit()
    baglanti.close()
    return {"mesaj": f"{urun_id} numaralı ürün silindi!"}

@app.put("/urunler/{urun_id}")
def urun_guncelle(urun_id: int, urun: Urun):
    baglanti = sqlite3.connect("envanter.db")
    imlec = baglanti.cursor()
    imlec.execute(
        "UPDATE urunler SET ad = ?, fiyat = ?, stok = ? WHERE id = ?",
        (urun.ad, urun.fiyat, urun.stok, urun_id)
    )
    baglanti.commit()
    baglanti.close()
    return {"mesaj": f"{urun_id} numaralı ürün güncellendi!"}
    

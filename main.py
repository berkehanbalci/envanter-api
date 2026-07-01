import sqlite3
from fastapi import FastAPI

app = FastAPI()
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
    

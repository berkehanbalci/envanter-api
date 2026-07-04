from database import veritabani_hazirla, veritabani_baglan
from database import veritabani_hazirla
from models import Urun, Kategori
from fastapi import FastAPI, HTTPException, Depends
from auth import router as auth_router, token_dogrula

app = FastAPI()

veritabani_hazirla()

app.include_router(auth_router)

@app.get("/")
def ana_sayfa():
    return {"mesaj": "Envanter API çalışıyor!"}

@app.get("/urunler")
def urunleri_getir():
    baglanti = veritabani_baglan()
    imlec = baglanti.cursor()
    imlec.execute("""
    SELECT urunler.id, urunler.ad, urunler.fiyat, urunler.stok, kategoriler.ad
    FROM urunler
    JOIN kategoriler ON urunler.kategori_id = kategoriler.id
    """)
    satirlar = imlec.fetchall()
    baglanti.close()

    urunler = []
    for satir in satirlar:
        urun = {
            "id": satir[0],
            "ad": satir[1],
            "fiyat": satir[2],
            "stok": satir[3],
            "kategori": satir[4] 
        }
        urunler.append(urun)
    return urunler  

@app.get("/urunler/{urun_id}")
def urun_getir(urun_id: int):
    baglanti = veritabani_baglan()
    imlec = baglanti.cursor()
    imlec.execute("""SELECT urunler.id, urunler.ad, urunler.fiyat, urunler.stok, kategoriler.ad 
    FROM urunler 
    JOIN kategoriler ON urunler.kategori_id = kategoriler.id
    WHERE urunler.id = ?
    """, (urun_id,))
    satir = imlec.fetchone()
    baglanti.close()
    
    if satir is None:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")
    
    return {
        "id": satir[0],
        "ad": satir[1],
        "fiyat": satir[2],
        "stok": satir[3],
        "kategori": satir[4]
    }

@app.get("/kategoriler")
def kategori_listele():
    baglanti = veritabani_baglan()
    imlec = baglanti.cursor()

    imlec.execute("SELECT id, ad FROM kategoriler")
    satirlar = imlec.fetchall()
    baglanti.close()

    kategoriler = []
    for satir in satirlar:
        urun = {
            "id": satir[0],
            "ad": satir[1],
        }
        kategoriler.append(urun)
    return kategoriler   

@app.get("/kategori-raporu")
def kategori_raporu():
    baglanti = veritabani_baglan()
    imlec = baglanti.cursor()

    imlec.execute("""
        SELECT kategoriler.id, kategoriler.ad, SUM(urunler.stok)
        FROM urunler
        JOIN kategoriler ON urunler.kategori_id = kategoriler.id
        GROUP BY kategoriler.ad
        ORDER BY kategoriler.id ASC
    """)

    satirlar = imlec.fetchall()
    baglanti.close()

    kategori_raporu = []
    for satir in satirlar:
        urun = {
            "id": satir[0],
            "ad": satir[1],
            "stok": satir[2]
        }
        kategori_raporu.append(urun)
    return kategori_raporu   

@app.post("/urunler")
def urun_ekle(urun: Urun, kullanici_adi: str = Depends(token_dogrula)):
    baglanti = veritabani_baglan()
    imlec = baglanti.cursor()
    
    imlec.execute("SELECT stok FROM urunler WHERE ad = ? AND fiyat = ?", (urun.ad, urun.fiyat))
    sonuc = imlec.fetchone()
    
    if sonuc:
        yeni_stok = sonuc[0] + urun.stok
        imlec.execute("UPDATE urunler SET stok = ? WHERE ad = ? AND fiyat = ?", (yeni_stok, urun.ad, urun.fiyat))
        mesaj = f"{urun.ad} stoğu güncellendi! Yeni stok: {yeni_stok}"
    else:
        imlec.execute("""
            SELECT id
            FROM kategoriler
            WHERE ad = ?
        """, (urun.kategori_adi,))
        kategori_sonuc = imlec.fetchone()
        if kategori_sonuc:
            kategori_id = kategori_sonuc[0]
            imlec.execute(
                "INSERT INTO urunler (ad, fiyat, stok, kategori_id) VALUES (?, ?, ?, ?)",
                (urun.ad, urun.fiyat, urun.stok, kategori_id)
            )
            mesaj = f"{urun.ad} eklendi!"    
        else:
            baglanti.close()
            raise HTTPException(status_code=404, detail=f"{urun.kategori_adi} kategorisi bulunamadı! Önce kategoriyi ekleyin.")
        
    
    baglanti.commit()
    baglanti.close()
    return {"mesaj": mesaj}

@app.delete("/urunler/{urun_id}")
def urun_sil(urun_id: int, kullanici_adi: str = Depends(token_dogrula)):
    baglanti = veritabani_baglan()
    imlec = baglanti.cursor()
    imlec.execute("SELECT id FROM urunler WHERE id = ?", (urun_id,))
    sonuc = imlec.fetchone()

    if sonuc is None:
        baglanti.close()
        raise HTTPException(status_code=404, detail="Ürün bulunamadı!")

    imlec.execute("DELETE FROM urunler WHERE id = ?", (urun_id,))
    baglanti.commit()
    baglanti.close()
    return {"mesaj": f"{urun_id} numaralı ürün silindi!"}

@app.put("/urunler/{urun_id}")
def urun_guncelle(urun_id: int, urun: Urun, kullanici_adi: str = Depends(token_dogrula)):
    baglanti = veritabani_baglan()
    imlec = baglanti.cursor()

    imlec.execute("SELECT id FROM urunler WHERE id = ?", (urun_id,))
    sonuc = imlec.fetchone()

    if sonuc is None:
        baglanti.close()
        raise HTTPException(status_code=404, detail="Ürün bulunamadı!")

    imlec.execute("SELECT id FROM kategoriler WHERE ad = ?", (urun.kategori_adi,))
    kategori_sonuc = imlec.fetchone()
    if kategori_sonuc is None:
        baglanti.close()
        raise HTTPException(status_code=404, detail=f"{urun.kategori_adi} kategorisi bulunamadı!")
    
    kategori_id = kategori_sonuc[0]

    imlec.execute(
        "UPDATE urunler SET ad = ?, fiyat = ?, stok = ?, kategori_id = ? WHERE id = ?",
        (urun.ad, urun.fiyat, urun.stok, kategori_id, urun_id)
    )
    baglanti.commit()
    baglanti.close()
    return {"mesaj": f"{urun_id} numaralı ürün güncellendi!"}


@app.post("/kategoriler")
def kategori_ekle(kategori: Kategori, kullanici_adi: str = Depends(token_dogrula)):
    baglanti = veritabani_baglan()
    imlec = baglanti.cursor()
    
    imlec.execute("SELECT id FROM kategoriler WHERE ad = ?", (kategori.ad,))
    sonuc = imlec.fetchone()
    
    if sonuc:
        baglanti.close()
        raise HTTPException(status_code=409, detail=f"{kategori.ad} kategorisi zaten mevcut!")
    else:
        imlec.execute(
            "INSERT INTO kategoriler (ad) VALUES (?)", (kategori.ad,))
        mesaj = f"{kategori.ad} eklendi!"
    
    baglanti.commit()
    baglanti.close()
    return {"mesaj": mesaj}

@app.delete("/kategoriler/{kategori_id}")
def kategori_sil(kategori_id: int, kullanici_adi: str = Depends(token_dogrula)):
    baglanti = veritabani_baglan()
    imlec = baglanti.cursor()
    
    
    imlec.execute("SELECT id FROM kategoriler WHERE id = ?", (kategori_id,))
    if imlec.fetchone() is None:
        baglanti.close()
        raise HTTPException(status_code=404, detail="Kategori bulunamadı!")
    
    
    imlec.execute("SELECT id FROM urunler WHERE kategori_id = ?", (kategori_id,))
    if imlec.fetchone() is not None:
        baglanti.close()
        raise HTTPException(status_code=409, detail="Bu kategoride ürünler var, önce onları silin/taşıyın!")
    
    
    imlec.execute("DELETE FROM kategoriler WHERE id = ?", (kategori_id,))
    baglanti.commit()
    baglanti.close()
    return {"mesaj": f"{kategori_id} numaralı kategori silindi!"}    
    
import sqlite3

def veritabani_hazirla():
    baglanti = sqlite3.connect("envanter.db")
    imlec = baglanti.cursor()

    imlec.execute("""
        CREATE TABLE IF NOT EXISTS urunler(
            id INTEGER PRIMARY KEY,
            ad TEXT,
            fiyat REAL,
            stok INTEGER,
            kategori_id INTEGER
        )
    """)

    imlec.execute("""
        CREATE TABLE IF NOT EXISTS kategoriler(
            id INTEGER PRIMARY KEY,
            ad TEXT UNIQUE
        )
    """)

    imlec.execute("""
        CREATE TABLE IF NOT EXISTS kullanicilar(
            id INTEGER PRIMARY KEY,
            kullanici_adi TEXT UNIQUE,
            sifre_hash TEXT
        )
    """)

    baglanti.commit()
    baglanti.close()
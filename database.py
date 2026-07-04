import sqlite3
import os

VERITABANI_ADI = os.getenv("VERITABANI_ADI", "envanter.db")

def veritabani_baglan():
    return sqlite3.connect(VERITABANI_ADI)

def veritabani_hazirla():
    baglanti = veritabani_baglan()
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
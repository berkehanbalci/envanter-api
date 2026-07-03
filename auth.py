import sqlite3
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from jose import jwt
from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from models import Kullanici
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from fastapi import Depends

guvenlik_semasi = HTTPBearer()

load_dotenv()
GIZLI_ANAHTAR = os.getenv("GIZLI_ANAHTAR")
ALGORITMA = "HS256"
TOKEN_GECERLILIK_SURESI = 60 

router = APIRouter()
sifreleme = CryptContext(schemes=["bcrypt"], deprecated="auto")

def token_olustur(kullanici_adi: str):
    son_kullanma = datetime.utcnow() + timedelta(minutes=TOKEN_GECERLILIK_SURESI)
    veri = {
        "sub": kullanici_adi,
        "exp": son_kullanma
    }
    token = jwt.encode(veri, GIZLI_ANAHTAR, algorithm= ALGORITMA)
    return token

def token_dogrula(kimlik: HTTPAuthorizationCredentials = Depends(guvenlik_semasi)):
    token = kimlik.credentials
    try:
        veri = jwt.decode(token, GIZLI_ANAHTAR, algorithms= [ALGORITMA])
        kullanici_adi = veri.get("sub")
        if kullanici_adi is None:
            raise HTTPException(status_code=401, detail="Geçersiz token veya süresi dolmuş token!")
        return kullanici_adi
    except JWTError:
        raise HTTPException(status_code=401, detail="Geçersiz veya süresi dolmuş token!")        

@router.post("/kayit")
def kayit_ol(kullanici: Kullanici):
    baglanti = sqlite3.connect("envanter.db")
    imlec = baglanti.cursor()

    imlec.execute("""
    SELECT id 
    FROM kullanicilar 
    WHERE kullanici_adi = ?
    """, (kullanici.kullanici_adi,))
    sonuc = imlec.fetchone()

    if sonuc:

        baglanti.close()
        raise HTTPException(status_code=409, detail="Bu kullanıcı zaten alınmış!")

    sifre_hash = sifreleme.hash(kullanici.sifre)
    imlec.execute(
        "INSERT INTO kullanicilar (kullanici_adi, sifre_hash) VALUES (?, ?)",(kullanici.kullanici_adi, sifre_hash)
    )
    baglanti.commit()
    baglanti.close()
    return {"mesaj": f"{kullanici.kullanici_adi} kaydedildi!"}

@router.post("/giris")
def giris_yap(kullanici: Kullanici):
    baglanti = sqlite3.connect("envanter.db")
    imlec = baglanti.cursor()

    imlec.execute("""
        SELECT sifre_hash
        FROM kullanicilar
        WHERE kullanici_adi = ?
    """, (kullanici.kullanici_adi,))
    sonuc = imlec.fetchone()
    baglanti.close()

    if sonuc is None:
        raise HTTPException(status_code=401, detail="Kullanıcı adı veya şifre hatalı!")

    kayitli_hash = sonuc[0]
    if not sifreleme.verify(kullanici.sifre, kayitli_hash):
        raise HTTPException(status_code=401, detail="Kullanıcı adı veya şifre hatalı")

    token = token_olustur(kullanici.kullanici_adi)
    return {"access_token": token, "token_type": "bearer"}  

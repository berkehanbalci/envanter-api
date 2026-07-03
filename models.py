from pydantic import BaseModel

class Urun(BaseModel):
    ad: str
    fiyat: float
    stok: int
    kategori_adi: str

class Kategori(BaseModel):
    ad: str


class Kullanici(BaseModel):
    kullanici_adi: str
    sifre: str    
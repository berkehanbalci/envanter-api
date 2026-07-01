# Envanter API

FastAPI ile yazılmış, ürünleri yöneten bir web API'si

## Özellikler
Şu an: ürünleri listeleme. İleride: ekleme, güncelleme, silme

## Kullanılan Teknolojiler
- Python
- FastAPI
- SQLite
- Uvicorn

## Kurulum
pip install fastapi uvicorn

## Çalıştırma
Terminalde şu komutu çalıştırın:

```
uvicorn main:app --reload
```

Ardından tarayıcıdan http://127.0.0.1:8000 adresine gidin.

## Endpoint'ler
- GET /urunler → tüm ürünleri listeler
- GET / → API durumunu döndürür
- GET /docs → otomatik API dokümantasyonu (Swagger)
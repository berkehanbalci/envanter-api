# Envanter API

FastAPI ile yazılmış, ürünleri ve kategorileri yöneten bir REST API. Ürünler ve kategoriler için tam CRUD işlemleri, ilişkisel veritabanı yapısı (JOIN), stok yönetimi ve hata kontrolü içerir.

## Özellikler

- Ürün ekleme, listeleme, güncelleme ve silme (tam CRUD)
- Kategori ekleme, listeleme ve silme
- İlişkisel yapı: her ürün bir kategoriye bağlıdır (JOIN ile birleştirilir)
- Akıllı stok yönetimi: aynı isim ve aynı fiyattaki ürün tekrar eklenirse stok artırılır, farklı fiyattaysa ayrı kayıt açılır
- Kategori bazlı stok raporu (toplam stok)
- Hata yönetimi: bulunamayan kayıtlar için 404, çakışan işlemler için 409
- İlişkisel bütünlük: içinde ürün bulunan kategori silinemez
- Veritabanı ilk çalıştırmada otomatik oluşturulur

## Kullanılan Teknolojiler

- Python
- FastAPI
- SQLite
- Pydantic
- Uvicorn

## Kurulum

```
pip install fastapi uvicorn
```

## Çalıştırma

Terminalde şu komutu çalıştırın:

```
uvicorn main:app --reload
```

Ardından tarayıcıdan http://127.0.0.1:8000 adresine gidin.

İnteraktif dokümantasyon (Swagger) için: http://127.0.0.1:8000/docs

## Endpoint'ler

### Ürünler

- `GET /urunler` — tüm ürünleri kategorileriyle birlikte listeler
- `GET /urunler/{id}` — tek bir ürünü getirir
- `POST /urunler` — yeni ürün ekler (aynı isim + aynı fiyat varsa stok artırır)
- `PUT /urunler/{id}` — ürünü günceller
- `DELETE /urunler/{id}` — ürünü siler

### Kategoriler

- `GET /kategoriler` — tüm kategorileri listeler
- `POST /kategoriler` — yeni kategori ekler
- `DELETE /kategoriler/{id}` — kategoriyi siler (içinde ürün yoksa)

### Raporlama

- `GET /kategori-raporu` — her kategorideki toplam stok miktarını gösterir

### Diğer

- `GET /` — API durumunu döndürür
- `GET /docs` — otomatik API dokümantasyonu (Swagger)

## Örnek Kullanım

Kategori ekleme:

```
POST /kategoriler
{
  "ad": "gıda"
}
```

Ürün ekleme:

```
POST /urunler
{
  "ad": "su",
  "fiyat": 10,
  "stok": 200,
  "kategori_adi": "gıda"
}
```

## Veri Modeli

Ürün ve kategori bilgileri SQLite veritabanında iki tabloda tutulur:

- **urunler**: id, ad, fiyat, stok, kategori_id
- **kategoriler**: id, ad

Ürünler `kategori_id` üzerinden kategorilere bağlanır ve sorgularda JOIN ile birleştirilir.
# Envanter API

FastAPI ile yazılmış, ürünleri ve kategorileri yöneten bir REST API. Ürünler ve kategoriler için tam CRUD işlemleri, ilişkisel veritabanı yapısı (JOIN), stok yönetimi, JWT tabanlı kimlik doğrulama ve hata kontrolü içerir.

## Özellikler

- Ürün ekleme, listeleme, güncelleme ve silme (tam CRUD)
- Kategori ekleme, listeleme ve silme
- İlişkisel yapı: her ürün bir kategoriye bağlıdır (JOIN ile birleştirilir)
- Akıllı stok yönetimi: aynı isim ve aynı fiyattaki ürün tekrar eklenirse stok artırılır, farklı fiyattaysa ayrı kayıt açılır
- Kategori bazlı stok raporu (toplam stok)
- Kullanıcı kaydı ve girişi (şifreler bcrypt ile hash'lenir, düz metin saklanmaz)
- JWT tabanlı yetkilendirme: veri değiştiren işlemler (ekleme, güncelleme, silme) sadece giriş yapmış kullanıcılar tarafından yapılabilir; listeleme herkese açıktır
- Hata yönetimi: bulunamayan kayıtlar için 404, çakışan işlemler için 409, yetkisiz erişim için 401
- İlişkisel bütünlük: içinde ürün bulunan kategori silinemez
- Veritabanı ilk çalıştırmada otomatik oluşturulur

## Kullanılan Teknolojiler

- Python
- FastAPI
- SQLite
- Pydantic
- Uvicorn
- python-jose (JWT üretimi ve doğrulaması)
- passlib + bcrypt (şifre hash'leme)
- python-dotenv (gizli anahtar yönetimi)

## Proje Yapısı

```
envanter-api/
├── main.py       # FastAPI uygulaması ve ürün/kategori endpoint'leri
├── models.py     # Pydantic veri modelleri (Urun, Kategori, Kullanici)
├── database.py   # Veritabanı bağlantısı ve tablo tanımları
├── auth.py       # Kayıt, giriş, JWT üretimi ve doğrulama
├── .env          # Gizli anahtar (deposuna dahil değildir)
└── README.md
```

## Kurulum

```
pip install fastapi uvicorn python-jose[cryptography] python-dotenv passlib bcrypt
```

Proje klasöründe bir `.env` dosyası oluşturup içine bir gizli anahtar tanımlayın:

```
GIZLI_ANAHTAR=kendi-belirleyeceginiz-uzun-ve-rastgele-bir-metin
```

## Çalıştırma

Terminalde şu komutu çalıştırın:

```
uvicorn main:app --reload
```

Ardından tarayıcıdan http://127.0.0.1:8000 adresine gidin.

İnteraktif dokümantasyon (Swagger) için: http://127.0.0.1:8000/docs

Swagger üzerinden korumalı bir endpoint'i denemek için önce `/giris` ile bir token alın, sağ üstteki **Authorize** butonuna tıklayıp token'ı yapıştırın.

## Endpoint'ler

🔓 herkese açık · 🔒 giriş yapılmış kullanıcı gerektirir (JWT token)

### Kimlik Doğrulama

- 🔓 `POST /kayit` — yeni kullanıcı kaydı oluşturur
- 🔓 `POST /giris` — kullanıcı adı ve şifre ile giriş yapar, JWT token döndürür

### Ürünler

- 🔓 `GET /urunler` — tüm ürünleri kategorileriyle birlikte listeler
- 🔓 `GET /urunler/{id}` — tek bir ürünü getirir
- 🔒 `POST /urunler` — yeni ürün ekler (aynı isim + aynı fiyat varsa stok artırır)
- 🔒 `PUT /urunler/{id}` — ürünü günceller
- 🔒 `DELETE /urunler/{id}` — ürünü siler

### Kategoriler

- 🔓 `GET /kategoriler` — tüm kategorileri listeler
- 🔒 `POST /kategoriler` — yeni kategori ekler
- 🔒 `DELETE /kategoriler/{id}` — kategoriyi siler (içinde ürün yoksa)

### Raporlama

- 🔓 `GET /kategori-raporu` — her kategorideki toplam stok miktarını gösterir

### Diğer

- 🔓 `GET /` — API durumunu döndürür
- 🔓 `GET /docs` — otomatik API dokümantasyonu (Swagger)

## Örnek Kullanım

Kayıt olma:

```
POST /kayit
{
  "kullanici_adi": "berkehan123",
  "sifre": "guvenli-bir-sifre"
}
```

Giriş yapma (token almak için):

```
POST /giris
{
  "kullanici_adi": "berkehan123",
  "sifre": "guvenli-bir-sifre"
}
```

Dönen `access_token`, korumalı endpoint'lerde `Authorization: Bearer <token>` header'ı ile gönderilir.

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

Ürün ve kategori bilgileri SQLite veritabanında üç tabloda tutulur:

- **urunler**: id, ad, fiyat, stok, kategori_id
- **kategoriler**: id, ad
- **kullanicilar**: id, kullanici_adi, sifre_hash

Ürünler `kategori_id` üzerinden kategorilere bağlanır ve sorgularda JOIN ile birleştirilir.
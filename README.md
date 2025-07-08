# SmartFace-Checkin-System
A real-time face recognition system integrated with an MSSQL database for secure and automated attendance tracking. This project captures faces from a camera feed, compares them with stored embeddings, logs recognized and unrecognized faces, and keeps all data safely in a structured database.

# 📌 Yüz Tanıma Tabanlı Kapı Erişim Sistemi

## 🔍 Proje Tanımı
Bu proje, **Python**, **OpenCV**, **Face Recognition** ve **MSSQL** kullanarak geliştirilen bir **yüz tanıma tabanlı kapı erişim sistemi**dir. Sistem, kullanıcıların yüz verilerini veritabanında saklar ve gerçek zamanlı kamera görüntüsünden alınan yüzleri veritabanındaki yüzlerle karşılaştırarak **erişim izni** veya **reddi** verir.

---

## ✅ Kimlik Doğrulama ve Yetkilendirme
- Kullanıcılar sisteme giriş yapmak için **kullanıcı adı** ve **şifre** kullanır.
- Şifreler **SHA-256** algoritmasıyla hashlenerek güvenli bir şekilde saklanır.
- Giriş başarılı olursa kullanıcının rolü belirlenir (**admin** veya **user**).
- **Yalnızca admin yetkisine sahip kullanıcılar** yüz tanıma sürecini başlatabilir.
- Bu yapı sayesinde yetkisiz kişilerin sisteme erişimi engellenir.

---

## 📂 Proje Bileşenleri

| Dosya | Açıklama |
|---------------------|---------------------------------------------------------------------------------------------|
| **AddToDatabase.py** | Yüz verilerini işleyerek MSSQL veritabanına ekler veya günceller. |
| **Authentication.py** | Kullanıcı girişini doğrular, şifreleri SHA-256 ile hashler. |
| **Authorization.py** | Kullanıcı yetkilendirmesini yapar ve giriş loglarını MSSQL'e kaydeder. |
| **EncodeGenerator.py** | Yüz verilerini vektör formatına (embedding) çevirir. |
| **main.py** | Gerçek zamanlı kamera görüntüsünü alır, yüz tanıma yapar ve kapı erişimini yönetir. |

---

## 🛠 Çalışma Mantığı

### 1️⃣ Yüz Verilerinin Kaydedilmesi (`AddToDatabase.py`)
- **Images** klasöründeki tüm yüz görselleri okunur.
- Her görsel için **face_recognition** kütüphanesiyle yüz vektörleri (embedding) oluşturulur.
- Kişi veritabanında yoksa eklenir, varsa güncellenir.
- **SQL Injection** riskine karşı koruma yapılır.

---

### 2️⃣ Kullanıcı Girişi (`Authentication.py`)
- Kullanıcıdan **kullanıcı adı** ve **şifre** istenir.
- Şifre, **SHA-256** ile hashlenir ve veritabanındaki hash ile karşılaştırılır.
- Giriş başarılı olursa kullanıcının rolü döndürülür.

---

### 3️⃣ Yetkilendirme ve Loglama (`Authorization.py`)
- Kullanıcının rolü kontrol edilir (**admin değilse erişim engellenir**).
- Giriş bilgileri **MSSQL** veritabanındaki **Log** tablosuna kaydedilir.

---

### 4️⃣ Yüz Tanıma ve Kapı Açma (`main.py`)
- MSSQL’den kayıtlı yüz verileri çekilir.
- Kamera görüntüsü işlenerek yüz tespiti yapılır.
- Bulunan yüzler, veritabanındaki yüz vektörleriyle karşılaştırılır.
- Eşleşme durumunda:
  - **Yetkili kişi tanındıysa:** Kapı açılır.
  - **Tanınmayan yüz tespit edilirse:** Log’a kaydedilir, alarm verilir.

---

## 📊 Veritabanı (MSSQL) Yapısı

| Tablo | Açıklama |
|----------------|----------------------------------------------------------|
| **Users** | Kullanıcı bilgileri (ID, Username, Password, Role) |
| **Kisiler** | Yüz verileri ve ad-soyad bilgileri |
| **Log** | Kullanıcı giriş denemeleri ve yetkisiz yüz algılamaları |

---

## 🔑 Öne Çıkan Güvenlik Özellikleri
- ✔ **SHA-256 Şifreleme:** Şifreler düz metin olarak saklanmaz.
- ✔ **SQL Injection Koruması:** Zararlı sorgular engellenir.
- ✔ **Yetkilendirme:** Sadece admin yetkisi olan kullanıcılar sistemi yönetebilir.
- ✔ **Gerçek Zamanlı Kayıt:** Yetkisiz giriş denemeleri MSSQL üzerinde kayıt altına alınır.

---

## 🚀 Amaç
Bu proje, fiziksel erişim güvenliğini artırmak için tasarlanmış modern, güvenilir ve ölçeklenebilir bir çözüm sunar.

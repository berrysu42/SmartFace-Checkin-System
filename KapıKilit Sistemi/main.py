from Authentication import login, get_db_connection  # Kullanıcı girişi
from Authorization import check_authorization, log_entry  # Yetkilendirme
import cv2
import face_recognition
import numpy as np
import json
from AddToDatabase import get_db_connection  # MSSQL bağlantısı

# Kullanıcı giriş ekranı
print("🔐 Lütfen giriş yapın:")
username = input("Kullanıcı Adı: ")
password = input("Şifre: ")

# Kullanıcı doğrulaması
user_role = login(username, password)
if user_role is None:
    print("❌ Giriş başarısız! Kullanıcı adı veya şifre hatalı.")
    exit()

print(f"✅ Giriş başarılı! Rolünüz: {user_role}")

# Eğer kullanıcı admin değilse, yüz tanıma başlatılmaz
if user_role != "admin":
    print("⛔ Yetkisiz kullanıcı! Yüz tanıma başlatılamaz.")
    exit()

# Veritabanından yüz verilerini çekme işlemi
conn = get_db_connection()  # Bu fonksiyon Authentication'dan alınıyor.
cursor = conn.cursor()
cursor.execute("SELECT ID, AdSoyad, YuzVerisi FROM Kisiler")
face_data = cursor.fetchall()

encodeListKnown = []
personIds = []
personNames = []

for person_id, name, embedding in face_data:
    embedding_array = np.array(json.loads(embedding))
    encodeListKnown.append(embedding_array)
    personIds.append(person_id)
    personNames.append(name)

print("✅ Yüz verileri yüklendi.")

# Yüz tanıma başlatılıyor
cap = cv2.VideoCapture(0)  # Kamera açma

while True:
    success, img = cap.read()  # Kameradan görüntü alma
    if not success:
        continue  # Görüntü alınamazsa devam etme

    imgK = cv2.resize(img, (0, 0), None, 0.5, 0.5)  # Görüntüyü yeniden boyutlandırma
    imgK = cv2.cvtColor(imgK, cv2.COLOR_BGR2RGB)  # Görüntüyü RGB'ye dönüştürme

    # Yüz tespiti
    faceCurFrame = face_recognition.face_locations(imgK)
    encodeCurFrame = face_recognition.face_encodings(imgK, faceCurFrame)

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)  # Yüzleri karşılaştırma
            faceDistance = face_recognition.face_distance(encodeListKnown, encodeFace)  # Mesafe hesaplama

            if len(faceDistance) > 0:
                matchIndex = np.argmin(faceDistance)  # En düşük mesafeyi bulma
            else:
                print("⚠️ Eşleşme bulunamadı!")
                continue

            if matches[matchIndex]:
                # Yüz eşleşmesi sağlandı
                id = personIds[matchIndex]
                name = personNames[matchIndex]

                print(f"✅ Yetkili kişi tespit edildi: {name}")
                log_entry(id, True)  # Yetkili giriş kaydını yapma
                print("🚪 Kapı açılıyor...")

            else:
                print("⚠️ Bilinmeyen Yüz Algılandı!")
                log_entry(None, False)  # Bilinmeyen yüz kaydını yapma

    cv2.imshow("Face Recognition", img)  # Tanıma penceresini gösterme
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break  # 'q' tuşuna basıldığında çıkma

cap.release()  # Kamera kaydını durdurma
cv2.destroyAllWindows()  # Pencereleri kapatma

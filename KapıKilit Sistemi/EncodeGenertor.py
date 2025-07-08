import cv2
import face_recognition
import os
import pyodbc
import json
import numpy as np
'''
Başka server üzerinden bağlantı sağlamak için(Dinamik atama)
server = input("MSSQL Server Adresi veya IP (Lokal ise 'localhost' yazın): ").strip()
database = "FaceRecognitionDB"

conn = pyodbc.connect(
    f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
)
cursor = conn.cursor()'''
def get_db_connection():
    try:
        conn = pyodbc.connect(
            "DRIVER={SQL Server};SERVER=localhost;DATABASE=FaceRecognitionDB;Trusted_Connection=yes;"
        )
        return conn
    except Exception as e:
        print(f"❌ MSSQL bağlantı hatası: {e}")
        return None

# Yüz verilerini çıkaran fonksiyon
def findEncodings(imagesList):
    """Yüz verilerini çıkaran fonksiyon"""
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(img)
        encodeList.append(encodings[0] if encodings else None)
    return encodeList

# Yüz verilerini veritabanına ekleyen veya güncelleyen fonksiyon
def save_or_update_encoding(encodeListKnown, personelNames):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()

        try:
            for i in range(len(encodeListKnown)):
                if encodeListKnown[i] is not None:
                    emb_str = json.dumps(encodeListKnown[i].tolist())  # NumPy dizisini JSON formatına çevirme

                    # Kişiyi kontrol et, var mı yok mu?
                    cursor.execute("SELECT COUNT(*) FROM Kisiler WHERE AdSoyad = ?", (personelNames[i],))
                    result = cursor.fetchone()[0]

                    if result > 0:
                        # Kişi varsa yüz verisini güncelle
                        cursor.execute("UPDATE Kisiler SET YuzVerisi = ? WHERE AdSoyad = ?", (emb_str, personelNames[i]))
                        print(f"🔄 Güncellendi: {personelNames[i]}")
                    else:
                        # Kişi yoksa yeni kişi olarak ekle
                        cursor.execute("INSERT INTO Kisiler (AdSoyad, YuzVerisi) VALUES (?, ?)", (personelNames[i], emb_str))
                        print(f"✅ Eklendi: {personelNames[i]}")

            # Değişiklikleri kaydet
            conn.commit()
            print("✅ Embeddings successfully saved to MSSQL.")
            #print("✅ Veritabanı işlemi başarıyla tamamlandı.")
        except Exception as e:
            print(f"❌ Veritabanı işlemi sırasında hata oluştu: {e}")
        finally:
            # Bağlantıyı kapat
            conn.close()
            print("🔌 MSSQL bağlantısı kapatıldı.")

# Görselleri yükleme
folderPath = 'Images'
pathList = os.listdir(folderPath)

imgList = []
personelNames = []

for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    personelNames.append(os.path.splitext(path)[0])  # Dosya adından isim çıkar

print("🔍 Encoding başladı...")
encodeListKnown = findEncodings(imgList)
print("✅ Encoding tamamlandı.")

# Yüz verilerini veritabanına kaydet ve güncelle
save_or_update_encoding(encodeListKnown, personelNames)



import re
import cv2
import face_recognition
import os
import json
import numpy as np
import pyodbc

# SQL Injection önleme
def temizle_isim(isim):
    return re.sub(r"[^\w\s]", "", isim).strip()

def get_db_connection():
    """
    MSSQL veritabanına bağlanmak için fonksiyon.
    """
    try:
        conn = pyodbc.connect(
            "DRIVER={SQL Server};SERVER=localhost;DATABASE=FaceRecognitionDB;Trusted_Connection=yes;",
            autocommit=True
        )
        return conn
    except Exception as e:
        print(f"❌ Veritabanı bağlantı hatası: {e}")
        return None

conn = get_db_connection()
if not conn:
    exit()

cursor = conn.cursor()
print("✅ MSSQL bağlantısı başarılı.")

print("📂 Klasörden resimler okunuyor...")

folderPath = "Images"
pathList = os.listdir(folderPath)

imgList = []
personelNames = []

for path in pathList:
    img_path = os.path.join(folderPath, path)
    img = cv2.imread(img_path)
    if img is not None:
        imgList.append(img)
        personelNames.append(temizle_isim(os.path.splitext(path)[0]))
    else:
        print(f"⚠️ Geçersiz dosya atlandı: {img_path}")

def findEncodings(imagesList):
    """Yüz verilerini çıkaran fonksiyon"""
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(img)
        encodeList.append(encodings[0] if encodings else None)
    return encodeList

print("🔍 Encoding başladı...")
encodeListKnown = findEncodings(imgList)
print("✅ Encoding tamamlandı.")

try:
    for i in range(len(encodeListKnown)):
        if encodeListKnown[i] is not None:
            emb_str = json.dumps(encodeListKnown[i].tolist())

            cursor.execute("SELECT 1 FROM Kisiler WHERE AdSoyad = ?", (personelNames[i],))
            result = cursor.fetchone()

            if result:
                cursor.execute("UPDATE Kisiler SET YuzVerisi = ? WHERE AdSoyad = ?", (emb_str, personelNames[i]))
                print(f"🔄 Güncellendi: {personelNames[i]}")
            else:
                cursor.execute("INSERT INTO Kisiler (AdSoyad, YuzVerisi) VALUES (?, ?)", (personelNames[i], emb_str))
                print(f"✅ Eklendi: {personelNames[i]}")

    print("✅ Klasörden okunan veriler başarıyla eklendi.")
except Exception as e:
    print(f"❌ Veritabanı hatası: {e}")
finally:
    conn.close()
    print("🔌 MSSQL bağlantısı kapatıldı.")

print("✅ İşlem tamamlandı.")

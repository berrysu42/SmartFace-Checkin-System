import pyodbc
import hashlib

import pyodbc
import hashlib

def get_db_connection():
    """
    MSSQL bağlantısını döndürür.
    """
    conn = pyodbc.connect(
        "DRIVER={SQL Server};SERVER=localhost;DATABASE=FaceRecognitionDB;Trusted_Connection=yes;"
    )
    return conn


def hash_password(password):
    """
    Kullanıcı şifresini güvenli hale getirmek için SHA-256 ile hash'ler.
    """
    return hashlib.sha256(password.encode()).hexdigest()


def login(username, password):
    """
    Kullanıcı adı ve şifreyi MSSQL'de doğrular.
    Eğer doğruysa kullanıcının rolünü döndürür.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Şifreyi hash'leme
    hashed_password = hash_password(password)
    print(f"Hashlenen Şifre: {hashed_password}")  #  Hash'lenmiş şifreyi yazdır

    cursor.execute("SELECT Role, Password FROM Users WHERE Username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user:
        stored_password = user[1]
        print(f"Veritabanındaki Şifre: {stored_password}")  #  Veritabanındaki şifreyi yazdır
        if hashed_password == stored_password:
            return user[0]  # Kullanıcının rolünü döndürür
    return None  # Kullanıcı yoksa None döndürür



def register_user(username, password):
    """
    Yeni kullanıcı kaydeder;
    Şifreyi hash'ler ve kullanıcıyı veritabanına ekler.
    """
    hashed_password = hash_password(password)  # Şifreyi hash'le
    conn = get_db_connection()
    cursor = conn.cursor()

    # Kullanıcıyı veritabanına ekleme
    cursor.execute("INSERT INTO Users (Username, Password, Role) VALUES (?, ?, ?)",
                   (username, hashed_password, "user"))  # Varsayılan rol: user
    conn.commit()
    conn.close()
    print("✅ Yeni kullanıcı başarıyla kaydedildi.")

from Authentication import login, get_db_connection  # MSSQL bağlantısını kullanma
from datetime import datetime

def check_authorization(user_id):
    """
    Kullanıcının yetkisini kontrol eder.
    Eğer kullanıcının rolü 'admin' ise True, değilse False döner.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Role FROM Users WHERE ID = ?", (user_id,))
    role = cursor.fetchone()
    conn.close()

    return role and role[0] == "admin"  # Admin ise True döner

def log_entry(user_id, success):
    """
    Kullanıcının giriş logunu kaydeder.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Real-Time
    status = "Başarılı" if success else "Başarısız"

    cursor.execute("INSERT INTO Log (UserID, Success, Timestamp) VALUES (?, ?, ?)",
                   (user_id, status, timestamp))
    conn.commit()
    conn.close()

    if success:
        print(f"✅ Kullanıcı {user_id} giriş yaptı ({timestamp}).")
    else:
        print(f"⛔ Yetkisiz giriş denemesi ({timestamp})!")

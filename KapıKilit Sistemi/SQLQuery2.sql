-- Kullanýcý kaydederken:
INSERT INTO Users (Username, Password, Role) 
VALUES ('admin', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 'admin');

CREATE TABLE Users (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    Username NVARCHAR(50) UNIQUE NOT NULL,
    Password NVARCHAR(255) NOT NULL,  -- Hash'lenmiþ þifre
    Role NVARCHAR(10) NOT NULL  -- "admin" veya "user"
);

CREATE TABLE Log (
    LogID INT IDENTITY(1,1) PRIMARY KEY,
    UserID INT NULL,
    Success VARCHAR(50),
    Timestamp DATETIME
);

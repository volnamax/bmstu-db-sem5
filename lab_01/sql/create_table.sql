-- Сценарий создания базы данных и базовых таблиц
CREATE TABLE IF NOT EXISTS Clients (
    ClientID SERIAL PRIMARY KEY,
    Имя VARCHAR(50) NOT NULL,
    Фамилия VARCHAR(50) NOT NULL,
    Телефон VARCHAR(20) NOT NULL,
    Email VARCHAR(50),
    Адрес VARCHAR(255)
);
CREATE TABLE IF NOT EXISTS Cars (
    CarID SERIAL PRIMARY KEY,
    ClientID INTEGER,
    Марка VARCHAR(50) NOT NULL,
    Модель VARCHAR(50) NOT NULL,
    Год_выпуска INTEGER,
    VIN VARCHAR(50)
);
CREATE TABLE IF NOT EXISTS Masters (
    MasterID SERIAL PRIMARY KEY,
    Имя VARCHAR(50) NOT NULL,
    Фамилия VARCHAR(50) NOT NULL,
    Специализация VARCHAR(50) NOT NULL,
    Опыт_работы INTEGER,
    Телефон VARCHAR(20)
);
CREATE TABLE IF NOT EXISTS Services (
    ServiceID SERIAL PRIMARY KEY,
    Название VARCHAR(50) NOT NULL,
    Описание TEXT NOT NULL,
    Стоимость INTEGER,
    Продолжительность INTEGER
);
CREATE TABLE IF NOT EXISTS Orders (
    OrderID SERIAL PRIMARY KEY,
    CarID INTEGER NOT NULL,
    MasterID INTEGER NOT NULL,
    ServiceID INTEGER NOT NULL,
    Дата_заказа DATE NOT NULL,
    Статус_заказа VARCHAR(50) NOT NULL,
    Комментарии TEXT,
    FOREIGN KEY (CarID) REFERENCES Cars(CarID),
    FOREIGN KEY (MasterID) REFERENCES Masters(MasterID),
    FOREIGN KEY (ServiceID) REFERENCES Services(ServiceID)
);
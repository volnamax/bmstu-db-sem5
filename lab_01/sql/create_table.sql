-- Сценарий создания базы данных и базовых таблиц
CREATE TABLE IF NOT EXISTS Clients (
    ClientID SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    second_name VARCHAR(50) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(50),
    adress VARCHAR(255)
);
CREATE TABLE IF NOT EXISTS Cars (
    CarID SERIAL PRIMARY KEY,
    ClientID INTEGER,
    mark VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    year INTEGER,
    VIN VARCHAR(50)
);
CREATE TABLE IF NOT EXISTS Masters (
    MasterID SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    second_name VARCHAR(50) NOT NULL,
    specialization VARCHAR(50) NOT NULL,
    experience INTEGER,
    phone VARCHAR(20)
);
CREATE TABLE IF NOT EXISTS Services (
    ServiceID SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    cost INTEGER,
    duration INTEGER
);
CREATE TABLE IF NOT EXISTS Orders (
    OrderID SERIAL PRIMARY KEY,
    CarID INTEGER NOT NULL,
    MasterID INTEGER NOT NULL,
    ServiceID INTEGER NOT NULL,
    date_order DATE NOT NULL,
    status_order VARCHAR(50) NOT NULL,
    comments TEXT,
    FOREIGN KEY (CarID) REFERENCES Cars(CarID),
    FOREIGN KEY (MasterID) REFERENCES Masters(MasterID),
    FOREIGN KEY (ServiceID) REFERENCES Services(ServiceID)
);
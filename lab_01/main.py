import psycopg2
import random
from faker import Faker

# Устанавливаем соединение с вашей базой данных
conn = psycopg2.connect(
    database="autoservice",
    user="postgres",
    password="1564",
    host="127.0.0.1",
    port="5432",
)

fake = Faker()  # Убедитесь, что эта строка присутствует в вашем скрипте

# Подключение к базе данных PostgreSQL (предполагая, что база данных уже создана)
cursor = conn.cursor()

# Создание таблиц
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS Clients (
    ClientID SERIAL PRIMARY KEY,
    Имя VARCHAR(50),
    Фамилия VARCHAR(50),
    Телефон VARCHAR(20),
    Email VARCHAR(50),
    Адрес VARCHAR(255)
)
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS Cars (
    CarID SERIAL PRIMARY KEY,
    ClientID INTEGER,
    Марка VARCHAR(50),
    Модель VARCHAR(50),
    Год_выпуска INTEGER,
    VIN VARCHAR(50),
    FOREIGN KEY (ClientID) REFERENCES Clients(ClientID)
)
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS Masters (
    MasterID SERIAL PRIMARY KEY,
    Имя VARCHAR(50),
    Фамилия VARCHAR(50),
    Специализация VARCHAR(50),
    Опыт_работы INTEGER,
    Телефон VARCHAR(20)
)
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS Services (
    ServiceID SERIAL PRIMARY KEY,
    Название VARCHAR(50),
    Описание TEXT,
    Стоимость INTEGER,
    Продолжительность INTEGER
)
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS Orders (
    OrderID SERIAL PRIMARY KEY,
    CarID INTEGER,
    MasterID INTEGER,
    ServiceID INTEGER,
    Дата_заказа DATE,
    Статус_заказа VARCHAR(50),
    Комментарии TEXT,
    FOREIGN KEY (CarID) REFERENCES Cars(CarID),
    FOREIGN KEY (MasterID) REFERENCES Masters(MasterID),
    FOREIGN KEY (ServiceID) REFERENCES Services(ServiceID)
)
"""
)


# Генерация и вставка данных
client_ids = []
for i in range(1000):
    cursor.execute('INSERT INTO Clients (Имя, Фамилия, Телефон, Email, Адрес) VALUES (%s, %s, %s, %s, %s) RETURNING ClientID', 
                   (fake.first_name()[:20], fake.last_name()[:20], fake.phone_number()[:20], fake.email()[:50], fake.address()[:255]))
    client_id = cursor.fetchone()
    if client_id:
        client_ids.append(client_id[0])

car_ids = []
for i in range(1000):
    cursor.execute('INSERT INTO Cars (ClientID, Марка, Модель, Год_выпуска, VIN) VALUES (%s, %s, %s, %s, %s) RETURNING CarID', 
                   (random.choice(client_ids), fake.company_suffix()[:50], fake.catch_phrase()[:50], fake.year(), fake.vin()[:50]))
    car_id = cursor.fetchone()
    if car_id:
        car_ids.append(car_id[0])

master_ids = []
for i in range(1000):
    cursor.execute('INSERT INTO Masters (Имя, Фамилия, Специализация, Опыт_работы, Телефон) VALUES (%s, %s, %s, %s, %s) RETURNING MasterID', 
                   (fake.first_name()[:20], fake.last_name()[:20], fake.job()[:20], random.randint(1, 20), fake.phone_number()[:20]))
    master_id = cursor.fetchone()
    if master_id:
        master_ids.append(master_id[0])

service_ids = []
for i in range(1000):
    cursor.execute('INSERT INTO Services (Название, Описание, Стоимость, Продолжительность) VALUES (%s, %s, %s, %s) RETURNING ServiceID', 
                   (fake.bs()[:50], fake.text()[:255], random.randint(100, 10000), random.randint(1, 8)))
    service_id = cursor.fetchone()
    if service_id:
        service_ids.append(service_id[0])

# Проверка, что списки не пусты
if not car_ids or not master_ids or not service_ids:
    raise ValueError("Some IDs were not generated. Check the insertion into the Cars, Masters, and Services tables.")

for i in range(1000):
    cursor.execute('INSERT INTO Orders (CarID, MasterID, ServiceID, Дата_заказа, Статус_заказа, Комментарии) VALUES (%s, %s, %s, %s, %s, %s)', 
                   (random.choice(car_ids), random.choice(master_ids), random.choice(service_ids), fake.date(), fake.random_element(elements=("в ожидании", "в работе", "завершено")), fake.text()[:255]))

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

import psycopg2
import random
from faker import Faker
from prettytable import PrettyTable
import csv


fake = Faker(locale="ru_RU")


try:
    # Устанавливаем соединение с вашей базой данных
    conn = psycopg2.connect(
        database="postgres",  # postgres
        user="postgres",
        password="1564",
        host="127.0.0.1",
        port="5432",
    )
    # Подключение к базе данных PostgreSQL (предполагая, что база данных уже создана)
    cursor = conn.cursor()
except Exception as e:
    print(f"Не удалось подключиться к базе данных: {e}")


def endConneting(conn):
    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()


END = "7"
DROPTABLE = "1"
INSERTRANDOMDATA = "2"
CREATETABLES = "3"
PRINTTABLE = "4"
DROPONETABLE = "5"
INPUTCOUNTROWS = "0"
SAVETOCSV = "6"


def printMenu():
    menu_text = """
    ========== МЕНЮ --- Автосервис ==========
    0 | Ввести кол-во записей в таблицы
    1 | Удалить все таблицы (c потерей данных)
    2 | Заполнить таблицы рандомными данными 
       (удаляет предыдущие таблицы с данными и создает новые)
    3 | Создать таблицы
    4 | Вывод таблицы
    5 | Удалить определенные таблицы (c потерей данных)
    6 | Сохранить данные в CSV
    7 | Выход

    Введите число (1, 2, 3, 4, 5, 6 или 7) для выбора опции из меню:
    """
    print(menu_text)
    rc = input("> ")
    return rc


def insertRandomData(count):
    try:
        client_ids = insertRandomClients(cursor, fake, count)
        if not client_ids:
            raise ValueError("Ошибка вставки данных в таблицу clients")
    except Exception as e:
        print(f"Ошибка при вставке данных клиентов: {e}")
        dropAll()
        return 1

    try:
        cars_ids = insertRandomCars(cursor, fake, count, client_ids)
        if not cars_ids:
            raise ValueError("Ошибка вставки данных в таблицу cars")
    except Exception as e:
        print(f"Ошибка при вставке данных автомобилей: {e}")
        dropAll()
        return 1

    try:
        master_ids = insertRandomMasters(cursor, fake, count)
        if not master_ids:
            raise ValueError("Ошибка вставки данных в таблицу master")
    except Exception as e:
        print(f"Ошибка при вставке данных master: {e}")
        dropAll()
        return 1

    try:
        services_ids = insertRandomServices(cursor, fake, count)
        if not services_ids:
            raise ValueError("Ошибка вставки данных в таблицу services_id")
    except Exception as e:
        print(f"Ошибка при вставке данных services_id: {e}")
        dropAll()
        return

    try:
        orders_ids = insertRandomOrder(
            cursor, fake, count, [cars_ids, client_ids, services_ids]
        )
        if not orders_ids:
            raise ValueError("Ошибка вставки данных в таблицу orders_ids")
    except Exception as e:
        print(f"Ошибка при вставке данных orders_ids: {e}")
        dropAll()
        return
    return


def get_positive_integer():
    while True:
        try:
            user_input = input("Введите положительное целое число: ")
            number = int(user_input)
            if number > 0:
                return number
            else:
                print("Ошибка: число должно быть больше 0. Попробуйте еще раз.")
        except ValueError:
            print(
                "Ошибка: введенное значение не является корректным числом. Попробуйте еще раз."
            )


def  saveToCSV(cursor):
    for i in ["clients", "cars", "masters", "orders", "services"]:
        
        # Выберите данные, которые вы хотите экспортировать в CSV
        cursor.execute(f"SELECT * FROM {i}")
        
        # Получите результаты запроса
        rows = cursor.fetchall()

        # Получите заголовки столбцов из описания курсора
        column_names = [desc[0] for desc in cursor.description]

        # Пишем данные в файл CSV
        with open(f'{i}.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Пишем заголовки столбцов
            writer.writerow(column_names)
            
            # Пишем данные
            writer.writerows(rows)

        print("Data exported successfully!")
    

def main():
    rc = INPUTCOUNTROWS
    COUNT_CLIENTS = 1000
    while rc != END:
        rc = printMenu()

        if rc == INPUTCOUNTROWS:
            COUNT_CLIENTS = get_positive_integer()

        elif rc == DROPTABLE:
            try:
                dropAll()
            except Exception as e:
                print(f"Ошибка при удаление таблиц: {e}")

        elif rc == INSERTRANDOMDATA:
            try:
                dropAll()
                createTables(cursor)
            except Exception as e:
                print(f"Ошибка при инициализации базы данных: {e}")

            insertRandomData(COUNT_CLIENTS)
            print("Все таблицы успешно заполнены")
        elif rc == CREATETABLES:
            try:
                createTables(cursor)
            except Exception as e:
                print(f"Ошибка при инициализации базы данных: {e}")
        elif rc == PRINTTABLE:
            try:
                printTable(cursor)
            except Exception as e:
                print(f"Ошибка при выводе: {e}")
        elif rc == DROPONETABLE:
            try:
                delOneTable(cursor)
            except Exception as e:
                print(f"Ошибка при удаление таблиц: {e}")
        elif rc == SAVETOCSV:
            try:
                saveToCSV(cursor)
            except Exception as e:
                print(f"Ошибка копирования: {e}")
                
        elif rc == END:
            try:
                endConneting(conn)
                return 0

            except Exception as e:
                print(f"Ошибка: {e}")
            
        else:
            print(f"Ошибка выбора меню")

    return 0


def delOneTable(cursor):
    menu_text = """
        Выберите таблицу, которую хотите удалить :
    1 | Таблица машин
    2 | Таблица клиентов
    3 | Таблица мастеров
    4 | Таблица сервиса 
    5 | Таблица заказов

    Введите число (1, 2, 3, 4 или 5) для выбора опции из меню:
    """
    print(menu_text)
    rc = input("> ")

    match rc:
        case "1":
            dropTable(cursor, "cars")
        case "2":
            dropTable(cursor, "clients")
        case "3":
            dropTable(cursor, "masters")
        case "4":
            dropTable(cursor, "services")
        case "5":
            dropTable(cursor, "orders")
        case _:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")


def printTable(cursor):
    menu_text = """
        Выберите таблицу, которую хотите вывести:
    1 | Таблица машин
    2 | Таблица клиентов
    3 | Таблица мастеров
    4 | Таблица сервиса 
    5 | Таблица заказов

    Введите число (1, 2, 3, 4 или 5) для выбора опции из меню:
    """
    print(menu_text)
    rc = input("> ")

    match rc:
        case "1":
            printT(cursor, "cars")
        case "2":
            printT(cursor, "clients")
        case "3":
            printT(cursor, "masters")
        case "4":
            printT(cursor, "services")
        case "5":
            printT(cursor, "orders")
        case _:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")


def printT(cursor, name_table):
    cursor.execute(f"SELECT * FROM {name_table}")
    rows = cursor.fetchall()

    x = PrettyTable()

    # Получаем названия колонок
    column_names = [desc[0] for desc in cursor.description]
    x.field_names = column_names

    for row in rows:
        truncated_row = [str(cell)[:25] if isinstance(cell, str) else cell for cell in row]
        x.add_row(truncated_row)

    print(x)


def dropTable(cursor, table_name):
    try:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE")
        print(f"Таблица '{table_name}' успешно удалена.")
    except Exception as e:
        print(f"Произошла ошибка при удалении таблицы '{table_name}':", e)


def dropAll():
    dropTable(cursor, "clients")
    dropTable(cursor, "cars")
    dropTable(cursor, "masters")
    dropTable(cursor, "services")
    dropTable(cursor, "orders")


def insertRandomClients(cursor, fake, num_clients):
    client_ids = []
    for i in range(num_clients):
        first_name = fake.first_name()[:20]
        last_name = fake.last_name()[:20]
        phone = fake.phone_number()[:20]
        email = fake.email()[:50]
        address = fake.address()[:255]

        query = (
            f"INSERT INTO Clients (Имя, Фамилия, Телефон, Email, Адрес) "
            f"VALUES (%s, %s, %s, %s, %s) RETURNING ClientID"
        )

        try:
            cursor.execute(query, (first_name, last_name, phone, email, address))
            client_id = cursor.fetchone()
            if client_id:
                client_ids.append(client_id[0])
        except Exception as e:
            print(f"Ошибка при вставке данных clients: {e}")
            # Здесь можно добавить обработку ошибок, если это необходимо.
            break

    return client_ids


def insertRandomCars(cursor, fake, num_cars, client_ids):
    car_ids = []

    brands = [
        "Toyota",
        "Honda",
        "Ford",
        "Chevrolet",
        "BMW",
        "Mercedes-Benz",
        "Audi",
        "Volkswagen",
        "Nissan",
        "Hyundai",
        "Kia",
        "Subaru",
        "Mazda",
        "Lexus",
        "Tesla",
        "Jaguar",
        "Land Rover",
        "Volvo",
        "Porsche",
        "Ferrari",
        "Maserati",
        "Lamborghini",
        "Aston Martin",
        "Bentley",
        "Rolls-Royce",
        "Peugeot",
        "Citroën",
        "Renault",
        "Fiat",
        "Alfa Romeo",
        "Opel",
        "Skoda",
        "SEAT",
        "Mitsubishi",
        "Suzuki",
        "Isuzu",
        "Daihatsu",
        "Acura",
        "Infiniti",
        "Lincoln",
        "Cadillac",
        "Chrysler",
        "Dodge",
        "Jeep",
        "Ram",
        "GMC",
        "Buick",
        "Genesis",
        "Saab",
        "Mini",
        "McLaren",
        "Bugatti",
        "Pagani",
        "Koenigsegg",
        "Lotus",
        "MG",
        "Tata",
        "Mahindra",
        "Geely",
        "Changan",
        "BYD",
        "Great Wall",
        "Lancia",
        "Dacia",
        "Smart",
        "SsangYong",
        "Scion",
        "Saturn",
        "Hummer",
        "Pontiac",
        "Daewoo",
        "Oldsmobile",
        "Plymouth",
        "Holden",
        "HSV",
    ]

    models = [
        "Civic",
        "Corolla",
        "Mustang",
        "Camaro",
        "3 Series",
        "C-Class",
        "A4",
        "Golf",
        "Altima",
        "Elantra",
        "Forte",
        "Impreza",
        "Mazda3",
        "ES",
        "Model 3",
        "F-PACE",
        "Range Rover",
        "XC60",
        "911",
        "488 GTB",
        "Levante",
        "Huracán",
        "DB11",
        "Continental GT",
        "Phantom",
        "208",
        "C4",
        "Clio",
        "500",
        "Giulia",
        "Astra",
        "Octavia",
        "Ibiza",
        "Lancer",
        "Swift",
        "D-Max",
        "Copen",
        "TLX",
        "Q50",
        "Navigator",
        "Escalade",
        "300",
        "Challenger",
        "Wrangler",
        "1500",
        "Sierra",
        "Enclave",
        "G70",
        "9-3",
        "Cooper",
        "720S",
        "Chiron",
        "Huayra",
        "Regera",
        "Evija",
        "ZS",
        "Nexon",
        "XUV500",
        "Emgrand 7",
        "CS35",
        "Qin",
        "H6",
        "Ypsilon",
        "Duster",
        "ForTwo",
        "Rexton",
        "tC",
        "Vue",
        "H2",
        "Firebird",
        "Lanos",
        "Cutlass",
        "Barracuda",
        "Commodore",
        "Maloo",
    ]

    for i in range(num_cars):
        mark = random.choice(brands)
        model = random.choice(models)
        id_own = random.choice(client_ids)
        year = fake.year()
        vin = fake.vin()[:50]
        query = f"INSERT INTO Cars (ClientID, Марка, Модель, Год_выпуска, VIN) VALUES (%s, %s, %s, %s, %s) RETURNING CarID"

        try:
            cursor.execute(query, (id_own, mark, model, year, vin))
            car_id = cursor.fetchone()
            if car_id:
                car_ids.append(car_id[0])
        except Exception as e:
            print(f"Ошибка при вставке данных cars: {e}")
            # Здесь можно добавить обработку ошибок, если это необходимо.
            break

    return car_ids


def insertRandomMasters(cursor, fake, num_master):
    master_ids = []
    for i in range(num_master):
        name = fake.first_name()[:20]
        last_name = fake.last_name()[:20]
        job = fake.job()[:20]
        year_job = random.randint(1, 20)
        phone = fake.phone_number()[:20]

        query = f"INSERT INTO Masters (Имя, Фамилия, Специализация, Опыт_работы, Телефон) VALUES (%s, %s, %s, %s, %s) RETURNING MasterID"

        try:
            cursor.execute(query, (name, last_name, job, year_job, phone))
            master_id = cursor.fetchone()
            if master_id:
                master_ids.append(master_id[0])
        except Exception as e:
            print(f"Ошибка при вставке данных master: {e}")
            # Здесь можно добавить обработку ошибок, если это необходимо.
            break
    return master_ids


def insertRandomServices(cursor, fake, num_service):
    service_ids = []

    for i in range(num_service):
        name = fake.bs()[:50]
        text_job = fake.text()[:255]
        price = random.randint(100, 10000)
        year_job = random.randint(1, 20)
        time = random.randint(1, 8)

        query = f"INSERT INTO Services (Название, Описание, Стоимость, Продолжительность) VALUES (%s, %s, %s, %s) RETURNING ServiceID"

        try:
            cursor.execute(query, (name, text_job, price, time))
            service_id = cursor.fetchone()
            if service_id:
                service_ids.append(service_id[0])
        except Exception as e:
            print(f"Ошибка при вставке данных services: {e}")
            # Здесь можно добавить обработку ошибок, если это необходимо.
            break
    return service_ids


def insertRandomOrder(cursor, fake, num_order, arr_info_ids):
    orders_ids = []
    status = ["Ожидает", "В процессе", "Завершено", "Отменено"]

    car_ids = arr_info_ids[0]
    master_ids = arr_info_ids[1]
    service_ids = arr_info_ids[2]

    if not car_ids or not master_ids or not service_ids:
        raise ValueError(
            "Some IDs were not generated. Check the insertion into the Cars, Masters, and Services tables."
        )

    for i in range(num_order):
        year = fake.date()
        status_now = random.choice(status)
        text_my = fake.text()[:255]
        query = f"INSERT INTO Orders (CarID, MasterID, ServiceID, Дата_заказа, Статус_заказа, Комментарии) VALUES (%s, %s, %s, %s, %s, %s) RETURNING OrderID"

        try:
            cursor.execute(
                query,
                (
                    random.choice(car_ids),
                    random.choice(master_ids),
                    random.choice(service_ids),
                    year,
                    status_now,
                    text_my,
                ),
            )
            orders_id = cursor.fetchone()
            if orders_id:
                orders_ids.append(orders_id[0])
        except Exception as e:
            print(f"Ошибка при вставке данных order: {e}")
            # Здесь можно добавить обработку ошибок, если это необходимо.
            break
    return orders_ids


def createTables(cursor):
    # Создание таблиц
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Clients (
        ClientID SERIAL PRIMARY KEY,
        Имя VARCHAR(50) NOT NULL,
        Фамилия VARCHAR(50) NOT NULL,
        Телефон VARCHAR(20) NOT NULL, --проверка регуляркой 
        Email VARCHAR(50),  -- UNIQUE Добавляем ограничение на уникальность Email
        Адрес VARCHAR(255) CHECK (LENGTH(Адрес) <= 255) -- Ограничение длины поля Адрес

    )
    """
    )
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Cars (
        CarID SERIAL PRIMARY KEY,
        ClientID INTEGER,
        Марка VARCHAR(50) NOT NULL,
        Модель VARCHAR(50) NOT NULL,
        Год_выпуска INTEGER CHECK (Год_выпуска >= 1900 AND Год_выпуска <= EXTRACT(YEAR FROM NOW())),
        VIN VARCHAR(50) UNIQUE,
        FOREIGN KEY (ClientID) REFERENCES Clients(ClientID)
    )
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Masters (
        MasterID SERIAL PRIMARY KEY,
        Имя VARCHAR(50) NOT NULL,
        Фамилия VARCHAR(50) NOT NULL,
        Специализация VARCHAR(50) NOT NULL,
        Опыт_работы INTEGER CHECK (Опыт_работы >= 0),
        Телефон VARCHAR(20) --регулярочку бы 
    )
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Services (
        ServiceID SERIAL PRIMARY KEY,
        Название VARCHAR(50) NOT NULL,
        Описание TEXT NOT NULL ,
        Стоимость INTEGER CHECK (Стоимость >1),
        Продолжительность INTEGER CHECK (Продолжительность > 0)
    )
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Orders (
        OrderID SERIAL PRIMARY KEY,
        CarID  INTEGER NOT NULL,
        MasterID INTEGER NOT NULL,
        ServiceID INTEGER NOT NULL,
        Дата_заказа DATE NOT NULL,
        Статус_заказа VARCHAR(50) NOT NULL CHECK (Статус_заказа IN ('Ожидает', 'В процессе', 'Завершено', 'Отменено')),
        Комментарии TEXT ,
        FOREIGN KEY (CarID) REFERENCES Cars(CarID),
        FOREIGN KEY (MasterID) REFERENCES Masters(MasterID),
        FOREIGN KEY (ServiceID) REFERENCES Services(ServiceID)
    )
    """
    )
    return cursor


if __name__ == "__main__":
    main()

-- Сценарий определения ограничений

ALTER TABLE Clients ADD CONSTRAINT CHK_Address_Length CHECK (LENGTH(Адрес) <= 255);
ALTER TABLE Cars ADD CONSTRAINT CHK_Car_Year CHECK (Год_выпуска >= 1900 AND Год_выпуска <= EXTRACT(YEAR FROM NOW()));
ALTER TABLE Cars ADD CONSTRAINT CHK_VIN UNIQUE(VIN);
ALTER TABLE Masters ADD CONSTRAINT CHK_Experience CHECK (Опыт_работы >= 0);
ALTER TABLE Services ADD CONSTRAINT CHK_Cost CHECK (Стоимость > 1);
ALTER TABLE Services ADD CONSTRAINT CHK_Duration CHECK (Продолжительность > 0);
ALTER TABLE Orders ADD CONSTRAINT CHK_Order_Status CHECK (Статус_заказа IN ('Ожидает', 'В процессе', 'Завершено', 'Отменено'));

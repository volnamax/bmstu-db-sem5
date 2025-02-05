-- Сценарий определения ограничений

ALTER TABLE Clients ADD CONSTRAINT CHK_Address_Length CHECK (LENGTH(adress) <= 255);
ALTER TABLE Cars ADD CONSTRAINT CHK_Car_Year CHECK (year >= 1900 AND year <= EXTRACT(YEAR FROM NOW()));
ALTER TABLE Cars ADD CONSTRAINT CHK_VIN UNIQUE(VIN);
ALTER TABLE Masters ADD CONSTRAINT CHK_Experience CHECK (experience >= 0);
ALTER TABLE Services ADD CONSTRAINT CHK_Cost CHECK (cost > 1);
ALTER TABLE Services ADD CONSTRAINT CHK_Duration CHECK (duration > 0);
ALTER TABLE Orders ADD CONSTRAINT CHK_Order_Status CHECK (status_order IN ('wait', 'process', 'done', 'canceled'));


ALTER TABLE Clients ADD CONSTRAINT CHK_Name_NULL CHECK (name IS NOT NULL);
ALTER TABLE Clients ADD CONSTRAINT CHK_SecondName_NULL CHECK ( second_name IS  NOT NULL);
ALTER TABLE Clients ADD CONSTRAINT CHK_Tel_NULL CHECK ( phone IS  NOT NULL);


ALTER TABLE Cars ADD CONSTRAINT CHK_Mark_NULL CHECK ( mark IS NOT NULL);
ALTER TABLE Cars ADD CONSTRAINT CHK_Mod_NULL CHECK ( model IS NOT NULL);



ALTER TABLE Masters ADD CONSTRAINT CHK_NameMaster_NULL CHECK (name IS NOT NULL);
ALTER TABLE Masters ADD CONSTRAINT CHK_SecondNameMAster_NULL CHECK ( second_name IS NOT NULL);
ALTER TABLE Masters ADD CONSTRAINT CHK_Spec_NULL CHECK ( specialization IS NOT NULL);


ALTER TABLE Services ADD CONSTRAINT CHK_NameService_NULL CHECK ( name IS NOT NULL);
ALTER TABLE Services ADD CONSTRAINT CHK_Opisanie_NULL CHECK ( description IS NOT NULL);


ALTER TABLE Orders ADD CONSTRAINT CHK_CarID_NULL CHECK ( CarID IS NOT NULL);
ALTER TABLE Orders ADD CONSTRAINT CHK_MasterId_NULL CHECK ( MasterID IS NOT NULL);
ALTER TABLE Orders ADD CONSTRAINT CHK_ServiceID_NULL CHECK ( ServiceID IS NOT NULL);
ALTER TABLE Orders ADD CONSTRAINT CHK_DatOrder_NULL CHECK ( date_order IS NOT NULL);
ALTER TABLE Orders ADD CONSTRAINT CHK_Status_NULL CHECK ( status_order IS NOT NULL)

#!/bin/bash

# Замените 'max' на ваше имя пользователя, 'autoservice' на вашу базу данных,
# и укажите полные пути к соответствующим SQL-файлам.

username="max"
database="autoservice"
sql_directory="/home/max/c/bmstu_bd/bmstu_5bd/lab_01/sql"

# Выполнить SQL-скрипты с помощью psql

psql -U "$username" -d "$database" -f "$sql_directory/drop.sql"
psql -U "$username" -d "$database" -f "$sql_directory/create_table.sql"
psql -U "$username" -d "$database" -f "$sql_directory/constraints.sql"
psql -U "$username" -d "$database" -f "$sql_directory/copy.sql"

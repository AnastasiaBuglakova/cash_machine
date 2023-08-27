import pymysql
from config import host, password, user, db_name

#
# try:
#     connection = pymysql.connect(
#         host=host,  # localhost
#         port=3306,
#         user=user,  # "root"
#         password=password,  # "1234"
#         database=db_name,  # lesson_2
#         cursorclass=pymysql.cursors.DictCursor
#     )
#     print("Connected successfully")
#     try:
#         cursor = connection.cursor()
#
#         # create table
#         # drop_query = "DROP TABLE IF EXISTS users;"
#         # cursor.execute(drop_query)
#         # print("Table users dropped successfully")
#
#         create1_query = "CREATE TABLE IF NOT EXISTS users" \
#                         "(id INT PRIMARY KEY AUTO_INCREMENT, firstname VARCHAR(45), lastname VARCHAR(45)" \
#                         ");"
#         cursor.execute(create1_query)
#         print("Table USERS created successfully")
#         # "FOREIGN KEY (card_id) REFERENCES cards(id)
#
#         # drop_query2 = "DROP TABLE IF EXISTS cards;"
#         # cursor.execute(drop_query2)
#         # print("Table cards dropped successfully")
#
#         create3_query = "CREATE TABLE IF NOT EXISTS cards" \
#                         "(card_num BIGINT UNSIGNED PRIMARY KEY, user_id INT PRIMARY KEY AUTO_INCREMENT, sum_on_card FLOAT, FOREIGN KEY (user_id) REFERENCES users(id)" \
#                         ");"
#         cursor.execute(create3_query)
#         print("Table cards created successfully")
#
#         drop_query3 = "DROP TABLE IF EXISTS operations;"
#         cursor.execute(drop_query3)
#         print("Table operations dropped successfully")
#
#         create2_query = "CREATE TABLE IF NOT EXISTS operations" \
#                         "(id INT PRIMARY KEY AUTO_INCREMENT, card_num BIGINT UNSIGNED, date DATE, type_op VARCHAR(10), summ FLOAT, duty FLOAT," \
#                         "FOREIGN KEY (card_num) REFERENCES cards(card_num)" \
#                         ");"
#         cursor.execute(create2_query)
#         print("Table operations created successfully")
#
#         # insert data
#         insert_query = "INSERT users(firstname) VALUES ('Алина'), " \
#                        "('Test');"
#         cursor.execute(insert_query)
#         connection.commit()
#         print("Insert successfully")
#
#         # update
#         cursor.execute("UPDATE users SET firstname = 'Mikle'"
#                        "WHERE id = 4")
#         # добавляю столбец "pin INT" в таблицу с картами
#         add_column_query = "ALTER TABLE cards ADD COLUMN pin INT NOT NULL"
#         cursor.execute(add_column_query)
#         connection.commit()
#         print("Insert pin successfully")
#
#         # delete
#         cursor.execute("DELETE FROM users WHERE id = 2")
#         connection.commit()
#
#         #  select-ы
#         cursor.execute("SELECT * FROM cards;")
#         rows = cursor.fetchall()
#         for row in rows:
#             print(row)
#
#     finally:
#         connection.close()
#
# except Exception as ex:
#     print("Disconnected")
#     print(ex)


def find_card_and_pin(c, p):
    res = []
    try:
        connection = pymysql.connect(
            host=host,  # localhost
            port=3306,
            user=user,  # "root"
            password=password,  # "1234"
            database=db_name,  # lesson_2
            cursorclass=pymysql.cursors.DictCursor
        )
        print("Connected successfully")
        try:
            cursor = connection.cursor()
            #  select-ы
            cursor.execute("SELECT card_num, pin FROM cards;")
            rows = cursor.fetchall()
            for row in rows:
                if c in row.values() and p in row.values():
                    res.append(True)
                    current_card = row['card_num']

        finally:
            connection.close()

    except Exception as ex:
        print("Disconnected")
        print(ex)

    return any(res), current_card


def request_to_take(current_card_, full_amount_to_take_):
    row_from_db = None
    try:
        connection = pymysql.connect(
            host=host,  # localhost
            port=3306,
            user=user,  # "root"
            password=password,  # "1234"
            database=db_name,  # lesson_2
            cursorclass=pymysql.cursors.DictCursor
        )
        print("Connected successfully")
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT card_num, sum_on_card FROM cards;")
            rows = cursor.fetchall()
            for row in rows:
                if current_card_ in row.values():
                    print('row = ', row, current_card_, full_amount_to_take_)
                    row_from_db = row
                    break

        finally:
            connection.close()

    except Exception as ex:
        print("Disconnected")
        print(ex)
    return row_from_db


def take_money_from_card(current_card_, full_amount_of_money_):
import pymysql
from config import host, password, user, db_name


def find_card_and_pin(c, p):
    current_card = []
    num_operations = 0
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
            cursor.execute("SELECT card_num, pin, sum_on_card FROM cards;")
            rows = cursor.fetchall()
            for row in rows:
                if c in row.values() and p in row.values():
                    current_card.append(c)
                    current_card.append(row['sum_on_card'])

                    cursor.execute("SELECT * FROM operations;")
                    rows = cursor.fetchall()
                    for r in rows:
                        if c in r.values():
                            num_operations += 1
                    current_card.append(num_operations)
                    break
            else:
                current_card = None

        finally:
            connection.close()

    except Exception as ex:
        print("Disconnected")
        print(ex)
    if current_card and current_card[1] is None:
        current_card[1] = 0
    return current_card


def take_money_from_card(current_card_, full_amount_of_money_, tax_to_take_):
    """Function takes number of card and amount of money and requests to MySQL
    to update data in cards and operations tables.
    Returns sum on card"""
    row_from_db = 'здесь д.б. быть строка данных по карте из таблицы карт БД'
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
            cursor.execute(
                f'UPDATE cards SET sum_on_card = sum_on_card - {full_amount_of_money_} '
                f'WHERE card_num = {current_card_};')
            connection.commit()

            cursor.execute(
                f'INSERT operations (card_num, type_op, summ, duty, date) VALUES ({current_card_}, "take_money", '
                f'{full_amount_of_money_}, {tax_to_take_}, DATE(NOW()));')
            connection.commit()

            cursor.execute(f"SELECT card_num, sum_on_card FROM cards WHERE card_num = {current_card_};")
            row_from_db = cursor.fetchall()
            print(row_from_db[0]['sum_on_card'])
        finally:
            connection.close()
    except Exception as ex:
        print("Disconnected")
        print(ex)
    return row_from_db[0]['sum_on_card']


def push_money_to_card(current_card_, amount_to_push_, tax_):
    print(f"{current_card_=}, {amount_to_push_=}")
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
            cursor.execute(f"SELECT sum_on_card FROM cards WHERE card_num = {current_card_};")
            sum_on_card_from_db = cursor.fetchall()[0]['sum_on_card']
            print("sum_on_card_from_db", sum_on_card_from_db)
            if sum_on_card_from_db is not None:
                cursor.execute(
                    f'UPDATE cards SET sum_on_card = sum_on_card + {amount_to_push_}-{tax_} WHERE card_num = {current_card_};')
            else:
                cursor.execute(
                    f'UPDATE cards SET sum_on_card = {amount_to_push_}-{tax_} WHERE card_num = {current_card_};')
            connection.commit()
            cursor.execute(
                f'INSERT operations(card_num, type_op, summ, duty, date) VALUES ({current_card_}, "push_money", {amount_to_push_}, {tax_}, DATE(NOW()));')
            connection.commit()
            cursor.execute(f"SELECT card_num, sum_on_card FROM cards WHERE card_num = {current_card_};")
            row_from_db = cursor.fetchall()
            connection.commit()
            print(row_from_db)
        finally:
            connection.close()
    except Exception as ex:
        print("Disconnected")
        print(ex)
    return row_from_db[0]['sum_on_card']


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

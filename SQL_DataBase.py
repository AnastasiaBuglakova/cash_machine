import pymysql
from config import host, password, user, db_name
import logging

FORMAT = '{levelname:8} | {asctime:15} | {name:10}| {funcName:20} | {msg}'
logging.basicConfig(format=FORMAT, filename='logfile.log', filemode='a', encoding='utf-8', level=logging.DEBUG,
                    style="{")
logger = logging.getLogger(__name__)

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
        logger.info(msg='Успешное соединение с БД для идентификации данных карты')
        try:
            cursor = connection.cursor()
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
        logger.warning(msg='Нет соединения с БД для идентификации данных карты' + ex.__str__())
    if current_card == []:
        return None
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
        logger.info(msg='Успешное соединение с БД для снятия суммы')
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

        finally:
            connection.close()
    except Exception as ex:
        logger.warning(msg='Нет соединения с БД для снятия суммы со счета' + ex.__str__())

    return row_from_db[0]['sum_on_card']


def push_money_to_card(current_card_, amount_to_push_, tax_):
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
        logger.info(msg='Успешное соединение с БД для зачисления суммы')
        try:
            cursor = connection.cursor()
            cursor.execute(f"SELECT sum_on_card FROM cards WHERE card_num = {current_card_};")
            sum_on_card_from_db = cursor.fetchall()[0]['sum_on_card']
            logger.info(msg=f'На карте клиента {sum_on_card_from_db}')
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
            logger.info(msg=f'Данные по карте {row_from_db}')
        finally:
            connection.close()
    except Exception as ex:
        logger.warning(msg='Нет соединения с БД для зачисления суммы на счет' + ex.__str__())
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
#     try:
#         cursor = connection.cursor()
#
#         # create table
#         # drop_query = "DROP TABLE IF EXISTS users;"
#         # cursor.execute(drop_query)

#         create1_query = "CREATE TABLE IF NOT EXISTS users" \
#                         "(id INT PRIMARY KEY AUTO_INCREMENT, firstname VARCHAR(45), lastname VARCHAR(45)" \
#                         ");"
#         cursor.execute(create1_query)

#         # "FOREIGN KEY (card_id) REFERENCES cards(id)
#
#         # drop_query2 = "DROP TABLE IF EXISTS cards;"
#         # cursor.execute(drop_query2)
#
#         create3_query = "CREATE TABLE IF NOT EXISTS cards" \
#                         "(card_num BIGINT UNSIGNED PRIMARY KEY, user_id INT PRIMARY KEY AUTO_INCREMENT, sum_on_card FLOAT, FOREIGN KEY (user_id) REFERENCES users(id)" \
#                         ");"
#         cursor.execute(create3_query)
#
#         drop_query3 = "DROP TABLE IF EXISTS operations;"
#         cursor.execute(drop_query3)
#
#         create2_query = "CREATE TABLE IF NOT EXISTS operations" \
#                         "(id INT PRIMARY KEY AUTO_INCREMENT, card_num BIGINT UNSIGNED, date DATE, type_op VARCHAR(10), summ FLOAT, duty FLOAT," \
#                         "FOREIGN KEY (card_num) REFERENCES cards(card_num)" \
#                         ");"
#         cursor.execute(create2_query)
#
#         # insert data
#         insert_query = "INSERT users(firstname) VALUES ('Алина'), " \
#                        "('Test');"
#         cursor.execute(insert_query)
#         connection.commit()
#
#         # update
#         cursor.execute("UPDATE users SET firstname = 'Mikle'"
#                        "WHERE id = 4")
#         # добавляю столбец "pin INT" в таблицу с картами
#         add_column_query = "ALTER TABLE cards ADD COLUMN pin INT NOT NULL"
#         cursor.execute(add_column_query)
#         connection.commit()
#
#         # delete
#         cursor.execute("DELETE FROM users WHERE id = 2")
#         connection.commit()
#
#         #  select-ы
#         cursor.execute("SELECT * FROM cards;")
#         rows = cursor.fetchall()
#
#     finally:
#         connection.close()
#
# except Exception as ex:
#     print(ex)

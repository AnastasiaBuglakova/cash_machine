import pymysql
from config import host, password, user, db_name
from business_logic import logger


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
                if row['card_num'] == c and row['pin'] == p:
                    current_card.append(c)
                    current_card.append(row['sum_on_card'])
                    cursor.execute("SELECT * FROM operations;")
                    rows_op = cursor.fetchall()
                    for r in rows_op:
                        if r['card_num'] == c:
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
                f'UPDATE cards SET sum_on_card = sum_on_card - {full_amount_of_money_} WHERE card_num = {current_card_};')
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
            if sum_on_card_from_db:
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
        finally:
            connection.close()
    except Exception as ex:
        logger.warning(msg='Нет соединения с БД для зачисления суммы на счет' + ex.__str__())
        print(ex)
    return row_from_db[0]['sum_on_card']



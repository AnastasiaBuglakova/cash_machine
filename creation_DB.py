import pymysql
from config import host, password, user, db_name


try:
    connection = pymysql.connect(
        host=host,  # localhost
        port=3306,
        user=user,  # "root"
        password=password,  # "1234"
        database=db_name,  # lesson_2
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        cursor = connection.cursor()
        create3_query = "CREATE TABLE IF NOT EXISTS cards" \
                        "(card_num BIGINT UNSIGNED PRIMARY KEY, user_id INT PRIMARY KEY AUTO_INCREMENT, sum_on_card FLOAT" \
                        ");"
        cursor.execute(create3_query)

        drop_query3 = "DROP TABLE IF EXISTS operations;"
        cursor.execute(drop_query3)

        create2_query = "CREATE TABLE IF NOT EXISTS operations" \
                        "(id INT PRIMARY KEY AUTO_INCREMENT, card_num BIGINT UNSIGNED, date DATE, type_op VARCHAR(10), summ FLOAT, duty FLOAT," \
                        "FOREIGN KEY (card_num) REFERENCES cards(card_num) ON DELETE SET NULL" \
                        ");"
        cursor.execute(create2_query)

        # добавляю столбец "pin INT" в таблицу с картами
        add_column_query = "ALTER TABLE cards ADD COLUMN pin INT NOT NULL"
        cursor.execute(add_column_query)
        connection.commit()
        rows = cursor.fetchall()

    finally:
        connection.close()

except Exception as ex:
    print(ex)

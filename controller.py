import tkinter as tk
import SQL_DataBase
import constants as c
import logging

cash_mashine_state = {'operation': 'ready'}
"""Operation: 'ready', 'seeking card', 'take money', 'push money' """

amount_to_take = None
full_amount_to_take = None
amount_to_push = None
current_string = ''
current_card = None
current_card_sum_op = None

FORMAT = '{levelname:8} | {asctime:15} | {name:10}| {funcName:20} | {msg}'
logging.basicConfig(format=FORMAT, filename='logfile.log', filemode='a', encoding='utf-8', level=logging.DEBUG,
                    style="{")
logger = logging.getLogger(__name__)

logger.warning(msg='Запуск работы банкомата')


def add_digit(digit):
    """ Adding digit in the end of entered string of entry"""
    value = ent.get()
    if "Введите номер карты" in value:
        value = value.replace("Введите номер карты", '')

    elif 'Введите пин-код' in value:
        value = value.replace("Введите пин-код", '')

    elif 'Выберите операцию: Снять, пополнить, выйти' in value:
        value = value.replace("Выберите операцию: Снять, пополнить, выйти", '')

    elif 'Введите сумму снятия:' in value:
        value = value.replace("Введите сумму снятия:", '')

    elif f"Сумма пополнения и снятия должна быть кратна {c.BASE}" in value:
        value = value.replace(f"Сумма пополнения и снятия должна быть кратна {c.BASE}", '')

    elif "Введите сумму, которую хотите внести на счет:" in value:
        value = value.replace("Введите сумму, которую хотите внести на счет:", '')

    elif "Сумма пополнения и снятия должна быть кратна " in value:
        value = value.replace("Сумма пополнения и снятия должна быть кратна ")
    ent.delete(0, tk.END)
    ent.insert(0, value + digit)


def operation_with_money(full_amount_to_take_):
    """Функция проверяет достаточность средств на счете и отправляет запрос в БД на снятие и пополнение счета """
    """с учетом комиссии банка"""
    global amount_to_take, amount_to_push

    if current_card_sum_op[1] >= full_amount_to_take_ and cash_mashine_state['operation'] == 'take money':
        ent.delete(0, tk.END)
        ent.insert(0, f"Приступаем к операции. Полная сумма к снятию {full_amount_to_take - calculate_tax_size()}")
        logger.info(msg=f'Сумма выдаваемая клиенту:{amount_to_take}, Сумма, снимаемая со счета:{full_amount_to_take_}')
        current_card_sum_op[1] = SQL_DataBase.take_money_from_card(current_card_sum_op[0], full_amount_to_take_,
                                                                   calculate_tax_size())
        return True

    elif current_card_sum_op[1] >= full_amount_to_take_ and cash_mashine_state['operation'] == 'push money':
        ent.delete(0, tk.END)
        ent.insert(0, f"Приступаем к операции. Сумма к зачислению {full_amount_to_take}")
        logger.info(msg=f'Сумма зачисляемая на счет:{amount_to_take}, Сумма, получаемая от клиента:{full_amount_to_take_}')
        current_card_sum_op[1] = SQL_DataBase.push_money_to_card(current_card_sum_op[0], amount_to_push,
                                                                 calculate_tax_size())
        return True
    else:
        return False


def calculate_tax_size():
    """Функция вычисляет размер комиссии по данным о карте из списка current_card_sum_op, """
    """включая налог на богатсво и плату за 3ю операцию"""
    tax = 0
    logging.debug(
        msg=f'Текущие данные по карте {current_card_sum_op = }')
    if (current_card_sum_op[2] + 1) % 3 == 0:
        tax += c.PERCENT_FOR_3RD_OPERATION * current_card_sum_op[1]
        logging.info(
            msg=f'К сумме снятия/пополнения добавлена комиссия за 3-ю операцию {tax}')
    if current_card_sum_op[1] >= c.WEALTH_LIMIT:
        tax += c.WEALTH_PERCENT * current_card_sum_op[1]
        logging.info(
            msg=f'К сумме снятия/пополнения добавлен налог на богатсво {c.WEALTH_PERCENT * current_card_sum_op[1]}')
    return tax


def get_entry():
    """Функция обрабатывает нажание на кнопку Enter при вводе номера карты, пин кода карты и вводе суммы к снятию или зачисления"""
    global current_string, amount_to_take, full_amount_to_take, amount_to_push, \
        current_card, current_card_sum_op
    if current_string.isalpha():
        del_entry()
    while "+" not in current_string and cash_mashine_state['operation'] == 'ready':
        if not current_string:
            current_string += ent.get().strip()
            current_card = current_string
            logger.debug(msg=f"Введен номер карты: {current_card}")
            del_entry()
            ent.insert(0, "Введите пин-код")
            break
        else:
            pin_num = ent.get()
            if "Введите пин-код" not in pin_num:
                current_string += '+' + pin_num
                logger.debug(msg=f"Введен пин-код: {pin_num}")
                cash_mashine_state['operation'] = 'seeking card'
                logger.debug(msg="Текущий режим: seeking card")
                del_entry()
    if cash_mashine_state['operation'] == 'seeking card':
        card, pin = tuple(map(int, current_string.split("+")))
        current_card_sum_op = SQL_DataBase.find_card_and_pin(card, pin)
        if not current_card_sum_op is None:
            logger.info(msg=f"Успешный вход с номером карты: {current_card}")
            ent.insert(0, "Выберите операцию: Снять, пополнить, выйти")
        else:
            logger.warning(msg=f"Неудачная попытка входа с данными номера карты + пин-кодом: {current_string}")
            ent.insert(0, 'Неверно введены номер карты и/или пин-код')
            cash_mashine_state['operation'] == 'ready'
            logger.debug(msg="Текущий режим: ready")
            current_string = ""

    elif cash_mashine_state['operation'] == 'take money':
        amount_to_take = int(ent.get())
        while amount_to_take % c.BASE != 0 or amount_to_push == 0:
            logger.info(msg=f'Запрошено снятие со счета суммы {amount_to_take}')
            del_entry()
            ent.insert(0, f"Сумма пополнения и снятия должна быть кратна {c.BASE}")
            amount_to_take = int(ent.get().replace(f"Сумма пополнения и снятия должна быть кратна {c.BASE}", '0'))
        logger.info(msg=f'Принят запрос снятиия суммы {amount_to_take}')
        if c.MIN_DUTY_TO_TAKE < amount_to_take * c.DUTY_TO_TAKE_PERCENT < c.MAX_DUTY_TO_TAKE:
            full_amount_to_take = round(amount_to_take * (1 + c.DUTY_TO_TAKE_PERCENT), 2)
        elif amount_to_take * c.DUTY_TO_TAKE_PERCENT < c.MIN_DUTY_TO_TAKE:
            full_amount_to_take = round(amount_to_take + c.MIN_DUTY_TO_TAKE, 2)
        else:
            full_amount_to_take = round(amount_to_take + c.MAX_DUTY_TO_TAKE, 2)
        full_amount_to_take += calculate_tax_size()
        logger.info(msg=f'Сумма снятия с учетом стоимости обслуживания {full_amount_to_take}')
        request_take = operation_with_money(full_amount_to_take)
        if request_take:
            del_entry()
            ent.insert(0, f"Сумма снята, на карте осталось {current_card_sum_op[1]}")
        else:
            del_entry()
            ent.insert(0, f"Недостаточно средств на счете {current_card_sum_op[1]}")

    elif cash_mashine_state['operation'] == 'push money':
        amount_to_push = int(ent.get())
        while amount_to_push % c.BASE != 0 or amount_to_push == 0:
            logger.info(msg=f'Запрошено пополнение счета на сумму {amount_to_push}')
            del_entry()
            ent.insert(0, f"Сумма пополнения и снятия должна быть кратна {c.BASE}")
            amount_to_push = int(ent.get().replace(f"Сумма пополнения и снятия должна быть кратна {c.BASE}", '0'))
        logger.info(msg=f'Принят запрос зачисления суммы {amount_to_push}')
        ent.delete(0, tk.END)
        ent.insert(0, "Приступаем к операции")
        full_amount_to_take = calculate_tax_size()
        request_push = operation_with_money(full_amount_to_take)
        if request_push:
            ent.delete(0, tk.END)
            ent.insert(0, f"Cумма зачислена. На счете {current_card_sum_op[1]}")
        else:
            del_entry()
            ent.insert(0, f"Недостаточно средств на счете {current_card_sum_op[1]}")


def clear_entry():
    ent.delete(len(ent.get()) - 1)


def digit_button(digit):
    return tk.Button(win, text=digit, font=('Arial', 25), command=lambda: add_digit(digit))


def del_entry():
    ent.delete(0, last=633)


def press_key(event):
    # print(repr(event.char))
    if event.char.isdigit():
        add_digit(event.char)
    elif event.char != '':
        clear_entry()


def take_cash():
    global current_card, amount_to_take
    logger.info(msg=f'Выбор операции снятия со счета')
    cash_mashine_state['operation'] = 'take money'
    logger.debug(msg="Текущий режим: take money")
    del_entry()
    ent.insert(0, "Введите сумму снятия:")


def push_cash():
    global current_card, amount_to_take
    logger.info(msg=f'Выбор операции пополнения счета')
    cash_mashine_state['operation'] = 'push money'
    logger.debug(msg="Текущий режим: push money")
    del_entry()
    ent.insert(0, "Введите сумму, которую хотите внести на счет:")


def exit():
    global current_card, current_string
    logger.info(
        msg=f'Клиент с номером карты {current_card} вышел из системы.')
    current_card = None
    cash_mashine_state['operation'] = 'ready'
    current_string = ''
    current_card = None

    del_entry()
    ent.insert(6, "Введите номер карты")


win = tk.Tk()
win.title('Дисплей банкомата')
photo = tk.PhotoImage(file='pic_atm_cash_icon.png')
win.iconphoto(False, photo)
win.config(bg='gray')
win.geometry("365x600+1000+100")
win.resizable(False, False)
label1 = tk.Label(win, text="Добрый день!",
                  bg='gray',
                  font=('Arial', 20, 'bold'),
                  pady=20,
                  ).grid(row=0, column=0, columnspan=5)

ent = tk.Entry(win, width=20, bg='black', justify=tk.CENTER, font=('Arial', 15))
ent.grid(row=5, column=0, columnspan=5, sticky='we')
ent.insert(6, "Введите номер карты")

t = 'Для снятия нажимите 1,\nдля пополнения нажмите - 2, \nдля выхода любую другую цифру'
action_label = tk.Label(win, text=t, bg='gray', pady=15, state="disabled")
action_label.grid(row=8, column=0,
                  columnspan=4,
                  sticky='w')

btn1 = digit_button('1').grid(row=11, column=0, ipadx=10, ipady=15, sticky='w')
btn2 = digit_button("2").grid(row=11, column=1, ipadx=10, ipady=15, sticky='w')
btn3 = digit_button("3").grid(row=11, column=2, ipadx=10, ipady=15, sticky='w')
btn11 = tk.Button(win, text="Cancel", command=del_entry, fg='#f59b7f', font=('Arial', 25)) \
    .grid(row=11, column=3, ipadx=20, ipady=15, columnspan=2, stick='we')

btn4 = digit_button("4").grid(row=12, column=0, ipadx=10, ipady=15)
btn5 = digit_button("5").grid(row=12, column=1, ipadx=10, ipady=15)
btn6 = digit_button("6").grid(row=12, column=2, ipadx=10, ipady=15)
btn12 = tk.Button(win, text="Clear", command=clear_entry, fg='#e3db4d', font=('Arial', 25)) \
    .grid(row=12, column=3, ipadx=20, ipady=15, columnspan=2, stick='we')

btn7 = digit_button("7").grid(row=13, column=0, ipadx=10, ipady=15)
btn8 = digit_button("8").grid(row=13, column=1, ipadx=10, ipady=15)
btn9 = digit_button("9").grid(row=13, column=2, ipadx=10, ipady=15)
btn0 = digit_button("0").grid(row=14, column=0, ipadx=10, ipady=15, columnspan=3, stick='we')
btn13 = tk.Button(win, text="Enter", command=get_entry, fg='#6ea30a', font=('Arial', 25)) \
    .grid(row=13, column=3, ipadx=20, ipady=15, columnspan=2, stick='we')

btn14 = tk.Button(win, text="Снять", state='active', command=take_cash, font=('Arial', 22)) \
    .grid(row=8, column=0, ipadx=10, ipady=10, columnspan=3, stick='wens')
btn15 = tk.Button(win, text="Пополнить", state='active', command=push_cash, font=('Arial', 22)) \
    .grid(row=8, column=3, ipadx=10, ipady=10, columnspan=2, stick='wens')
btn16 = tk.Button(win, text="Выйти", state='active', command=exit, font=('Arial', 22)) \
    .grid(row=9, column=0, ipadx=10, ipady=10, columnspan=5, stick='we')

win.bind('<Key>', press_key)

win.mainloop()

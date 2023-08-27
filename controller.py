import tkinter as tk
import SQL_DataBase
import view

MAX_DUTY_TO_TAKE = 600
MIN_DUTY_TO_TAKE = 30
DUTY_TO_TAKE_PERCENT = 1.5 / 100

cash_mashine_state = {'operation': 'ready'}
"""Operation: 'ready', 'seeking card', 'take money', 'deposit money' """
"""Operation: 'ready', 'seeking card', 'take money', 'deposit money' """
amount_to_take = None
full_amount_to_take = None


def add_digit(digit):
    """ Adding digit in the end of entered string of entry"""
    value = ent.get()
    if "Введите номер карты" in value:
        value = value.replace("Введите номер карты", '')
        print(value)
    elif 'Введите пин-код' in value:
        value = value.replace("Введите пин-код", '')
        print(value)
    elif 'Выберите операцию: Снять, пополнить, выйти' in value:
        value = value.replace("Выберите операцию: Снять, пополнить, выйти", '')
        print(value)
    elif 'Введите сумму снятия:' in value:
        value = value.replace("Введите сумму снятия:", '')
        print(value)
    ent.delete(0, tk.END)
    ent.insert(0, value + digit)


def operation_with_money(db_data):
    global full_amount_to_take
    print('full_amount_to_take=-------',full_amount_to_take)
    if cash_mashine_state['operation'] == 'take money':
        print('зашла раз')
        if db_data['sum_on_card'] is None or db_data['sum_on_card'] < full_amount_to_take:
            print('зашла два')
            # ent.delete(0, tk.END)
            ent.insert(0, "Недостаточно средств на счете")
        elif db_data['sum_on_card'] >= full_amount_to_take:
            print('зашла три')

            ent.insert(0, "Приступаем к операции")
            SQL_DataBase.take_money_from_card(current_card, full_amount_to_take)


def get_entry():
    global res, amount_to_take, full_amount_to_take
    global current_card
    global btn14, btn15, btn16
    while "+" not in res and not current_card:
        if res == '':
            res += ent.get().strip()
            print(res)
            del_entry()
            ent.insert(0, "Введите пин-код")
            break
        else:
            pin_num = ent.get()
            if "Введите пин-код" not in pin_num and len(pin_num) == 4:
                res += '+' + pin_num
                cash_mashine_state['operation'] = 'seeking card'
                del_entry()

    if cash_mashine_state['operation'] == 'seeking card':
        current_request = SQL_DataBase.find_card_and_pin(int(res.split("+")[0]), int(res.split("+")[1]))
        if current_request[0]:
            print('Наш клиент', )
            current_card = current_request[1]
            print("Выберите операцию: Снять, пополнить, выйти")
            ent.insert(0, "Выберите операцию: Снять, пополнить, выйти")
        else:
            print('Неверно введены номер карты и/или пин-код')
            ent.insert(0, 'Неверно введены номер карты и/или пин-код')

    if cash_mashine_state['operation'] == 'take money':
        amount_to_take = int(ent.get())
        if MIN_DUTY_TO_TAKE < amount_to_take * DUTY_TO_TAKE_PERCENT < MAX_DUTY_TO_TAKE:
            full_amount_to_take =round(amount_to_take * (1 + DUTY_TO_TAKE_PERCENT), 2)
        elif amount_to_take * DUTY_TO_TAKE_PERCENT < MIN_DUTY_TO_TAKE:
            full_amount_to_take = round(amount_to_take + MIN_DUTY_TO_TAKE, 2)
        else:
            full_amount_to_take = round(amount_to_take + MAX_DUTY_TO_TAKE, 2)
        print(f'{full_amount_to_take = }')
        db_data = SQL_DataBase.request_to_take(current_card, full_amount_to_take)
        print(db_data)
        operation_with_money(db_data)
        del_entry()


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
    cash_mashine_state['operation'] = 'take money'
    del_entry()
    ent.insert(0, "Введите сумму снятия:")


def push_cash():
    global current_card
    pass


current_card = None
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
res = ''
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
    .grid(row=11, column=3, ipadx=20, ipady=15, columnspan=2, stick='w')

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
# '<Key>' - обработка любого события нажатия на клавишу

btn14 = tk.Button(win, text="Снять", state='active', command=take_cash, font=('Arial', 22)) \
    .grid(row=8, column=0, ipadx=10, ipady=10, columnspan=3, stick='wens')
btn15 = tk.Button(win, text="Пополнить", state='active', command=push_cash, font=('Arial', 22)) \
    .grid(row=8, column=3, ipadx=10, ipady=10, columnspan=2, stick='wens')
btn16 = tk.Button(win, text="Выйти", state='active', command=lambda x: x, font=('Arial', 22)) \
    .grid(row=9, column=0, ipadx=10, ipady=10, columnspan=5, stick='we')

print(globals())
win.bind('<Key>', press_key)

win.mainloop()

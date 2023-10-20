import tkinter as tk
import SQL_DataBase
import constants as c
import business_logic as bl

state = ['ready']
amount_to_take, amount_to_push, full_amount_to_take, current_card_sum_op = None, None, None, None
current_card = ''


def add_digit(digit):
    """ Adding digit in the end of entered string of entry"""
    value = ent.get()
    for text in c.texts.values():
        if isinstance(text, str) and text in value:
            value = value.replace(text, '')
    ent.delete(0, tk.END)
    ent.insert(0, value + digit)


def get_entry():
    """The function handles pressing the Enter button when entering a card number,
    PIN code of the card and entering the amount to be withdrawn or credited"""

    global current_card_sum_op, current_card, amount_to_take, full_amount_to_take, amount_to_push

    if state[0] == 'ready':
        if not current_card:
            current_card = ent.get().strip()
            bl.logger.debug(msg=f"Введен номер карты: {current_card}")
            ent.delete(0, tk.END)
            ent.insert(0, c.texts['enter pin'])
        else:
            pin_num = ent.get()
            bl.logger.debug(msg=f"Введен пин-код: {pin_num}. Текущий режим: {state[0]}")
            ent.delete(0, tk.END)
            current_card_sum_op = SQL_DataBase.find_card_and_pin(int(current_card), int(pin_num))
            if current_card_sum_op:
                bl.logger.info(msg=f"Успешный вход с номером карты: {current_card}")
                ent.insert(0, c.texts['choose operation'])
            else:
                bl.logger.warning(msg=f"Неудачная попытка входа с данными {current_card, pin_num}")
                ent.insert(0, c.texts['wrong data'])

    elif state[0] == 'take money':
        amount_to_take = int(ent.get())
        bl.logger.info(msg=f'Запрошено снятие со счета суммы {amount_to_take}')
        if amount_to_take == 0 or amount_to_take % c.BASE != 0:
            ent.delete(0, tk.END)
            ent.insert(0, c.texts['base problem'])
        else:
            full_amount_to_take = bl.calculate_amount_to_take(amount_to_take, current_card_sum_op)
            ent.delete(0, tk.END)
            if current_card_sum_op[1] >= full_amount_to_take:
                current_card_sum_op[1] = bl.take_money(amount_to_take, full_amount_to_take, current_card_sum_op)
                current_info = f"{c.texts['after taking'][0]} {amount_to_take}, " \
                               f"{c.texts['after taking'][1]} {full_amount_to_take - amount_to_take}, " \
                               f"{c.texts['after taking'][2]} {current_card_sum_op[1]}"
                ent.insert(0, current_info)
                bl.logger.info(msg=current_info)
                current_card_sum_op[2] +=1
            else:
                current_info = f"{c.texts['not enough money']} {current_card_sum_op[1]}"
                ent.insert(0, current_info)
                bl.logger.info(msg=current_info)

    elif state[0] == 'push money':
        amount_to_push = int(ent.get())
        if amount_to_push == 0 or amount_to_push % c.BASE != 0:
            ent.delete(0, tk.END)
            ent.insert(0, c.texts['base problem'])
        else:
            ent.delete(0, tk.END)
            tax_to_push = bl.calculate_tax_size(tuple(current_card_sum_op))
            current_card_sum_op[1] = SQL_DataBase.push_money_to_card(current_card, amount_to_push, tax_to_push)
            if current_card_sum_op[1]:
                ent.delete(0, tk.END)
                current_info = f"{c.texts['after pushing'][0]} {amount_to_push}, " \
                               f"{c.texts['after pushing'][1]} {tax_to_push}, "\
                               f"{c.texts['after pushing'][2]} {current_card_sum_op[1]}"
                bl.logger.info(current_info)
                ent.insert(0, current_info)
            else:
                ent.delete(0, tk.END)
                ent.insert(0, f"{c.texts['not enough money']} {current_card_sum_op[1]}")


def clear_entry():
    ent.delete(len(ent.get()) - 1)


def digit_button(digit):
    return tk.Button(win, text=digit, font=('Arial', 25), command=lambda: add_digit(digit))


def press_key(event):
    # print(repr(event.char))
    if event.char.isdigit():
        add_digit(event.char)
    elif event.char != '':
        clear_entry()


def take_cash():
    if current_card_sum_op:
        state[0] = 'take money'
        bl.logger.info(msg=f'Выбор операции снятия со счета.')
        ent.delete(0, tk.END)
        ent.insert(0, c.texts['enter sum take'])


def push_cash():
    if current_card_sum_op:
        bl.logger.info(msg=f'Выбор операции пополнения счета.')
        state[0] = 'push money'
        ent.delete(0, tk.END)
        ent.insert(0, c.texts['enter sum push'])


def exit():
    global current_card_sum_op, current_card

    if current_card_sum_op:
        bl.logger.info(msg=f'Клиент с номером карты {current_card} вышел из системы.')
        current_card_sum_op = None
    state[0] = 'ready'
    current_card = ''
    ent.delete(0, tk.END)
    ent.insert(6, c.texts['enter card num'])


win = tk.Tk()
win.title('Дисплей банкомата')
photo = tk.PhotoImage(file='pic_atm_cash_icon.png')
win.iconphoto(False, photo)
win.config(bg='gray')
win.geometry("439x600+1000+100")
win.resizable(False, False)
label1 = tk.Label(win, text="Добрый день!",
                  bg='gray',
                  font=('Arial', 20, 'bold'),
                  pady=20,
                  ).grid(row=0, column=0, columnspan=5)

ent = tk.Entry(win, width=19, justify=tk.CENTER, font=('Arial', 15))
ent.grid(row=5, column=0, columnspan=5, sticky='we')

btn1 = digit_button('1').grid(row=12, column=0, ipadx=20, ipady=15, sticky='w')
btn2 = digit_button("2").grid(row=12, column=1, ipadx=20, ipady=15, sticky='w')
btn3 = digit_button("3").grid(row=12, column=2, ipadx=20, ipady=15, sticky='w')
btn11 = tk.Button(win, text="Cancel", command=exit, fg='#f59b7f', font=('Arial', 25)) \
    .grid(row=12, column=3, ipadx=20, ipady=15, columnspan=2, stick='we')

btn4 = digit_button("4").grid(row=13, column=0, ipadx=20, ipady=15)
btn5 = digit_button("5").grid(row=13, column=1, ipadx=20, ipady=15)
btn6 = digit_button("6").grid(row=13, column=2, ipadx=20, ipady=15)
btn12 = tk.Button(win, text="Clear", command=clear_entry, fg='#e3db4d', font=('Arial', 25)) \
    .grid(row=13, column=3, ipadx=20, ipady=15, columnspan=2, stick='we')

btn7 = digit_button("7").grid(row=14, column=0, ipadx=20, ipady=15)
btn8 = digit_button("8").grid(row=14, column=1, ipadx=20, ipady=15)
btn9 = digit_button("9").grid(row=14, column=2, ipadx=20, ipady=15)
btn0 = digit_button("0").grid(row=15, column=0, ipadx=10, ipady=15, columnspan=3, stick='we')
btn13 = tk.Button(win, text="Enter", command=get_entry, fg='#6ea30a', font=('Arial', 25)) \
    .grid(row=14, column=3, ipadx=20, ipady=15, columnspan=2, stick='we')

btn14 = tk.Button(win, text="Снять", state='active', command=take_cash, font=('Arial', 22)) \
    .grid(row=8, column=0, ipadx=10, ipady=10, columnspan=3, stick='wens')
btn15 = tk.Button(win, text="Пополнить", state='active', command=push_cash, font=('Arial', 22)) \
    .grid(row=8, column=3, ipadx=10, ipady=10, columnspan=2, stick='wens')
btn16 = tk.Button(win, text="Выйти", state='active', command=exit, font=('Arial', 22)) \
    .grid(row=9, column=0, ipadx=10, ipady=10, columnspan=5, stick='we')

ent.insert(6, c.texts['enter card num'])

win.bind('<Key>', press_key)

win.mainloop()

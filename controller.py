import tkinter as tk
import SQL_DataBase
import view


def add_digit(digit):
    value = ent.get()
    if "Введите номер карты" in value:
        value = value.replace("Введите номер карты", '')
        print(value)
    elif 'Введите пин-код' in value:
        value = value.replace("Введите пин-код", '')
        print(value)
    ent.delete(0, tk.END)

    ent.insert(0, value + digit)


def get_entry():
    global res
    while "+" not in res:
        if res == '':
            res += ent.get().strip().replace(' ', '')
            print(res)
            del_entry()
            ent.insert(0, "Введите пин-код")
            break
        else:
            pin_num = ent.get()
            if "Введите пин-код" not in pin_num and len(pin_num) == 4:
                res += '+' + pin_num
                print(res)
                del_entry()

    else:
        if SQL_DataBase.find_card_and_pin(int(res.split('+')[0]), int(res.split('+')[1])):
            print('Наш клиент')
            ent.insert(0, "Снять - 0, Пополнить - 1, Выход = 2 - 9")
            # lab_empty(state='active')
        else:
            print('шулер')


def clear_entry():
    ent.delete(len(ent.get()) - 1)


def digit_button(digit):
    return tk.Button(win, text=digit, font=('Arial', 25), command=lambda: add_digit(digit))


def del_entry():
    ent.delete(0, last=633)


def press_key(event):
    print(repr(event.char))
    if event.char.isdigit():
        add_digit(event.char)
    elif event.char != '':
        clear_entry()


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
# listbox2=Listbox(root,height=5,width=15,selectmode=SINGLE)
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
win.bind('<Key>', press_key)

win.mainloop()

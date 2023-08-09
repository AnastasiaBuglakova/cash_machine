import tkinter as tk
import SQL_DataBase
import view

def add_digit(digit):
    value = ent.get() + str(digit)
    ent.delete(0, tk.END)
    ent.insert(0, value)

def get_entry():
    global label1
    card_num = ent.get()
    pin_num = ent_pin.get()
    res = (int(('').join(card_num.strip().replace(' ', ''))), int(pin_num))
    print(res)
    if SQL_DataBase.find_card_and_pin(res[0],res[1]):
        print('Наш клиент')
        label1.grid_remove()
    else:
        print('шулер')

def clear_entry():
    ent.delete(len(ent.get())-1)
def digit_button(digit):
    return tk.Button(win, text=digit, font=('Arial', 25), command=lambda: add_digit(digit))

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
                  # relief=tk.RAISED,
                  ). grid(row=0, column=0, columnspan=5)

ent = tk.Entry(win, width=20, bg='black', justify=tk.RIGHT, font=('Arial', 25))
ent.grid(row=5, column=0, columnspan=5, sticky='we')
ent_pin = tk.Entry(win, show='*', width=20, bg='black', font=('Arial', 25))
ent_pin.grid(row=7, column=0, columnspan=5, sticky='we')
lab_card = tk.Label(win, text='Введите номер карты: ', bg='gray', pady=15)\
    .grid(row=4, column=0, columnspan=3, sticky='w')
lab_pin = tk.Label(win, text='Введите пин-код: ', bg='gray', pady=15).grid(row=6, column=0, columnspan=3, sticky='w')
lab_empty = tk.Label(win, text='', bg='gray', pady=15).grid(row=8, column=0, columnspan=3, sticky='w')
btn1 = digit_button('1').grid(row=11, column=0, ipadx=10, ipady=15, sticky='w')
btn2 = digit_button("2").grid(row=11, column=1, ipadx=10, ipady=15, sticky='w')
btn3 = digit_button("3").grid(row=11, column=2, ipadx=10, ipady=15, sticky='w')
btn11 = tk.Button(win, text="Cancel", fg='#f59b7f', font=('Arial', 25)) \
    .grid(row=11, column=3, ipadx=20, ipady=15, columnspan=2, stick='w')

btn4 = digit_button("4").grid(row=12, column=0, ipadx=10, ipady=15)
btn5 = digit_button("5").grid(row=12, column=1, ipadx=10, ipady=15)
btn6 = digit_button("6").grid(row=12, column=2, ipadx=10, ipady=15)
btn12 = tk.Button(win, text="Clear", command=clear_entry,fg='#e3db4d', font=('Arial', 25))\
    .grid(row=12, column=3,ipadx=20, ipady=15,columnspan=2,stick='we')

btn7 = digit_button("7").grid(row=13, column=0, ipadx=10, ipady=15)
btn8 = digit_button("8").grid(row=13, column=1, ipadx=10, ipady=15)
btn9 = digit_button("9").grid(row=13, column=2, ipadx=10, ipady=15)
btn0 = digit_button("0").grid(row=14, column=0, ipadx=10, ipady=15, columnspan=3, stick='we')
btn13 = tk.Button(win, text="Enter", command=get_entry, fg='#6ea30a', font=('Arial', 25))\
    .grid(row=13, column=3,ipadx=20,ipady=15, columnspan=2, stick='we')

win.mainloop()

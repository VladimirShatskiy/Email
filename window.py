from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog





def start():
    def type():
        res = Emails.get()
        i = 0
        for item in res.split(';'):
            print(item, i)
            i +=1



    window = Tk()
    window.title("Добро пожаловать в приложение для рассылки почты Яндекс")
    window.geometry('700x480')
    lbl = Label(window, text="Кому", font=("Arial", 12))
    lbl.grid(column=0, row=0)
    Emails = Entry(window, width=80)
    Emails.grid(column=1, row=0)
    lbl1 = Label(window, text="Заголовок письма", font=("Arial", 12))
    lbl1.grid(column=0, row=1)
    Head = Entry(window, width=80)
    Head.grid(column=1, row=1)
    lbl2 = Label(window, text="Текст письма", font=("Arial", 12))
    lbl2.grid(column=0, row=2)
    Body = scrolledtext.ScrolledText(window, width=40, height=10)
    Body.insert(INSERT, 'Коллеги, добрый день\n\n\n\n\n\n\n')
    Body.grid(column=1, row=2)
        # files = filedialog.askopenfilenames()

    btn = Button(window, text="Начать рассылку!", command=type)
    btn.grid(column=1, row=5)
    window.mainloop()
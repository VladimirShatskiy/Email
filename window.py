from tkinter import END, Tk, Label, Entry, Button, INSERT
from tkinter import scrolledtext
from tkinter import filedialog
from re import split

from main import send_email

files_global = []


def start():
    font_size = 10
    font_name = "Calibri"

    def save_data():
        global files_global
        data = {}
        data['text'] = Body.get(1.0, END)
        Cc_get = Cc.get()
        if not Cc_get:
            data['cc'] = []
        else:
            data['cc'] = Cc.get().replace('\n', '').split(';')
        data['To'] = split('\n|,|;| ', Emails.get())
        # data['To'] = Emails.get().replace('\n', '').split(';')
        data['files'] = files_global
        data['head'] = Head.get()

        if not data['head'] or not data['cc']:
            window1 = Tk()
            window1.title("Внимание !!!")
            window1.geometry('250x100')
            window1.configure(bg='blue')
            window1.eval('tk::PlaceWindow . center')
            lbl = Label(window1, text="       Поля обязательные к заполнению:\n\n  'Копия'\n\n  'Тема письма'",
                        font=(font_name, font_size), bg='blue', fg='white')
            lbl.grid(column=0, row=0)

            return

        number_to = len(data['To'])
        step = 49
        for item in range(0, number_to, step):
            send_email(data['To'][item: item + step], data['head'], data['text'], data['files'], data['cc'])

    def get_file():
        global files_global
        files = filedialog.askopenfilenames()
        l = len(files)
        lbl1 = Label(window, text=f"Загрузил {l} файл(а)", font=(font_name, font_size))
        lbl1.grid(column=0, row=8)
        files_global = files

    with open('email.txt', 'r', encoding='utf-8') as file_open:
        text_email = file_open.read()

    window = Tk()
    window.title("Добро пожаловать в приложение для рассылки почты Яндекс")
    window.geometry('900x700')
    window.eval('tk::PlaceWindow . center')

    lbl = Label(window, text="Кому", font=(font_name, font_size))
    lbl.grid(column=0, row=0)
    Emails = Entry(window, width=80)
    Emails.grid(column=1, row=0)

    lb2 = Label(window, text="Копия", font=(font_name, font_size))
    lb2.grid(column=0, row=1)
    Cc = Entry(window, width=80)
    Cc.grid(column=1, row=1)

    lbl1 = Label(window, text=" ", font=(font_name, font_size))
    lbl1.grid(column=0, row=2)

    lbl1 = Label(window, text="Тема письма", font=(font_name, font_size))
    lbl1.grid(column=0, row=3)
    Head = Entry(window, width=80)
    Head.grid(column=1, row=3)

    lbl1 = Label(window, text=" ", font=(font_name, font_size))
    lbl1.grid(column=0, row=4)

    lbl2 = Label(window, text="Текст письма", font=(font_name, font_size))
    lbl2.grid(column=0, row=5)
    Body = scrolledtext.ScrolledText(window, width=80, height=30)
    Body.insert(INSERT, text_email)
    Body.grid(column=1, row=5)

    lbl1 = Label(window, text=" ", font=(font_name, font_size))
    lbl1.grid(column=0, row=6)

    btn = Button(window, text="Прикрепить файлы", command=get_file)
    btn.grid(column=0, row=7)

    btn = Button(window, text="Начать рассылку!", command=save_data)
    btn.grid(column=1, row=7)

    window.mainloop()

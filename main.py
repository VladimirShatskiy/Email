import os, sys
import smtplib

from configparser import ConfigParser
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate

import window


def send_email(to_addr, subject, text, file_to_attach):
    """
    Отправка электронного письма с вложением
    """

    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, "email.ini")
    # проверка наличия файла `email.ini`
    if os.path.exists(config_path):
        cfg = ConfigParser()
        cfg.read(config_path)
        # извлечение переменных из конфигурации
        server = cfg.get("smtp", "server")
        port = cfg.get("smtp", "port")
        from_addr = cfg.get("smtp", "email")
        passwd = cfg.get("smtp", "passwd")
        cc = cfg.get("smtp", "cc")
    else:
        print("Конфигурация не найдена!")
        sys.exit(1)

    # формируем тело письма
    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)
    if text:
        # текст письма отправляем как вложение
        msg.attach(MIMEText(text))
    msg["To"] = ', '.join(to_addr)
    msg["cc"] = cc
    emails = to_addr

    attachment = MIMEBase('application', "octet-stream")
    header = 'Content-Disposition', f'attachment; filename="{file_to_attach}"'
    try:
        with open(file_to_attach, "rb") as fh:
            data = fh.read()
        attachment.set_payload(data)
        encoders.encode_base64(attachment)
        attachment.add_header(*header)
        msg.attach(attachment)
    except IOError:
        print(f"Ошибка при открытии файла вложения {file_to_attach}")

    try:
        smtp = smtplib.SMTP(server, port)
        smtp.starttls()
        smtp.ehlo()
        smtp.login(from_addr, passwd)
        smtp.sendmail(from_addr, emails, msg.as_string())
    except smtplib.SMTPException as err:
        print('Что - то пошло не так...')
        raise err
    finally:
        smtp.quit()


if __name__ == "__main__":
    to_addr = ["shatskiy.v@gmail.com", "shatskiy.v@inbox.ru", "vshatsky@nmrauto.ru"]
    subject = "Тестовое письмо от Python."
    text = "Тестовое письмо для отправки!\nС Уважением\nя"
    file_attach = 'temp.txt'
    # send_email(to_addr, subject, text, file_attach)
    window.start()

    print("act")
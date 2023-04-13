import os, sys
import smtplib
from configparser import ConfigParser
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
import window
from pathlib import Path


def send_email(to_addr, subject, text, file_to_attach, cc):
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
    if len(to_addr) > 1:
        msg["To"] = ', '.join(to_addr)
    else:
        msg["To"] = to_addr[0]

    if len(to_addr) > 1:
        msg["cc"] = ', '.join(cc)
    else:
        if cc:
           msg["cc"] = cc[0]

    emails = to_addr + cc

    try:
        for path in file_to_attach:
            part = MIMEBase('application', "octet-stream")
            with open(path, 'rb') as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment', filename=Path(path).name)
            msg.attach(part)

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
    window.start()


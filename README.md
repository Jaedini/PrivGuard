# PrivGuard 🛡️ 


<p align="center">
  <img src="https://img.shields.io/github/stars/Jaedini/PrivGuard?style=flat-square&logo=github" />
  <img src="https://img.shields.io/github/forks/Jaedini/PrivGuard?style=flat-square" />
  <img src="https://img.shields.io/github/issues/Jaedini/PrivGuard?style=flat-square" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg" />
  <img src="https://img.shields.io/badge/Status-Stable-brightgreen?style=flat-square" />
  <img src="https://img.shields.io/badge/Platform-Windows-blue?style=flat-square" />
</p>

---

<p align="center">
  <img src="assets/Screenshot.png" alt="PrivGuard UI" width="700"/>
</p>

<p align="center">
  <b> Moderne Dateiverschlüsselung mit Dark Mode & Installer</b>
</p>

---

##  Features
- 🔑 AES-Verschlüsselung mit **Salt-Datei**  
- 🌙 Dunkles UI + **Log Panel**  
- 💻 Einfache Bedienung, moderne GUI (PyQt)  
- 🛠️ Installer via **Inno Setup**   
- 🌍 Multi-Language (Deutsch, Englisch, Französisch, bald mehr)  

---

##  Installation

###  Windows (Empfohlen)
1. Lade den 👉 [PrivGuard Installer v3.0](https://github.com/Jaedini/PrivGuard/releases) herunter  
2. Führe den Installer aus  
3. Starte PrivGuard über Startmenü oder Desktop-Icon  

---
##  Release Notes
🚀 v3.0.0

- ✅ Überarbeitete GUI (Dark Mode + Log Panel)

- ✅ Installer über Inno Setup

- ✅ Neue Projektstruktur (src/, tests/, docs/)

---

##  FAQ

**❓ Ist PrivGuard Open Source?**  
➡️ Ja, lizenziert unter MIT.  

**❓ Wo finde ich die Logs?**  
➡️ `%APPDATA%/PrivGuard/privguard.log`  

---

##  Security Policy

Melde Sicherheitsprobleme **nicht** öffentlich im Issue Tracker.  
Sende eine E-Mail an:  
📧 [privguardhelpdesk@gmail.com](mailto:privguardhelpdesk@gmail.com)  

---

##  Maintainer
**Jaeden Hommel** – [GitHub](https://github.com/Jaedini)  

---

##  Kontakt
📧 [privguardhelpdesk@gmail.com](mailto:privguardhelpdesk@gmail.com)  

---

##  GitHub
- 👉 [GitHub Issues](https://github.com/Jaedini/PrivGuard/issues)  
- 👉 [Releases](https://github.com/Jaedini/PrivGuard/releases)  
- 👉 [Pull Requests](https://github.com/Jaedini/PrivGuard/pulls)  

---

##  Lizenz
Dieses Projekt ist unter der **MIT Lizenz** veröffentlicht.  
Siehe [LICENSE](LICENSE) für weitere Informationen.

---

##  Build

## Installer erstellen (Inno Setup)
1. Lade [Inno Setup](https://jrsoftware.org/isinfo.php) herunter
2. Öffne setup/privguard.iss
3. Klicke auf **Build Installer**
   
**Mit PyInstaller**
```bash
pyinstaller --noconsole --onefile --name PrivGuard src/main.py



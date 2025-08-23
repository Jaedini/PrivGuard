<h1 align="center">🔐 PrivGuard v3.0</h1>
<p align="center">
  <i>Ein modernes Open-Source Tool für sichere Dateiverschlüsselung mit einer intuitiven GUI.</i>
</p>

<p align="center">
  <img src="assets/screenshot.png" alt="PrivGuard Screenshot" width="700"/>
</p>

---

<p align="center">
  <!-- Badges -->
  <a href="https://github.com/Jaedini/PrivGuard/releases">
    <img src="https://img.shields.io/github/v/release/Jaedini/PrivGuard?style=for-the-badge&color=blue" alt="Release">
  </a>
  <a href="https://github.com/Jaedini/PrivGuard/stargazers">
    <img src="https://img.shields.io/github/stars/Jaedini/PrivGuard?style=for-the-badge&color=yellow" alt="Stars">
  </a>
  <a href="https://github.com/Jaedini/PrivGuard/forks">
    <img src="https://img.shields.io/github/forks/Jaedini/PrivGuard?style=for-the-badge&color=lightgrey" alt="Forks">
  </a>
  <a href="https://github.com/Jaedini/PrivGuard/issues">
    <img src="https://img.shields.io/github/issues/Jaedini/PrivGuard?style=for-the-badge&color=orange" alt="Issues">
  </a>
  <a href="https://github.com/Jaedini/PrivGuard/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/Jaedini/PrivGuard?style=for-the-badge&color=green" alt="License">
  </a>
</p>

---

✨ Features
- 🔑 **AES-256 Verschlüsselung** mit PBKDF2 Key-Derivation  
- 📦 **Automatische Backup-Funktion** vor jeder Verschlüsselung  
- 📂 **Rekursive Verschlüsselung** mit 3-stufiger Sicherheitswarnung  
- 🖥️ **Intuitive moderne GUI** (PySide6)  
- 🛡️ **Recovery-Mechanismus** mit Salt-Datei  
- 📜 **Log-System** (`%APPDATA%/PrivGuard/privguard.log`)  
- 🌙 **Dark Mode Unterstützung**  

---

🛠️ Tech Stack
- **Python 3.11+**  
- **PySide6** (GUI)  
- **Cryptography** (AES256)  
- **PyInstaller** (Build)  
- **Inno Setup** (Windows Installer)  
- **pytest** (Tests)  

---

📥 Installation

🖥️ Windows (Empfohlen)
1. Lade den [📦 PrivGuard Installer v3.0](https://github.com/Jaedini/PrivGuard/releases) herunter  
2. Führe den Installer aus  
3. Starte PrivGuard über Startmenü oder Desktop-Icon  

🐍 Entwickler-Setup
```bash
git clone https://github.com/Jaedini/PrivGuard.git
cd PrivGuard
pip install -r requirements.txt
python main.py

📸 Screenshots
<p align="center"> <img src="assets/screenshot.png" alt="PrivGuard UI" width="700"/> </p>

🧪 Tests
```bash
pytest tests/

📦 Build
Mit PyInstaller
```bash
pyinstaller --noconsole --onefile --name PrivGuard src/main.py
Installer erstellen (Inno Setup)
1. Lade [Inno Setup](https://jrsoftware.org/isinfo.php) herunter
2. Öffne setup/privguard.iss
3. Klicke auf Build Installer

📢 Release Notes
🚀 v3.0.0
✅ Neues Recovery-System mit Salt-Datei
✅ Überarbeitete GUI (Dark Mode + Log Panel) 
✅ Installer über Inno Setup
✅ Neue Projektstruktur (src/, tests/, docs/)

🗺️ Roadmap
 macOS & Linux Support (AppImage, dmg)

 Cloud-Backup Integration (optional)

 Portable Version ohne Installation

 Multi-Language Support (Deutsch, Englisch, Französisch)

 ❓ FAQ

❓ Kann ich verschlüsselte Dateien wiederherstellen, wenn ich mein Passwort verliere?
➡️ Nur wenn du die Salt-Datei gesichert hast. Ohne Passwort + Salt-Datei ist eine Wiederherstellung unmöglich.

❓ Ist PrivGuard Open Source?
➡️ Ja, lizenziert unter MIT.

❓ Wo finde ich die Logs?
➡️ %APPDATA%/PrivGuard/privguard.log

🔒 Security Policy

Melde Sicherheitsprobleme **nicht** öffentlich im Issue Tracker.
Sende eine E-Mail an: [privguardsupport@protonmail.com](mailto:privguardsupport@protonmail.com)

👨‍💻 Maintainer

Jaeden Hommel – [GitHub](https://github.com/Jaedini)

📬 Kontakt
📧[privguardsupport@protonmail.com](mailto:privguardsupport@protonmail.com)

🐙[GitHub Issues](https://github.com/Jaedini/PrivGuard/issues)


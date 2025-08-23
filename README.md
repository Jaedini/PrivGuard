🔐 PrivGuard v3.0

**PrivGuard** ist ein Open-Source-Tool zur sicheren Dateiverschlüsselung mit moderner GUI.  
Es richtet sich an Entwickler, Security-Interessierte und alle, die ihre Daten zuverlässig schützen möchten.

---

✨ Features
- AES-256 Verschlüsselung (PBKDF2 Key-Derivation, HMAC-Integrity)
- Backup-Funktion vor jeder Verschlüsselung
- Rekursive Verschlüsselung mit zusätzlicher Sicherheitswarnung
- Moderne, minimalistische GUI (PySide6)
- Recovery via Salt-Datei
- Logging aller Operationen

---

📦 Installation

1. Lade den Installer herunter:  
   👉 [PrivGuard Installer v3.0](https://DEINNAME.github.io/PrivGuard/PrivGuardInstaller.exe)

2. Führe den Installer aus.

3. Starte PrivGuard über Desktop-Icon oder Startmenü.

---

🖥️ Screenshots
![PrivGuard GUI](assets/screenshot.png)

---

🚀 Development Setup

```bash
# Repo klonen
git clone https://github.com/DEINNAME/PrivGuard.git
cd PrivGuard

# Virtuelle Umgebung
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)

# Dependencies
pip install -r requirements.txt

# Start
python privguard.py

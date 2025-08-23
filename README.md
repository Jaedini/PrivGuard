🔐 PrivGuard v3.0

PrivGuard ist ein modernes Open-Source-Tool zur **lokalen Verschlüsselung von Dateien und Ordnern** mit einer benutzerfreundlichen, modernen GUI.

[![GitHub release](https://img.shields.io/github/v/release/Jaedini/PrivGuard?style=for-the-badge)](https://github.com/Jaedini/PrivGuard/releases)
[![License](https://img.shields.io/github/license/Jaedini/PrivGuard?style=for-the-badge)](LICENSE)
[![Downloads](https://img.shields.io/github/downloads/Jaedini/PrivGuard/total?style=for-the-badge)](https://github.com/Jaedini/PrivGuard/releases)
[![Issues](https://img.shields.io/github/issues/Jaedini/PrivGuard?style=for-the-badge)](https://github.com/Jaedini/PrivGuard/issues)

---

✨ Features

- 🔒 **AES256 Verschlüsselung** mit PBKDF2 Key-Derivation  
- 💾 **Backup-Funktion** vor jeder Verschlüsselung  
- ⚡ **Rekursive Verschlüsselung** mit 3-stufiger Sicherheitswarnung  
- 🖥️ Intuitive moderne **GUI (PySide6 / Qt)**  
- 🛡️ **Recovery-Mechanismus** mit Salt-Datei  
- 📜 **Log-System** (lokal gespeichert in `%APPDATA%\PrivGuard\privguard.log`)  

---

📸 Screenshots

*(Hier kannst du echte Screenshots einfügen – z. B. GUI im Light/Dark-Mode)*

<img src="assets/screenshot.png" width="600">

---

📥 Installation

Windows (empfohlen)

1. Lade die neueste Version herunter:  
   👉 [**PrivGuard Installer v3.0**](https://github.com/Jaedini/PrivGuard/releases/latest)

2. Führe den Installer aus.

3. Starte **PrivGuard** über das Startmenü oder das Desktop-Symbol.

Manuelle Installation (Entwickler)

```bash
# Repository klonen
git clone https://github.com/DEIN-USERNAME/PrivGuard.git
cd PrivGuard

# Virtuelle Umgebung erstellen
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
.venv\Scripts\activate      # Windows

# Abhängigkeiten installieren
pip install -r requirements.txt

# Anwendung starten
python PrivGuard.py

#!/usr/bin/env python3
"""
PrivGuard 3.0 - Lokale Dateiverschlüsselung mit GUI
"""

import os
import sys
import shutil
import base64
import logging
import threading
from pathlib import Path

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel,
    QProgressBar, QCheckBox, QFileDialog, QMessageBox, QFrame, QButtonGroup, QRadioButton,
    QTextEdit
)
from PySide6.QtCore import Qt, Signal, QObject
from PySide6.QtGui import QIcon, QTextCursor

# ===================== Konstanten =====================
MAGIC_HEADER = b"ENCRYPTED_FILE_V3::"
HMAC_LEN = 32
SALT_FILENAME = ".salt"
BACKUP_FOLDER_NAME = ".backup"
KDF_ITERATIONS = 390_000

# ----------------- Pfade & Logging -----------------
def appdata_dir() -> str:
    base = os.getenv("APPDATA") or os.path.join(Path.home(), ".config")
    p = os.path.join(base, "PrivGuard")
    os.makedirs(p, exist_ok=True)
    return p

LOG_DIR = appdata_dir()
LOGFILE = os.path.join(LOG_DIR, "privguard.log")

# File + Stream Logging
logging.basicConfig(
    filename=LOGFILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ===================== Utilities =====================
def resource_path(rel: str) -> str:
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, rel)  # type: ignore
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), rel)

def is_drive_root(path: str) -> bool:
    try:
        p = Path(path).resolve()
        return str(p) == p.anchor
    except Exception:
        return False

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=KDF_ITERATIONS,
        backend=default_backend(),
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))

def compute_hmac(key: bytes, data: bytes) -> bytes:
    h = hmac.HMAC(key, hashes.SHA256(), backend=default_backend())
    h.update(data)
    return h.finalize()

def find_or_create_salt(target: str) -> bytes:
    p = Path(target)
    base = p if p.is_dir() else p.parent
    salt_file = base / SALT_FILENAME
    if salt_file.exists():
        return salt_file.read_bytes()
    salt = os.urandom(16)
    salt_file.write_bytes(salt)
    return salt

# ===================== Signals =====================
class WorkerSignals(QObject):
    progress = Signal(int, str, int, int)   # percent, file, current, total
    finished = Signal(str)
    error = Signal(str)
    log = Signal(str)

# ===================== Kernfunktionen =====================
def _iter_files(target: str):
    for root, _dirs, files in os.walk(target):
        for fn in files:
            yield os.path.join(root, fn)

def encrypt_all(target: str, password: str, backup: bool, recursive: bool, signals: WorkerSignals | None = None):
    try:
        target = os.path.abspath(target)
        salt = find_or_create_salt(target)
        key = derive_key(password, salt)
        fernet = Fernet(key)

        backup_root = os.path.join(target if os.path.isdir(target) else os.path.dirname(target), BACKUP_FOLDER_NAME)
        if backup:
            os.makedirs(backup_root, exist_ok=True)

        if os.path.isdir(target):
            files = list(_iter_files(target)) if recursive else [os.path.join(target, f) for f in os.listdir(target) if os.path.isfile(os.path.join(target, f))]
        else:
            files = [target]

        skip_prefixes = {
            os.path.abspath(backup_root),
            os.path.abspath(LOGFILE),
        }

        files = [f for f in files if os.path.basename(f) != SALT_FILENAME and
                 not any(os.path.abspath(f).startswith(prefix) for prefix in skip_prefixes)]

        total = max(1, len(files))
        for idx, fp in enumerate(files, start=1):
            try:
                with open(fp, "rb") as f:
                    data = f.read()
                if data.startswith(MAGIC_HEADER):
                    if signals:
                        signals.progress.emit(int(idx / total * 100), fp, idx, total)
                    continue

                if backup:
                    base = target if os.path.isdir(target) else os.path.dirname(target)
                    rel = os.path.relpath(fp, start=base)
                    dest = os.path.join(backup_root, rel)
                    os.makedirs(os.path.dirname(dest), exist_ok=True)
                    shutil.copy2(fp, dest)

                enc = fernet.encrypt(data)
                tag = compute_hmac(key, enc)
                with open(fp, "wb") as f:
                    f.write(MAGIC_HEADER + tag + enc)

                if signals:
                    signals.progress.emit(int(idx / total * 100), fp, idx, total)
                    signals.log.emit(f"✔ Verschlüsselt: {fp}")
            except Exception as e:
                if signals:
                    signals.error.emit(f"Fehler bei: {fp} → {e}")
                    signals.log.emit(f"❌ Fehler bei {fp}: {e}")

        if signals:
            signals.finished.emit("✅ Verschlüsselung abgeschlossen.")
    except Exception as e:
        if signals:
            signals.error.emit(f"Fehler: {e}")

def decrypt_all(target: str, password: str, signals: WorkerSignals | None = None):
    try:
        target = os.path.abspath(target)
        salt = find_or_create_salt(target)
        key = derive_key(password, salt)
        fernet = Fernet(key)

        if os.path.isdir(target):
            files = list(_iter_files(target))
        else:
            files = [target]

        files = [f for f in files if os.path.basename(f) != SALT_FILENAME]

        total = max(1, len(files))
        for idx, fp in enumerate(files, start=1):
            try:
                with open(fp, "rb") as f:
                    data = f.read()
                if not data.startswith(MAGIC_HEADER):
                    if signals:
                        signals.progress.emit(int(idx / total * 100), fp, idx, total)
                    continue

                file_hmac = data[len(MAGIC_HEADER):len(MAGIC_HEADER) + HMAC_LEN]
                encrypted = data[len(MAGIC_HEADER) + HMAC_LEN:]

                if compute_hmac(key, encrypted) != file_hmac:
                    raise ValueError("Integrität fehlgeschlagen (HMAC mismatch)")

                plaintext = fernet.decrypt(encrypted)
                with open(fp, "wb") as f:
                    f.write(plaintext)

                if signals:
                    signals.progress.emit(int(idx / total * 100), fp, idx, total)
                    signals.log.emit(f"🔓 Entschlüsselt: {fp}")
            except Exception as e:
                if signals:
                    signals.error.emit(f"Fehler bei: {fp} → {e}")
                    signals.log.emit(f"❌ Fehler bei {fp}: {e}")

        if signals:
            signals.finished.emit("✅ Entschlüsselung abgeschlossen.")
    except Exception as e:
        if signals:
            signals.error.emit(f"Fehler: {e}")

# ===================== GUI =====================
class PrivGuardGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PrivGuard 3.0")
        self.setFixedSize(1050, 720)

        icon_path = resource_path("favicon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.setStyleSheet("""
            QWidget { background-color: #1E1F28; color: #EEE; font-family: 'Segoe UI'; }
            QLabel { color: #D8D8D8; }
            QFrame#line { background: #2C2F36; max-height: 1px; min-height: 1px; }
            QPushButton { background-color: #3CB371; color: #FFF; padding: 8px 12px; border-radius: 6px; border: 0; }
            QPushButton:hover { background-color: #2E8B57; }
            QPushButton#btn_decrypt { background-color: #FF6B6B; }
            QPushButton#btn_decrypt:hover { background-color: #E04F4F; }
            QPushButton#btn_recursive { background-color: #FFB84D; color: #000; }
            QPushButton#btn_recursive:hover { background-color: #E09E35; }
            QPushButton:disabled { background-color: #555; }
            QLineEdit { background-color: #2C2F36; padding: 8px; border-radius: 4px; color: #FFF; border: 1px solid #333; }
            QCheckBox { padding: 4px; }
            QProgressBar { border: 1px solid #2C2F36; border-radius: 5px; text-align: center; background-color: #2C2F36; color: #FFF; height: 20px; }
            QProgressBar::chunk { background-color: #3CB371; border-radius: 5px; }
            QTextEdit { background-color: #15161D; border: 1px solid #2C2F36; color: #A8FFA8; font-family: Consolas; font-size: 12px; }
        """)

        self.signals = WorkerSignals()
        self.signals.progress.connect(self.update_progress)
        self.signals.finished.connect(self.operation_finished)
        self.signals.error.connect(self.operation_error)
        self.signals.log.connect(self.append_log)

        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)

        # Header mit Titel & Version
        header = QHBoxLayout()
        title = QLabel("PrivGuard")
        title.setStyleSheet("font-size: 22px; font-weight: 600; color: #FFFFFF;")
        version = QLabel("v3.0")
        version.setStyleSheet("color: #888; font-size: 14px; margin-left: 10px;")
        header.addWidget(title)
        header.addWidget(version)
        header.addStretch()
        root.addLayout(header)
        root.addWidget(self._line())

        # Modus Auswahl
        mode_box = QHBoxLayout()
        self.radio_encrypt = QRadioButton("Encrypt")
        self.radio_decrypt = QRadioButton("Decrypt")
        self.radio_encrypt.setChecked(True)
        self.mode_group = QButtonGroup(self)
        self.mode_group.addButton(self.radio_encrypt)
        self.mode_group.addButton(self.radio_decrypt)
        mode_box.addWidget(self.radio_encrypt)
        mode_box.addWidget(self.radio_decrypt)
        root.addLayout(mode_box)

        # Pfad Auswahl
        row1 = QHBoxLayout()
        self.input_path = QLineEdit()
        self.btn_browse = QPushButton("Wählen…")
        row1.addWidget(QLabel("Datei / Ordner:"))
        row1.addWidget(self.input_path, 1)
        row1.addWidget(self.btn_browse)
        root.addLayout(row1)

        # Passwort
        root.addWidget(QLabel("Passwort:"))
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.Password)
        root.addWidget(self.input_pass)

        # Optionen
        self.chk_backup = QCheckBox("Backup (.backup) erstellen")
        self.chk_backup.setChecked(True)
        root.addWidget(self.chk_backup)

        # Buttons
        row2 = QHBoxLayout()
        self.btn_start = QPushButton("Start")
        self.btn_recursive = QPushButton("Rekursiv Modus")
        self.btn_recursive.setObjectName("btn_recursive")
        row2.addWidget(self.btn_start)
        row2.addWidget(self.btn_recursive)
        root.addLayout(row2)

        # Progress
        self.progress = QProgressBar()
        root.addWidget(self.progress)
        self.label_status = QLabel("Bereit")
        self.label_status.setAlignment(Qt.AlignCenter)
        root.addWidget(self.label_status)

        # Log Panel
        root.addWidget(QLabel("Log:"))
        self.log_panel = QTextEdit()
        self.log_panel.setReadOnly(True)
        root.addWidget(self.log_panel, 2)

        # Events
        self.btn_browse.clicked.connect(self.choose_path)
        self.btn_start.clicked.connect(lambda: self.run_operation(False))
        self.btn_recursive.clicked.connect(self.run_recursive)

    def _line(self) -> QFrame:
        line = QFrame()
        line.setObjectName("line")
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        return line

    def choose_path(self):
        path = QFileDialog.getExistingDirectory(self, "Ordner wählen")
        if not path:
            file_tuple = QFileDialog.getOpenFileName(self, "Datei wählen")
            path = file_tuple[0]
        if path:
            self.input_path.setText(path)

    def run_recursive(self):
        reply = QMessageBox.warning(
            self, "Warnung – Rekursiver Modus",
            "⚠ Rekursiver Modus verschlüsselt ALLES gnadenlos in allen Unterordnern.\n\n"
            "Dies kann nicht rückgängig gemacht werden, außer mit dem Passwort.\n\n"
            "Fortfahren?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.run_operation(True)

    def run_operation(self, recursive: bool):
        path = self.input_path.text().strip()
        pw = self.input_pass.text()
        if not path or not os.path.exists(path):
            QMessageBox.information(self, "Hinweis", "Bitte gültigen Pfad auswählen.")
            return
        if not pw:
            QMessageBox.information(self, "Hinweis", "Bitte ein Passwort eingeben.")
            return

        do_encrypt = self.radio_encrypt.isChecked()
        self.btn_start.setEnabled(False)
        self.btn_recursive.setEnabled(False)
        self.progress.setValue(0)
        self.label_status.setText("Läuft …")
        self.log_panel.clear()

        def worker():
            if do_encrypt:
                encrypt_all(path, pw, backup=self.chk_backup.isChecked(), recursive=recursive, signals=self.signals)
            else:
                decrypt_all(path, pw, signals=self.signals)

        t = threading.Thread(target=worker, daemon=True)
        t.start()

    def update_progress(self, percent: int, filename: str, current: int, total: int):
        self.progress.setValue(max(0, min(100, percent)))
        self.label_status.setText(f"{percent}% – Datei {current}/{total}: {os.path.basename(filename)}")

    def operation_finished(self, msg: str):
        self.label_status.setText(msg)
        self.btn_start.setEnabled(True)
        self.btn_recursive.setEnabled(True)

    def operation_error(self, msg: str):
        self.label_status.setText(msg)

    def append_log(self, msg: str):
        self.log_panel.append(msg)
        self.log_panel.moveCursor(QTextCursor.End)

# ===================== Main =====================
def main():
    app = QApplication(sys.argv)
    w = PrivGuardGUI()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

import os
import threading
from pathlib import Path

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel,
    QProgressBar, QCheckBox, QFileDialog, QMessageBox, QFrame, QTextEdit,
    QRadioButton, QButtonGroup, QSplitter
)
from PySide6.QtCore import Qt, AlignmentFlag
from PySide6.QtGui import QIcon

from src.core.crypto import encrypt_all, decrypt_all, is_drive_root
from src.core.workers import WorkerSignals
from src.gui.styles import APP_STYLE
from src.utils.logger import log_file_path

# Lies Version
VERSION = Path("version.txt").read_text(encoding="utf-8").strip()
class PrivGuardUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"PrivGuard {VERSION}")
        self.setFixedSize(1100, 700)

        # Icon laden
        icon_path = os.path.join("assets", "favicon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.setStyleSheet(APP_STYLE)

        # Worker Signals
        self.signals = WorkerSignals()
        self.signals.progress.connect(self.update_progress)
        self.signals.finished.connect(self.operation_finished)
        self.signals.error.connect(self.operation_error)

        self._build_ui()

    def _build_ui(self):
        root = QHBoxLayout(self)

        # Sidebar
        side = QVBoxLayout()
        title = QLabel("PrivGuard")
        title.setStyleSheet("font-size: 22px; font-weight: 600; color: #FFFFFF;")
        side.addWidget(title)
        side.addWidget(self._line())

        # Moduswahl
        mode_label = QLabel("Modus")
        mode_label.setStyleSheet("color: #AAAAAA;")
        side.addWidget(mode_label)

        self.radio_encrypt = QRadioButton("Encrypt")
        self.radio_decrypt = QRadioButton("Decrypt")
        self.radio_encrypt.setChecked(True)

        self.mode_group = QButtonGroup(self)
        self.mode_group.addButton(self.radio_encrypt)
        self.mode_group.addButton(self.radio_decrypt)

        side.addWidget(self.radio_encrypt)
        side.addWidget(self.radio_decrypt)
        side.addStretch()

        # Content + Logs als Splitter
        splitter = QSplitter(Qt.Vertical)

        # Content Panel
        content_widget = QWidget()
        content = QVBoxLayout(content_widget)

        lbl_path = QLabel("Datei / Ordner")
        self.input_path = QLineEdit()
        self.btn_browse = QPushButton("Wählen…")

        row1 = QHBoxLayout()
        row1.addWidget(self.input_path, 1)
        row1.addWidget(self.btn_browse)

        content.addWidget(lbl_path)
        content.addLayout(row1)
        content.addWidget(self._line())

        lbl_pw = QLabel("Passwort")
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.Password)

        content.addWidget(lbl_pw)
        content.addWidget(self.input_pass)
        content.addWidget(self._line())

        # Optionen
        self.chk_backup = QCheckBox("Backup (.backup) erstellen")
        self.chk_backup.setChecked(True)

        self.chk_recursive = QCheckBox("Rekursiv (ALLE Unterordner und Dateien)")
        self.chk_recursive.setChecked(False)

        content.addWidget(self.chk_backup)
        content.addWidget(self.chk_recursive)

        # Start
        self.btn_start = QPushButton("Start")
        content.addWidget(self.btn_start)

        self.progress = QProgressBar()
        content.addWidget(self.progress)

        self.label_status = QLabel("Bereit")
        self.label_status.setAlignment(Qt.AlignCenter)
        self.label_status.setStyleSheet("color: #9AD0B1;")
        content.addWidget(self.label_status)

        content.addStretch()

        splitter.addWidget(content_widget)

        # Log Panel
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setStyleSheet("background-color: #14151C; color: #00FF90; font-family: Consolas;")
        self.log_view.setPlaceholderText("Log-Ausgabe…")
        splitter.addWidget(self.log_view)
        splitter.setSizes([500, 200])

        # Layout einfügen
        root.addLayout(side, 1)
        root.addWidget(splitter, 3)

        # Events
        self.btn_browse.clicked.connect(self.choose_path)
        self.btn_start.clicked.connect(self.run_operation)

    def _line(self) -> QFrame:
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        return line

    # ---------- UI Actions ----------
    def choose_path(self):
        path = QFileDialog.getExistingDirectory(self, "Ordner wählen")
        if not path:
            file_tuple = QFileDialog.getOpenFileName(self, "Datei wählen")
            path = file_tuple[0]
        if path:
            self.input_path.setText(path)

    def _triple_confirm_drive_root(self, path: str) -> bool:
        if not is_drive_root(path):
            return True
        t = f"Achtung: Du willst das Laufwerk ({path}) verschlüsseln."
        r1 = QMessageBox.warning(self, "Bestätigung 1/3",
                                 f"{t}\n\nDas kann ALLE Dateien betreffen. Fortfahren?",
                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if r1 != QMessageBox.Yes:
            return False
        r2 = QMessageBox.warning(self, "Bestätigung 2/3",
                                 "Sicher? Ein Backup wird empfohlen.",
                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if r2 != QMessageBox.Yes:
            return False
        r3 = QMessageBox.critical(self, "Letzte Bestätigung 3/3",
                                  "Letzte Chance zum Abbrechen!\nJetzt wirklich verschlüsseln?",
                                  QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        return r3 == QMessageBox.Yes

    def _confirm_recursive(self) -> bool:
        if not self.chk_recursive.isChecked():
            return True
        msg = QMessageBox.warning(
            self, "Warnung",
            "Rekursiver Modus aktiv!\nALLE Unterordner und Dateien werden verschlüsselt.\n\nFortfahren?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        return msg == QMessageBox.Yes

    def run_operation(self):
        path = self.input_path.text().strip()
        pw = self.input_pass.text()

        if not path or not os.path.exists(path):
            QMessageBox.information(self, "Hinweis", "Bitte gültigen Pfad auswählen.")
            return
        if not pw:
            QMessageBox.information(self, "Hinweis", "Bitte ein Passwort eingeben.")
            return

        do_encrypt = self.radio_encrypt.isChecked()

        if do_encrypt and not self._triple_confirm_drive_root(path):
            self.label_status.setText("Abgebrochen.")
            return

        if do_encrypt and not self._confirm_recursive():
            self.label_status.setText("Abgebrochen (rekursiv).")
            return

        self.btn_start.setEnabled(False)
        self.progress.setValue(0)
        self.label_status.setText("Läuft …")

        def worker():
            if do_encrypt:
                encrypt_all(path, pw,
                            backup=self.chk_backup.isChecked(),
                            recursive=self.chk_recursive.isChecked(),
                            signals=self.signals)
            else:
                decrypt_all(path, pw, signals=self.signals)

        t = threading.Thread(target=worker, daemon=True)
        t.start()

    def update_progress(self, percent: int, filename: str):
        self.progress.setValue(max(0, min(100, percent)))
        self.label_status.setText(f"{percent}% – {os.path.basename(filename)}")
        self.log_view.append(f"[+] {filename}")

    def operation_finished(self, msg: str):
        self.label_status.setText(msg)
        self.btn_start.setEnabled(True)
        self.log_view.append(f"[✓] {msg}")

    def operation_error(self, msg: str):
        self.label_status.setText(msg)
        self.log_view.append(f"[!] {msg}")

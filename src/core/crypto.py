import os
import shutil
import base64
import logging
from pathlib import Path
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
from .workers import WorkerSignals
from src.utils.logger import log_file_path

MAGIC_HEADER = b"ENCRYPTED_FILE_V3::"
HMAC_LEN = 32
SALT_FILENAME = ".salt"
BACKUP_FOLDER_NAME = ".backup"
KDF_ITERATIONS = 390_000
LOGFILE = log_file_path()

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

        files = []
        if os.path.isdir(target):
            files = list(_iter_files(target)) if recursive else [os.path.join(target, f) for f in os.listdir(target)]
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
                        signals.progress.emit(int(idx / total * 100), fp)
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
                    signals.progress.emit(int(idx / total * 100), fp)
            except Exception as e:
                logging.exception(f"Fehler beim Verschlüsseln: {fp}")
                if signals:
                    signals.error.emit(f"Fehler bei: {fp} → {e}")

        if signals:
            signals.finished.emit("Verschlüsselung abgeschlossen.")
    except Exception as e:
        logging.exception("Fatal in encrypt_all")
        if signals:
            signals.error.emit(f"Fehler: {e}")

def decrypt_all(target: str, password: str, signals: WorkerSignals | None = None):
    try:
        target = os.path.abspath(target)
        salt = find_or_create_salt(target)
        key = derive_key(password, salt)
        fernet = Fernet(key)

        files = []
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
                        signals.progress.emit(int(idx / total * 100), fp)
                    continue

                file_hmac = data[len(MAGIC_HEADER):len(MAGIC_HEADER) + HMAC_LEN]
                encrypted = data[len(MAGIC_HEADER) + HMAC_LEN:]

                if compute_hmac(key, encrypted) != file_hmac:
                    raise ValueError("Integrität fehlgeschlagen (HMAC mismatch)")

                plaintext = fernet.decrypt(encrypted)
                with open(fp, "wb") as f:
                    f.write(plaintext)

                if signals:
                    signals.progress.emit(int(idx / total * 100), fp)
            except Exception as e:
                logging.exception(f"Fehler beim Entschlüsseln: {fp}")
                if signals:
                    signals.error.emit(f"Fehler bei: {fp} → {e}")

        if signals:
            signals.finished.emit("Entschlüsselung abgeschlossen.")
    except Exception as e:
        logging.exception("Fatal in decrypt_all")
        if signals:
            signals.error.emit(f"Fehler: {e}")

# https://github.com/Guilherme-alexander/CYBER-VAULT
from pathlib import Path
import hashlib
import sqlite3
import secrets
import tempfile
import shutil
import zipfile
import os

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


PBKDF2_ITERATIONS = 300_000
KEY_LENGTH = 32
CHUNK_SIZE = 8192


# ======================================================
# password -> AES key
# ======================================================

def derive_key(password: str, salt: bytes, iterations: int = PBKDF2_ITERATIONS) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LENGTH,
        salt=salt,
        iterations=iterations,
    )
    return kdf.derive(password.encode("utf-8"))


def password_hash(password: str, salt: bytes, iterations: int = PBKDF2_ITERATIONS) -> str:
    key = derive_key(password=password, salt=salt, iterations=iterations)
    return hashlib.sha256(key).hexdigest()


# ======================================================
# zip helpers
# ======================================================

def folder_to_zip_bytes(folder: Path) -> bytes:
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
    temp_path = Path(temp_file.name)
    temp_file.close()

    with zipfile.ZipFile(temp_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file in folder.rglob("*"):
            if file.is_file():
                zf.write(file, file.relative_to(folder))

    data = temp_path.read_bytes()
    temp_path.unlink(missing_ok=True)
    return data


def zip_bytes_to_folder(zip_bytes: bytes, folder: Path) -> None:
    folder.mkdir(parents=True, exist_ok=True)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
    temp_path = Path(temp_file.name)
    temp_file.write(zip_bytes)
    temp_file.close()

    with zipfile.ZipFile(temp_path, "r") as zf:
        zf.extractall(folder)

    temp_path.unlink(missing_ok=True)


# ======================================================
# AES-GCM
# ======================================================

def encrypt_blob(raw_data: bytes, key: bytes) -> tuple[bytes, bytes]:
    nonce = secrets.token_bytes(12)
    aes = AESGCM(key)
    encrypted = aes.encrypt(nonce, raw_data, None)
    return nonce, encrypted


def decrypt_blob(nonce: bytes, encrypted: bytes, key: bytes) -> bytes:
    aes = AESGCM(key)
    return aes.decrypt(nonce, encrypted, None)


# ======================================================
# sqlite
# ======================================================

def init_database(db_path: Path) -> None:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            username_hash TEXT,
            salt BLOB,
            password_hash TEXT,
            iterations INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vault(
            id INTEGER PRIMARY KEY,
            nonce BLOB,
            ciphertext BLOB,
            updated_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_vault_blob(db_path: Path, nonce: bytes, ciphertext: bytes) -> None:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vault")
    cursor.execute(
        "INSERT INTO vault(nonce, ciphertext, updated_at) VALUES(?, ?, datetime('now'))",
        (nonce, ciphertext),
    )
    conn.commit()
    conn.close()


def load_vault_blob(db_path: Path) -> tuple[bytes, bytes] | None:
    conn = sqlite3.connect(db_path)
    row = conn.execute("SELECT nonce, ciphertext FROM vault LIMIT 1").fetchone()
    conn.close()
    return (row[0], row[1]) if row else None


# ======================================================
# vault actions
# ======================================================

def lock_folder(folder: Path, db_path: Path, password: str, salt: bytes) -> None:
    key = derive_key(password=password, salt=salt)
    zip_bytes = folder_to_zip_bytes(folder)
    nonce, encrypted = encrypt_blob(zip_bytes, key)
    save_vault_blob(db_path=db_path, nonce=nonce, ciphertext=encrypted)
    secure_clear_folder(folder)


def unlock_folder(folder: Path, db_path: Path, password: str, salt: bytes) -> None:
    data = load_vault_blob(db_path)

    if not data:
        folder.mkdir(parents=True, exist_ok=True)
        return

    nonce, encrypted = data
    key = derive_key(password=password, salt=salt)
    zip_bytes = decrypt_blob(nonce, encrypted, key)
    zip_bytes_to_folder(zip_bytes, folder)


# ======================================================
# secure wipe
# ======================================================

def wipe_file(file_path: Path) -> None:
    if not file_path.exists():
        return

    size = file_path.stat().st_size
    with open(file_path, "r+b") as f:
        f.write(b"\x00" * size)
        f.flush()
        os.fsync(f.fileno())

    file_path.unlink(missing_ok=True)


def secure_clear_folder(folder: Path) -> None:
    if not folder.exists():
        return

    for item in folder.rglob("*"):
        if item.is_file():
            wipe_file(item)

    for item in sorted(folder.rglob("*"), reverse=True):
        if item.is_dir():
            shutil.rmtree(item, ignore_errors=True)

    folder.mkdir(parents=True, exist_ok=True)

# https://github.com/Guilherme-alexander/CYBER-VAULT
import ctypes
from ctypes import wintypes
from pathlib import Path
import sys
import sqlite3
import os

from PyQt5.QtWidgets import QApplication

from config import (
    load_config,
    set_open,
    set_close,
    verify_vault_hash,
    username_hash,
)
from encrypt import unlock_folder, lock_folder
from window import LoginWindow, VaultWindow, show_error


# ======================================================
# windows paths
# ======================================================

def windows_desktop() -> Path:
    buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, 0, None, 0, buf)
    return Path(buf.value)


def windows_onedrive_desktop() -> Path | None:
    one = os.environ.get("OneDrive")
    if not one:
        return None

    for name in ("Área de Trabalho", "Desktop"):
        pt = Path(one) / name
        if pt.exists():
            return pt

    return None


# ======================================================
# runtime
# ======================================================

def current_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).parent


# ======================================================
# vault detection
# ======================================================

def possible_roots() -> list[Path]:
    roots = [current_dir()]
    roots.append(windows_desktop() / "Vault")

    one = windows_onedrive_desktop()
    if one:
        roots.append(one / "Vault")

    return roots


def find_vault_root() -> Path | None:
    for root in possible_roots():
        cfg = root / ".config"
        if not cfg.exists():
            continue

        try:
            data = load_config(root)
            saved = data.get("ROOT_PATH", "")
            if saved:
                saved_root = Path(saved)
                if saved_root.exists():
                    return saved_root
            return root
        except Exception:
            continue

    return None


ROOT = find_vault_root()
DB_PATH = (ROOT / "vault.lock.db") if ROOT else None


# ======================================================
# helpers
# ======================================================

def folder_from_config() -> Path:
    cfg = load_config(ROOT)
    return ROOT / cfg["FOLDER"]


def folder_has_content(folder: Path) -> bool:
    if not folder.exists():
        return False
    return any(item.is_file() for item in folder.rglob("*"))


# ======================================================
# integrity
# ======================================================

def verify_integrity() -> bool:
    cfg = load_config(ROOT)
    expected = cfg.get("VAULT_HASH", "")
    if not expected:
        return True

    exe = ROOT / "vault.exe"
    if not exe.exists():
        return True

    return verify_vault_hash(exe, expected)


# ======================================================
# users
# ======================================================

def get_user_record():
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT username_hash, salt FROM users LIMIT 1"
    ).fetchone()
    conn.close()
    return row


def validate_user(username: str) -> bytes | None:
    row = get_user_record()
    if not row:
        return None

    db_hash, salt = row[0], row[1]
    if username_hash(username) != db_hash:
        return None

    return salt


# ======================================================
# auto lock
# ======================================================

def auto_lock_if_needed() -> None:
    cfg = load_config(ROOT)
    folder = folder_from_config()
    state = cfg.get("STATE", "CLOSE")

    if state == "OPEN" or folder_has_content(folder):
        set_close(ROOT)


# ======================================================
# controller
# ======================================================

class VaultApp:

    def __init__(self):
        self.login_window = None
        self.vault_window = None
        self.password = None
        self.salt = None
        self.folder = None

    def start(self):
        if not ROOT:
            show_error("Vault não encontrado.")
            return

        if not verify_integrity():
            show_error("Falha de integridade.")
            return

        auto_lock_if_needed()
        self.folder = folder_from_config()
        self.show_login()

    def show_login(self):
        self.login_window = LoginWindow(self.login)
        self.login_window.show()

    def login(self, username: str, password: str):
        salt = validate_user(username)

        if not salt:
            show_error("Usuário inválido.")
            return

        try:
            unlock_folder(
                folder=self.folder,
                db_path=DB_PATH,
                password=password,
                salt=salt,
            )
        except Exception:
            show_error("Senha inválida.")
            return

        self.password = password
        self.salt = salt

        set_open(ROOT)

        self.login_window.close()
        self.show_panel()

    def show_panel(self):
        self.vault_window = VaultWindow(self.folder, self.lock_now)
        self.vault_window.show()

    def lock_now(self):
        if not self.password or not self.salt:
            return

        try:
            lock_folder(
                folder=self.folder,
                db_path=DB_PATH,
                password=self.password,
                salt=self.salt,
            )
            set_close(ROOT)
        except Exception:
            show_error("Falha ao bloquear.")

        if self.vault_window:
            self.vault_window.close()

        self.show_login()


# ======================================================
# run
# ======================================================

def main():
    app = QApplication(sys.argv)
    controller = VaultApp()
    controller.start()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

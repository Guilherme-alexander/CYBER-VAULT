# https://github.com/Guilherme-alexander/CYBER-VAULT
from pathlib import Path
import hashlib
import ctypes

CONFIG_FILE = ".config"

FILE_ATTRIBUTE_HIDDEN = 0x02
FILE_ATTRIBUTE_NORMAL = 0x80

DEFAULT_CONFIG = {
    "STATE": "CLOSE",
    "FOLDER": "Vault",
    "ROOT_PATH": "",
    "USERNAME_HASH": "",
    "VAULT_HASH": "",
    "VERSION": "1",
}

THEME = {
    "bg": "#060910",
    "surface": "#0c1522",
    "surface2": "#101d2e",
    "green": "#00ff8f",
    "purple": "#a259ff",
    "gold": "#f5c542",
    "red": "#ff4d6d",
    "blue": "#4d9fff",
    "text": "#c8d8eb",
    "muted": "#8aa5c0",
}


# ======================================================
# helpers
# ======================================================

def config_path(vault_root: Path) -> Path:
    return vault_root / CONFIG_FILE


def _unhide(path: Path) -> None:
    """Remove hidden attribute so Python can write the file."""
    try:
        ctypes.windll.kernel32.SetFileAttributesW(str(path), FILE_ATTRIBUTE_NORMAL)
    except Exception:
        pass


def _hide(path: Path) -> None:
    """Re-apply hidden attribute after writing."""
    try:
        ctypes.windll.kernel32.SetFileAttributesW(str(path), FILE_ATTRIBUTE_HIDDEN)
    except Exception:
        pass


# ======================================================
# load / save
# ======================================================

def load_config(vault_root: Path) -> dict:
    path = config_path(vault_root)
    data = DEFAULT_CONFIG.copy()

    if not path.exists():
        save_config(vault_root, data)
        return data

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key.strip()] = value.strip()

    return data


def save_config(vault_root: Path, data: dict) -> None:
    path = config_path(vault_root)

    # FIX: remove hidden attribute before writing (PermissionError workaround)
    _unhide(path)

    lines = [f"{key}={value}" for key, value in data.items()]
    path.write_text("\n".join(lines), encoding="utf-8")

    # re-hide after writing
    _hide(path)


# ======================================================
# state
# ======================================================

def set_open(vault_root: Path) -> None:
    cfg = load_config(vault_root)
    cfg["STATE"] = "OPEN"
    save_config(vault_root, cfg)


def set_close(vault_root: Path) -> None:
    cfg = load_config(vault_root)
    cfg["STATE"] = "CLOSE"
    save_config(vault_root, cfg)


# ======================================================
# hashes
# ======================================================

def username_hash(username: str) -> str:
    return hashlib.sha256(username.encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


# ======================================================
# integrity
# ======================================================

def verify_vault_hash(file_path: Path, expected_hash: str) -> bool:
    if not file_path.exists():
        return False
    return file_sha256(file_path) == expected_hash

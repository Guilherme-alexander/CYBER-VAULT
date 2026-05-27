"""
AUTH: Guilherme Alexander | DATA: 05/2026
GITHUB: https://github.com/Guilherme-alexander

MIT License

Copyright (c) 2026 Guilherme Alexander

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import ctypes
from ctypes import wintypes
from pathlib import Path
import secrets
import sqlite3
import os
import sys
import time
import threading

from config import save_config, username_hash, file_sha256
from encrypt import init_database, password_hash, lock_folder, PBKDF2_ITERATIONS


VAULT_DIR_NAME = "Vault"
DB_FILE        = "vault.lock.db"
FILE_ATTRIBUTE_HIDDEN = 0x02


# ======================================================
# ANSI - cores Fallout terminal
# ======================================================

ESC = "\033["

class C:
    RESET      = f"{ESC}0m"
    BRIGHT     = f"{ESC}1m"
    DIM        = f"{ESC}2m"

    GREEN      = f"{ESC}32m"       # verde médio
    BGREEN     = f"{ESC}92m"       # verde brilhante (fósforo)
    DGREEN     = f"{ESC}2;32m"     # verde escuro / dim
    RED        = f"{ESC}31m"
    BRED       = f"{ESC}91m"
    YELLOW     = f"{ESC}33m"
    WHITE      = f"{ESC}97m"
    BLACK_BG   = f"{ESC}40m"
    CLEAR_LINE = f"{ESC}2K\r"

def g(text):  return f"{C.BGREEN}{text}{C.RESET}"       # verde neon
def d(text):  return f"{C.DGREEN}{text}{C.RESET}"       # verde dim
def r(text):  return f"{C.BRED}{text}{C.RESET}"         # vermelho erro
def y(text):  return f"{C.YELLOW}{text}{C.RESET}"       # amarelo aviso
def b(text):  return f"{C.WHITE}{C.BRIGHT}{text}{C.RESET}"  # branco bold

def enable_ansi_windows():
    """Habilita ANSI no terminal Windows (necessário no cmd.exe)."""
    try:
        import ctypes
        kernel = ctypes.windll.kernel32
        kernel.SetConsoleMode(kernel.GetStdHandle(-11), 7)
    except Exception:
        pass


# ======================================================
# banner ASCII art
# ======================================================

BANNER = r"""####################################################+ #++- -#############################################
##########################################.#### .-. .####++++.  #########################################
########################################   ##..##########++++++- ########################################
#######################################--##-+##+-####   .++++++++  ######################################
#######################################++##### +#+. -+#+  ++++-.++- +####################################
#######################################. ###  ############+-+##+ .++ -###################################
####################################### #. #.+######### -#######  ++   ##################################
#####################################     ##############+.####. ++++. +  .###############################
##################################   +## ###+#################.- .++  ####.  -###########################
###############################-  -####-+##  ####+###.   #####-- - + .#######   #########################
#############--+#############-  +###### ###+###--#######+#####++  .  ##########.  #######################
##########+.###+ ##########+  +#######+ ###### .##############++--  +############.  #####################
##########.####. #########  -#########- ######- ###############+#. -###############  +###################
##########-#### #########  ###########- ##.##########. -##########- +###############. .##################
##########.#### #######+ .############+ +  +-.    .+##. -#########  #################+  #################
##########-####- #####- -##############. #.+  +###-  +#.######.  .+####################  ################
#######      .###- +#- .################  ###################  +########################  ###############
##### ########+ .##    ##################  ################- -##########################+ .##############
#####.########## -##    .+################.  ############.  -##   +######################+ +#############
#####-        ++ ###.  ----.         ..----- . .########## -###- .   .####################  #############
##### #########. ### + --------------------  ##-     ++-  ####+ ......  -#################+ +############
##### +###++####+ #. # .-------------------- #####.   .######.  ........   ################  ############
######-.-###-.   ##-.# ....-----------------. +############   .............  ##############. ############
######.######### +# #. ..........---- ------- +######+.    .................  .############- +###########
#######.        +- #  .............   ------- +###### ........................  -##########+ -###########
#########+-      #  ........    .-### ------. ######- ..........................  #########+ -###########
##################  ################# ------ .######  ...........................  +#######- -###########
##################  ################# ------ #######  .........    ...............  .######. ############
##################. ################# ------ #######  .........         ..........   .#####  ############
################### .################ ------ ######+ .........       ###+  ......    ######  ############
###################  +############### ------ ######+ .........      +### ......     -#####  #############
###################+ .############### .----- ######+ ........       ###  ....      .######  #############
####################. -##############. ----- ######+ ........       #+  ...        ######  ##############
#####################  ##############+  .--- ######+ .......       -# ...         ######. +##############
######################  ############## ##.   ######+ .......       +             ######. +###############
#######################  +############ #############          -++# +            ######. -################
########################  +###########-###########################  +-        .######. +#################
#########################. .##########- ########################## .###+-    +######  ###################
###########################  +########+   #######################. .#####+ #. ####. -####################
############################-  #######+ .---    .++###++-.          ##### -++ -#-  ######################
##############################.  +##### .---...............          #######  .  ########################"""


# ======================================================
# efeito digitação
# ======================================================

def typewrite(text: str, delay: float = 0.012, color: str = C.BGREEN, newline: bool = True):
    sys.stdout.write(color)
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(C.RESET)
    if newline:
        sys.stdout.write("\n")
    sys.stdout.flush()


def typewrite_banner(banner: str, line_delay: float = 0.004):
    """Imprime banner linha a linha com efeito de digitação rápida."""
    lines = banner.splitlines()
    for line in lines:
        # # → verde brilhante, + → verde médio, . - → dim
        colored = ""
        for ch in line:
            if ch == "#":
                colored += f"{C.BGREEN}{ch}"
            elif ch == "+":
                colored += f"{C.GREEN}{ch}"
            elif ch in (".", "-"):
                colored += f"{C.DGREEN}{ch}"
            else:
                colored += f"{C.RESET}{ch}"
        colored += C.RESET
        print(colored)
        time.sleep(line_delay)


# ======================================================
# spinner de loading
# ======================================================

class Spinner:
    FRAMES = ["|", "/", "--", "\\"]

    def __init__(self, label: str = ""):
        self.label    = label
        self._active  = False
        self._thread  = None

    def _spin(self):
        i = 0
        while self._active:
            frame = self.FRAMES[i % len(self.FRAMES)]
            sys.stdout.write(f"\r{C.BGREEN}{frame}{C.RESET}  {C.GREEN}{self.label}{C.RESET}  ")
            sys.stdout.flush()
            i += 1
            time.sleep(0.12)

    def start(self, label: str = ""):
        if label:
            self.label = label
        self._active = True
        self._thread = threading.Thread(target=self._spin, daemon=True)
        self._thread.start()

    def stop(self, ok: bool = True, msg: str = ""):
        self._active = False
        if self._thread:
            self._thread.join()
        icon = g("[OK]") if ok else r("[FAIL]")
        text = msg or self.label
        sys.stdout.write(f"\r{C.CLEAR_LINE}{icon}  {C.GREEN}{text}{C.RESET}\n")
        sys.stdout.flush()


# ======================================================
# utilitários de print
# ======================================================

def sep(char: str = "-", width: int = 56):
    print(d(char * width))

def header(text: str):
    sep()
    typewrite(f"  {text}", delay=0.018, color=C.BGREEN)
    sep()

def prompt(label: str) -> str:
    sys.stdout.write(f"{C.GREEN}  {label} {C.BGREEN}>{C.RESET} ")
    sys.stdout.flush()
    return input()

def prompt_secret(label: str) -> str:
    import getpass
    sys.stdout.write(f"{C.GREEN}  {label} {C.BGREEN}>{C.RESET} ")
    sys.stdout.flush()
    return getpass.getpass("")

def ok(text: str):
    typewrite(f"  [OK]   {text}", delay=0.008, color=C.BGREEN)

def err(text: str):
    typewrite(f"  [ERR]  {text}", delay=0.008, color=C.BRED)

def warn(text: str):
    typewrite(f"  [!]    {text}", delay=0.010, color=C.YELLOW)

def info(text: str):
    typewrite(f"  >>     {text}", delay=0.008, color=C.GREEN)


# ======================================================
# windows paths
# ======================================================

def windows_desktop() -> Path:
    buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, 16, None, 0, buf)
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


def hide_path(path: Path) -> None:
    if path.exists():
        ctypes.windll.kernel32.SetFileAttributesW(str(path), FILE_ATTRIBUTE_HIDDEN)


# ======================================================
# menu seleção de local
# ======================================================

def ask_base_path() -> Path:
    while True:
        desktop = windows_desktop()
        one     = windows_onedrive_desktop()

        options = {}
        idx     = 1

        print()
        typewrite("  Onde criar o Vault?", delay=0.015, color=C.BGREEN)
        sep("·")

        if one and one != desktop:
            print(f"  {g(f'[{idx}]')}  {one}\\Vault")
            options[str(idx)] = one
            idx += 1

        print(f"  {g(f'[{idx}]')}  {desktop}\\Vault")
        options[str(idx)] = desktop
        idx += 1

        custom_idx = str(idx)
        print(f"  {d(f'[{idx}]')}  {d('Local personalizado')}")
        idx += 1

        exit_idx = str(idx)
        print(f"  {r(f'[{idx}]')}  {r('Sair')}")
        print()

        choice = prompt("Escolha").strip()

        if choice in options:
            return options[choice]

        if choice == custom_idx:
            raw = prompt("Digite o PATH").strip()
            if not raw:
                warn("Path vazio.")
                continue
            p = Path(raw)
            if not p.exists():
                err("Path não existe.")
                continue
            return p

        if choice == exit_idx:
            print()
            typewrite("  Até logo...", delay=0.04, color=C.DGREEN)
            sys.exit(0)

        warn("Opção inválida.")


# ======================================================
# helpers
# ======================================================

def vault_root(base: Path) -> Path:
    return base / VAULT_DIR_NAME

def db_path(root: Path) -> Path:
    return root / DB_FILE

def folder_path(root: Path, name: str) -> Path:
    return root / name

def ensure_empty_target(root: Path) -> None:
    if root.exists():
        raise FileExistsError(f"Vault já existe: {root}")


# ======================================================
# db
# ======================================================

def insert_user(db: Path, username: str, password: str, salt: bytes) -> None:
    conn = sqlite3.connect(db)
    conn.execute(
        "INSERT INTO users(username_hash, salt, password_hash, iterations) VALUES(?,?,?,?)",
        (username_hash(username), salt, password_hash(password=password, salt=salt), PBKDF2_ITERATIONS),
    )
    conn.commit()
    conn.close()


# ======================================================
# config
# ======================================================

def create_config(root: Path, folder_name: str, username: str) -> None:
    exe      = root / "vault.exe"
    exe_hash = file_sha256(exe) if exe.exists() else ""
    save_config(root, {
        "STATE":        "CLOSE",
        "FOLDER":       folder_name,
        "ROOT_PATH":    str(root),
        "USERNAME_HASH": username_hash(username),
        "VAULT_HASH":   exe_hash,
        "VERSION":      "1",
    })


# ======================================================
# build
# ======================================================

def build_vault() -> None:
    enable_ansi_windows()
    os.system("cls" if os.name == "nt" else "clear")

    # --- banner ---
    typewrite_banner(BANNER, line_delay=0.003)
    print()
    typewrite("  ROBCO INDUSTRIES (TM) TERMLINK PROTOCOL", delay=0.01, color=C.DGREEN)
    typewrite("  CYBER VAULT  //  BUILD WIZARD  //  v1.0", delay=0.01, color=C.GREEN)
    print()

    try:
        # --- localização ---
        header("PASSO 1 / 4  —  LOCALIZAÇÃO")
        base = ask_base_path()
        ok(f"Destino: {base}")

        # --- nome da pasta ---
        print()
        header("PASSO 2 / 4  —  CONFIGURAÇÃO")
        folder_name = prompt("Nome da pasta secreta").strip()
        if not folder_name:
            err("Nome inválido.")
            return

        # --- credenciais ---
        print()
        header("PASSO 3 / 4  —  CREDENCIAIS")
        username = prompt("Usuário").strip()
        if not username:
            err("Usuário inválido.")
            return

        password = prompt_secret("Senha")
        if not password:
            err("Senha inválida.")
            return

        confirm = prompt_secret("Confirme a senha")
        if password != confirm:
            err("Senhas não coincidem.")
            return

        # --- construindo ---
        print()
        header("PASSO 4 / 4  —  CONSTRUINDO VAULT")

        sp = Spinner()

        sp.start("Criando estrutura de pastas...")
        root   = vault_root(base)
        ensure_empty_target(root)
        root.mkdir(parents=True, exist_ok=False)
        folder = folder_path(root, folder_name)
        folder.mkdir()
        time.sleep(0.4)
        sp.stop(ok=True, msg="Estrutura criada")

        sp.start("Inicializando banco de dados...")
        db   = db_path(root)
        init_database(db)
        time.sleep(0.3)
        sp.stop(ok=True, msg="Banco de dados pronto")

        sp.start("Gerando salt criptográfico...")
        salt = secrets.token_bytes(32)
        time.sleep(0.3)
        sp.stop(ok=True, msg="Salt gerado  (32 bytes)")

        sp.start("Registrando usuário  (PBKDF2 x300000)...")
        insert_user(db, username, password, salt)
        sp.stop(ok=True, msg="Usuário registrado")

        sp.start("Criptografando vault  (AES-256-GCM)...")
        lock_folder(folder=folder, db_path=db, password=password, salt=salt)
        sp.stop(ok=True, msg="Vault criptografado")

        sp.start("Salvando configuração...")
        create_config(root, folder_name, username)
        time.sleep(0.2)
        sp.stop(ok=True, msg="Configuração salva")

        sp.start("Aplicando atributos ocultos...")
        hide_path(folder)
        hide_path(db)
        hide_path(root / ".config")
        time.sleep(0.2)
        sp.stop(ok=True, msg="Arquivos ocultados")

        # --- sucesso ---
        print()
        sep("=")
        typewrite("  VAULT CRIADO COM SUCESSO", delay=0.02, color=C.BGREEN)
        sep("=")
        info(f"Local  :  {root}")
        info(f"Pasta  :  {folder_name}")
        info(f"Usuário:  {username}")
        info(f"Cifra  :  AES-256-GCM + PBKDF2-SHA256")
        sep()
        warn("Guarde sua senha. Sem ela o vault é irrecuperável.")
        sep()
        print()

    except FileExistsError as e:
        print()
        err(str(e))

    except Exception as e:
        print()
        err(f"Erro inesperado: {e}")

    finally:
        input(d("\n  Pressione ENTER para sair..."))


# ======================================================
# run
# ======================================================

if __name__ == "__main__":
    build_vault()

# https://github.com/Guilherme-alexander/CYBER-VAULT
from pathlib import Path
import os
import sys

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QLineEdit,
    QMessageBox,
    QFrame,
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QFontDatabase


# ======================================================
# fallout terminal theme
# ======================================================

# Fontes pixel nativas do Windows (sem instalar nada)
# Prioridade: Fixedsys > Terminal > Lucida Console > Courier New
PIXEL_FONTS = ["Fixedsys Excelsior 3.01", "Fixedsys", "Terminal", "Lucida Console", "Courier New"]

GREEN_BRIGHT  = "#39ff14"   # fósforo principal
GREEN_MID     = "#2ab52a"   # labels
GREEN_DIM     = "#1a7a1a"   # subtítulos / bordas
GREEN_DARK    = "#0d3a0d"   # separadores / fundo sutil
GREEN_MUTED   = "#1a5a1a"   # placeholder / status

BG_MAIN       = "#000000"   # fundo total
BG_CARD       = "#020d02"   # card interior
BG_INPUT      = "#010a01"   # input

DANGER        = "#c94f4f"   # botão lock


STYLE = f"""
QWidget {{
    background: {BG_MAIN};
    color: {GREEN_BRIGHT};
    font-size: 14pt;
    font-family: "Fixedsys Excelsior 3.01", "Fixedsys", "Terminal",
                 "Lucida Console", "Courier New", monospace;
}}

QFrame#Card {{
    background: {BG_CARD};
    border: 1px solid {GREEN_DIM};
    border-radius: 2px;
}}

QLabel#Title {{
    color: {GREEN_BRIGHT};
    font-size: 26pt;
    letter-spacing: 6px;
    font-weight: 700;
}}

QLabel#Sub {{
    color: {GREEN_DIM};
    font-size: 11pt;
    letter-spacing: 3px;
}}

QLabel#FieldLabel {{
    color: {GREEN_MID};
    font-size: 12pt;
    letter-spacing: 2px;
}}

QLabel#PathLabel {{
    color: {GREEN_DIM};
    font-size: 11pt;
    letter-spacing: 1px;
}}

QLabel#Status {{
    color: {GREEN_MUTED};
    font-size: 10pt;
    letter-spacing: 2px;
}}

QLineEdit {{
    background: {BG_INPUT};
    border: 1px solid {GREEN_DIM};
    border-radius: 2px;
    padding: 9px 11px;
    color: {GREEN_BRIGHT};
    letter-spacing: 2px;
    selection-background-color: {GREEN_DIM};
    selection-color: {GREEN_BRIGHT};
}}

QLineEdit:focus {{
    border: 1px solid {GREEN_BRIGHT};
}}

QLineEdit::placeholder {{
    color: {GREEN_MUTED};
}}

QPushButton {{
    background: {BG_INPUT};
    border: 1px solid {GREEN_BRIGHT};
    border-radius: 2px;
    padding: 12px;
    color: {GREEN_BRIGHT};
    font-size: 14pt;
    letter-spacing: 4px;
    font-weight: 600;
}}

QPushButton:hover {{
    background: {GREEN_BRIGHT};
    color: {BG_MAIN};
}}

QPushButton:pressed {{
    background: {GREEN_MID};
    color: {BG_MAIN};
}}

QPushButton#Danger {{
    border: 1px solid {DANGER};
    color: {DANGER};
}}

QPushButton#Danger:hover {{
    background: {DANGER};
    color: {BG_MAIN};
}}

QMessageBox {{
    background: {BG_MAIN};
    color: {GREEN_BRIGHT};
}}
"""


# ======================================================
# header bar (ROBCO INDUSTRIES linha + cursor piscando)
# ======================================================

class TerminalHeader(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 8)
        layout.setSpacing(4)

        robco = QLabel("ROBCO INDUSTRIES (TM) TERMLINK PROTOCOL")
        robco.setObjectName("Status")

        self.cursor = QLabel("█")
        self.cursor.setObjectName("FieldLabel")
        self.cursor.setAlignment(Qt.AlignRight)

        row = QVBoxLayout()
        row.addWidget(robco)

        layout.addLayout(row)
        layout.addWidget(self.cursor)

        self._visible = True
        timer = QTimer(self)
        timer.timeout.connect(self._blink)
        timer.start(550)

    def _blink(self):
        self._visible = not self._visible
        self.cursor.setText("█" if self._visible else " ")


# ======================================================
# login window
# ======================================================

class LoginWindow(QWidget):

    def __init__(self, on_login):
        super().__init__()
        self.on_login = on_login
        self.setWindowTitle("Cyber Vault")
        self.setFixedSize(540, 480)
        self.setStyleSheet(STYLE)
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(28, 20, 28, 20)
        root.setSpacing(0)

        root.addWidget(TerminalHeader())

        # separator
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet(f"color: {GREEN_DARK};")
        root.addWidget(sep)
        root.addSpacing(14)

        card = QFrame()
        card.setObjectName("Card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(10)

        title = QLabel("CYBER VAULT")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel(">> ENCRYPTED SECURE WORKSPACE <<")
        subtitle.setObjectName("Sub")
        subtitle.setAlignment(Qt.AlignCenter)

        user_label = QLabel("> USERNAME:")
        user_label.setObjectName("FieldLabel")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("ENTER USERNAME_")

        pass_label = QLabel("> PASSWORD:")
        pass_label.setObjectName("FieldLabel")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("••••••••_")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.returnPressed.connect(self._login_clicked)

        login_btn = QPushButton("> UNLOCK VAULT <")
        login_btn.clicked.connect(self._login_clicked)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(16)
        layout.addWidget(user_label)
        layout.addWidget(self.username_input)
        layout.addSpacing(6)
        layout.addWidget(pass_label)
        layout.addWidget(self.password_input)
        layout.addSpacing(14)
        layout.addWidget(login_btn)

        root.addStretch()
        root.addWidget(card)
        root.addStretch()

        # status bar
        status = QLabel("STATE: LOCKED  |  AES-256-GCM  |  PBKDF2 x300000")
        status.setObjectName("Status")
        status.setAlignment(Qt.AlignCenter)
        root.addWidget(status)

    def _login_clicked(self):
        self.on_login(
            self.username_input.text().strip(),
            self.password_input.text(),
        )


# ======================================================
# vault panel
# ======================================================

class VaultWindow(QWidget):

    def __init__(self, folder_path: Path, on_lock):
        super().__init__()
        self.folder_path = folder_path
        self.on_lock = on_lock
        self.setWindowTitle("Cyber Vault")
        self.setFixedSize(580, 440)
        self.setStyleSheet(STYLE)
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(28, 20, 28, 20)
        root.setSpacing(0)

        root.addWidget(TerminalHeader())

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet(f"color: {GREEN_DARK};")
        root.addWidget(sep)
        root.addSpacing(14)

        card = QFrame()
        card.setObjectName("Card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(10)

        title = QLabel("VAULT ONLINE")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignCenter)

        path_label = QLabel(f"> {self.folder_path}")
        path_label.setObjectName("PathLabel")
        path_label.setWordWrap(True)

        open_btn = QPushButton("> OPEN FOLDER")
        open_btn.clicked.connect(self._open_folder)

        lock_btn = QPushButton("> LOCK NOW  <<  DANGER")
        lock_btn.setObjectName("Danger")
        lock_btn.clicked.connect(self.on_lock)

        layout.addWidget(title)
        layout.addSpacing(6)
        layout.addWidget(path_label)
        layout.addSpacing(18)
        layout.addWidget(open_btn)
        layout.addWidget(lock_btn)

        root.addStretch()
        root.addWidget(card)
        root.addStretch()

        status = QLabel("STATE: OPEN  |  AES-256-GCM  |  PBKDF2 x300000")
        status.setObjectName("Status")
        status.setAlignment(Qt.AlignCenter)
        root.addWidget(status)

    def _open_folder(self):
        os.startfile(self.folder_path)


# ======================================================
# helpers
# ======================================================

def show_error(message: str) -> None:
    msg = QMessageBox()
    msg.setWindowTitle("Cyber Vault")
    msg.setText(message)
    msg.setStyleSheet(STYLE)
    msg.exec_()


def show_info(message: str) -> None:
    msg = QMessageBox()
    msg.setWindowTitle("Cyber Vault")
    msg.setText(message)
    msg.setStyleSheet(STYLE)
    msg.exec_()


# ======================================================
# preview
# ======================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)

    def login(u, p):
        print(u, p)

    w = LoginWindow(login)
    w.show()
    sys.exit(app.exec_())

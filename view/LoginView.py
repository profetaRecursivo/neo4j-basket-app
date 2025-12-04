import sys
from pathlib import Path

root_path = Path(__file__).parent.parent
sys.path.insert(0, str(root_path))

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from backend.services.Auth import Auth
from view.MainView import MainView


class LoginView(QWidget):
    def __init__(self):
        super().__init__()
        self.auth_service = Auth()
        self.main_view = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Basquet App TBD")
        self.setFixedSize(450, 350)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #e0e0e0;
            }
            QLineEdit {
                background-color: #2d2d2d;
                border: 2px solid #404040;
                border-radius: 8px;
                padding: 12px 15px;
                color: #e0e0e0;
                font-size: 15px;
            }
            QLineEdit:focus {
                border: 2px solid #0078d4;
                background-color: #333333;
            }
            QPushButton {
                background-color: #0078d4;
                border: none;
                border-radius: 8px;
                padding: 14px;
                color: #ffffff;
                font-size: 15px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QPushButton#exitBtn {
                background-color: #d13438;
            }
            QPushButton#exitBtn:hover {
                background-color: #b02a2e;
            }
            QPushButton#exitBtn:pressed {
                background-color: #8e2024;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # Título
        title = QLabel("Basquet App")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 28, QFont.Bold))
        title.setStyleSheet("color: #0078d4; margin-bottom: 10px; min-height: 45px;")
        layout.addWidget(title)

        subtitle = QLabel("Sistema de Gestión")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setStyleSheet("color: #8a8a8a; margin-bottom: 20px; min-height: 25px;")
        layout.addWidget(subtitle)

        layout.addSpacing(10)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuario")
        self.username_input.setMinimumHeight(45)
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(45)
        layout.addWidget(self.password_input)

        self.password_input.returnPressed.connect(self.handle_login)

        layout.addSpacing(10)

        self.login_btn = QPushButton("Acceder")
        self.login_btn.setMinimumHeight(45)
        self.login_btn.clicked.connect(self.handle_login)
        layout.addWidget(self.login_btn)

        exit_btn = QPushButton("Salir")
        exit_btn.setObjectName("exitBtn")
        exit_btn.setMinimumHeight(45)
        exit_btn.clicked.connect(self.close)
        layout.addWidget(exit_btn)

        self.setLayout(layout)

    def handle_login(self):
        self.login_btn.setEnabled(False)

        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Por favor ingrese usuario y contraseña")
            self.login_btn.setEnabled(True)
            return

        result = self.auth_service.login(username, password)

        if result["success"]:
            from backend.services.UIService import UIService

            ui_service = UIService(result["user"])
            ui_result = ui_service.get_ui_ids()

            if ui_result["success"]:
                self.main_view = MainView(
                    ui_result["ui_ids"], result["user"], result["user"]
                )
                self.main_view.show()
                self.close()
            else:
                QMessageBox.critical(
                    self, "Error", "Error al cargar interfaces disponibles"
                )
                self.login_btn.setEnabled(True)
        else:
            QMessageBox.critical(self, "Error", "Credenciales incorrectas")
            self.password_input.clear()
            self.login_btn.setEnabled(True)

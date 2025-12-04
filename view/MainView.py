import sys
from pathlib import Path

root_path = Path(__file__).parent.parent
sys.path.insert(0, str(root_path))

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from view.UIDefs import UIRegistry
from backend.services.Auth import Auth


class MainView(QWidget):
    def __init__(self, ui_ids, session_id, username):
        super().__init__()
        self.ui_ids = ui_ids
        self.session_id = session_id
        self.username = username
        self.ventanas_abiertas = []  

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Basquet App TBD")
        self.setFixedSize(550, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #e0e0e0;
            }
            QPushButton {
                border: none;
                border-radius: 10px;
                padding: 18px;
                color: #ffffff;
                font-size: 15px;
                font-weight: 600;
                text-align: center;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("Basquet App")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 32, QFont.Bold))
        title.setStyleSheet("color: #0078d4; margin: 20px 0; min-height: 50px;")
        layout.addWidget(title)

        layout.addSpacing(30)

        # Crear botones para cada UI disponible
        for ui_id in self.ui_ids:
            if ui_id in UIRegistry:
                ui_name, ui_func, ui_color = UIRegistry[ui_id]()
                btn = QPushButton(ui_name)
                btn.setFont(QFont("Segoe UI", 14))
                btn.setMinimumHeight(60)
                hover_color = self.darken_color(ui_color, 0.85)
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {ui_color};
                        color: white;
                        border: none;
                        border-radius: 8px;
                        padding: 15px;
                        text-align: center;
                        font-weight: bold;
                        min-height: 60px;
                    }}
                    QPushButton:hover {{
                        background-color: {hover_color};
                    }}
                """)
                btn.clicked.connect(
                    lambda checked=False, func=ui_func: self.abrir_ventana(func)
                )
                layout.addWidget(btn)

        layout.addStretch()

        self.setLayout(layout)

    def abrir_ventana(self, func):
        """Abre una ventana y guarda la referencia para evitar que se destruya"""
        ventana = func()
        if ventana:  
            self.ventanas_abiertas.append(ventana)

    def darken_color(self, color, factor=0.8):
        """Oscurece un color hex para el hover"""
        color = color.lstrip("#")
        rgb = tuple(int(color[i : i + 2], 16) for i in (0, 2, 4))
        darker = tuple(int(c * factor) for c in rgb)
        return f"#{darker[0]:02x}{darker[1]:02x}{darker[2]:02x}"

    def closeEvent(self, event):
        """Cierra la sesión al cerrar la ventana"""
        auth = Auth()
        auth.logout(self.username)
        event.accept()

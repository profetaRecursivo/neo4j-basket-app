import sys
from pathlib import Path
import re

root_path = Path(__file__).parent.parent
sys.path.insert(0, str(root_path))

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QDateEdit,
    QMessageBox,
    QFormLayout,
    QGroupBox,
    QCheckBox,
    QDoubleSpinBox,
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from backend.database.DBManager import DBManager
import backend.services.AtletaService as AtletaService


class RegistrarAtletasView(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DBManager()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Registro de Atleta")
        self.setGeometry(100, 100, 600, 750)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #e0e0e0;
            }
            QLineEdit, QComboBox, QDateEdit {
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-radius: 5px;
                padding: 10px;
                color: #e0e0e0;
                min-height: 25px;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
                border: 2px solid #28a745;
            }
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 12px 25px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QGroupBox {
                border: 2px solid #3d3d3d;
                border-radius: 8px;
                margin-top: 20px;
                font-weight: bold;
                padding-top: 15px;
            }
            QGroupBox::title {
                color: #28a745;
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
            }
            QCheckBox {
                color: #e0e0e0;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(40, 30, 40, 30)

        title = QLabel("🏀 Registro de Nuevo Atleta")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setStyleSheet("color: #28a745;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        group_personal = QGroupBox("📋 Datos Personales")
        form_personal = QFormLayout()
        form_personal.setSpacing(12)

        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Ej: Juan Carlos")
        form_personal.addRow("Nombres:", self.input_nombre)

        self.input_apellido = QLineEdit()
        self.input_apellido.setPlaceholderText("Ej: Pérez García")
        form_personal.addRow("Apellidos:", self.input_apellido)

        self.input_fecha_nac = QDateEdit()
        self.input_fecha_nac.setCalendarPopup(True)
        self.input_fecha_nac.setDisplayFormat("dd/MM/yyyy")

        max_date = QDate.currentDate().addYears(-10)
        min_date = QDate.currentDate().addYears(-100)
        self.input_fecha_nac.setDateRange(min_date, max_date)
        self.input_fecha_nac.setDate(max_date)
        form_personal.addRow("Fecha de Nacimiento:", self.input_fecha_nac)

        self.combo_sexo = QComboBox()
        self.combo_sexo.addItem("Masculino", "M")
        self.combo_sexo.addItem("Femenino", "F")
        form_personal.addRow("Sexo:", self.combo_sexo)

        self.combo_pais = QComboBox()
        form_personal.addRow("País:", self.combo_pais)

        group_personal.setLayout(form_personal)
        layout.addWidget(group_personal)

        group_deportivo = QGroupBox("⚡ Datos Deportivos")
        form_deportivo = QFormLayout()
        form_deportivo.setSpacing(12)

        self.input_altura = QDoubleSpinBox()
        self.input_altura.setRange(0.50, 2.50)
        self.input_altura.setSingleStep(0.01)
        self.input_altura.setDecimals(2)
        self.input_altura.setSuffix(" m")
        self.input_altura.setValue(1.75)
        form_deportivo.addRow("Altura:", self.input_altura)

        self.input_peso = QDoubleSpinBox()
        self.input_peso.setRange(30.0, 200.0)
        self.input_peso.setSingleStep(0.5)
        self.input_peso.setDecimals(2)
        self.input_peso.setSuffix(" kg")
        self.input_peso.setValue(70.0)
        form_deportivo.addRow("Peso:", self.input_peso)

        self.check_generar_usuario = QCheckBox(
            "El usuario y contraseña serán generados automáticamente"
        )
        self.check_generar_usuario.setChecked(True)
        self.check_generar_usuario.setStyleSheet("color: #64b5f6; margin-top: 10px;")
        form_deportivo.addRow("", self.check_generar_usuario)

        group_deportivo.setLayout(form_deportivo)
        layout.addWidget(group_deportivo)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.clicked.connect(self.close)
        btn_cancelar.setStyleSheet("background-color: #dc3545;")
        btn_layout.addWidget(btn_cancelar)

        btn_guardar = QPushButton("Guardar Atleta")
        btn_guardar.clicked.connect(self.guardar_atleta)
        btn_layout.addWidget(btn_guardar)

        layout.addLayout(btn_layout)
        layout.addStretch()

        self.setLayout(layout)
        self.cargar_paises()

    def cargar_paises(self):
        from backend.services.PaisService import PaisService
        return PaisService().get_all_countries()

    def guardar_atleta(self):
        if not self.validar_formulario():
            return

        fecha = self.input_fecha_nac.date().toPyDate().strftime("%Y-%m-%d")

        resultado = AtletaService.create_atleta(
            nombres=self.input_nombre.text(),
            apellidos=self.input_apellido.text(),
            fecha_nacimiento=fecha,
            sexo=self.combo_sexo.currentData(),
            id_pais=self.combo_pais.currentData(),
            altura=self.input_altura.value(),
            peso_kg=self.input_peso.value(),
        )

        if resultado["success"]:
            QMessageBox.information(
                self,
                "✅ Éxito",
                "Atleta registrado correctamente",
            )
            self.limpiar_formulario()
        else:
            QMessageBox.critical(
                self, "❌ Error", f"Error al registrar:\n{resultado['error']}"
            )

    def validar_formulario(self):
        nombre = self.input_nombre.text().strip()
        if not nombre:
            QMessageBox.warning(self, "⚠️ Validación", "El nombre es requerido")
            self.input_nombre.setFocus()
            return False

        if len(nombre) < 2:
            QMessageBox.warning(
                self, "⚠️ Validación", "El nombre debe tener al menos 2 caracteres"
            )
            self.input_nombre.setFocus()
            return False

        name_regex = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$")
        if not name_regex.match(nombre):
            QMessageBox.warning(
                self, "⚠️ Validación", "El nombre solo puede contener letras y espacios"
            )
            self.input_nombre.setFocus()
            return False

        apellido = self.input_apellido.text().strip()
        if not apellido:
            QMessageBox.warning(self, "⚠️ Validación", "El apellido es requerido")
            self.input_apellido.setFocus()
            return False

        if len(apellido) < 2:
            QMessageBox.warning(
                self, "⚠️ Validación", "El apellido debe tener al menos 2 caracteres"
            )
            self.input_apellido.setFocus()
            return False

        if not name_regex.match(apellido):
            QMessageBox.warning(
                self,
                "⚠️ Validación",
                "El apellido solo puede contener letras y espacios",
            )
            self.input_apellido.setFocus()
            return False

        if self.combo_pais.currentIndex() == 0 or self.combo_pais.currentData() is None:
            QMessageBox.warning(self, "⚠️ Validación", "Debe seleccionar un país")
            self.combo_pais.setFocus()
            return False

        return True

    def limpiar_formulario(self):
        self.input_nombre.clear()
        self.input_apellido.clear()
        self.input_altura.setValue(1.75)
        self.input_peso.setValue(70.0)
        self.input_fecha_nac.setDate(QDate.currentDate().addYears(-10))
        self.combo_sexo.setCurrentIndex(0)
        self.combo_pais.setCurrentIndex(0)

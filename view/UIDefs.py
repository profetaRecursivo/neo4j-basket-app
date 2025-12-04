from PyQt5.QtWidgets import QMessageBox
from view.RegistrarAtletasView import RegistrarAtletasView


def abrir_dashboard_individual():
    QMessageBox.information(
        None, "En desarrollo", "Dashboard Individual - En desarrollo"
    )


def abrir_dashboard_equipo():
    QMessageBox.information(
        None, "En desarrollo", "Dashboard por Equipo - En desarrollo"
    )


def abrir_registrar_atletas():
    ventana = RegistrarAtletasView()
    ventana.show()
    return ventana


def abrir_registrar_entrenadores():
    QMessageBox.information(
        None, "En desarrollo", "Registrar Entrenadores - En desarrollo"
    )


UIRegistry = {
    "dashboard_individual": lambda: ("📊 Dashboard Individual", abrir_dashboard_individual, "#4CAF50"),
    "dashboard_por_equipo": lambda: ("👥 Dashboard por Equipo", abrir_dashboard_equipo, "#2196F3"),
    "registrar_atleta": lambda: ("⚡ Registrar Atletas", abrir_registrar_atletas, "#FF9800"),
    "registrar_entrenadores": lambda: ("🏀 Registrar Entrenadores", abrir_registrar_entrenadores, "#9C27B0"),
}
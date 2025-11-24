import sys
from pathlib import Path

root_path = Path(__file__).parent.parent
sys.path.insert(0, str(root_path))

from PyQt5.QtWidgets import QApplication
from view.LoginView import LoginView


def main():
    app = QApplication(sys.argv)
    login = LoginView()
    login.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

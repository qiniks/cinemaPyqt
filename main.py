import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow
from res.styles import APP_STYLE

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLE)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

from PyQt6.QtWidgets import QMainWindow, QApplication
from paginaPrincipal import Ui_MainWindow
import sys

# Ficheiro main que serve para arrancar com aplicação

class LuxuryWheelsApp (QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()



app = QApplication(sys.argv)
Luxury = LuxuryWheelsApp()
sys.exit(app.exec())
from Frontend.src.menu import MainWindowQ
from PyQt5.QtWidgets import QApplication
from back.backend import FilterSpace

if __name__ == '__main__':


    app = QApplication([])
    window = MainWindowQ()
    window.show()

    app.exec()



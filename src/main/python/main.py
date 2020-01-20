from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QFileDialog, QMessageBox

from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtGui import QPixmap,  QFont
import sys
import os
import logging

# Set logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.disable(logging.DEBUG)

Form, Window = uic.loadUi("main_window.ui")


def main():
    app = QApplication([])
    window = Window()
    form = Form()
    form.setupUi(window)
    window.resize(640, 480)
    window.setWindowTitle('Windows Domain Settings')
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

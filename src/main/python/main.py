from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QFileDialog, QMessageBox, QDialog

from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QPixmap,  QFont
import sys
import os
import logging
import platform
import webbrowser
import urllib3
import subprocess

current_version = float(1.0)

try:
    os.chdir(os.path.dirname(sys.argv[0]))
except Exception:
    pass


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.environ.get("_MEIPASS2", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


# Set logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.disable(logging.DEBUG)

# What OS is running
what_os = platform.system()
if 'Windows' in what_os:
    username = os.environ.get('USERNAME')
    start_location = 'c:\\Users\\{}\\Documents'.format(username)
    logging.info('OS: Windows')
elif 'Linux' in what_os:
    username = os.environ.get('USER')
    start_location = '/home/{}/Documents'.format(username)
    logging.info('OS: Linux')
elif 'Darwin' in what_os:
    username = os.environ.get('USER')
    start_location = '/Users/{}/Documents'.format(username)
    logging.info('OS: MacOS')
else:
    exit()


# PyQT GUI
class MainPage(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Load Main UI
        loadUi(resource_path('../resources/ui/main_window.ui'), self)
        # Set Size Application
        self.setFixedSize(500, 640)
        # Set Application Icon
        self.setWindowIcon(QtGui.QIcon(resource_path('../icons/logo.png')))
        self.setWindowTitle('Windows Domain Settings')
        # Logo
        # label_logo
        # self.label_logo = QLabel(self)
        # self.label_logo.setGeometry(50, 40, 50, 50)
        # pixmap = QPixmap(resource_path('../icons/logo.png'))
        # pixmap = pixmap.scaledToWidth(50)
        # self.label_logo.setPixmap(pixmap)

        # Info menu
        self.actionInfo.triggered.connect(self.open_info_window)

        # Initial update check
        self.check_update()

        # Update button
        self.actionUpdate.triggered.connect(self.website_update)

        # Check workgroup or domain
        self.check_workgroup = subprocess.check_output(['powershell.exe',
                                                 '(Get-WmiObject -Class Win32_ComputerSystem).Workgroup'])

        # Get-WmiObject -Class Win32_ComputerSystem - Complete check
        # (Get-WmiObject -Class Win32_ComputerSystem).Workgroup - Workgroup of niet
        # (Get-WmiObject -Class Win32_ComputerSystem).PartOfDomain - Boolean domain of niet

        if self.check_workgroup:
            self.domainLineEdit.setPlaceholderText(str(self.check_workgroup, encoding="utf-8"))
        # logging.info(type(self.domain_or_workgroup))
        logging.info('Computer in domain: ' + str(self.check_workgroup, encoding="utf-8"))

    def website_update(self):
        webbrowser.open('https://github.com/jebr/WindowsDomainSettings/releases')

    def check_update(self):
        # Version check
        try:
            timeout = urllib3.Timeout(connect=2.0, read=7.0)
            http = urllib3.PoolManager(timeout=timeout)
            response = http.request('GET',
                                    'https://raw.githubusercontent.com/jebr/WindowsDomainSettings/master/version.txt')
            data = response.data.decode('utf-8')

            new_version = float(data)

            if current_version < new_version:
                logging.info('Current software version: v{}'.format(current_version))
                logging.info('New software version available v{}'.format(new_version))
                logging.info('https://github.com/jebr/WindowsDomainSettings/releases')
                self.infobox_update('There is an update available\n Do you want to download it now?')
                self.statusBar().showMessage('New software version available v' + str(new_version))
                self.actionUpdate.setEnabled(True)
            else:
                logging.info('Current software version: v{}'.format(current_version))
                logging.info('Latest release: v{}'.format(new_version))
                logging.info('Software up-to-date')
                self.statusBar().showMessage('Windows Domain Settings version v' + str(new_version))
                self.actionUpdate.setEnabled(False)

        except urllib3.exceptions.MaxRetryError:
            logging.error('No internet connection, max retry error')
        except urllib3.exceptions.ResponseError:
            logging.error('No internet connection, no response error')

    def open_info_window(self):
        info_window_ = InfoWindow()
        info_window_.exec_()

    # Messageboxen
    def criticalbox(self, message):
        buttonReply = QMessageBox.critical(self, 'Error', message, QMessageBox.Close)

    def warningbox(self, message):
        buttonReply = QMessageBox.warning(self, 'Warning', message, QMessageBox.Close)

    def infobox(self, message):
        buttonReply = QMessageBox.information(self, 'Info', message, QMessageBox.Close)

    def infobox_update(self, message):
        buttonReply = QMessageBox.information(self, 'Info', message, QMessageBox.Yes, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            webbrowser.open('https://github.com/jebr/WindowsDomainSettings/releases')


class InfoWindow(QDialog):
    def __init__(self):
        super().__init__(None, QtCore.Qt.WindowCloseButtonHint)
        loadUi(resource_path('../resources/ui/info_dialog.ui'), self)
        self.setWindowIcon(QtGui.QIcon(resource_path('../icons/logo.png')))
        self.setFixedSize(320, 240)
        self.setWindowTitle('Windows Domain Settings')
        # Logo
        self.label_info_logo.setText("")
        self.label_info_logo = QLabel(self)
        info_icon = QPixmap(resource_path('../icons/logo.png'))
        info_icon = info_icon.scaledToWidth(40)
        self.label_info_logo.setPixmap(info_icon)
        # TODO Nakijken of dit nog nodig is na het nieuwe onwerp
        if 'Darwin' in what_os:
            self.label_info_logo.move(70, 20)
        else:
            self.label_info_logo.move(50, 25)
        # Labels
        self.label_info_title.setText('WDS v{}'.format(current_version))
        self.label_info_copyright.setText('Copyright {} {} 2020'.format('©', ' <a href="https://switchit.nu">SwitchIT</a'))
        self.label_info_copyright.setOpenExternalLinks(True)
        self.label_info_link.setText('<a href="https://github.com/jebr/WindowsDomainSettings">GitHub repository</a>')
        self.label_info_link.setOpenExternalLinks(True)
        self.label_info_dev.setText('Developers\nJeroen Brauns')


def main():
    app = QApplication(sys.argv)
    window = MainPage()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

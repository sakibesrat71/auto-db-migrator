import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, QCheckBox, QHBoxLayout
from ui_elems.ChangeLogWindow import ChangeLogWindow
from ui_elems.DbConnectorWindow import DbConnectorWindow
class MotherWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):  
        self.setWindowTitle('Mother Window')
        self.setGeometry(100, 100, 600, 400)

        # Set the central widget to InputForm initially
        self.input_form = DbConnectorWindow(self)
        # self.changelog_window = ChangeLogWindow(self)
        self.setCentralWidget(self.input_form)

        self.show()

    def show_changelog_window(self,current_xml):
        # Change the central widget to ChangeLogWindow
        
        self.changelog_window = ChangeLogWindow(self)
        self.input_form.liquibaseInitiatorCreated.connect(self.changelog_window.receive_liquibase_initiator)
        self.changelog_window.current_xml = current_xml
        self.changelog_window.initUI()
        self.setCentralWidget(self.changelog_window)
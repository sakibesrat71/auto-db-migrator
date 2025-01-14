import sys
from ui_elems.ChangeLogWindow import ChangeLogWindow
from ui_elems.EntryPointUI import MotherWindow
from ui_elems.DbConnectorWindow import DbConnectorWindow
from PyQt5.QtWidgets import QApplication
from logics.PrevDbStateChanger import PrevDbStateChanger
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MotherWindow()
    sys.exit(app.exec_())
    
         

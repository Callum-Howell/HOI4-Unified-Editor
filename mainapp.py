from PySide2 import QtCore, QtWidgets, QtGui


#

class ModFile:
    def __init__(self):
        self.directory = ""
        self.event_files_list = []
        self.ideology_list = []
        self.loc_files_list = []

    @staticmethod
    def blank_gen():
        pass

    @staticmethod
    def import_gen():
        pass

# Main Loop

main_app = QtWidgets.QApplication([])
label = QtWidgets.QLabel('Hello World!')
label.show()
main_app.exec_()
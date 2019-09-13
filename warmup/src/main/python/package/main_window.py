from PySide2 import QtWidgets, QtGui, QtCore

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Application de base")

        self.setup_ui()

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        self.button = QtWidgets.QPushButton("Clique!")

    def modify_widgets(self):
        pass

    def create_layouts(self):
        self.main_layout = QtWidgets.QHBoxLayout(self)

    def add_widgets_to_layouts(self):
        self.main_layout.addWidget(self.button)

    def setup_connections(self):
        self.button.clicked.connect(self.bouton_clicked)

    def bouton_clicked(self):
        message_box = QtWidgets.QMessageBox()
        message_box.setWindowTitle("Bravo")
        message_box.setText("Tu as réussi ta première application!")
        message_box.exec_()
    
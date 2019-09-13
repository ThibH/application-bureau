from PySide2 import QtWidgets, QtGui, QtCore
from pprint import pprint


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Explorateur de fichiers")
        self.setup_ui()
        self.populate()
        self.tree_view.setAlternatingRowColors(True)
        self.tree_view.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.tree_view.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

    def setup_ui(self):
        self.create_widgets()
        self.add_actions_to_toolbar()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        self.toolbar = QtWidgets.QToolBar()
        self.main_widget = QtWidgets.QWidget()
        self.tree_view = QtWidgets.QTreeView()
        self.list_view = QtWidgets.QListView()
        self.path = "/"
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath((QtCore.QDir.rootPath()))

    def add_actions_to_toolbar(self):
        self.toolbar.addAction(QtGui.QIcon("/Users/thibh/Documents/repositories/pipeline/shed_ui/img/home2.png"), "Open In Explorer")

    def modify_widgets(self):
        self.list_view.setViewMode(QtWidgets.QListView.IconMode)
        self.list_view.setUniformItemSizes(True)

    def create_layouts(self):
        self.main_layout = QtWidgets.QHBoxLayout(self.main_widget)

    def add_widgets_to_layouts(self):
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)
        self.setCentralWidget(self.main_widget)
        self.main_layout.addWidget(self.tree_view)
        self.main_layout.addWidget(self.list_view)

    def setup_connections(self):
        self.tree_view.clicked.connect(self.treeview_clicked)
        self.list_view.doubleClicked.connect(self.list_view_double_clicked)
        self.list_view.clicked.connect(self.list_view_clicked)
        self.list_view.doubleClicked.connect(self.list_view_double_clicked)

    def populate(self):
        self.tree_view.setModel(self.model)
        self.list_view.setModel(self.model)
        self.list_view.setRootIndex(self.model.index(self.path))
        self.tree_view.setRootIndex(self.model.index(self.path))
        self.tree_view.setSortingEnabled(True)

    def treeview_clicked(self, index):
        index_item = self.model.index(index.row(), 0, index.parent())
        if self.model.isDir(index_item):

            filename = self.model.fileName(index_item)
            filepath = self.model.filePath(index_item)

            self.list_view.setRootIndex(self.model.index(filepath))

        else:
            filename_parent = self.model.filePath(index_item.parent())
            self.list_view.setRootIndex(self.model.index(filename_parent))

    def list_view_double_clicked(self, index):
        index_item = self.model.index(index.row(), 0, index.parent())
        filepath = self.model.filePath(index_item)
        self.list_view.setRootIndex(self.model.index(filepath))
        
    def list_view_clicked(self, index):
        self.tree_view.selectionModel().setCurrentIndex(index, QtCore.QItemSelectionModel.ClearAndSelect)
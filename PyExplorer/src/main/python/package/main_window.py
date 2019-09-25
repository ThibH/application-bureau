from pprint import pprint
import os
from functools import partial

from PySide2 import QtWidgets, QtGui, QtCore


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, ctx):
        super().__init__()

        self.ctx = ctx
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
        self.sld_iconSize = QtWidgets.QSlider()

    def add_actions_to_toolbar(self):
        self.actions = {}
        actions = ["home", "desktop", "documents", "movies", "pictures", "music"]
        standard_path = QtCore.QStandardPaths()
        for action in actions:
            path = eval(f"standard_path.standardLocations(QtCore.QStandardPaths.{action.capitalize()}Location)[0]")
            icon = self.ctx.get_resource(f"{action}.svg")
            self.actions[action] = self.toolbar.addAction(QtGui.QIcon(icon), action.capitalize())
            self.actions[action].triggered.connect(partial(self.change_location, path))

    def modify_widgets(self):
        css_file = self.ctx.get_resource("style.css")
        with open(css_file, "r") as f:
            self.setStyleSheet(f.read())
        self.list_view.setViewMode(QtWidgets.QListView.IconMode)
        self.list_view.setUniformItemSizes(True)
        self.tree_view.setSortingEnabled(True)
        self.list_view.setIconSize(QtCore.QSize(48, 48))
        self.sld_iconSize.setValue(48)
        self.sld_iconSize.setRange(48, 256)

    def create_layouts(self):
        self.main_layout = QtWidgets.QHBoxLayout(self.main_widget)

    def add_widgets_to_layouts(self):
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)
        self.setCentralWidget(self.main_widget)
        self.main_layout.addWidget(self.tree_view)
        self.main_layout.addWidget(self.list_view)
        self.main_layout.addWidget(self.sld_iconSize)

    def setup_connections(self):
        self.tree_view.clicked.connect(self.treeview_clicked)
        self.list_view.doubleClicked.connect(self.list_view_double_clicked)
        self.list_view.clicked.connect(self.list_view_clicked)
        self.list_view.doubleClicked.connect(self.list_view_double_clicked)
        self.sld_iconSize.valueChanged.connect(self.change_icon_size)

    def change_icon_size(self, value):
        self.list_view.setIconSize(QtCore.QSize(value, value))

    def change_location(self, path):
        self.tree_view.setRootIndex(self.model.index(path))
        self.list_view.setRootIndex(self.model.index(path))

    def populate(self):
        self.tree_view.setModel(self.model)
        self.list_view.setModel(self.model)
        self.list_view.setRootIndex(self.model.index(self.path))
        self.tree_view.setRootIndex(self.model.index(self.path))

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
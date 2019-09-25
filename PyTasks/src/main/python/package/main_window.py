import platform

from PySide2 import QtWidgets, QtGui, QtCore

import package.api.task

COLORS = {False: (235, 64, 52), True: (160, 237, 83)}


class TaskItem(QtWidgets.QListWidgetItem):
    def __init__(self, text, done, list_widget):
        super().__init__(text)

        self.list_widget = list_widget
        self.done = done
        self.text = text
        self.setSizeHint(QtCore.QSize(self.sizeHint().width(), 50))
        self.set_background_color()
        self.list_widget.addItem(self)
        
    def toggle_state(self):
        self.done = not self.done
        self.set_background_color()
        package.api.task.set_task_status(content=self.text, done=self.done)

    def set_background_color(self):
        color = COLORS.get(self.done)
        self.setBackgroundColor(QtGui.QColor(*color))
        style_sheet = "QListView::item:selected {background: rgb("
        style_sheet += f"{color[0]}, {color[1]}, {color[2]});"
        style_sheet += "color: rgb(0, 0, 0);"
        style_sheet += "}"
        self.list_widget.setStyleSheet(style_sheet)


class MainWindow(QtWidgets.QWidget):
    def __init__(self, ctx):
        super().__init__()

        self.width = 250
        self.height = 0
        self.ctx = ctx
        self.setup_ui()
        self.populate_tasks()

    def setup_ui(self):
        self.create_widgets()
        self.create_layouts()
        self.modify_widgets()
        self.add_widgets_to_layouts()
        self.setup_connections()
        self.setup_tray()

    def setup_tray(self):
        self.tray = QtWidgets.QSystemTrayIcon()

        icon = QtGui.QIcon(self.ctx.get_resource("icon.png"))

        self.tray.setIcon(icon)
        self.tray.setVisible(True)

        self.tray.activated.connect(self.tray_icon_click)

    def create_widgets(self):
        self.lw_tasks = QtWidgets.QListWidget()
        self.frm_options = QtWidgets.QFrame()
        self.btn_add = QtWidgets.QPushButton()
        self.btn_clean = QtWidgets.QPushButton()
        self.btn_quit = QtWidgets.QPushButton()

    def modify_widgets(self):
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self.setStyleSheet("border: none;")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        
        self.lw_tasks.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.lw_tasks.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.btn_add.setIcon(QtGui.QIcon(self.ctx.get_resource("add.svg")))
        self.btn_clean.setIcon(QtGui.QIcon(self.ctx.get_resource("clean.svg")))
        self.btn_quit.setIcon(QtGui.QIcon(self.ctx.get_resource("close.svg")))

    def create_layouts(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.frm_options_layout = QtWidgets.QHBoxLayout(self.frm_options)

    def add_widgets_to_layouts(self):
        self.main_layout.addWidget(self.lw_tasks)
        self.main_layout.addWidget(self.frm_options)
        self.frm_options_layout.addWidget(self.btn_add)
        self.frm_options_layout.addStretch()
        self.frm_options_layout.addWidget(self.btn_clean)
        self.frm_options_layout.addWidget(self.btn_quit)

    def setup_connections(self):
        self.btn_add.clicked.connect(self.add_task)
        self.btn_clean.clicked.connect(self.clean_tasks)
        self.btn_quit.clicked.connect(self.close)
        self.lw_tasks.itemClicked.connect(lambda task_item: task_item.toggle_state())

    def add_task(self):
        text, ok = QtWidgets.QInputDialog.getText(self, "Ajouter une tâche", "Contenu de la tâche :")
        if ok:
            package.api.task.add_task(content=text)
            self.populate_tasks()

        self.center_under_tray()
        self.do_animation()

    def center_under_tray(self):
        tray_x, tray_y, _, _ = self.tray.geometry().getCoords()
        if platform.system() == "Windows":
            self.move(tray_x - (self.width / 2), min(tray_y - 200, tray_y - self.get_height()))
        else:
            self.move(tray_x - (self.width / 2), tray_y + 25)

    def clean_tasks(self):
        for i in range(self.lw_tasks.count()):
            lw_item = self.lw_tasks.item(i)
            if lw_item.done:
                package.api.task.remove_task(lw_item.text)

        self.populate_tasks()
        self.center_under_tray()
        self.do_animation()

    def do_animation(self):
        self.anim = QtCore.QPropertyAnimation(self, b"size")
        self.anim.setDuration(250)
        self.anim.setEasingCurve(QtCore.QEasingCurve.InOutBack)
        self.anim.setStartValue(QtCore.QSize(self.width, self.height))
        self.anim.setEndValue(QtCore.QSize(self.width, self.get_height()))
        self.anim.start()

    def get_height(self):
        self.height = (self.lw_tasks.count() + 2) * 50
        return self.height

    def populate_tasks(self):
        self.lw_tasks.clear()
        tasks = package.api.task.get_tasks()
        for task, done in tasks.items():
            TaskItem(text=task, done=done, list_widget=self.lw_tasks)

    def tray_icon_click(self):
        self.center_under_tray()
        self.do_animation()

        if self.isHidden():
            self.showNormal()
            self.activateWindow()
        else:
            self.hide()

from PySide2 import QtWidgets, QtGui, QtCore

COLORS = {"todo": (235, 64, 52), "done": (160, 237, 83)}

class TaskItem(QtWidgets.QListWidgetItem):
    def __init__(self, text, done, list_widget):
        super().__init__(text)

        self.list_widget = list_widget
        self.done = done
        self.setSizeHint(QtCore.QSize(self.sizeHint().width(), 50))
        self.set_background_color()
        
    def toggle_state(self):
        self.done = not self.done
        self.set_background_color()

    def set_background_color(self):
        color = COLORS.get("done" if self.done else "todo")
        self.setBackgroundColor(QtGui.QColor(*color))
        style_sheet = "QListView::item:selected {background: rgb("
        style_sheet += f"{color[0]}, {color[1]}, {color[2]});"
        style_sheet += "color: rgb(0, 0, 0);"
        style_sheet += "}"
        self.list_widget.setStyleSheet(style_sheet)

class MainWindow(QtWidgets.QWidget):
    def __init__(self, ctx):
        super().__init__()

        self.ctx = ctx

        self.setup_ui()
        
        lw_item = TaskItem(text="Finir tuto Python", done=True, list_widget=self.lw_tasks)
        lw_item2 = TaskItem(text="Acheter valise", done=False, list_widget=self.lw_tasks)
        lw_item3 = TaskItem(text="Aller au Apple Store", done=False, list_widget=self.lw_tasks)
        self.lw_tasks.addItem(lw_item)
        self.lw_tasks.addItem(lw_item2)
        self.lw_tasks.addItem(lw_item3)

        self.tray_icon_click()

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

    def get_height(self):
        tasks = self.lw_tasks.count()
        height = (tasks + 2) * 50
        return height

    def create_widgets(self):
        self.lw_tasks = QtWidgets.QListWidget()
        self.frm_options = QtWidgets.QFrame()
        self.btn_quit = QtWidgets.QPushButton()

    def modify_widgets(self):
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.setStyleSheet("border: none;")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.lw_tasks.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.lw_tasks.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.btn_quit.setIcon(QtGui.QIcon(self.ctx.get_resource("close.svg")))

    def create_layouts(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.frm_options_layout = QtWidgets.QHBoxLayout(self.frm_options)

    def add_widgets_to_layouts(self):
        self.main_layout.addWidget(self.lw_tasks)
        self.main_layout.addWidget(self.frm_options)
        self.frm_options_layout.addWidget(self.btn_quit, QtCore.Qt.AlignRight, QtCore.Qt.AlignRight)

    def setup_connections(self):
        self.btn_quit.clicked.connect(self.close)
        self.lw_tasks.itemClicked.connect(self.task_clicked)

    def center_under_tray(self):
        tray_x, tray_y, _, _ = self.tray.geometry().getCoords()
        self.move(tray_x - 100, tray_y + 25)
        
    def task_clicked(self, task_item):
        task_item.toggle_state()

    def tray_icon_click(self):

        # Calculate position
        self.center_under_tray()
        self.do_animation()

        if self.isHidden():
            # Show GUI and bring to focus
            self.showNormal()
            # self.raise_()
            self.activateWindow()
        else:
            self.hide()

    def do_animation(self):
        self.anim = QtCore.QPropertyAnimation(self, b"size")
        self.anim.setDuration(250)
        self.anim.setEasingCurve(QtCore.QEasingCurve.InOutBack)
        self.anim.setStartValue(QtCore.QSize(250, 0))
        self.anim.setEndValue(QtCore.QSize(250, self.get_height()))
        self.anim.start()

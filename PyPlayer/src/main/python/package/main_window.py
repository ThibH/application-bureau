from functools import partial

from PySide2 import QtWidgets, QtCore, QtMultimedia, QtMultimediaWidgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.open_icon = self.style().standardIcon(QtWidgets.QStyle.SP_DriveDVDIcon)
        self.play_icon = self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay)
        self.previous_icon = self.style().standardIcon(QtWidgets.QStyle.SP_MediaSkipBackward)
        self.pause_icon = self.style().standardIcon(QtWidgets.QStyle.SP_MediaPause)
        self.stop_icon = self.style().standardIcon(QtWidgets.QStyle.SP_MediaStop)
        self.setup_ui()
        self.update_buttons(self.player.state())

    def setup_ui(self):
        self.create_widgets()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        self.video_widget = QtMultimediaWidgets.QVideoWidget()
        self.player = QtMultimedia.QMediaPlayer()
        self.toolbar = QtWidgets.QToolBar()
        self.file_menu = self.menuBar().addMenu("&File")

        # ACTIONS
        self.act_open = self.file_menu.addAction(self.open_icon, "Open")
        self.act_open.setShortcut("Ctrl+O")
        self.act_play = self.toolbar.addAction(self.play_icon, "Play")
        self.act_previous = self.toolbar.addAction(self.previous_icon, "Previous")
        self.act_pause = self.toolbar.addAction(self.pause_icon, "Pause")
        self.act_stop = self.toolbar.addAction(self.stop_icon, "Stop")
    
    def add_widgets_to_layouts(self):
        self.addToolBar(self.toolbar)
        self.setCentralWidget(self.video_widget)
        self.player.setVideoOutput(self.video_widget)

    def setup_connections(self):
        self.player.stateChanged.connect(self.update_buttons)
        self.act_open.triggered.connect(self.open)
        self.act_play.triggered.connect(self.play)
        self.act_previous.triggered.connect(partial(self.player.setPosition, 0))
        self.act_pause.triggered.connect(self.player.pause)
        self.act_stop.triggered.connect(self.player.stop)

    def play(self):
        self.player.play()
        self.video_widget.resize(QtCore.QSize(1, 1))

    def open(self):
        file_dialog = QtWidgets.QFileDialog(self)
        supportedMimeTypes = ["video/mp4", "*.*"]
        file_dialog.setMimeTypeFilters(supportedMimeTypes)
        movies_dir = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.MoviesLocation)
        file_dialog.setDirectory(movies_dir)
        if file_dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.player.setMedia(file_dialog.selectedUrls()[0])
            self.player.play()

    def update_buttons(self, state):
        self.act_play.setEnabled(state != QtMultimedia.QMediaPlayer.PlayingState)
        self.act_pause.setEnabled(state == QtMultimedia.QMediaPlayer.PlayingState)
        self.act_stop.setEnabled(state != QtMultimedia.QMediaPlayer.StoppedState)
        self.act_previous.setEnabled(self.player.position() > 0)
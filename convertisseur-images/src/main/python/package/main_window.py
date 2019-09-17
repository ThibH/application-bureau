from PySide2 import QtWidgets, QtGui, QtCore

from package.image import CustomImage

class ConvertImageThread(QtCore.QThread):
    image_converted = QtCore.Signal(object, bool)

    def __init__(self, images_to_convert, quality, size, folder):
        QtCore.QThread.__init__(self)
        self.images_to_convert = images_to_convert
        self.quality = quality
        self.size = size
        self.folder = folder

    def run(self):
        for image_lw_item in self.images_to_convert:
            image = CustomImage(path=image_lw_item.text(), folder=self.folder)
            success = image.reduce_image(size=self.size, quality=self.quality)
            self.image_converted.emit(image_lw_item, success)
      


class MainWindow(QtWidgets.QWidget):
    def __init__(self, ctx):
        super().__init__()

        self.ctx = ctx
        self.setWindowTitle("Convertisseur d'images")
        self.setup_ui()

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        self.lbl_quality = QtWidgets.QLabel("Qualité:")
        self.spn_quality = QtWidgets.QSpinBox()
        self.lbl_size = QtWidgets.QLabel("Taille:")
        self.spn_size = QtWidgets.QSpinBox()
        self.lbl_dossierOut = QtWidgets.QLabel("Dossier de sortie:")
        self.le_dossierOut = QtWidgets.QLineEdit()
        self.lw_files = QtWidgets.QListWidget()
        self.btn_convert = QtWidgets.QPushButton("Conversion")
        self.lbl_dropInfo = QtWidgets.QLabel("^ Déposez les images sur l'interface")

    def modify_widgets(self):
        self.spn_quality.setRange(1, 100)
        self.spn_quality.setValue(75)
        self.spn_size.setRange(1, 100)
        self.spn_size.setValue(50)
        self.le_dossierOut.setPlaceholderText("Dossier de sortie...")
        self.le_dossierOut.setText("reduced")
        self.setAcceptDrops(True)
        self.lw_files.setAlternatingRowColors(True)
        self.lw_files.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)
        self.lbl_dropInfo.setVisible(False)

    def create_layouts(self):
        self.main_layout = QtWidgets.QGridLayout(self)

    def add_widgets_to_layouts(self):
        self.main_layout.addWidget(self.lbl_quality, 0, 0, 1, 1)
        self.main_layout.addWidget(self.spn_quality, 0, 1, 1, 1)
        self.main_layout.addWidget(self.lbl_size, 1, 0, 1, 1)
        self.main_layout.addWidget(self.spn_size, 1, 1, 1, 1)
        self.main_layout.addWidget(self.lbl_dossierOut, 2, 0, 1, 1)
        self.main_layout.addWidget(self.le_dossierOut, 2, 1, 1, 1)
        self.main_layout.addWidget(self.lw_files, 3, 0, 1, 2)
        self.main_layout.addWidget(self.lbl_dropInfo, 4, 0, 1, 2)
        self.main_layout.addWidget(self.btn_convert, 5, 0, 1, 2)

    def setup_connections(self):
        self.btn_convert.clicked.connect(self.convert_images)
        QtWidgets.QShortcut(QtGui.QKeySequence("Backspace"), self.lw_files, self.delete_selected_items)

    def convert_images(self):
        quality = self.spn_quality.value()
        size = self.spn_size.value() / 100.0
        folder = self.le_dossierOut.text()

        images_lw_items = [self.lw_files.item(i) for i in range(self.lw_files.count())]

        self.prg_dialog = QtWidgets.QProgressDialog("Conversion des images", "On annule tout !", 1, len(images_lw_items))
        self.prg_dialog.show()

        self.convert_thread = ConvertImageThread(images_to_convert=images_lw_items,
                                                 quality=quality,
                                                 size=size,
                                                 folder=folder)
        self.convert_thread.start()
        self.convert_thread.image_converted.connect(self.image_converted)

    def delete_selected_items(self):
        for lw_item in self.lw_files.selectedItems():
            row = self.lw_files.row(lw_item)
            self.lw_files.takeItem(row)

    def image_converted(self, lw_item, success):
        if success:
            lw_item.setIcon(self.ctx.img_checked)
            self.prg_dialog.setValue(self.prg_dialog.value() + 1)

    def dragEnterEvent(self, event):
        self.lbl_dropInfo.setVisible(True)
        event.accept()

    def dragLeaveEvent(self, event):
        self.lbl_dropInfo.setVisible(False)

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
            for url in event.mimeData().urls():
                filepath = str(url.toLocalFile())
                self.add_file(path=filepath)
        else:
            event.ignore()
        
        self.lbl_dropInfo.setVisible(False)

    def add_file(self, path):
        items = [self.lw_files.item(index).text() for index in range(self.lw_files.count())]
        if path not in items:
            lw_item = QtWidgets.QListWidgetItem(path)
            lw_item.setIcon(self.ctx.img_unchecked)
            self.lw_files.addItem(lw_item)
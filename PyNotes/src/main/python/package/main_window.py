from PySide2 import QtWidgets, QtGui, QtCore
from package.api.note import Notes, Note


class MainWindow(QtWidgets.QWidget):
    def __init__(self, ctx):
        super().__init__()

        self.ctx = ctx
        self.setWindowTitle("Prise de notes")
        self.setup_ui()
        self.notes = Notes()
        self.populate_notes()

    def setup_ui(self):
        self.create_widgets()
        self.modify_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        self.btn_createNote = QtWidgets.QPushButton("Créer une note")
        self.lw_notes = QtWidgets.QListWidget()
        self.te_contenu = QtWidgets.QTextEdit()

    def modify_widgets(self):
        css_file = self.ctx.get_resource("style.css")
        with open(css_file, "r") as f:
            self.setStyleSheet(f.read())

    def create_layouts(self):
        self.main_layout = QtWidgets.QGridLayout(self)

    def add_widgets_to_layouts(self):
        self.main_layout.addWidget(self.btn_createNote, 0, 0, 1, 1)
        self.main_layout.addWidget(self.lw_notes, 1, 0, 1, 1)
        self.main_layout.addWidget(self.te_contenu, 0, 1, 2, 1)

    def setup_connections(self):
        self.lw_notes.itemSelectionChanged.connect(self.populate_note_content)
        self.btn_createNote.clicked.connect(self.create_note)
        self.te_contenu.textChanged.connect(self.save_note)
        QtWidgets.QShortcut(QtGui.QKeySequence("Backspace"), self.lw_notes, self.delete_selected_note)

    def create_note(self):
        title, result = QtWidgets.QInputDialog.getText(self, "Ajouter une note", "Titre")
        if result and title:
            note = Note(title=title)
            note.save()
            self.add_note_to_listwidget(note=note)

    def delete_selected_note(self):
        selected_items = self.lw_notes.selectedItems()
        if not selected_items:
            return False

        selected_item = selected_items[0]
        selected_item.note.delete()
        self.lw_notes.takeItem(self.lw_notes.row(selected_item))

    def populate_notes(self):
        for note in self.notes:
            self.add_note_to_listwidget(note=note)

    def add_note_to_listwidget(self, note):
        lw_item = QtWidgets.QListWidgetItem(note.title)
        lw_item.note = note
        self.lw_notes.addItem(lw_item)

    def populate_note_content(self):
        selected_notes = self.lw_notes.selectedItems()
        if not selected_notes:
            self.te_contenu.clear()
            return False

        selected_note = selected_notes[0]
        self.te_contenu.setText(selected_note.note.content)

    def save_note(self):
        selected_notes = self.lw_notes.selectedItems()
        if not selected_notes:
            return False

        selected_note = selected_notes[0]
        selected_note.note.content = self.te_contenu.toPlainText()
        selected_note.note.save()



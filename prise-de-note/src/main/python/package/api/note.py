import os
from uuid import uuid4
import json
from glob import glob

from package.api.constants import NOTES_DIR

class Notes(list):
    def __init__(self):
        self._retrieve_notes()

    def _retrieve_notes(self):
        fichiers = glob(os.path.join(NOTES_DIR, "*.json"))
        for fichier in fichiers:
            with open(fichier, "r") as f:
                note_data = json.load(f)
                note_uuid = os.path.splitext(os.path.basename(fichier))[0]
                note_title = note_data.get("title")
                note_content = note_data.get("content")
                note = Note(uuid=note_uuid, title=note_title, content=note_content)
                self.append(note)

class Note:
    def __init__(self, title="", content="", uuid=None):
        if uuid:
            self.uuid = uuid
            self.title, self.content = self._get_note_data()
        else:
            self.uuid = str(uuid4())
            self.title = title
            self.content = content

    def __repr__(self):
        return f"{self.title} ({self.uuid})"

    def __str__(self):
        return self.title

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if isinstance(value, str):
            self._content = value
        else:
            print("Svp, entrez du texte.")

    def _get_note_data(self):
        if not os.path.exists(self.path):
            raise FileNotFoundError("Le fichier {self.path} n'existe pas.")

        with open(self.path, "r") as f:
            data = json.load(f)
            if data.get("title") is None or data.get("content") is None:
                raise AttributeError("Le titre ou le contenu n'ont pas été trouvés.")
            return data.get("title"), data.get("content")

    @property
    def path(self):
        return os.path.join(NOTES_DIR, self.uuid + ".json")
        
    def save(self):
        if not os.path.exists(NOTES_DIR):
            os.makedirs(NOTES_DIR, exist_ok=True)

        data = {"title": self.title, "content": self.content}
        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)
            print("Contenu sauvegardé avec succès.")

if __name__ == "__main__":
    pass    



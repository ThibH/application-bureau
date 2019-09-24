import os
from uuid import uuid4
import json
from glob import glob

from package.api.constants import NOTES_DIR

class Notes(list):
    def __init__(self):
        self._retrieve_notes()

    def _retrieve_notes(self):
        """Récupération des notes depuis le disque dur"""
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
        """Note individuelle
        
        Args:
            title (str, optional): Le titre de la note. Defaults to "".
            content (str, optional): Le contenu de la note. Defaults to "".
            uuid (uuid4, optional): ID unique et aléatoire. Defaults to None.
        """
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
        """Retourne le contenu de la note
        
        Returns:
            str: Contenu de la note
        """
        return self._content

    @content.setter
    def content(self, value):
        """Modifie le contenu de la note
        
        Args:
            value (str): Contenu de la note
        """
        if isinstance(value, str):
            self._content = value
        else:
            print("Svp, entrez du texte.")

    def delete(self):
        """Supression de la note sur le disque
        
        Returns:
            bool: Retourne vrai si la note a bien été supprimée
        """
        os.remove(self.path)
        if not os.path.exists(self.path):
            return True
        return False

    def _get_note_data(self):
        """Récupère le titre et le contenu de la note
        
        Raises:
            FileNotFoundError: Le fichier correspondant à la note n'a pas été trouvé sur le disque
            AttributeError: Le titre ou le contenu de la note n'a pas été trouvé
        
        Returns:
            str, str: Le titre et le contenu de la note
        """
        if not os.path.exists(self.path):
            raise FileNotFoundError("Le fichier {self.path} n'existe pas.")

        with open(self.path, "r") as f:
            data = json.load(f)
            if data.get("title") is None or data.get("content") is None:
                raise AttributeError("Le titre ou le contenu n'ont pas été trouvés.")
            return data.get("title"), data.get("content")

    @property
    def path(self):
        """Le chemin sur disque de la note
        
        Returns:
            str: Chemin sur disque de la note
        """
        return os.path.join(NOTES_DIR, self.uuid + ".json")
        
    def save(self):
        """Sauvegarde le contenu de la note sur le disque"""
        if not os.path.exists(NOTES_DIR):
            os.makedirs(NOTES_DIR, exist_ok=True)

        data = {"title": self.title, "content": self.content}
        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)

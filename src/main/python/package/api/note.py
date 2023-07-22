import os.path
import json
from uuid import uuid4
from glob import glob

from package.api.constants import NOTES_DIR

def get_notes():
    notes=[]
    fichiers = glob(os.path.join(NOTES_DIR, "*.json"))
    for fichier in fichiers:
        with open(fichier, "r") as f:
            note_data = json.load(f)
            note_uuid = os.path.splitext(os.path.basename(fichier))[0]
            note_title = note_data.get("title")
            note_content = note_data.get("content")
            note = Note(uuid=note_uuid, title=note_title, content=note_content)
            notes.append(note)
    return notes

class Note:
    def __init__(self, title="", content="", uuid=None):
        if uuid:
            self.uuid = uuid
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
            self._content=value
        else:
            raise TypeError("Invalid error, requires a string value!")

    def delete(self):
        os.remove(self.path)
        if os.path.exists(self.path):
            return False
        return True


    @property
    def path(self):  # mentioning @property above a function allows calling it as a parameter
        return os.path.join(NOTES_DIR, self.uuid + ".json")

    def save(self):
        if not os.path.exists(NOTES_DIR):
            os.makedirs(NOTES_DIR)
        data = {"title": self.title, "content": self.content}
        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)

if __name__ == '__main__':
    #n = Note(title="Ceci est un titre", content="Ceci est un contenu")
    #n.uuid="e9ac26c6-0c54-4b98-a731-1c44f751bebf" #need to specify the uuid to target the file we want to delete by editing uuid parameter of the instance
    #because uuid is initialized randomly in each instanciation
    #resultat = n.delete()
    #print(resultat)
    #for i in range(5):
    #    n = Note(title=f"Titre {i}", content=f"Contenu {i}")
    #    n.save()
    notes = get_notes()
    print(notes)


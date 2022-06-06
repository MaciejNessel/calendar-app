from App.Notes.Note import Note
from App.Json.JsonManager import JsonManager
import json


class NotesManager:
    def __init__(self, json_manager):
        self.__notes = {}
        self.__json_manager = json_manager

    def load(self):
        self.__notes.clear()
        data = self.__json_manager.get_notes()
        for note in data:
            new_note = Note(note.get('title'), note.get('text'), note.get('id_'))
            self.__notes.update({note.get('id_'): new_note})

    def get(self, id_):
        result = self.__notes.get(id_)
        return result

    def get_all(self):
        return self.__notes

    def add(self, note=None, title=None, text=None):
        if note is None:
            id_ = JsonManager.generate_id()
            self.__notes[id_] = Note(title, text, id_)
            return True
        try:
            if type(note) != Note:
                raise AttributeError
            else:
                self.__notes[note.get_id()] = note
                return True
        except AttributeError:
            print("An exception occurred: (AttributeError) NotesManager add_note()")
            return False

    def delete(self, id_):
        try:
            del self.__notes[id_]
        except KeyError:
            print("An exception occurred: (KeyError) NotesManager delete_note()")

    def reset(self):
        self.__notes.clear()

    def save(self):
        result = {"noteDetails": []}
        for note in self.__notes.items():
            result["noteDetails"].append((json.loads(note[1].to_json())))
        return result

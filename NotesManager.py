from Note import Note


class NotesManager:
    __notes = {}

    def __init__(self, json_manager):
        self.__json_manager = json_manager
        self.load_notes()

    def load_notes(self):
        try:
            self.__notes = self.__json_manager.load_notes()
        except AttributeError:
            print("An exception occurred: (AttributeError) NotesManager load_notes()")

    def get_note(self, id_):
        try:
            return self.__notes[id_]
        except KeyError:
            print("An exception occurred: (KeyError) NotesManager get_note()")
            return None

    def add_note(self, note):
        try:
            if type(note) != Note:
                raise AttributeError
            else:
                self.__notes[note.get_id()] = note
        except AttributeError:
            print("An exception occurred: (AttributeError) NotesManager add_note()")

    def delete_note(self, id_):
        try:
            del self.__notes[id_]
        except KeyError:
            print("An exception occurred: (KeyError) NotesManager delete_note()")

    def reset_notes(self):
        self.__notes.clear()

    def save_changes(self):
        for note in self.__notes:
            note.to_json()

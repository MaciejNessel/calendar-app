import json
from app.json.json_encoder import JsonEncoder

class Event:
    def __init__(self, title, short_desc, desc, id_, notes_id, color):
        self.__title = title
        self.__short_desc = short_desc
        self.__desc = desc
        self.__id_ = id_
        self.__notes_id = notes_id
        self.__color = color

    # Return Event object in json format
    def to_json(self):
        return json.dumps(self, cls=JsonEncoder, indent=2)

    # Getters to all Attributes

    def get_title(self):
        return self.__title

    def get_short_desc(self):
        return self.__short_desc

    def get_desc(self):
        return self.__desc

    def get_id(self):
        return self.__id_

    def get_notes_id(self):
        return self.__notes_id

    def get_color(self):
        return self.__color

    # Setter to __title
    def set_title(self, title):
        self.__title = title

    # Setter to __shortDesc
    def set_short_desc(self, short_desc):
        self.__short_desc = short_desc

    # Setter to __desc
    def set_desc(self, desc):
        self.__desc = desc

    def set_color(self, new_color):
        self.__color = new_color

    # Add note of Id to __notes_id(Event)
    def addNote(self, note_id):
        self.__notes_id.append(note_id)

    # Remove note of Id from __notes_id(Event)
    def removeNote(self, note_id):
        self.__notes_id.remove(note_id)

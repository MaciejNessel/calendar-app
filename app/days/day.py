import json
from app.json.json_encoder import JsonEncoder


class Day:
    def __init__(self, date, events_, notes):
        self.__date = date
        self.__events = events_
        self.__notes = notes

    def add_event_to_day(self, event):
        self.__events.append(event)

    def add_note_to_day(self, note):
        self.__notes.add(note)

    def get_events(self):
        return self.__events

    def get_notes(self):
        return self.__notes

    def delete_event(self, event_id):
        to_remove = None
        for x in self.__events:
            if x.get("id_", None) == event_id:
                to_remove = x
                break

        if not to_remove:
            return False

        self.__events.remove(to_remove)

        if len(self.__events) == 0:
            return True

        return False

    def to_json(self):
        return json.dumps(self, cls=JsonEncoder, indent=2)

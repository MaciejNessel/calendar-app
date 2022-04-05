from Event import Event
from Note import Note


class Day:
    def __init__(self, date, events_, notes):
        self.__date = date
        self.__events = events_
        self.__notes = notes

    def add_event_to_day(self, event):
        try:
            if type(event) != Event:
                raise AttributeError
            else:
                self.__events.add(event)
        except AttributeError:
            print("An exception occurred: (AttributeError) Day add_event_to_day()")

    def add_note_to_day(self, note):
        try:
            if type(note) != Note:
                raise AttributeError
            else:
                self.__events.add(note)
        except AttributeError:
            print("An exception occurred: (AttributeError) Day add_event_to_day()")

    def get_events(self):
        return self.__events

    def get_notes(self):
        return self.__notes

    def to_json(self):
        pass
        # TODO json_manager.save_day(this)

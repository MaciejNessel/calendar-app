from app.events.event import Event
from app.json.json_manager import JsonManager
import json

class EventsManager:
    def __init__(self, json_manager):
        self.__events = {}
        self.__json_manager = json_manager

    # Load events from JSON file
    def load(self):
        self.__events.clear()
        data = self.__json_manager.get_events()
        for event in data:
            new_event = Event(event.get('title'), event.get('short_desc'),
                              event.get('desc'), event.get('id_'), event.get('notes_id'), event.get('color'))
            self.__events.update({event.get('id_'): new_event})

    # Add Event to local list
    def add(self, event=None, title="", short_desc="", desc="", notes_id=[], color=""):
        if event is None:
            id_ = str(JsonManager.generate_id())
            self.__events[id_] = Event(title, short_desc, desc, id_, notes_id, color)
            return id_
        else:
            self.__events[event.get_id()] = event
            return str(event.get_id())

    # Get Event
    def get(self, id_):
        if id_ not in self.__events.keys():
            return None
        else:
            return self.__events[id_]

    # Reset events
    def reset(self):
        self.__events.clear()
        self.load()

    # Delete Event of id
    def delete(self, id_):
        del self.__events[id_]

    # Save Changes to JSON - toJSON
    def save(self):
        result = {"eventDetails": []}
        for event in self.__events.items():
            result["eventDetails"].append((json.loads(event[1].to_json())))
        return result

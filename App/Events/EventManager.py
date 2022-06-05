from App.Events.Event import Event
from App.Json.JsonManager import JsonManager
import json

class EventsManager:
    def __init__(self, json_manager):
        self.__events = {}
        self.__json_manager = json_manager

    # Load events from JSON file
    def load(self):
        data = self.__json_manager.get_events()
        for event in data:
            new_event = Event(event.get('title'), event.get('short_desc'),
                              event.get('desc'), event.get('id_'), event.get('notes_id'))
            self.__events.update({event.get('id_'): new_event})

    # Add Event to local list
    def add(self, event=None, title="", short_desc="", desc="", notes_id=[]):
        if event is None:
            id_ = JsonManager.generate_id()
            self.__events[str(id_)] = Event(title, short_desc, desc, id_, notes_id)
            return str(id_)
        else:
            self.__events[event.get_id()] = event
            return str(event.get_id())

    # Get Event
    def get(self, id_):
        if id_ not in self.__events.keys():
            return None
        else:
            return self.__events[id_]

    # Reset Events
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

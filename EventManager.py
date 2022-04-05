import Event


####        EventsManager

class EventsManager:
    _events = []
    _data = None
    _highestId = -1

    def __init__(self, jsonManager):
        self._data = jsonManager

    #Load events from JSON file
    def load(self):
        self._events = self._data.loadEvents()

    #Add Event to local list
    def add(self, event = None, title = "", shortDesc = "", desc = "", noteId = []):
        if(event == None):
            event = Event(title, shortDesc, desc, self._highestId, noteId)
        
        self._events.append(event)

    #Get Event
    def get(self, id):
        return self._events[id]

    #Reset Events
    def reset(self):
        self.load()

    #Delete Event of id
    def delete(self, id):
        self._events.remove(id)

    #Save Changes to JSON - toJSON
    def save(self):
        #todo:
        #   Petla dodajaca eventy za pomoca funkcji toJSON kazdego eventu
        pass
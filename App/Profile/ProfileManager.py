from App.Events.EventManager import EventsManager
from App.Notes.NotesManager import NotesManager
from App.Days.DayManager import DayManager
from App.Json.JsonManager import JsonManager


class ProfileManager:
    def __init__(self, username):
        self.json_manager = JsonManager()
        self.event_manager = EventsManager(self.json_manager)
        self.day_manager = DayManager(self.json_manager)
        self.note_manager = NotesManager(self.json_manager)
        self.username = username
        self.load_user_data()

    def save_profile(self):
        self.json_manager.save(self.note_manager, self.event_manager, self.day_manager)

    def load_user_data(self):
        self.json_manager.load_data(self.username)
        self.event_manager.load()
        self.day_manager.load()
        self.note_manager.load()

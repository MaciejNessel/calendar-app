import json
from App.Events.EventManager import EventsManager
from App.Notes.NotesManager import NotesManager
from App.Days.DayManager import DayManager
from App.Json.JsonManager import JsonManager

from datetime import datetime, timedelta


class ProfileManager:
    def __init__(self, username, json_manager):
        self.json_manager = json_manager
        self.event_manager = EventsManager(self.json_manager)
        self.day_manager = DayManager(self.json_manager)
        self.note_manager = NotesManager(self.json_manager)
        self.username = username
        self.load_user_data()
        self.actual_date = datetime.now()

    def set_actual_date(self, new_date):
        self.actual_date = new_date

    def change_actual_date(self, days):
        self.actual_date += timedelta(days=days)

    def save_profile(self):
        self.json_manager.save(self.note_manager, self.event_manager, self.day_manager)

    def load_user_data(self):
        self.json_manager.load_data(self.username)
        self.event_manager.load()
        self.day_manager.load()
        self.note_manager.load()

    def add_to_location_history(self, last_location):
        self.location_history.append(last_location)

    def change_date(self, new_date):
        self.actual_date = new_date

    def get_date(self):
        return self.actual_date

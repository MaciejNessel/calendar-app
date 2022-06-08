import json
from app.events.event import Event
from app.events.event_manager import EventsManager
from app.notes.note import Note
from app.notes.notes_manager import NotesManager
from app.days.day_manager import DayManager
from app.json.json_manager import JsonManager

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

    def save_profile(self):
        self.json_manager.save(self.note_manager, self.event_manager, self.day_manager)

    def load_user_data(self):
        self.json_manager.load_data(self.username)
        self.event_manager.load()
        self.day_manager.load()
        self.note_manager.load()

    # date methods

    def set_actual_date(self, new_date):
        self.actual_date = new_date

    def change_actual_date(self, days):
        self.actual_date += timedelta(days=days)

    def get_date(self):
        return self.actual_date
    
    def get_date_range(self):
        actual_date_temp = self.actual_date
        actual_date_temp -= timedelta(days=actual_date_temp.weekday())
        return actual_date_temp, actual_date_temp + timedelta(days=6)

    # note methods

    def set_note(self, title, desc, id = -1):
        if id != -1:
            self.note_manager.add(note = Note(title, desc, id))
        else:
            self.note_manager.add(title= title, text=desc)

    def get_note(self, id):
        return self.note_manager.get(id)

    def get_all_notes_id(self):
        return self.note_manager.get_all()

    def delete_note(self, note):
        self.note_manager.delete(note.get_id())

    # event methods

    def save_event(self, event):
        self.event_manager.add(event=event)

    def get_event(self, id):
        return self.event_manager.get(id)

    def delete_event(self, event):
        self.day_manager.delete_event(event.get_id())
        self.event_manager.delete(event.get_id())

    # day methods

    def get_day(self, day=None, month=None, year=None, date=None):
        if date == None:
            return self.day_manager.get_day(day=day, month=month, year=year)
        else:
            return self.day_manager.get_day(date=date)

    def add_event_to_day(self, date, event_id, start, end):
        self.day_manager.add_event_to_day(date=date, event_id=event_id, start=start,
                                                             end=end)

    def is_event_in_day(self, event_id, day = None, date = None):
        if day == None:
            day = self.get_day(date=date)

        if day == None:
            return False
        
        for event in day.get_events():
            if event["id_"] == event_id:
                return True
        
        return False
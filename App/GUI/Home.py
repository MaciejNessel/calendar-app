from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from App.Days.DayManager import DayManager
from App.Events.EventManager import EventsManager
from App.Notes.NotesManager import NotesManager


class UserManager:
    def __init__(self, json_manager, username):
        self.username = username
        self.json_manager = json_manager
        self.day_manager = DayManager(json_manager)
        self.events_manager = EventsManager(json_manager)
        self.note_manager = NotesManager(json_manager)

        self.events_manager.load()
        self.day_manager.load()
        self.note_manager.load()


class Home(GridLayout):
    def __init__(self, app, json_manager, username, **kw):
        super(Home, self).__init__(**kw)

        self.user_manager = UserManager(json_manager, username)
        self.app = app

        self.cols = 1
        self.padding = 0.1 * Window.width

        # TODO Od tego miejsca zalogowano jako username.

        self.tests()
        self.add_widget(Button(text='Change user', on_release=lambda x: self.app.back_to_login()))

    def tests(self):
        self.add_widget(Label(text=self.user_manager.username))
        for event in self.user_manager.json_manager.get_events():
            self.add_widget(Label(text=event.get('title')))
            self.add_widget(Label(text=event.get('short_desc')))



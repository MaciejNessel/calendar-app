from kivy.app import App
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, NoTransition, Screen
from App.GUI.Event import EventAdd
from App.GUI.Login import Login
from App.GUI.MenuElements import *
from App.GUI.Note import NoteAdd, NoteEdit, NoteInfo
from App.Json.JsonManager import JsonManager
from App.Profile.ProfileManager import ProfileManager


class MyApp(App):
    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)
        self.screen_manager = ScreenManager(transition=NoTransition())
        self.home = None
        self.add_screen(Login(self), "Login")
        self.json_manager = JsonManager()
        self.profile_manager = None
        self.base = "WeekMenu"
        self.actual_event = None

    def build(self):
        Window.clearcolor = "#0d1b2a"
        Window.size = (900, 600)
        Window.minimum_width, Window.minimum_height = Window.size
        return self.screen_manager

    def add_screen(self, layout, name):
        screen = Screen(name=name)
        screen.add_widget(layout)
        self.screen_manager.add_widget(screen)

    def change_user(self, username):
        if not self.json_manager.load_data(username):
            Factory.Error("Loading " + username + " data failed.").open()
            return

        self.profile_manager = ProfileManager(username=username, json_manager=self.json_manager)
        self.base = "WeekMenu"

        if self.home:
            self.screen_manager.remove_widget(self.home)

        self.home = Screen(name="WeekMenu")
        self.home.add_widget(WeekMenu(self))

        self.screen_manager.add_widget(self.home)
        self.screen_manager.current = "WeekMenu"

    def change_logged_screen(self, screen_name, id=-1):
        temp_home = Screen(name=screen_name)
        if screen_name == "WeekMenu":
            temp_home.add_widget(WeekMenu(self))
        elif screen_name == "Base":
            return self.change_logged_screen(self.base)
        elif screen_name == "NoteInfo":
            temp_home.add_widget(NoteInfo(self, id=id))
        elif screen_name == "NoteEdit":
            temp_home.add_widget(NoteEdit(self, id=id))
        elif screen_name == "DayMenu":
            temp_home.add_widget(DayMenu(self, -1))
        elif screen_name == "EventAdd":
            temp_home.add_widget(EventAdd(self))
        elif screen_name == "NoteAdd":
            temp_home.add_widget(NoteAdd(self))
        else:
            return

        if self.home:
            self.screen_manager.add_widget(temp_home)
            self.screen_manager.remove_widget(self.home)

        self.home = temp_home

        self.screen_manager.current = screen_name

    def back_to_login(self):
        self.screen_manager.current = 'Login'

    def changeBase(self):
        if self.base == "WeekMenu":
            self.base = "DayMenu"
        else:
            self.base = "WeekMenu"

    def set_base(self, base):
        self.base = base

    def reset_actual_event(self):
        self.actual_event = None
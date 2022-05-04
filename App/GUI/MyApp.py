from email.policy import default
from kivy.app import App
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, NoTransition, Screen

from App.GUI.Login import Login
from App.GUI.Home import Home
from App.GUI.MenuElements import *
from App.Json.JsonManager import JsonManager

from App.GUI.Error import Error
from App.Profile.ProfileManager import ProfileManager

class MyApp(App):
    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)
        self.screen_manager = ScreenManager()
        self.home = None
        self.add_screen(Login(self), "Login")
        self.json_manager = JsonManager()
        self.profile_manager = None
        self.base = "WeekMenu"
        self.actualEvent = None

    def build(self):
        #Window.clearcolor = (1, 1, 1, 1)
        return self.screen_manager

    def add_screen(self, layout, name):
        screen = Screen(name=name)
        screen.add_widget(layout)
        self.screen_manager.add_widget(screen)

    def change_user(self, username):
        if not self.json_manager.load_data(username):
            Factory.Error("Loading "+username+" data failed.").open()
            return

        self.profile_manager = ProfileManager(username = username, json_manager=self.json_manager)
        self.base = "WeekMenu"


        if self.home:
            self.screen_manager.remove_widget(self.home)

        self.home = Screen(name = "WeekMenu")
        self.home.add_widget(WeekMenu(self))

        self.screen_manager.add_widget(self.home)
        self.screen_manager.current = "WeekMenu"

    def change_logged_screen(self, screen_name, id=-1):
        temp_home = Screen(name = screen_name)
        if screen_name == "WeekMenu":
            temp_home.add_widget(WeekMenu(self))
        elif screen_name == "DateChanger":
            temp_home.add_widget(DateChanger(self))
        elif screen_name == "Base":
            return self.change_logged_screen(self.base)
        elif screen_name == "NoteInfo":
            temp_home.add_widget(NoteInfo(self, id=id))
        elif screen_name == "NoteEdit":
            temp_home.add_widget(NoteEdit(self, id=id))
        elif screen_name == "DayMenu":
            temp_home.add_widget(DayMenu(self, -1))
        else:
            return

        if self.home:
            self.screen_manager.remove_widget(self.home)

        self.home = temp_home
        self.screen_manager.add_widget(self.home)
        self.screen_manager.current = screen_name
        

    def back_to_login(self):
        self.screen_manager.current = 'Login'

    def changeBase(self):
        if self.base == "WeekMenu":
            self.base = "DayMenu"
        else:
            self.base = "WeekMenu"
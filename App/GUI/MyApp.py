from kivy.app import App
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, NoTransition, Screen

from App.GUI.Login import Login
from App.GUI.Home import Home
from App.Json.JsonManager import JsonManager

from App.GUI.Error import Error

class MyApp(App):
    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)
        self.screen_manager = ScreenManager()
        self.home = None
        self.add_screen(Login(self), "Login")
        self.json_manager = JsonManager()

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

        if self.home:
            self.screen_manager.remove_widget(self.home)

        self.home = Screen(name="Home")
        self.home.add_widget(Home(self, self.json_manager, username))

        self.screen_manager.add_widget(self.home)
        self.screen_manager.current = 'Home'

    def back_to_login(self):
        self.screen_manager.current = 'Login'




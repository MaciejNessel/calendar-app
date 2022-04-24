from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from App.Json.JsonManager import JsonManager
from App.GUI.Message import Message
from App.GUI.Error import Error
from App.GUI.Buttons import PrimaryButton, UsersButton


class SelectUser(Popup):
    def __init__(self, app, **kw):
        super(SelectUser, self).__init__(**kw)
        self.app = app
        self.size_hint = (.7, .7)
        layout = GridLayout(cols=1)
        layout.padding = 20
        layout.spacing = 20
        self.title = "Select user"
        back_btn = PrimaryButton(text='Back',
                                 on_release=lambda x: self.dismiss())
        back_btn.size_hint = (1, .2)
        layout.add_widget(self.users_list())
        layout.add_widget(back_btn)
        self.add_widget(layout)

    def users_list(self):
        layout = GridLayout(cols=1,
                            size_hint_y=None,
                            spacing=2)
        scroll_view = ScrollView()
        users = JsonManager.get_users()
        color_even = True
        for user in users:
            btn = UsersButton(text=user.get('username'),
                              on_release=lambda instance: self.login(instance))
            btn.size_hint = (1, None)
            btn.size = (1, 30)
            if color_even:
                btn.btn_color = (0, 0, 0, 0)
            color_even = not color_even
            layout.add_widget(btn)

        scroll_view.add_widget(layout)
        return scroll_view

    def login(self, instance):
        self.dismiss()
        self.app.change_user(instance.text)

# Template for NewUser, ImportData and ExportData
class LoginPopup(Popup):
    def __init__(self, **kw):
        super(LoginPopup, self).__init__(**kw)
        self.size_hint = (.7, .7)
        layout = GridLayout(cols=1,
                            spacing=10,
                            padding=20)

        self.input_field = TextInput(multiline=False)
        layout.add_widget(self.input_field)

        self.main_btn = PrimaryButton()
        layout.add_widget(self.main_btn)

        back_btn = PrimaryButton(text='Back',
                                 on_release=lambda x: self.dismiss())
        layout.add_widget(back_btn)

        self.add_widget(layout)

class NewUser(LoginPopup):
    def __init__(self, app, **kw):
        super(NewUser, self).__init__(**kw)
        self.app = app
        self.title = "Create a new user"
        self.main_btn.text = "Confirm"
        self.main_btn.on_release = lambda: self.add(self.input_field.text)

    def add(self, text):
        if text == '':
            return
        result = self.app.json_manager.create_new_user(text)
        self.dismiss()
        if result[0]:
            Factory.Message(result[1]).open()
        else:
            Factory.Error(result[1]).open()

class ImportData(LoginPopup):
    def __init__(self, app, **kw):
        super(ImportData, self).__init__(**kw)
        self.app = app
        self.title = "Import data"
        self.main_btn.text = "Import"
        self.main_btn.on_release = lambda: self.import_data(self.input_field.text)

    def import_data(self, url):
        if self.app.json_manager.import_data(url):
            Factory.Message("Data imported successfully.").open()
        else:
            Factory.Error("Data import failed").open()

        self.dismiss()

class ExportData(LoginPopup):
    def __init__(self, app, **kw):
        super(ExportData, self).__init__(**kw)
        self.app = app
        self.title = "Export data"
        self.main_btn.text = "Export"
        self.main_btn.on_release = lambda: self.export()

    def export(self):
        self.input_field.text = self.app.json_manager.export_data()

class Login(GridLayout):
    def __init__(self, app, **kw):
        super(Login, self).__init__(**kw)
        self.cols = 1
        self.padding = 0.1 * Window.width
        self.spacing = 20
        LabelBase.register(name='Lemonada',
                           fn_regular='../../lemonada.ttf')
        select_user_btn = PrimaryButton(text='Select user',
                                        on_release=lambda x: Factory.SelectUser(app).open())
        new_user_btn = PrimaryButton(text='Add new user',
                                     on_release=lambda x: Factory.NewUser(app).open())
        import_btn = PrimaryButton(text='Import data',
                                   on_release=lambda x: Factory.ImportData(app).open())
        export_btn = PrimaryButton(text='Export data',
                                   on_release=lambda x: Factory.ExportData(app).open())
        self.add_widget(Label(text="Calendar App", font_size=50, font_name="Lemonada"))
        self.add_widget(select_user_btn)
        self.add_widget(new_user_btn)
        self.add_widget(import_btn)
        self.add_widget(export_btn)
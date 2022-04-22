from kivy.core.window import Window
from kivy.factory import Factory
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from App.Json.JsonManager import JsonManager


class NewUser(Popup):
    def __init__(self, app, **kw):
        super(NewUser, self).__init__(**kw)
        self.app = app
        self.title = "Add new user"
        layout = GridLayout(cols=1)

        layout.add_widget(Label(text="Add new user: "))
        input_username = TextInput(multiline=False)
        layout.add_widget(input_username)
        back_btn = Button(text='Back',
                          on_release=lambda x: self.dismiss())
        layout.add_widget(back_btn)
        add_btn = Button(text='Add',
                         on_release=lambda x: self.add(input_username.text))
        layout.add_widget(add_btn)
        self.add_widget(layout)

    def add(self, text):
        if text == '':
            return
        result = self.app.json_manager.create_new_user(text)
        self.dismiss()
        if result[0]:
            Factory.Message(result[1]).open()
        else:
            Factory.Error(result[1]).open()


class SelectUser(Popup):
    def __init__(self, app, **kw):
        super(SelectUser, self).__init__(**kw)
        self.app = app
        layout = GridLayout(cols=1)
        self.title = "Select user"
        back_btn = Button(text='Back',
                          on_release=lambda x: self.dismiss())

        layout.add_widget(self.users_list())
        layout.add_widget(back_btn)
        self.add_widget(layout)

    def users_list(self):
        layout = GridLayout(cols=1, size_hint_y=None)
        scroll_view = ScrollView()
        users = JsonManager.get_users()
        for user in users:
            btn = Button(text=user.get('username'),
                         on_release=lambda instance: self.login(instance))
            layout.add_widget(btn)
        scroll_view.add_widget(layout)
        return scroll_view

    def login(self, instance):
        self.dismiss()
        self.app.change_user(instance.text)


class ImportData(Popup):
    def __init__(self, app, **kw):
        super(ImportData, self).__init__(**kw)
        self.app = app
        self.title = "Import data"
        layout = GridLayout(cols=1)

        file_chooser = FileChooserListView()
        select_btn = Button(text='Select',
                            on_release=lambda x: self.load(file_chooser.path, file_chooser.selection))
        back_btn = Button(text='Back',
                          on_release=lambda x: self.dismiss())

        layout.add_widget(file_chooser)
        layout.add_widget(select_btn)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def load(self, path, filename):
        self.app.json_manager.import_data(path, filename)

class Login(GridLayout):
    def __init__(self, app, **kw):
        super(Login, self).__init__(**kw)
        self.cols = 1
        self.padding = 0.1 * Window.width
        select_user_btn = Button(text='Select user',
                                 on_release=lambda x: Factory.SelectUser(app).open())
        new_user_btn = Button(text='Add new user',
                              on_release=lambda x: Factory.NewUser(app).open())
        import_btn = Button(text='Import data from file',
                            on_release=lambda x: Factory.ImportData(app).open())

        self.add_widget(select_user_btn)
        self.add_widget(new_user_btn)
        self.add_widget(import_btn)

from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from App.GUI.Buttons import PrimaryButton, ColorButton, NoteButton, TitleButton, ScrollGrid
from kivy.factory import Factory
from kivy.uix.scrollview import ScrollView


class NoteAdd(GridLayout):
    def __init__(self, app, **kw):
        super(NoteAdd, self).__init__(**kw)
        self.cols = 1
        self.background = ""
        self.background_color = "#0d1b2a"
        self.padding = 50
        self.spacing = 20
        title = "title"
        desc = "description"

        self.title = TextInput()
        self.title.text = title
        self.add_widget(Label(text="Title", font_size='15sp', font_name="Lemonada", size_hint_y=None, height=15))
        self.add_widget(self.title)

        self.desc = TextInput()
        self.desc.text = desc
        self.add_widget(Label(text="Content", font_size='15sp', font_name="Lemonada", size_hint_y=None, height=15))
        self.add_widget(self.desc)

        buttons = GridLayout()
        buttons.cols = 2

        buttons.add_widget(
            PrimaryButton(text="Accept", on_release=lambda x: self.accept(app), size_hint_y=None, height=100))
        buttons.add_widget(
            PrimaryButton(text="Back", on_release=lambda x: self.back(app), size_hint_y=None, height=100))

        self.add_widget(buttons)

    def accept(self, app):
        app.profile_manager.set_note(self.title.text, self.desc.text)

        self.back(app)

    def back(self, app):
        app.change_logged_screen("Base")


class NoteEdit(GridLayout):
    def __init__(self, app, id, **kw):
        super(NoteEdit, self).__init__(**kw)

        self.cols = 1
        self.padding = 100
        self.spacing = 20
        note = app.profile_manager.get_note(id)

        title = note.get_title()
        description = note.get_text()

        self.title = TextInput()
        self.title.text = title
        self.add_widget(Label(text="Title", font_size='15sp', font_name="Lemonada", size_hint_y=None, height=15))
        self.add_widget(self.title)

        self.short_desc = TextInput()
        self.short_desc.text = description
        self.add_widget(Label(text="Content", font_size='15sp', font_name="Lemonada", size_hint_y=None, height=15))
        self.add_widget(self.short_desc)

        buttons = GridLayout()
        buttons.cols = 2
        buttons.add_widget(PrimaryButton(text="Accept", on_release=lambda x: self.accept(app, id, self.title.text,
                                                                                         self.short_desc.text)))  # TODO: saving changes to temporary json
        buttons.add_widget(
            PrimaryButton(text="Cancel", on_release=lambda x: self.back(app, id)))

        self.add_widget(buttons)

    def accept(self, app, id, title, short_desc):
        app.profile_manager.set_note(title, short_desc, id)
        app.change_logged_screen("NoteInfo", id=id)

    def back(self, app, id):
        app.change_logged_screen("NoteInfo", id=id)


class NoteInfo(GridLayout):
    def __init__(self, app, id, **kw):
        super(NoteInfo, self).__init__(**kw)

        self.cols = 1
        self.padding = 100
        self.spacing = 20
        self.note = app.profile_manager.get_note(id)

        title = self.note.get_title()
        description = self.note.get_text()

        self.add_widget(ColorButton(text=title, font_size='24sp', font_name="Lemonada", background_color="#1b263b"))
        self.add_widget(ColorButton(text=description, background_color="#1b263b"))

        # buttons
        buttons = GridLayout()

        buttons.cols = 3
        buttons.add_widget(PrimaryButton(text="Edit", on_release=lambda x: self.edit(app, id)))
        buttons.add_widget(PrimaryButton(text="Delete", on_release=lambda x: self.delete(app)))
        buttons.add_widget(PrimaryButton(text="Cancel", on_release=lambda x: self.cancel(app)))

        self.add_widget(buttons)

    def edit(self, app, id):
        app.change_logged_screen("NoteEdit", id=id)

    def delete(self, app):
        Factory.ConfirmPopup(text="The data cannot be recovered.", function=self.delete_confirmed, app=app).open()

    def delete_confirmed(self, app):
        app.profile_manager.delete_note(self.note)
        app.change_logged_screen("Base")

    def cancel(self, app):
        app.change_logged_screen("Base")

class Note(GridLayout):
    def __init__(self, app, id, note, **kw):
        super(Note, self).__init__(**kw)

        self.cols = 1
        self.id = id
        self.note = note

        self.size_hint_y = None
        self.height = 70

        self.app = app

        title = note.get_title()
        description = note.get_text()

        # Title
        self.add_widget(NoteButton(text=title, background_color="#4E496F", bold=True, height=30))
        
        # Description
        self.add_widget(NoteButton(text=description, background_color="#7871AA"))

    def on_touch_down(self, touch):
        self.app.change_logged_screen("NoteInfo", self.id)
        return super().on_touch_down(touch)


class NotesTable(GridLayout):
    def __init__(self, app, **kw):
        super(NotesTable, self).__init__(**kw)
        
        self.cols = 1
        all_notes_ids = app.profile_manager.get_all_notes_id()

        header = TitleButton(text="Notes", font_name="Lemonada")
        self.add_widget(header)

        scroll_list = ScrollGrid()

        id = 0

        for x in all_notes_ids:
            scroll_list.add_widget(Note(app=app, id=x,
                                        note=app.profile_manager.get_note(x)))
            id += 1

        scroll_view = ScrollView(do_scroll_x=False,
                                 do_scroll_y=True)
        scroll_view.add_widget(scroll_list)
        self.add_widget(scroll_view)
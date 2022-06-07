from datetime import date, timedelta, datetime

from kivy.factory import Factory
from kivy.uix.actionbar import ActionDropDown
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from App.GUI.Buttons import PrimaryButton, UsersButton, TopButton, TitleButton, NoteButton, MenuButton, ScrollGrid

from App.GUI.Event import EventInfo, SingleEvent, EventAdd


# TO DO button for exits ect


class DayMenu(GridLayout):
    def __init__(self, app, day, **kw):
        super(DayMenu, self).__init__(**kw)

        self.cols = 1
        self.add_widget(MenuPanel(app=app))

        current_date = app.profile_manager.get_date().strftime("%d %B %Y, %A")
        current_date_label = Label(text=current_date, size_hint_y=None, height=50, font_size='24sp', font_name="Lemonada")
        self.add_widget(current_date_label)

        day_info = GridLayout(cols=3, spacing=10)

        left = GridLayout(cols=1)
        left.add_widget(TitleButton(text="Events", font_name="Lemonada"))
        left.add_widget(OneDayLayoutClickable(app=app, day=day, header=False))

        day_info.add_widget(left)

        day_info.add_widget(EventInfo(app=app))

        right = GridLayout()
        right.cols = 1
        right.add_widget(NotesTable(app=app))

        day_info.add_widget(right)

        self.add_widget(day_info)

class NoteAdd(GridLayout):
    def __init__(self, app, **kw):
        super(NoteAdd, self).__init__(**kw)
        self.cols = 1
        
        title = "title"
        desc = "description"

        self.title = TextInput()
        self.title.text = title
        self.add_widget(self.title)

        self.desc = TextInput()
        self.desc.text = desc
        self.add_widget(self.desc)

        buttons = GridLayout()
        buttons.cols = 2

        buttons.add_widget(PrimaryButton(text="Accept", on_release= lambda x: self.accept(app)))
        buttons.add_widget(PrimaryButton(text="Back", on_release=  lambda x: self.back(app)))
        
        self.add_widget(buttons)

    def accept(self, app):
        
        #add note
        app.profile_manager.add_note(self.title.text, self.desc.text)


        self.back(app)

    def back(self, app):
        app.change_logged_screen("Base")


class NoteEdit(GridLayout):
    def __init__(self, app, id, **kw):
        super(NoteEdit, self).__init__(**kw)

        self.cols = 1

        note = app.profile_manager.get_note(id)

        title = note.get_title()
        description = note.get_text()

        self.title = TextInput()
        self.title.text = title
        self.add_widget(self.title)

        self.short_desc = TextInput()
        self.short_desc.text = description
        self.add_widget(self.short_desc)

        # buttons

        buttons = GridLayout()
        buttons.cols = 2
        buttons.add_widget(PrimaryButton(text="Accept", on_release=lambda x: self.accept(app, id, self.title.text,
                                                                                         self.short_desc.text)))  # TODO: saving changes to temporary json
        buttons.add_widget(
            PrimaryButton(text="Cancel", on_release=lambda x: app.change_logged_screen("NoteInfo", id=id)))

        self.add_widget(buttons)

    def accept(self, app, id, title, short_desc):
        app.profile_manager.set_note(title, short_desc, id)
        app.change_logged_screen("NoteInfo", id=id)


class NoteInfo(GridLayout):
    def __init__(self, app, id, **kw):
        super(NoteInfo, self).__init__(**kw)

        self.cols = 1

        self.note = app.profile_manager.get_note(id)

        

        title = self.note.get_title()
        description = self.note.get_text()

        self.add_widget(Label(text=title))
        self.add_widget(Label(text=description))

        # buttons
        buttons = GridLayout()

        buttons.cols = 3
        buttons.add_widget(PrimaryButton(text="Edit", on_release=lambda x: app.change_logged_screen("NoteEdit", id=id)))
        buttons.add_widget(
            PrimaryButton(text="Delete", on_release=lambda x: self.delete(app)))
        buttons.add_widget(PrimaryButton(text="Cancel", on_release=lambda x: app.change_logged_screen("Base")))

        self.add_widget(buttons)

    def delete(self, app):
        app.profile_manager.delete_note(self.note)

        app.change_logged_screen("Base")


class Note(GridLayout):
    def __init__(self, app, function, id, note, **kw):
        super(Note, self).__init__(**kw)

        self.cols = 1
        self.id = id
        self.note = note

        self.size_hint_y = None
        self.height = 70

        self.on_release = function

        title = note.get_title()
        description = note.get_text()

        self.add_widget(NoteButton(text=title, background_color="#4E496F", bold=True, height=30))
        self.add_widget(NoteButton(text=description, background_color="#7871AA"))

    def on_touch_down(self, touch):
        self.on_release("NoteInfo", self.id)
        return super().on_touch_down(touch)


class NotesTable(GridLayout):
    def __init__(self, app, **kw):
        super(NotesTable, self).__init__(**kw)
        self.cols = 1
        allNotesID = app.profile_manager.get_all_notes_id()

        header = TitleButton(text="Notes", font_name="Lemonada")
        self.add_widget(header)

        scroll_list = ScrollGrid()

        id = 0
        for x in allNotesID:
            scroll_list.add_widget(Note(app=app, function=app.change_logged_screen, id=x,
                                        note=app.profile_manager.get_note(x)))
            id += 1

        scroll_view = ScrollView(do_scroll_x=False,
                                 do_scroll_y=True)
        scroll_view.add_widget(scroll_list)
        self.add_widget(scroll_view)


class MenuPanel(BoxLayout):
    def __init__(self, app, **kw):
        super(MenuPanel, self).__init__(**kw)

        self.size_hint_y = None
        self.height = 90
        self.padding = (0, 20)
        self.spacing = 10

        self.dropdown = ActionDropDown(size_hint_x=None, width=200)
        self.dropdown.container.spacing = -3
        self.dropdown.add_widget(TopButton(text="Save", on_release=lambda x: self.opt1(app)))
        self.dropdown.add_widget(TopButton(text="Reset", on_release=lambda x: self.opt2(app)))
        self.dropdown.add_widget(TopButton(text="Back", on_release=lambda x: self.opt3(app)))

        dropdown_btn = MenuButton()

        dropdown_btn.bind(on_release=self.dropdown.open)

        self.add_widget(dropdown_btn)
        self.add_widget(
            PrimaryButton(text="+ Event", on_release=lambda _: self.event_add(app), size_hint=(None, None), width=100,
                          height=50))

        self.add_widget(DateShower(app=app))

        self.add_widget(
            PrimaryButton(text="+ Note", on_release=lambda _: self.note_add(app), size_hint=(None, None), width=100,
                          height=50))

        swap_view_button = PrimaryButton(text="Swap view", on_release=lambda _: self.swap_view(app))
        self.add_widget(swap_view_button)

    def opt1(self, app):
        self.dropdown.dismiss()
        app.profile_manager.save_profile()

    def opt2(self, app):
        self.dropdown.dismiss()
        app.change_logged_screen("Base")
        app.profile_manager.load_user_data()

    def opt3(self, app):
        self.dropdown.dismiss()
        app.back_to_login()

    def swap_view(self, app):
        app.profile_manager.actual_date = app.profile_manager.actual_date
        app.changeBase()
        app.change_logged_screen("Base")

    def event_add(self, app):
        app.change_logged_screen("EventAdd")

    def note_add(self, app):
        app.change_logged_screen("NoteAdd")


class OneDayLayoutClickable(GridLayout):
    def __init__(self, app, day, header=True, **kw):
        super(OneDayLayoutClickable, self).__init__(**kw)
        self.cols = 1
        self.time = app.profile_manager.actual_date
        scrollable_events = ScrollView(do_scroll_x=False,
                                       do_scroll_y=True)
        scroll_list = ScrollGrid()
        if day != -1:
            week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

            for x in week:
                if self.time.strftime("%a") == x:
                    break
                else:
                    day -= 1

            self.time += timedelta(days=day)

        day_ = int(self.time.strftime("%d"))
        month_ = int(self.time.strftime("%m"))
        year_ = int(self.time.strftime("%Y"))

        day__ = app.profile_manager.get_events_of_day(day_, month_, year_)

        if day__ is not None:
            for x in day__.get_events():
                scroll_list.add_widget(SingleEvent(app=app, event=x, time=self.time))

        scrollable_events.add_widget(scroll_list)

        self.swap_function = app.changeBase
        self.swap_function_2 = app.change_logged_screen
        if header: self.add_header(app)
        self.add_widget(scrollable_events)

    def swapFunction(self, app):
        app.profile_manager.actual_date = self.time
        self.swap_function()
        self.swap_function_2("Base")

    def add_header(self, app):
        is_today = (self.time.strftime("%d%m%Y") == datetime.now().strftime("%d%m%Y"))
        event_header = TitleButton(on_release=lambda _: self.swapFunction(app))
        event_header.is_selected = is_today
        event_header.day_number = self.time.strftime("%d")
        event_header.day_name = self.time.strftime("%A")
        self.add_widget(event_header)


class DateShower(GridLayout):
    def __init__(self, app, **kw):
        super(DateShower, self).__init__(**kw)
        self.cols = 3
        self.height = 50
        self.app = app
        self.size_hint_y = None
        self.add_widget(PrimaryButton(text="<<",
                                      on_release=lambda x: self.change_date(
                                          - 7 * (app.base == "WeekMenu") - 1 * (app.base != "WeekMenu")),
                                      size_hint=(None, None), width=50, height=50))

        date_buttons = Button(size_hint=(None, None),
                              background_normal='resources/calendar.png',
                              height=50,
                              width=100,
                              on_release=lambda x: Factory.DateChanger(app).open())

        self.add_widget(date_buttons)
        self.add_widget(PrimaryButton(text=">>", on_release=lambda x: self.change_date(
            7 * (app.base == "WeekMenu") + 1 * (app.base != "WeekMenu")),
                                      size_hint=(None, None), width=50, height=50))

    def change_date(self, days):
        self.app.reset_actual_event()
        self.app.profile_manager.change_actual_date(days)
        self.app.change_logged_screen("Base")


class DateChanger(Popup):
    def __init__(self, app, **kw):
        super(DateChanger, self).__init__(**kw)
        self.size_hint = (.7, .7)
        self.cols = 1
        self.title = ""
        layout = GridLayout(cols=1,
                            spacing=10,
                            padding=20)

        textField = TextInput()
        textField.text = str(app.profile_manager.get_date()).split(" ")[0]

        layout.add_widget(textField)

        buttonsGrid = GridLayout()
        buttonsGrid.cols = 2
        buttonsGrid.add_widget(PrimaryButton(text="Accept", on_release=lambda x: self.accept(app, textField.text)))
        buttonsGrid.add_widget(PrimaryButton(text="Cancel", on_release=lambda x: self.dismiss()))

        layout.add_widget(buttonsGrid)
        self.add_widget(layout)

    def accept(self, app, date_):
        self.dismiss()
        if len(date_.split("-")) != 3:
            return

        if len(date_.split("-")[0]) != 4:
            return

        if len(date_.split("-")[1]) < 1 or len(date_.split("-")[1]) > 2:
            return

        if len(date_.split("-")[2]) < 1 or len(date_.split("-")[2]) > 2:
            return

        app.profile_manager.set_actual_date(
            date(int(date_.split("-")[0]), int(date_.split("-")[1]), int(date_.split("-")[2])))

        app.change_logged_screen("Base")


class WeekMenu(GridLayout):
    def __init__(self, app, **kw):
        super(WeekMenu, self).__init__(**kw)
        self.cols = 1

        self.add_widget(MenuPanel(app=app))

        week_grid = GridLayout(cols=4)
        left_range, right_range = app.profile_manager.get_date_range()
        left_range, right_range = left_range.strftime("%b %d, %Y"), right_range.strftime("%b %d, %Y")

        date_range_label = Label(text=left_range+" - "+right_range, size_hint_y=None, height=50, font_size='24sp', font_name="Lemonada")
        self.add_widget(date_range_label)

        for x in range(7):
            week_grid.add_widget(OneDayLayoutClickable(app=app, day=x))


        week_grid.add_widget(NotesTable(app=app))


        self.add_widget(week_grid)

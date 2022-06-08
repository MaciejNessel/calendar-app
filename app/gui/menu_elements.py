import re
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
from app.gui.buttons import PrimaryButton, TopButton, TitleButton, MenuButton, ScrollGrid

from app.gui.event import EventInfo, SingleEvent
from app.gui.note import NotesTable


# TO DO button for exits ect


class ConfirmPopup(Popup):
    def __init__(self, text, function, app=None, **kw):
        super(ConfirmPopup, self).__init__(**kw)
        
        self.title = ""
        self.size_hint = (.7, .7)
        self.background = ""
        self.background_color = "#0d1b2a"
        self.layout = GridLayout(cols=1)
        self.layout.add_widget(Label(text=text))

        confirm_btn = PrimaryButton(text='Confirm',
                                    size_hint=(1, .2))
        if app:
            confirm_btn.bind(on_release=lambda x: (function(app), self.dismiss()))
        else:
            confirm_btn.bind(on_release=lambda x: (function(), self.dismiss()))
        self.layout.add_widget(confirm_btn)

        back_btn = PrimaryButton(text='Cancel',
                                 on_release=lambda x: self.dismiss(),
                                 size_hint=(1, .2))
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)


class DayMenu(GridLayout):
    def __init__(self, app, day, **kw):
        super(DayMenu, self).__init__(**kw)

        self.cols = 1
        self.add_widget(MenuPanel(app=app))

        current_date = app.profile_manager.get_date().strftime("%d %B %Y, %A")
        current_date_label = Label(text=current_date, size_hint_y=None, height=50, font_size='24sp',
                                   font_name="Lemonada")
        self.add_widget(current_date_label)

        day_info = GridLayout(cols=3, spacing=10)

        left = GridLayout(cols=1)
        left.add_widget(TitleButton(text="events", font_name="Lemonada"))
        left.add_widget(OneDayLayoutClickable(app=app, day=day, header=False))

        day_info.add_widget(left)

        day_info.add_widget(EventInfo(app=app))

        right = GridLayout()
        right.cols = 1
        right.add_widget(NotesTable(app=app))

        day_info.add_widget(right)

        self.add_widget(day_info)


class MenuPanel(BoxLayout):
    def __init__(self, app, **kw):
        super(MenuPanel, self).__init__(**kw)

        self.size_hint_y = None
        self.height = 90
        self.padding = (0, 20)
        self.spacing = 10

        self.dropdown = ActionDropDown(size_hint_x=None, width=200)
        self.dropdown.container.spacing = -3
        self.dropdown.add_widget(TopButton(text="Save", on_release=lambda x: self.save_profile(app)))
        self.dropdown.add_widget(TopButton(text="Reset", on_release=lambda x: self.reset_profile(app)))
        self.dropdown.add_widget(TopButton(text="Export", on_release=lambda x: self.export_profile(app)))
        self.dropdown.add_widget(TopButton(text="Back", on_release=lambda x: self.back(app)))

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

    def save_profile(self, app):
        self.dropdown.dismiss()
        app.profile_manager.save_profile()
        Factory.Message(text="Successfully saved").open()

    def reset_profile(self, app):
        self.dropdown.dismiss()
        Factory.ConfirmPopup(text="Unsaved data will be lost", function=self.reset_function, app=app).open()

    def reset_function(self, app):
        app.profile_manager.load_user_data()
        app.change_logged_screen("Base")

    def export_profile(self, app):
        url = app.profile_manager.export_profile()
        Factory.MessageCopy(text="Exported successfully", copy=url).open()

    def back(self, app):
        self.dropdown.dismiss()
        Factory.ConfirmPopup(text="Unsaved data will be lost", function=app.back_to_login).open()

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
        self.time = app.profile_manager.get_date()

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

        # date = [day, month, year]
        date = []
        date.append(int(self.time.strftime("%d")))
        date.append(int(self.time.strftime("%m")))
        date.append(int(self.time.strftime("%Y")))

        actual_day = app.profile_manager.get_day(date[0], date[1], date[2])

        events = []

        id = 0

        if actual_day is not None:
            for event in actual_day.get_events():
                events.append((event["start"], id, SingleEvent(app=app, event=event, time=self.time)))
                id += 1

        events.sort(reverse=False)

        for event in events:
            scroll_list.add_widget(event[2])

        scrollable_events.add_widget(scroll_list)

        if header: self.add_header(app)
        self.add_widget(scrollable_events)

    def swapFunction(self, app):
        app.profile_manager.actual_date = self.time
        app.changeBase()
        app.change_logged_screen("Base")

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
        self.background = ""
        self.background_color = "#0d1b2a"
        self.title = "Go to"
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

        if not re.search("^[0-9]{4}-[0-9]{2}-[0-9]{2}$", date_):
            Factory.Error(text="Wrong date format.").open()
            return

        year = int(date_.split("-")[0])
        month = int(date_.split("-")[1])
        day = int(date_.split("-")[2])

        if day > 31 or day < 1:
            Factory.Error(text="The wrong day number was given").open()
            return
        if month > 12 or month < 1:
            Factory.Error(text="The wrong month number was given").open()
            return

        try:
            app.profile_manager.set_actual_date(date(year, month, day))
        except ValueError:
            Factory.Error(text="Day is out of range for month").open()

        app.change_logged_screen("Base")


class WeekMenu(GridLayout):
    def __init__(self, app, **kw):
        super(WeekMenu, self).__init__(**kw)
        self.cols = 1

        self.add_widget(MenuPanel(app=app))

        week_grid = GridLayout(cols=4)
        left_range, right_range = app.profile_manager.get_date_range()
        left_range, right_range = left_range.strftime("%b %d, %Y"), right_range.strftime("%b %d, %Y")

        date_range_label = Label(text=left_range + " - " + right_range, size_hint_y=None, height=50, font_size='24sp',
                                 font_name="Lemonada")
        self.add_widget(date_range_label)

        for x in range(7):
            week_grid.add_widget(OneDayLayoutClickable(app=app, day=x))

        week_grid.add_widget(NotesTable(app=app))

        self.add_widget(week_grid)

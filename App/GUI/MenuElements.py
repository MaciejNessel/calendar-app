from cgi import test
from datetime import date, timedelta
from pickle import SHORT_BINUNICODE
from re import S
from sqlite3 import Date
from tkinter import Button, Grid, Menu
from turtle import onrelease
from typing import OrderedDict, Text
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from matplotlib.pyplot import text
from numpy import short
from urllib3 import encode_multipart_formdata

from App.Json.JsonManager import JsonManager
from App.GUI.Message import Message
from App.GUI.Error import Error
from App.GUI.Buttons import PrimaryButton, UsersButton

# TO DO button for exits ect

class EventInfo(GridLayout):
    def __init__(self, app, **kw):
        super(EventInfo, self).__init__(**kw)

        self.cols = 1
    
        if app.actualEvent != None:
            event_id = app.actualEvent

            self.event = app.profile_manager.get_event(event_id)

            title = self.event.get_title()
            short_desc = self.event.get_short_desc()
            desc = self.event.get_desc()

            self.title = TextInput()
            self.title.text = title
            self.add_widget(self.title)

            self.short_desc = TextInput()
            self.short_desc.text = short_desc
            self.add_widget(self.short_desc)

            self.desc = TextInput()
            self.desc.text = desc
            self.add_widget(self.desc)

            self.add_widget(PrimaryButton(text="Save Changes", on_release = lambda x: self.edit_event(app)))

    def edit_event(self, app):
        self.event.set_title(str(self.title.text))
        self.event.set_short_desc(str(self.short_desc.text))
        self.event.set_desc(str(self.desc.text))
        app.profile_manager.save_event(self.event)
        app.change_logged_screen("Base")


class Event(GridLayout):
    def __init__(self, app, event, time, **kw):
        super(Event, self).__init__(**kw)

        self.cols = 1

        event_id = event["id_"]
        start = event["start"]
        end = event["end"]

        event_ = app.profile_manager.get_event(event_id)

        title = event_.get_title()
        self.time = app.profile_manager.actual_date  # .strftime("%x")
        short_desc = event_.get_short_desc()

        self.id = event_id

        self.app = app

        self.time = time


        self.add_widget(PrimaryButton(text=title, on_release = lambda x: self.onrel()))
        self.add_widget(PrimaryButton(text=self.time.strftime("%x"), on_release = lambda x: self.onrel()))
        self.add_widget(PrimaryButton(text=short_desc, on_release = lambda x: self.onrel()))


    def onrel(self):
        self.app.actualEvent = self.id
        self.app.profile_manager.set_actual_date(self.time)
        self.app.set_base("DayMenu")
        self.app.change_logged_screen("Base")

class DayMenu(GridLayout):
    def __init__(self, app, day, **kw):
        super(DayMenu, self).__init__(**kw)

        self.cols = 3

        left = GridLayout()
        left.cols = 1
        left.add_widget(DateShower(app=app))
        left.add_widget(OneDayLayoutClickable(app=app, day=day))

        self.add_widget(left)

        self.add_widget(EventInfo(app=app))

        right = GridLayout()
        right.cols = 1
        right.add_widget(MenuPanel(app=app))
        right.add_widget(NotesTable(app=app))

        self.add_widget(right)

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
        buttons.add_widget(PrimaryButton(text="Accept", on_release = lambda x: self.accept(app, id, self.title.text, self.short_desc.text))) #TODO: saving changes to temporary json
        buttons.add_widget(PrimaryButton(text="Cancel", on_release = lambda x: app.change_logged_screen("NoteInfo", id=id)))

        self.add_widget(buttons)

    def accept(self, app, id, title, short_desc):
        app.profile_manager.set_note(title, short_desc, id)
        app.change_logged_screen("NoteInfo", id=id)

class NoteInfo(GridLayout):
    def __init__(self, app, id, **kw):
        super(NoteInfo, self).__init__(**kw)

        self.cols = 1

        note = app.profile_manager.get_note(id)

        title = note.get_title()
        description = note.get_text()

        self.add_widget(Label(text=title))
        self.add_widget(Label(text=description))

        # buttons
        buttons = GridLayout()

        buttons.cols = 3
        buttons.add_widget(PrimaryButton(text="Edit", on_release = lambda x: app.change_logged_screen("NoteEdit", id=id)))
        buttons.add_widget(PrimaryButton(text="Delete", on_release = lambda x: app.change_logged_screen("NoteEdit", id=id)))
        buttons.add_widget(PrimaryButton(text="Cancel", on_release = lambda x: app.change_logged_screen("Base")))

        self.add_widget(buttons)

class Note(GridLayout):
    def __init__(self, app, function, id, note, **kw):
        super(Note, self).__init__(**kw)

        self.cols = 1
        self.id = id
        self.note = note

        self.on_release = function

        title = note.get_title()
        description = note.get_text()

        self.add_widget(Label(text = title))
        self.add_widget(Label(text = description))

    def on_touch_down(self, touch):
        self.on_release("NoteInfo", self.id)
        return super().on_touch_down(touch)

class NotesTable(ScrollView):
    def __init__(self, app, **kw):
        super(NotesTable, self).__init__(**kw)

        self.do_scroll_y = True
        

        allNotesID = app.profile_manager.get_all_notes_id()

        id = 0

        scroll_list = GridLayout()
        scroll_list.row_default_height = 10     # TO DO: set up height of one note!
        scroll_list.cols = 1

        for x in allNotesID:
            scroll_list.add_widget(Note(app=app, function=app.change_logged_screen, id = x, note = app.profile_manager.get_note(x)))    # TO DO: fill with notes
            id+=1

        self.add_widget(scroll_list)


class MenuPanel(GridLayout):
    def __init__(self, app, **kw):
        super(MenuPanel, self).__init__(**kw)
        self.cols = 3

        self.add_widget(PrimaryButton(text="S", on_release = lambda x: self.opt1(app)))
        self.add_widget(PrimaryButton(text="R", on_release = lambda x: self.opt2(app)))
        self.add_widget(PrimaryButton(text="B", on_release = lambda x: self.opt3(app)))

    def opt1(self, app):
        app.profile_manager.save_profile()

    def opt2(self, app):
        app.change_logged_screen("Base")
        app.profile_manager.load_user_data()

    def opt3(self, app):
        app.back_to_login()

class EventAdd(GridLayout):
    def __init__(self, app, **kwargs):
        super(EventAdd, self).__init__(**kwargs)

        self.cols = 1

        title = "title"
        short_desc = "short_desc"
        desc = "full desc"
        date = str(app.profile_manager.actual_date.strftime("%x"))
        start = "00:00"
        end = "24:00"

        self.title = TextInput()
        self.title.text = title
        self.add_widget(self.title)

        self.short_desc = TextInput()
        self.short_desc.text = short_desc
        self.add_widget(self.short_desc)

        self.desc = TextInput()
        self.desc.text = desc
        self.add_widget(self.desc)

        self.date = TextInput()
        self.date.text = date
        self.add_widget(self.date)

        self.start = TextInput()
        self.start.text = start
        self.add_widget(self.start)

        self.end = TextInput()
        self.end.text = end
        self.add_widget(self.end)

        buttons = GridLayout()
        buttons.cols = 2
        buttons.add_widget(PrimaryButton(text="Accept", on_release = lambda x: self.add(app)))
        buttons.add_widget(PrimaryButton(text="Back", on_release = lambda x: self.back(app)))

        self.add_widget(buttons)

    def add(self, app):
        # todo: data validation

        # create event, eventy dla dnia sa w dict o id rownych iod wydarzeń
        event_id = app.profile_manager.event_manager.add(title=self.title.text, short_desc=self.short_desc.text, desc=self.desc.text)
        # add to day list
        app.profile_manager.day_manager.add_event_to_day(date=self.date.text, event_id=event_id, start=self.start.text, end=self.end.text)
        self.back(app)

    def back(self, app):
        app.change_logged_screen("Base")

class OneDayLayoutClickable(GridLayout):
    def __init__(self, app, day, **kw):
        super(OneDayLayoutClickable, self).__init__(**kw)
        self.cols = 1

        self.time = app.profile_manager.actual_date  # .strftime("%x")

        scrollable_events = ScrollView()
        scrollable_events.do_scroll_y = True

        scroll_list = GridLayout()
        scroll_list.cols = 1

        scroll_list.row_default_height = 20
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


        if day__ != None:
            for x in day__.get_events():
                print(type(x))
                scroll_list.add_widget(Event(app=app, event=x, time=self.time))





        scrollable_events.add_widget(scroll_list)

        self.add_widget(scrollable_events)
        
        options_panel = GridLayout()
        options_panel.cols = 3
        options_panel.add_widget(PrimaryButton(text = "+", on_release = lambda x: self.event_add(app)))
        options_panel.add_widget(PrimaryButton(text = self.time.strftime("%x")))

        self.swap_function = app.changeBase
        self.swap_function_2 = app.change_logged_screen
        options_panel.add_widget(PrimaryButton(text = "SWAP", on_release= lambda x: self.swapFunction(app)))

        self.add_widget(options_panel)

    def event_add(self, app):
        app.change_logged_screen("EventAdd")

    def swapFunction(self, app):
        app.profile_manager.actual_date = self.time
        self.swap_function()
        self.swap_function_2("Base")

        

class DateShower(GridLayout):
    def __init__(self, app, **kw):
        super(DateShower, self).__init__(**kw)

        date_text = str(app.profile_manager.actual_date.strftime("%x"))

        self.cols = 3

        self.app = app

        self.add_widget(PrimaryButton(text="<<", on_release = lambda x: self.change_date( - 7 * (app.base == "WeekMenu") - 1 * (app.base != "WeekMenu"))))

        date_buttons = PrimaryButton(text=date_text, on_release = lambda x: app.change_logged_screen("DateChanger"))

        self.add_widget(date_buttons)
        self.add_widget(PrimaryButton(text=">>", on_release = lambda x: self.change_date(7 * (app.base == "WeekMenu") + 1 * (app.base != "WeekMenu"))))

    def change_date(self, days):
        self.app.profile_manager.change_actual_date(days)
        self.app.change_logged_screen("Base")


class DateChanger(GridLayout):
    def __init__(self, app, **kw):
        super(DateChanger, self).__init__(**kw)

        self.cols = 1

        textField = TextInput()
        textField.text = str(app.profile_manager.get_date()).split(" ")[0]

        self.add_widget(textField)

        buttonsGrid = GridLayout()
        buttonsGrid.cols = 2
        buttonsGrid.add_widget(PrimaryButton(text="Accept", on_release = lambda x: self.accept(app, textField.text)))
        buttonsGrid.add_widget(PrimaryButton(text="Cancel", on_release = lambda x: app.change_logged_screen("Base")))

        self.add_widget(buttonsGrid)

    def accept(self, app, date_):
        if len(date_.split("-")) != 3:
            return

        if len(date_.split("-")[0]) != 4:
            return

        if len(date_.split("-")[1]) < 1 or len(date_.split("-")[1]) > 2:
            return

        if len(date_.split("-")[2]) < 1 or len(date_.split("-")[2]) > 2:
            return

        app.profile_manager.set_actual_date(date(int(date_.split("-")[0]), int(date_.split("-")[1]), int(date_.split("-")[2])))

        app.change_logged_screen("Base")
        

class WeekMenu(GridLayout):
    def __init__(self, app, **kw):
        super(WeekMenu, self).__init__(**kw)
        self.cols = 4

        for x in range(3):
            self.add_widget(OneDayLayoutClickable(app=app, day=x))

        gridv1 = GridLayout()
        gridv1.cols = 1

        menu_panel = MenuPanel(app=app)

        gridv1.add_widget(MenuPanel(app=app))
        gridv1.add_widget(NotesTable(app=app))

        self.add_widget(gridv1)

        for x in range(3):
            self.add_widget(OneDayLayoutClickable(app=app, day=x+3))
        
        gridv2 = GridLayout()
        gridv2.cols = 1
        gridv2.add_widget(DateShower(app=app))
        gridv2.add_widget(OneDayLayoutClickable(app=app, day=6))

        self.add_widget(gridv2)
        


"""class WeekMenu(GridLayout):
    def __init__(self, app, **kw):
        super(WeekMenu, self).__init__(**kw)
        self.cols = 2
        self.padding = 0
        self.spacing = 20
        self.add_widget(0)


        LabelBase.register(name='Lemonada',
                           fn_regular='lemonada.ttf')
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
        self.add_widget(export_btn)"""

from codecs import getincrementaldecoder
from kivy.factory import Factory
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from App.GUI.Buttons import PrimaryButton, EventButton, ColorButton, DatesButton, ScrollGrid
import re


class EventEdit(Popup):
    def __init__(self, app, event, **kw):
        super(EventEdit, self).__init__(**kw)
        self.event = event

        self.size_hint = (.7, .7)
        self.background_color = '#0d1b2a'
        layout = GridLayout(cols=1,
                            spacing=10,
                            padding=20)

        self.title_input = TextInput(text=event.get_title())
        layout.add_widget(self.title_input)

        self.short_desc_input = TextInput(text=event.get_short_desc())
        layout.add_widget(self.short_desc_input)

        self.desc_input = TextInput(text=event.get_desc())
        layout.add_widget(self.desc_input)

        self.main_btn = PrimaryButton(text='Accept', on_release=lambda x: self.edit_event(app))

        layout.add_widget(self.main_btn)

        back_btn = PrimaryButton(text='Back',
                                 on_release=lambda x: self.dismiss())
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def edit_event(self, app):
        self.dismiss()
        self.event.set_title(str(self.title_input.text))
        self.event.set_short_desc(str(self.short_desc_input.text))
        self.event.set_desc(str(self.desc_input.text))
        app.profile_manager.save_event(self.event)
        app.change_logged_screen("Base")


class EventInfo(GridLayout):
    def __init__(self, app, **kw):
        super(EventInfo, self).__init__(**kw)

        self.cols = 1
        event_id = app.actualEvent
        if not event_id or event_id == None:
            return

        self.event = app.profile_manager.get_event(event_id)

        self.title = self.event.get_title()
        self.short_desc = self.event.get_short_desc()
        self.desc = self.event.get_desc()
        self.color = self.event.get_color()

        self.add_widget(
            EventButton(text=self.title, background_color=self.color, font_size='24sp', size_hint_y=None, bold=True))
        self.add_widget(EventButton(text=self.short_desc, background_color=self.color, size_hint_y=None))
        self.add_widget(EventButton(text=self.desc, background_color=self.color, size_hint_y=None))

        buttons = GridLayout()
        buttons.cols = 2

        buttons.add_widget(
            PrimaryButton(text="Edit event", on_release=lambda x: Factory.EventEdit(app, self.event).open()))
        buttons.add_widget(PrimaryButton(text="Delete event", on_release=lambda x: self.delete(app)))

        self.add_widget(buttons)

    def delete(self, app):
        app.actualEvent = None

        app.profile_manager.delete_event(self.event)

        app.change_logged_screen("Base")


class SingleEvent(GridLayout):
    def __init__(self, app, event, time, **kw):
        super(SingleEvent, self).__init__(**kw)

        self.cols = 1

        event_id = event["id_"]
        start = event["start"]
        end = event["end"]
        self.size_hint_y = None
        self.height = 75

        event_ = app.profile_manager.get_event(event_id)

        if event_ == None:
            return

        title = event_.get_title()
        self.time = app.profile_manager.actual_date
        short_desc = event_.get_short_desc()
        color = event_.get_color()
        self.id = event_id
        self.app = app
        self.time = time

        header = EventButton(text=start + " - " + end, on_release=lambda x: self.onrel(), background_color=color,
                             bold=True)
        header.is_header = True
        self.add_widget(header)
        self.add_widget(EventButton(text=title, on_release=lambda x: self.onrel(), background_color=color, bold=True))
        self.add_widget(EventButton(text=short_desc, on_release=lambda x: self.onrel(), background_color=color))

    def onrel(self):
        self.app.actualEvent = self.id
        self.app.profile_manager.set_actual_date(self.time)
        self.app.set_base("DayMenu")
        self.app.change_logged_screen("Base")


class EventAdd(GridLayout):
    def __init__(self, app, **kwargs):
        super(EventAdd, self).__init__(**kwargs)
        self.color = "#000000"
        self.cols = 1
        self.spacing = 10
        self.padding = 20

        self.dates = []

        self.title = TextInput(size_hint_y=None, height=40)
        self.title.text = "title"
        self.add_widget(Label(text="Title", font_size='15sp', font_name="Lemonada", size_hint_y=None, height=15))
        self.add_widget(self.title)

        self.short_desc = TextInput(size_hint_y=None, height=40)
        self.short_desc.text = "short_desc"
        self.add_widget(Label(text="Short description", font_size='15sp', font_name="Lemonada", size_hint_y=None, height=15))
        self.add_widget(self.short_desc)

        self.desc = TextInput(size_hint_y=None, height=60)
        self.desc.text = "full desc"
        self.add_widget(Label(text="Description", font_size='15sp', font_name="Lemonada", size_hint_y=None, height=15))
        self.add_widget(self.desc)

        self.add_widget(Label(text="Color", font_size='15sp', font_name="Lemonada", size_hint_y=None, height=15))
        color_button = ColorButton(text="Change color", background_color=self.color)
        color_button.bind(on_release=lambda _: self.color_popup(color_button))
        self.add_widget(color_button)

        self.add_widget(Label(text="Dates", font_size='15sp', font_name="Lemonada", size_hint_y=None, height=15))
        date_button = PrimaryButton(text="Add date", on_release=lambda _: self.date_popup(app))
        self.dates_layout = ScrollGrid(cols=10)
        self.add_widget(date_button)
        self.add_widget(
            Label(text="click on a date to delete", font_size='10sp', font_name="Lemonada", size_hint_y=None,
                  height=15))

        date_layout_scroll = ScrollView(do_scroll_x=False,
                                        do_scroll_y=True)
        date_layout_scroll.add_widget(self.dates_layout)
        self.add_widget(date_layout_scroll)

        buttons = GridLayout()
        buttons.cols = 2
        buttons.add_widget(PrimaryButton(text="Accept", on_release=lambda x: self.add(app)))
        buttons.add_widget(PrimaryButton(text="Back", on_release=lambda x: self.back(app)))

        self.add_widget(buttons)

    def add(self, app):
        if not self.data_validation():
            return

        event_id = app.profile_manager.event_manager.add(title=self.title.text, short_desc=self.short_desc.text,
                                                         desc=self.desc.text, color=self.color)
        for el in self.dates:
            date = el.get('date')
            start = el.get('start')
            end = el.get('end')
            if not (date and start and end):
                return
            app.profile_manager.day_manager.add_event_to_day(date=date, event_id=event_id, start=start,
                                                             end=end)
        if len(self.dates) < 1:
            Factory.Error(text="Add at least one date").open()
            return

        self.back(app)

    def back(self, app):
        app.change_logged_screen("Base")

    # To monitor changes, we can bind to color property changes
    def on_color(self, instance, value):
        self.color = str(instance.hex_color)

    def color_popup(self, color_button):
        def set_color():
            popup.dismiss()
            self.color = clr_picker.color
            color_button.background_color = self.color

        popup = Popup(title="Choose color", background="", background_color="#0d1b2a")
        layout = GridLayout(cols=1)

        clr_picker = ColorPicker()
        clr_picker.bind(color=self.on_color)
        layout.add_widget(clr_picker)

        set_button = PrimaryButton(text="Accept", on_release=lambda _: set_color(), size_hint_y=None, height=100)
        layout.add_widget(set_button)

        popup.add_widget(layout)
        popup.open()

    def date_popup(self, app):
        def remove_date(dates_button, to_add):
            self.dates_layout.remove_widget(dates_button)
            self.dates.remove(to_add)

        def add_date():
            to_add = {"date": date.text, "start": start.text, "end": end.text}

            if to_add in self.dates:
                Factory.Error(text="The date has been entered previously").open()
                return
            if not self.date_validate(to_add):
                Factory.Error(text="Enter a valid data format. \n Date: YYYY-MM-DD \n Start, End: HH:MM").open()
                return
            self.dates.append(to_add)
            dates_button = DatesButton(text=date.text + "\n" + start.text + " - " + end.text)
            dates_button.bind(on_release=lambda _: remove_date(dates_button, to_add))
            self.dates_layout.add_widget(dates_button)
            popup.dismiss()

        popup = Popup(title="Add date",  background="", background_color="#0d1b2a")
        layout = GridLayout(cols=1, spacing=30)

        date = TextInput(size_hint_y=None, height=40)
        date.text = str(app.profile_manager.actual_date.strftime("%Y-%m-%d"))
        layout.add_widget(Label(text="Date", font_size='15sp', font_name="Lemonada", size_hint_y=None, height=15))
        layout.add_widget(date)

        start = TextInput(size_hint_y=None, height=40)
        start.text = "00:00"
        layout.add_widget(Label(text="Start hour", font_size='15sp', font_name="Lemonada", size_hint_y=None, height=15))
        layout.add_widget(start)

        end = TextInput(size_hint_y=None, height=40)
        layout.add_widget(Label(text="End hour", font_size='15sp', font_name="Lemonada", size_hint_y=None, height=15))
        end.text = "00:00"
        layout.add_widget(end)

        buttons_grid = GridLayout(cols=2)

        accept_button = PrimaryButton(text="Accept", on_release=lambda _: add_date(), size_hint_y=None, height=100)
        buttons_grid.add_widget(accept_button)

        back_button = PrimaryButton(text="Back", on_release=lambda _: popup.dismiss(), size_hint_y=None, height=100)
        buttons_grid.add_widget(back_button)

        layout.add_widget(buttons_grid)

        popup.add_widget(layout)
        popup.open()

    def date_validate(self, to_validate):
        date = to_validate.get('date')
        start = to_validate.get('start')
        end = to_validate.get('end')

        if not re.search("^[0-9]{4}-[0-9]{2}-[0-9]{2}$", date) \
                or not re.search("^[0-1][0-9]:[0-5][0-9]$", start) \
                or not re.search("^[0-1][0-9]:[0-5][0-9]$", end):
            return False

        if start > end:
            return False

        return True

    def data_validation(self):
        if len(self.title.text) > 25:
            Factory.Error(text="The title entered is too long. \n Maximum length: 25").open()
            return False

        if len(self.short_desc.text) > 50:
            Factory.Error(text="The short description entered is too long. \n Maximum length: 50").open()
            return False

        if len(self.desc.text) > 200:
            Factory.Error(text="The description entered is too long. \n Maximum length: 200").open()
            return False

        return True

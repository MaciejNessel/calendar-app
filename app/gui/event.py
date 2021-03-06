from codecs import getincrementaldecoder
from kivy.factory import Factory
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from app.gui.buttons import PrimaryButton, EventButton, ColorButton, DatesButton, ScrollGrid
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
        event_id = app.actual_event
        if not event_id or event_id == None:
            return

        self.event = app.profile_manager.get_event(event_id)

        actual_date = str(app.profile_manager.get_date()).split(" ")[0]
        actual_start, actual_end = app.profile_manager.get_hours()

        if not app.profile_manager.is_event_in_day(event_id=event_id, date=actual_date):
            return

        self.title = self.event.get_title()
        self.short_desc = self.event.get_short_desc()
        self.desc = self.event.get_desc()
        self.color = self.event.get_color()

        self.add_widget(
            EventButton(text=self.title, background_color=self.color, font_size='24sp', size_hint_y=None, bold=True))
        self.add_widget(EventButton(text=self.short_desc, background_color=self.color, size_hint_y=None))
        self.add_widget(EventButton(text=self.desc, background_color=self.color, size_hint_y=None))

        buttons = GridLayout(size_hint_y=None)
        buttons.cols = 4

        buttons.add_widget(ColorButton(text="Edit", on_release=lambda x: Factory.EventEdit(app, self.event).open()))
        buttons.add_widget(ColorButton(text="Delete\n  all", on_release=lambda x: self.delete(app)))
        buttons.add_widget(ColorButton(text="Delete\n  one", on_release=lambda x: self.delete_one(app, actual_date, actual_start, actual_end)))
        buttons.add_widget(ColorButton(text="Add\ndate", on_release=lambda x: self.add_date_popup(app)))

        self.add_widget(buttons)

    def delete(self, app):
        app.actual_event = None

        app.profile_manager.delete_event(self.event)

        app.change_logged_screen("Base")

    def delete_one(self, app, date, start, end):
        app.actual_event = None
        app.profile_manager.delete_event_one(self.event, date, start, end)
        app.change_logged_screen("Base")

    def add_date_popup(self, app):
        popup = Popup(background="", background_color="#0d1b2a", title="Enter date", size_hint=[.7, .7])
        layout = GridLayout(cols=1)

        date_input = TextInput(text=str(app.profile_manager.actual_date.strftime("%Y-%m-%d")))
        layout.add_widget(Label(text="Date", font_size='15sp', font_name="Lemonada", size_hint_y=None, height=15))
        layout.add_widget(date_input)

        start_input = TextInput(text="00:00")
        layout.add_widget(Label(text="Start hour", font_size='15sp', font_name="Lemonada", size_hint_y=None, height=15))
        layout.add_widget(start_input)

        end_input = TextInput(text="00:00")
        layout.add_widget(Label(text="End hour", font_size='15sp', font_name="Lemonada", size_hint_y=None, height=15))
        layout.add_widget(end_input)

        layout.add_widget(PrimaryButton(text="Confirm",
                                        on_release=lambda _: self.add_date(app, date_input, start_input, end_input,
                                                                           popup)))

        layout.add_widget(PrimaryButton(text="Back", on_release=lambda _: popup.dismiss()))

        popup.add_widget(layout)
        popup.open()

    def add_date(self, app, date_input, start_input, end_input, popup):
        date = {
            'date': date_input.text,
            'start': start_input.text,
            'end': end_input.text
        }
        if not date_validate(date):
            Factory.Error(text="Wrong date format").open()
            return
        app.profile_manager.add_event_to_day(date.get('date', ''), app.actual_event, date.get('start', ''),
                                             date.get('end', ''))
        Factory.Message(text="Date was successfully added").open()
        app.change_logged_screen("Base")
        popup.dismiss()


class SingleEvent(GridLayout):
    def __init__(self, app, event, time, **kw):
        super(SingleEvent, self).__init__(**kw)
        self.cols = 1
        event_id = event["id_"]
        self.start = event["start"]
        self.end = event["end"]
        self.size_hint_y = None
        self.height = 75

        event_ = app.profile_manager.get_event(event_id)
        if not event_:
            return

        title = event_.get_title()
        self.time = app.profile_manager.actual_date
        short_desc = event_.get_short_desc()
        color = event_.get_color()
        self.id = event_id
        self.app = app
        self.time = time

        header = EventButton(text=self.start + " - " + self.end, on_release=lambda x: self.onrel(), background_color=color,
                             bold=True)
        header.is_header = True
        self.add_widget(header)
        self.add_widget(EventButton(text=title, on_release=lambda x: self.onrel(), background_color=color, bold=True))
        self.add_widget(EventButton(text=short_desc, on_release=lambda x: self.onrel(), background_color=color))

    def onrel(self):
        self.app.actual_event = self.id
        self.app.profile_manager.set_actual_date(self.time)
        self.app.profile_manager.set_actual_hours(self.start, self.end)
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
        self.add_widget(
            Label(text="Short description", font_size='15sp', font_name="Lemonada", size_hint_y=None, height=15))
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
            app.profile_manager.add_event_to_day(date=date, event_id=event_id, start=start,
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
            if not date_validate(to_add):
                Factory.Error(text="Enter a valid data format. \n Date: YYYY-MM-DD \n Start, End: HH:MM").open()
                return
            self.dates.append(to_add)
            dates_button = DatesButton(text=date.text + "\n" + start.text + " - " + end.text)
            dates_button.bind(on_release=lambda _: remove_date(dates_button, to_add))
            self.dates_layout.add_widget(dates_button)
            popup.dismiss()

        popup = Popup(title="Add date", background="", background_color="#0d1b2a")
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


def date_validate(to_validate):
    try:
        date = to_validate.get('date')
        start = to_validate.get('start')
        end = to_validate.get('end')
    except AttributeError:
        return False

    if not re.search("^[0-9]{4}-[0-9]{2}-[0-9]{2}$", date) \
            or not re.search("^[0-2][0-9]:[0-5][0-9]$", start) \
            or not re.search("^[0-2][0-9]:[0-5][0-9]$", end):
        return False

    if start > end:
        return False

    return True

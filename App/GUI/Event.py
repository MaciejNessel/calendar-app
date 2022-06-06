from kivy.factory import Factory
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

from App.GUI.Buttons import PrimaryButton, EventButton


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
        if not event_id:
            return

        self.event = app.profile_manager.get_event(event_id)

        self.title = self.event.get_title()
        self.short_desc = self.event.get_short_desc()
        self.desc = self.event.get_desc()
        self.color = self.event.get_color()

        self.add_widget(EventButton(text=self.title, background_color=self.color, font_size='24sp', size_hint_y=None, bold=True))
        self.add_widget(EventButton(text=self.short_desc, background_color=self.color, size_hint_y=None))
        self.add_widget(EventButton(text=self.desc, background_color=self.color, size_hint_y=None))
        self.add_widget(PrimaryButton(text="Edit event", on_release=lambda x: Factory.EventEdit(app, self.event).open()))

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

        title = event_.get_title()
        self.time = app.profile_manager.actual_date
        short_desc = event_.get_short_desc()
        color = event_.get_color()
        self.id = event_id
        self.app = app
        self.time = time

        header = EventButton(text=start + " - " + end, on_release=lambda x: self.onrel(), background_color=color,
                             bold=True)
        header.is_header=True
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
        self.color = "#59a8ffa5"
        self.cols = 1
        self.spacing = 10
        self.padding = 20

        title = "title"
        short_desc = "short_desc"
        desc = "full desc"
        date = str(app.profile_manager.actual_date.strftime("%x"))
        start = "00:00"
        end = "24:00"

        self.title = TextInput(size_hint_y=None, height=40)
        self.title.text = title
        self.add_widget(self.title)

        self.short_desc = TextInput(size_hint_y=None, height=40)
        self.short_desc.text = short_desc
        self.add_widget(self.short_desc)

        self.desc = TextInput(size_hint_y=None, height=60)
        self.desc.text = desc
        self.add_widget(self.desc)

        self.date = TextInput(size_hint_y=None, height=40)
        self.date.text = date
        self.add_widget(self.date)

        self.start = TextInput(size_hint_y=None, height=40)
        self.start.text = start
        self.add_widget(self.start)

        self.end = TextInput(size_hint_y=None, height=40)
        self.end.text = end
        self.add_widget(self.end)

        clr_picker = ColorPicker()
        self.add_widget(clr_picker)

        clr_picker.bind(color=self.on_color)

        buttons = GridLayout()
        buttons.cols = 2
        buttons.add_widget(PrimaryButton(text="Accept", on_release=lambda x: self.add(app)))
        buttons.add_widget(PrimaryButton(text="Back", on_release=lambda x: self.back(app)))

        self.add_widget(buttons)

    def add(self, app):
        # todo: data validation

        # create event, eventy dla dnia sa w dict o id rownych iod wydarzeń
        event_id = app.profile_manager.event_manager.add(title=self.title.text, short_desc=self.short_desc.text,
                                                         desc=self.desc.text, color=self.color)
        # add to day list
        app.profile_manager.day_manager.add_event_to_day(date=self.date.text, event_id=event_id, start=self.start.text,
                                                         end=self.end.text)
        self.back(app)

    def back(self, app):
        app.change_logged_screen("Base")

    # To monitor changes, we can bind to color property changes
    def on_color(self, instance, value):
        self.color = str(instance.hex_color)

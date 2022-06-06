from kivy.uix.colorpicker import ColorPicker
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput

from App.GUI.Buttons import PrimaryButton, EventButton


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

            self.add_widget(PrimaryButton(text="Save Changes", on_release=lambda x: self.edit_event(app)))

    def edit_event(self, app):
        self.event.set_title(str(self.title.text))
        self.event.set_short_desc(str(self.short_desc.text))
        self.event.set_desc(str(self.desc.text))
        app.profile_manager.save_event(self.event)
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

        title = event_.get_title()
        self.time = app.profile_manager.actual_date
        short_desc = event_.get_short_desc()
        color = event_.get_color()
        self.id = event_id
        self.app = app
        self.time = time

        self.add_widget(
            EventButton(text=start + " - " + end, on_release=lambda x: self.onrel(), background_color=color, bold=True))
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

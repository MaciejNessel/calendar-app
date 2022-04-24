from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from App.GUI.Buttons import PrimaryButton


class Message(Popup):
    def __init__(self, text, **kw):
        super(Message, self).__init__(**kw)
        self.title = "Message"
        self.size_hint = (.7, .7)

        self.layout = GridLayout(cols=1)
        self.layout.add_widget(Label(text=text))

        back_btn = PrimaryButton(text='Back',
                                 on_release=lambda x: self.dismiss(),
                                 size_hint=(1, .2))
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

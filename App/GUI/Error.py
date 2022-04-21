from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

class Error(Popup):
    def __init__(self, text, **kw):
        super(Error, self).__init__(**kw)
        self.title = "Error"

        self.layout = GridLayout(cols=1)
        self.layout.add_widget(Label(text=text))

        back_btn = Button(text='Back',
                          on_release=lambda x: self.dismiss())
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

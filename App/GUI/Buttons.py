from kivy.lang import Builder
from kivy.uix.button import Button

kv = """
<PrimaryButton@Button>:
    font_name: "Lemonada"
    background_color: 0,0,0,0
    canvas.before:
        Color:
            rgba: (.4,.4,.4,1) if self.state=='normal' else (0,.7,.7,1)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [20,]
            
<UsersButton@Button>:
    btn_color: .4,.4,.4,.2
    background_color: 0,0,0,0
    canvas.before:
        Color:
            rgba: self.btn_color if self.state=='normal' else (0,.7,.7,1)
        Rectangle:
            pos: self.pos
            size: self.size
"""


class PrimaryButton(Button):
    pass
class UsersButton(Button):
    pass

Builder.load_string(kv)

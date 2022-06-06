from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

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
            
<EventButton@Button>:
    btn_color: .4,.4,.4,.2
    background_normal: ''
    background_down: ''
    background_color: 0, 1, 0, 1
    text_size: self.size
    canvas.before:
        Color:
            rgba: self.btn_color
        Rectangle:
            pos: self.pos
            size: self.size

<TopButton@Button>:
    size_hint_y: None
    height: 50

<TitleButton@Button>:
    size_hint_y: None
    height: 50

<NoteButton@Button>:
    size_hint_y: None
    btn_color: .4,.4,.4,.2
    background_normal: ''
    background_down: ''
    background_color: 0, 1, 0, 1
    text_size: self.size
    height: self.texture_size[1]
    canvas.before:
        Color:
            rgba: self.btn_color
        Rectangle:
            pos: self.pos
            size: self.size
            
            
<MenuButton@Button>:
    size_hint_x: None
    width: 50
    background_normal: 'resources/menu_hamburger.png'


<ScrollGrid>:
    size:(root.width, root.height)
    size_hint_y: None
    cols: 1
    height: self.minimum_height
"""


class PrimaryButton(Button):
    pass
class UsersButton(Button):
    pass
class EventButton(Button):
    pass
class TopButton(Button):
    pass
class TitleButton(Button):
    pass
class NoteButton(Button):
    pass
class MenuButton(Button):
    pass
class ScrollGrid(GridLayout):
    pass
Builder.load_string(kv)

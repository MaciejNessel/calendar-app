from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

kv = """
#:import utils kivy.utils

<PrimaryButton@Button>:
    font_name: "Lemonada"
    background_color: 0,0,0,0
    canvas.before:
        Color:
            rgb: utils.get_color_from_hex("#1b263b") if self.state=='normal' else utils.get_color_from_hex("#415a77")
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
    is_header: False
    text_size: root.width-cm(0.5), None
    canvas.before:
        Color:
            rgba: self.btn_color
        Rectangle:
            pos: self.pos
            size: self.size
            
<EventDetailsButton@Button>:
    btn_color: .4,.4,.4,.2
    background_normal: ''
    is_header: False
    text_size: root.width-cm(0.5), None
    canvas.before:
        Color:
            rgba: self.btn_color
        Rectangle:
            pos: self.pos
            size: self.size
            
<TopButton@Button>:
    background_color: "#415a77"
    size_hint_y: None
    height: 50
    

<TitleButton@Button>:
    background_normal: ''
    background_down: ''
    background_color: 0, 1, 0, 1
    is_selected: False
    background_color: "#1D334D" if self.is_selected==True else "#112339"
    day_number: ""
    day_name: ""
    size_hint_y: None
    height: 50
    BoxLayout:
        canvas.before:
            Color:
                rgba: root.background_color
        pos: root.pos
        size: root.size
        Label: 
            font_size: '24sp'
            text: root.day_number
            font_name: "Lemonada"
        Label: 
            text: root.day_name
            font_name: "Lemonada"

<NoteButton@Button>:
    size_hint_y: None
    btn_color: .4,.4,.4,.2
    background_normal: ''
    background_down: ''
    background_color: 0, 1, 0, 1
    text_size: root.width-cm(0.3), None
    height: self.texture_size[1]+cm(0.5)
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
    spacing: 5
    
<ColorButton@Button>:
    btn_color: .4,.4,.4,.2
    background_normal: ''
    background_down: ''
    background_color: 0, 1, 0, 1
    canvas.before:
        Color:
            rgba: self.btn_color
        Rectangle:
            pos: self.pos
            size: self.size
            
<DatesButton@Button>:
    background_color: 0,0,0,0
    size_hint: None, None
    height: 60 
"""


class PrimaryButton(Button):
    pass
class UsersButton(Button):
    pass
class EventButton(Button):
    pass
class EventDetailsButton(Button):
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
class NoteScrollGrid(ScrollGrid):
    pass
class ColorButton(Button):
    pass
class DatesButton(Button):
    pass


Builder.load_string(kv)

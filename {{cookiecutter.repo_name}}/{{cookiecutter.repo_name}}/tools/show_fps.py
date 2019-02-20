from kivy.lang import Builder
from kivy.uix.stacklayout import StackLayout
from kivy.clock import Clock

Builder.load_string('''
<ShowFPS>:
    Label:
        canvas:
            Color:
                rgba: (1, 0, 0, .5)
            Rectangle:
                pos: self.pos
                size: self.size
        id: show_fps
        size_hint_y: None
        text_size: self.size
        height: dp(25)
        halign: 'justify'
        valign: 'middle'
        text: 'FPS: 00'
''')

class ShowFPS(StackLayout):
    def __init__(self, root):
        super(ShowFPS, self).__init__()
        root.add_widget(self)
        Clock.schedule_interval(self.update_fps, 1)

    def update_fps(self, x):
        self.ids.show_fps.text = 'FPS: {:05.2f} - {:05.2f}'.format(Clock.get_fps(), Clock.get_rfps())


from os.path import abspath, dirname, join
from kivy.lang import Builder

Builder.load_file(join(
            dirname(abspath(__file__)), 'fb_widget.kv'))

class ImageButton: pass

class AccountWidget: pass


from os.path import abspath, dirname, join
from kivy.lang import Builder

Builder.load_file(join(
            dirname(abspath(__file__)), 'uix.kv'))

class ImageButton: pass

class AccountWidget: pass

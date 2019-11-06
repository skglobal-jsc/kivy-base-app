from os.path import join, abspath, dirname

from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.resources import resource_add_path

from kivy_base import IS_RELEASE, PLATFORM, IS_BINARY

resource_add_path(
    abspath(join(dirname(__file__), 'data')))

class {{cookiecutter.project_name|replace(' ', '')}}App(App):
    """
    {{cookiecutter.project_short_description|replace('\n', '\n    ')}}
    """

    def __init__(self, app_name, user_data_dir, **kwargs):
        super({{cookiecutter.project_name|replace(' ', '')}}App, self).__init__(**kwargs)

        self._app_name = app_name
        self._user_data_dir = user_data_dir
        self.title = app_name
        self.icon = Config.get('kivy', 'window_icon')

    def build(self):
        root = Builder.load_file('{{cookiecutter.repo_name}}/main-layout.kv')

        return root

    def on_start(self):
        # Display FPS of app
        # from .tools.show_fps import ShowFPS
        # ShowFPS()
        pass

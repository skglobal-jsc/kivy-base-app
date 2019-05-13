from os.path import join, abspath, dirname

from kivy.app import App
from kivy.lang import Builder
from kivy.resources import resource_add_path

from utils.platform import IS_RELEASE, PLATFORM, IS_BINARY

resource_add_path(
    abspath(join(dirname(__file__), 'data')))

class {{cookiecutter.project_name|replace(' ', '')}}App(App):
    """
    {{cookiecutter.project_short_description|replace('\n', '\n    ')}}
    """

    def build(self):
        # Add exception handler
        if IS_BINARY:
            from kivy.base import ExceptionManager
            from .tools.bug_reporter import DesignerException
            ExceptionManager.add_handler(DesignerException())

        root = Builder.load_file('{{cookiecutter.repo_name}}/main-layout.kv')

        return root

    def on_start(self):
        # Display FPS of app
        from .tools.show_fps import ShowFPS
        ShowFPS()

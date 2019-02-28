from kivy.app import App
from kivy.lang import Builder
from kivy.base import ExceptionManager

from utils.platform import PLATFORM


class {{cookiecutter.project_name|replace(' ', '')}}App(App):
    """
    {{cookiecutter.project_short_description|replace('\n', '\n    ')}}
    """

    def build(self):
        # Add exception handler
        # from .tools.bug_reporter import DesignerException
        # ExceptionManager.add_handler(DesignerException())

        root = Builder.load_file('{{cookiecutter.repo_name}}/main-layout.kv')

        # Display FPS of app
        # from .tools.show_fps import ShowFPS
        # ShowFPS(root)

        return root

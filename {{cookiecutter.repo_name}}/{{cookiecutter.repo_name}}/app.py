from kivy.app import App
from kivy.lang import Builder
from kivy.base import ExceptionManager

from utils.platform import PLATFORM

# from .tools.bug_reporter import DesignerException


class {{cookiecutter.project_name|replace(' ', '')}}App(App):
    """Kivy app

    """

    def build(self):
        root = Builder.load_file('{{cookiecutter.repo_name}}/{{cookiecutter.repo_name}}.kv')

        # Display FPS of app
        # from .tools.show_fps import ShowFPS
        # ShowFPS(root)

        # Add exception handler
        # ExceptionManager.add_handler(DesignerException())

        return root

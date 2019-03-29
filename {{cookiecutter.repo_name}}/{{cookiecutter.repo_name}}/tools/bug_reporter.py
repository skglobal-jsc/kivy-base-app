
from os.path import abspath, dirname, join, realpath
import sys
import traceback

from kivy.app import App
from kivy.base import ExceptionHandler, ExceptionManager
from kivy.core.window import Window
from kivy.core.clipboard import Clipboard
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.utils import platform
from kivy import __version__

__all__ = ('DesignerException', )

Builder.load_file(abspath(
            join(dirname(__file__),'bug_reporter.kv')))


class ReportWarning(Popup):
    text = StringProperty('')
    '''Warning Message
    '''

    __events__ = ('on_release',)

    def on_release(self, *args):
        pass


class BugReporter(FloatLayout):
    txt_traceback = ObjectProperty(None)
    '''TextView to show the traceback message
    '''

    def __init__(self, **kw):
        super(BugReporter, self).__init__(**kw)
        self.warning = None

    def on_clipboard(self, *args):
        '''Event handler to "Copy to Clipboard" button
        '''
        Clipboard.copy(self.txt_traceback.text)

    def on_report(self, *args):
        '''Event handler to "Report Bug" button
        '''
        warning = ReportWarning()
        warning.text = ('Warning. Some web browsers doesn\'t post the full'
                        ' traceback error. \n\nPlease, check if the last line'
                        ' of your report is "End of Traceback". \n\n'
                        'If not, use the "Copy to clipboard" button the get'
                        'the full report and post it manually."')
        warning.open()
        self.warning = warning

    def on_close(self, *args):
        '''Event handler to "Close" button
        '''
        App.get_running_app().stop()


class BugReporterApp(App):
    title = "Kivy Designer - Bug reporter"
    traceback = StringProperty('')

    def __init__(self, **kw):
        # self.traceback = traceback
        super(BugReporterApp, self).__init__(**kw)

    def build(self):
        rep = BugReporter()
        template = '''
## Environment Info

{}

## Traceback

```
{}
```

End of Traceback
'''
        env_info = 'Platform: ' + platform
        env_info += '\nPython: v{}'.format(sys.version)
        env_info += '\nKivy: v{}'.format(__version__)

        # if platform in ('win', 'linux', 'macosx'):
        #     import pkg_resources
        #     with open(join(dirname(realpath(__file__)),
        #         '..',
        #         '..',
        #         'requirements.txt'), 'r') as f:
        #         for i in f.readlines():
        #             try:
        #                 pkg_resources.require(i)
        #             except pkg_resources.DistributionNotFound as e:
        #                 env_info += '\n' + str(e)
        #                 continue
        #             except pkg_resources.RequirementParseError as e:
        #                 continue

        if isinstance(self.traceback, bytes):
            encoding = sys.getfilesystemencoding()
            if not encoding:
                encoding = sys.stdin.encoding
            if encoding:
                self.traceback = self.traceback.decode(encoding)
        rep.txt_traceback.text = template.format(env_info, self.traceback)

        return rep


class DesignerException(ExceptionHandler):

    raised_exception = False
    '''Indicates if the BugReporter has already raised some exception
    '''

    def handle_exception(self, inst):
        if self.raised_exception:
            return ExceptionManager.PASS
        App.get_running_app().stop()
        if isinstance(inst, KeyboardInterrupt):
            return ExceptionManager.PASS
        else:
            for child in Window.children:
                Window.remove_widget(child)
            self.raised_exception = True
            Window.fullscreen = False
            bapp = BugReporterApp(traceback=traceback.format_exc())
            bapp.run()
            return ExceptionManager.PASS


if __name__ == '__main__':
    from os.path import join, abspath, dirname
    from kivy.resources import resource_add_path
    resource_add_path(
        abspath(join(dirname(__file__), '..', 'data')))

    BugReporterApp(traceback='Bug example').run()

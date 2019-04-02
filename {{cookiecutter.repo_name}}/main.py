from __future__ import division, absolute_import

import sys
import os

__version_info__ = ({{cookiecutter.version|replace('.', ', ')}})
__version__ = '{{cookiecutter.version}}'
__app_name__ = '{{cookiecutter.project_name}}'

# Please change me to True when you want replease app
# and change back to Fasle when done it
# To use this in app add "from __main__ import IS_RELEASE"
IS_RELEASE = False


if __name__ == '__main__':
    # Run preparation steps and fix errors when running on multi platform
    # such as: set KIVY_HOME, copy config.ini to KIVY_HOME, enable HiDPI, ...
    from utils.platform import pre_run_app
    pre_run_app(__app_name__, IS_RELEASE)

    from utils.platform import PLATFORM, FIRST_RUN, IS_BINARY

    # Controlling the environment of Kivy
    # View more on https://kivy.org/doc/stable/guide/environment.html
    os.environ['KIVY_WINDOW'] = 'sdl2'
    # os.environ['KIVY_TEXT'] = 'sdl2'
    # os.environ['KIVY_VIDEO'] = 'ffpyplayer'
    os.environ['KIVY_AUDIO'] = 'sdl2'
    # os.environ['KIVY_CAMERA'] = ''
    # os.environ['KIVY_IMAGE'] = 'sdl2,gif'
    # os.environ['KIVY_SPELLING'] = ''
    # os.environ['KIVY_CLIPBOARD'] = 'sdl2'

    # os.environ['KIVY_DPI'] = '110'
    # os.environ['KIVY_METRICS_DENSITY'] = '1'
    # os.environ['KIVY_METRICS_FONTSCALE'] = '1.2'

    if PLATFORM == 'ios':
        os.environ['KIVY_IMAGE'] = 'imageio,tex,gif'

    import kivy
    kivy.require('{{cookiecutter.minimum_kivy_version}}')

    from kivy.logger import Logger
    from {{cookiecutter.repo_name}}.app import {{cookiecutter.project_name|replace(' ', '')}}App

    app = {{cookiecutter.project_name|replace(' ', '')}}App()
    app.name = __app_name__
    app.title = __app_name__

    # Print important info of app
    Logger.info('App: Version: ' + __version__ +
                    (' Release' if IS_RELEASE else ' Debug'))
    Logger.info('App: First run: ' + str(FIRST_RUN))
    Logger.info('Kivy home: {}'.format(kivy.kivy_home_dir))
    Logger.info('Current working: {}'.format(os.getcwd()))
    Logger.info('App data: {}'.format(app.user_data_dir))
    Logger.info('Python path: {}'.format(sys.path))
    # from kivy.metrics import Metrics
    # Logger.info('DPI: {} {}'.format(Metrics.dpi, Metrics.dpi_rounded))

    app.run()

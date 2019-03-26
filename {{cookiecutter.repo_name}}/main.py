from __future__ import division, absolute_import

import sys
import os

__version_info__ = ({{cookiecutter.version|replace('.', ', ')}})
__version__ = '{{cookiecutter.version}}'
__app_name__ = '{{cookiecutter.project_name}}'

IS_RELEASE = False


if __name__ == '__main__':
    # Controlling the environment of Kivy
    from buildtools.platform import pre_run_app
    pre_run_app(__app_name__, IS_RELEASE)

    from buildtools.platform import PLATFORM, FIRST_RUN

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
    app._app_name = __app_name__
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

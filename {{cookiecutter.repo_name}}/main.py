from __future__ import division, absolute_import

import sys
import os

__version_info__ = ({{cookiecutter.version|replace('.', ', ')}})
__version__ = '{{cookiecutter.version}}'
__app_name__ = '{{cookiecutter.project_name}}'

# for testing
# if 'testing' in sys.argv:

if __name__ == '__main__':
    # Controlling the environment of Kivy
    from utils.platform import pre_run_app,\
                                PLATFORM, FIRST_RUN

    pre_run_app(__app_name__)

    if PLATFORM == 'ios':
        os.environ['KIVY_IMAGE'] = 'imageio,tex,gif'

    # os.environ['KIVY_DPI'] = '1080'
    os.environ['KIVY_WINDOW'] = 'sdl2'
    # os.environ['KIVY_TEXT'] = 'sdl2'
    # os.environ['KIVY_VIDEO'] =
    os.environ['KIVY_AUDIO'] = 'sdl2'
    # os.environ['KIVY_CAMERA'] =
    # os.environ['KIVY_IMAGE'] = 'sdl2,gif'
    # os.environ['KIVY_SPELLING'] =
    # os.environ['KIVY_CLIPBOARD'] = 'sdl2'

    import kivy
    kivy.require('{{cookiecutter.minimum_kivy_version}}')
    from kivy.logger import Logger

    # if FIRST_RUN:
    #     from kivy.config import Config
    #     Config.set('myapp', 'default_font_style', 'myfont')
    #     Config.set('myapp', 'list_fonts', {'myfont': ['{{cookiecutter.repo_name}}/data/fonts/Osaka.ttc', False, 14, 13]})
    #     Config.write()
    #     Config.update_config('config.ini', overwrite=True)

    from {{cookiecutter.repo_name}}.app import {{cookiecutter.project_name|replace(' ', '')}}App

    app = {{cookiecutter.project_name|replace(' ', '')}}App()
    app._app_name = __app_name__
    Logger.info('App: Version: ' + __version__)
    Logger.info('Kivy home: {}'.format(kivy.kivy_home_dir))
    Logger.info('Current working: {}'.format(os.getcwd()))
    Logger.info('App data: {}'.format(app.user_data_dir))
    Logger.info('Python path: {}'.format(sys.path))
    # from kivy.metrics import Metrics
    # Logger.info('DPI: {} {}'.format(Metrics.dpi, Metrics.dpi_rounded))

    app.run()

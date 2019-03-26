
import os
import sys
from os.path import expanduser
from sys import platform as _sys_platform

def _get_platform():
    # On Android sys.platform returns 'linux2', so prefer to check the
    # presence of python-for-android environment variables (ANDROID_ARGUMENT
    # or ANDROID_PRIVATE).
    if 'ANDROID_ARGUMENT' in os.environ:
        return 'android'
    elif os.environ.get('KIVY_BUILD', '') == 'ios':
        return 'ios'
    elif _sys_platform in ('win32', 'cygwin'):
        return 'win'
    elif _sys_platform == 'darwin':
        return 'macosx'
    elif _sys_platform.startswith('linux'):
        return 'linux'
    elif _sys_platform.startswith('freebsd'):
        return 'linux'
    return 'unknown'

PLATFORM = _get_platform()
IS_BINARY = False
FIRST_RUN = False
KIVY_HOME = './.kivy'

def pre_run_app(app_name, is_release):
    global IS_BINARY, FIRST_RUN, KIVY_HOME

    if PLATFORM == 'win':
        try:
            # Fix High DPI Aware for app Windows
            # Reference https://stackoverflow.com/questions/44398075/can-dpi-scaling-be-enabled-disabled-programmatically-on-a-per-session-basis/44422362#44422362
            import ctypes
            shcore = ctypes.windll.shcore

            # Query DPI Awareness (Windows 10 and 8)
            # awareness = ctypes.c_int()
            # errorCode = shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))

            # if errorCode != 0:
            # Set DPI Awareness  (Windows 10 and 8)
            # the argument is the awareness level, which can be 0, 1 or 2
        if shcore.SetProcessDpiAwareness(2) != 0:
            raise OSError
        except OSError:
            print('Warning: Can\'t set process DPI Awareness')

        IS_BINARY = os.path.exists('./base_library.zip')
        if IS_BINARY:
            KIVY_HOME = os.path.join(os.environ['APPDATA'], app_name, '.kivy')

    # Fix run .app on Mac
    elif PLATFORM == 'macosx' \
        and not any(os.path.exists(i) for i in ['.Python', 'main.py']):
        IS_BINARY = True

        for i in sys.path:
            if os.path.exists(os.path.join(i, '.Python')):
                os.chdir(i)
                break
        else:
            import errno
            raise FileNotFoundError(
                            errno.ENOENT,
                            os.strerror(errno.ENOENT),
                            'app/Contents/MacOS')

        if IS_BINARY:
            KIVY_HOME = os.path.join(expanduser('~'), '.'+app_name, '.kivy')

    FIRST_RUN = not os.path.exists(KIVY_HOME)

    # Set home Kivy and load config
    if PLATFORM in ('win', 'macosx'):
        os.environ['KIVY_HOME'] = KIVY_HOME

        if FIRST_RUN:
            from configparser import RawConfigParser
            from .resolution import get_resolution
            config = RawConfigParser()
            config.read('config.ini')
            os.makedirs(KIVY_HOME)

            # rsize = 0.7
            # size = get_resolution()
            # config.set('graphics', 'width', int(size[0]*rsize))
            # config.set('graphics', 'height', int(size[1]*rsize))

            with open(os.path.join(KIVY_HOME, 'config.ini'), 'w') as configfile:
                config.write(configfile)

    if PLATFORM in ('ios', 'android'):
        try:
            import sitecustomize
        except ImportError:
            pass

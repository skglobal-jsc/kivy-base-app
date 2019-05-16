
import os
import sys
from os.path import expanduser, join, exists
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

def _get_user_data_dir(name):
    # Determine and return the user_data_dir.
    data_dir = ""
    if PLATFORM == 'ios':
        data_dir = expanduser(join('~/Documents', name))
    elif PLATFORM == 'android':
        from jnius import autoclass, cast
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        context = cast('android.content.Context', PythonActivity.mActivity)
        file_p = cast('java.io.File', context.getFilesDir())
        data_dir = join(file_p.getAbsolutePath(), name)
    elif PLATFORM == 'win':
        data_dir = os.path.join(os.environ['APPDATA'], name)
    elif PLATFORM == 'macosx':
        data_dir = '~/Library/Application Support/{}'.format(name)
        data_dir = expanduser(data_dir)
    else:  # _platform == 'linux' or anything else...:
        data_dir = os.environ.get('XDG_CONFIG_HOME', '~/.config')
        data_dir = expanduser(join(data_dir, name))

    return data_dir


# Please change me to True when you want replease app
# and change back to Fasle when done it
IS_RELEASE = False

PLATFORM = _get_platform()
IS_BINARY = False
FIRST_RUN = False
KIVY_HOME = './.kivy'

def pre_run_app(app_name):
    '''
    KIVY_HOME = './.kivy' when run 'python main.py'

    When app is packed:
    - Windows: KIVY_HOME = `%APPDATA%/<app_name>/.kivy`
    - Mac:  KIVY_HOME = `~/.<app_name>/.kivy`
    - iOS: `~/Documents/<app_name>` is returned (which is inside the
        app's sandbox).
    - Android: `Context.GetFilesDir + <app_name>` is returned.

    This function fix:

    - HiDPI on Windows
    - Run python in .app when packing by pyinstaller
    - Not found modules when build app by buildozer
    '''
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

    elif PLATFORM in ('ios', 'android'):
        # Fix not found modules when build app by buildozer
        try:
            import sitecustomize
        except ImportError:
            pass

        IS_BINARY = True
        KIVY_HOME = _get_user_data_dir(app_name)

    FIRST_RUN = not os.path.exists(KIVY_HOME)

    if IS_RELEASE and not IS_BINARY:
        print('-'*80)
        print('Warning: You are in RELEASE. Please change IS_RELEASE in main.py back to False')
        print('-'*80)

    # Set KIVY_HOME and load config
    os.environ['KIVY_HOME'] = KIVY_HOME

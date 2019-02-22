from .platform import PLATFORM

height = None
width = None
def callback(hwnd, extra):
    import win32gui
    global height, width
    if win32gui.GetWindowText(hwnd) != 'Window':
        return
    rect = win32gui.GetWindowRect(hwnd)
    width = rect[2] - rect[0]
    height = rect[3] - rect[1]

def get_resolution():
    global height, width

    if (height, width) == (None, None):
        if PLATFORM == 'win':
            # import win32gui
            # win32gui.EnumWindows(callback, None)
            from win32api import GetSystemMetrics
            width, height = GetSystemMetrics(0), GetSystemMetrics(1)
        elif PLATFORM == 'macosx':
            from subprocess import check_output
            from os.path import join, dirname
            import os
            import stat
            visFile = join(dirname(__file__), 'visibleFrame')
            st = os.stat(visFile)
            os.chmod(visFile, st.st_mode|stat.S_IEXEC)
            width, height = [int(i) for i in \
                                check_output(visFile).split()]

        if (height, width) == (None, None):
            Exception('Can\'t get screen resolution.')
    return width, height

# -*- mode: python -*-
import os
import sys
import platform
sys.path+=['.']

from kivy.tools.packaging.pyinstaller_hooks import get_deps_minimal, get_deps_all, hookspath, runtime_hooks

if platform.system() == 'Windows':
    from kivy.deps import sdl2, glew
    deps = [Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)]
    hiddenimports = ['win32timezone']
    binaries = []
else:
    deps = []
    hiddenimports = []
    binaries = [
    ('/System/Library/Frameworks/Tk.framework/Tk', 'tk'),
    ('/System/Library/Frameworks/Tcl.framework/Tcl', 'tcl')
    ]

hiddenimports += []

datas = [
    ('./{{cookiecutter.repo_name}}/data','{{cookiecutter.repo_name}}/data'),
    ('./{{cookiecutter.repo_name}}/*.kv', '{{cookiecutter.repo_name}}'),
    ('config.ini', '.'),
    ('utils/visibleFrame', 'utils')
]
block_cipher = None


# Embedde kivy file into python file
# from utils import embedde_kivy_file
# embedde_kivy_file('{{cookiecutter.repo_name}}')

a = Analysis(['main.py'],
             pathex=['.'],
             datas=datas,
             binaries=binaries,
             hiddenimports= hiddenimports,
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='{{cookiecutter.project_name}}',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          icon='./{{cookiecutter.repo_name}}/data/icon.ico',
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               *deps,
               icon='./{{cookiecutter.repo_name}}/data/icon.ico',
               strip=False,
               upx=True,
               name='{{cookiecutter.project_name}}')

if platform.system() == 'Darwin':
    app = BUNDLE(coll,
            name='{{cookiecutter.project_name}}.app',
            icon='./{{cookiecutter.repo_name}}/data/icon.icns',
            bundle_identifier=None,
            info_plist={
                'NSPrincipleClass': 'NSApplication',
                'NSHighResolutionCapable': True,
                },
    )

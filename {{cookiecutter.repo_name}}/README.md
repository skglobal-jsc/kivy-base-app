# {{cookiecutter.project_name}}

{{cookiecutter.project_short_description}}

Table of Contents:

[TOC]

## Features


- TODO
    - Add new app icon in `{{cookiecutter.repo_name}}/data` (replace existing file) and remove this todo.
    - Change `build_dir` and `ios.codesign.debug` in buildozer.spec when create new or clone project to local (do not commit it to git).
    - Generate a new GUID for Inno setup when create new project and remove this todo.
    - When change version, remember change in files: main.py and create-installer.iss

## Usage

### Launching the app

Go to project folder and run:

```bash
# On Mac, Linux
source ./.env/bin/activate
# On Windows
.\.env\Scripts\activate
python main.py
```

### Running the testsuite

Go to project folder and run:

```bash
# On Mac, Linux
source ./.env/bin/activate
# On Windows
.\.env\Scripts\activate
pytest
```

### Packaging project

**Make sure you follow all steps in [Environment preparing](https://kivy-skglobal.readthedocs.io/en/latest/#environment-preparing) and check all TODO**

- For Windows/MacOS, you must activate env and run pyinstaller:
    - Output folder will save in `dist` folder.
    - You must close all app and the opened file or folder in `dist` folder before packaging app. If you not, pyinstaller can't build project.

```bash
# On Mac, Linux
source ./.env/bin/activate
# On Windows
.\.env\Scripts\activate
pyinstaller ./main.spec
```

- To create installer:
    - Windows: download [Inno Setup](http://www.jrsoftware.org/isinfo.php) and run `create-installer.iss`. Output file will save in `Output` folder.
    - Mac: run cmd `pkgbuild --install-location /Applications --component 'dist/{{cookiecutter.project_name}}.app' 'dist/Install {{cookiecutter.project_name}}.pkg'`

- For Android/iOS, DO NOT packing app in env (to quit env run `deactivate`), should use Mac to packing and install [buildozer fork of Sk-global](https://github.com/Thong-Tran/buildozer/tree/fix-errors). When you change code in project, please run cmd again.

    - Android: (you should have java 8 and python 2.7)

    ```bash
    buildozer android debug
    ```

    File apk will be saved in `bin` folder.

    - iOS: (you should have XCode and update the latest iOS SDK)

    ```bash
    buildozer ios xcode
    ```

    When finish, this will open XCode and we will build app in that.

If you get error, read [this](https://kivy-skglobal.readthedocs.io/en/latest/development/packaging-project/) to fix it or contact to python@sk-global.biz for further instructions.

### Multi-language support

- To support multi-language, add ObservableTranslation to app.py:

```python
from .tools.language import ObservableTranslation

class MainApp(App):
    tr = ObservableTranslation('en', 'imgtrans')
    . . .
```

- Tag all text:

```kv
#:set tr app.tr

Label:
    text: tr._('History')
```

- Collect tag language (like `_('text')`):

```bash
python utils/pygettext.py -o {{cookiecutter.repo_name}}/po/en.po {{cookiecutter.repo_name}}
```

- Compile file language(.po):

```bash
python utils/msgfmt.py -o {{cookiecutter.repo_name}}/data/locales/ja/LC_MESSAGES/lang.mo {{cookiecutter.repo_name}}/po/ja.po
```

## Known issues

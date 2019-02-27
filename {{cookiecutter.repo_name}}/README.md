# {{cookiecutter.project_name}}

{{cookiecutter.project_short_description}}

## Features


- TODO
    - Add new app icon in `{{cookiecutter.repo_name}}/data` (replace existing file).
    - Change `build_dir` and `ios.codesign.debug` in buildozer.spec when create new or clone project (do not commit it to git).
    - Generate a new GUID for Inno setup.
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

**Make sure you follow all steps in [Environment preparing](https://kivy-skglobal.readthedocs.io/en/latest/#environment-preparing)**

- For Windows/MacOS, you must activate env and run pyinstaller:

```bash
# On Mac, Linux
source ./.env/bin/activate
# On Windows
.\.env\Scripts\activate
pyinstaller ./main.spec
```

- For Android/iOS, DO NOT packing app on env, should use Mac to packing and install [buildozer fork of Sk-global](https://github.com/Thong-Tran/buildozer/tree/fix-errors).

    - Android: (you should have java 8 and python 2.7)

    ```
    buildozer android debug
    ```

    - iOS: (you should have XCode and update the latest iOS SDK)

    ```
    buildozer ios xcode
    ```

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

```
python utils/pygettext.py -o {{cookiecutter.repo_name}}/po/en.po {{cookiecutter.repo_name}}
```

- Compile file language(.po):

```
python utils/msgfmt.py -o {{cookiecutter.repo_name}}/data/locales/ja/LC_MESSAGES/lang.mo {{cookiecutter.repo_name}}/po/ja.po
```

## Known issues

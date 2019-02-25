# {{cookiecutter.project_name}}

{{cookiecutter.project_short_description}}

## Features


- TODO
    - Add new app icon in `{{cookiecutter.repo_name}}/path`.
    - Change android.ndk_path in buildozer.spec
    - Generate a new GUID for Inno setup.
    - When change version, remember change in files: main.py, create-installer.iss

## Usage

### Launching the app

Go to project folder and run:

```bash
# On Mac, Linux
source ./.env/bin/activate
# On Windows
.\\.env\\Scripts\\activate
python main.py
```

### Running the testsuite

Go to project folder and run:

```bash
# On Mac, Linux
source ./.env/bin/activate
# On Windows
.\\.env\\Scripts\\activate
pytest
```

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

Toolbar:
    id: toolbar
    title: tr._('History')
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

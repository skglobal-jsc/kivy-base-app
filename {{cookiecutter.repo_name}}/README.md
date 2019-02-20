# {{cookiecutter.project_name}}

{{cookiecutter.project_short_description}}

## Features


- TODO
    - Add new app icon in `{{cookiecutter.repo_name}}/path`.
    - Change android.ndk_path in buildozer.spec
    - Generate a new GUID for Inno setup.
    - When change version, remember change in files: main.py, create-installer.iss

## Usage

### Before launch app

- Collect tag language (like `_('text')`):

```
python utils/pygettext.py -o {{cookiecutter.repo_name}}/po/en.po {{cookiecutter.repo_name}}
```

- Compile file language(.po):

```
python utils/msgfmt.py -o {{cookiecutter.repo_name}}/data/locales/ja/LC_MESSAGES/lang.mo {{cookiecutter.repo_name}}/po/ja.po
```

### Launching the app

Go to project folder and run `python main.py`

### Running the testsuite

Go to project folder and run `pytest`

## Known issues

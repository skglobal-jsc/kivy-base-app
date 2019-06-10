# {{cookiecutter.project_name}}

{{cookiecutter.project_short_description}}

Table of Contents:

[TOC]

## Features


- TODO
    - Add new app icon in `{{cookiecutter.repo_name}}/data` (replace existing file) and remove this todo.
    - Create `buildozer-local.spec` with below content and replace it for your own when create new or clone project to local (**do not commit it to git**).

    ```ini
    [app]
    # (str) Name of the certificate to use for signing the debug version
    # Get a list of available identities: buildozer ios list_identities
    ios.codesign.debug = "iPhone Developer: <lastname> <firstname> (<hexstring>)"

    # (str) Name of the certificate to use for signing the release version
    #ios.codesign.release = %(ios.codesign.debug)s

    [buildozer]
    # (str) Path to build artifact storage, absolute or relative to spec file
    build_dir = ./.buildozer
    ```

    - Generate a new GUID for Inno setup when create new project and remove this todo.
    - When change version, remember change in files: main.py and buildtools/create-installer.iss
    - When you release app please change `IS_RELEASE` in utils/platform.py to `True` and remember change back to `False` when done it.

## Usage

### Launching the app

Go to project folder and run:

```bash
pip3 install --upgrade virtualenv
python3 -m virtualenv .env
source ./.env/bin/activate

# On Windows
py -3 -m pip install --upgrade virtualenv
py -3 -m virtualenv .env
.\.env\Scripts\activate

pip install -r requirements.txt
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
    - You must close app and the opened file or folder in `dist` folder before packaging app. If you not, pyinstaller can't build project.

```bash
# On Mac, Linux
source ./.env/bin/activate
# On Windows
.\.env\Scripts\activate
pyinstaller ./desktop.spec
```

- To create installer:
    - Windows: download [Inno Setup](http://www.jrsoftware.org/isinfo.php) and run `.\buildtools\create-installer.iss`. Output file will save in `.\buildtools\Output` folder.
    - Mac: run cmd `pkgbuild --install-location /Applications --component 'dist/{{cookiecutter.project_name}}.app' 'dist/Install {{cookiecutter.project_name}} v{{cookiecutter.version}}.pkg'`

- For Android/iOS, install latest [buildozer fork of Sk-global](https://github.com/Thong-Tran/buildozer/tree/fix-errors). When you change code in project, please run cmd again.

    - Android: you should have linux device (or [WSL](https://docs.microsoft.com/en-us/windows/wsl)) java 8 to create apk

    ```bash
    buildozer android debug
    ```

    File apk will be saved in `bin` folder.

    - iOS: (you should have XCode and update the latest iOS SDK)

    ```bash
    buildozer ios xcode
    ```

    When finish, this will open XCode and we will build app in that.

If you get error, read [this](https://kivy-skglobal.readthedocs.io/en/latest/development/packaging-project/) to fix it or contact to {{cookiecutter.email}} for further instructions.

## Known issues

# RfCat-GUI

**important**

This project is just started ... what is currently available is just a simple mockup (some parts do not work yet and no testing done yet)

## Build

```shell
# clone repository
$ git clone https://github.com/Lupin3000/rfcat-gui.git

# change into cloned directory
$ cd rfcat-gui

# create virtualenv
$ virtualenv -p python3 .env

# install requirements
$ pip install -r requirements.txt

# create macOS application
$ python setup.py py2app -A
```

## Usage

Note: PlugIn your Dongle before start application!

```shell
# change directory
$ cd rfcat-gui/dist/

# run application
$ open -a RfCat-GUI.app 
```

![RfCat GUI](./github-src/example-picture.jpg)

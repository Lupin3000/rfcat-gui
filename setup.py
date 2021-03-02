from setuptools import setup

APP = ['RfCat-GUI']
DATA_FILES = []
OPTIONS = {'iconfile': 'RfCat-GUI.icns'}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

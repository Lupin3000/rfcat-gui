#!/usr/bin/env python3

from tkrfcat.TkRfcat import *

if __name__ == '__main__':

    RUN = Application('RfCat-GUI', False, '#fff', True)
    RUN.start_rfcat_ui()

import logging
from tkinter import Tk, FALSE


class BaseUi:

    def __init__(self, window_title, window_resizable, bg_color):
        """
        Base tkinter object

        :type window_title: str
        :param window_title: set window title
        :type window_resizable: bool
        :param window_resizable: set windows resizeable true or false
        :type bg_color: str
        :param bg_color: color code ('#ddd')
        """
        # initialize logging and set logging level
        self.__logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

        # create tkinter object
        self.__logger.info('ConfigureWindow')

        self._tk_obj = Tk()
        self._tk_obj.title(str(window_title))
        self._tk_obj.configure(bg=bg_color)

        if not bool(window_resizable):
            self._tk_obj.resizable(width=FALSE, height=FALSE)
        else:
            self._tk_obj.columnconfigure(0, weight=1)
            self._tk_obj.rowconfigure(0, weight=1)

    def run_app(self):
        """
        Start tkinter application mainloop
        """
        self.__logger.info('StartMainloop')
        self._tk_obj.mainloop()

    def quit_app(self):
        """
        Stop tkinter application
        """
        self._tk_obj.quit()

import logging
from tkinter import Tk, Menu, Toplevel, Label, INSERT, FALSE


class BaseUi:

    def __init__(self, window_title, window_resizable, bg_color, show_menu):
        """
        Base tkinter object

        :type window_title: str
        :param window_title: set window title
        :type window_resizable: bool
        :param window_resizable: set windows resizeable true or false
        :type bg_color: str
        :param bg_color: color code ('#ddd')
        :type show_menu: bool
        :param show_menu: set menu visible true or false
        """
        # initialize logging and set logging level
        self.__logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

        # create tkinter object
        self.__logger.info('ConfigureWindow')

        self.__window_title = str(window_title)

        self._tk_obj = Tk()
        self._tk_obj.title(str(self.__window_title))
        self._tk_obj.configure(bg=bg_color)

        if not bool(window_resizable):
            self._tk_obj.resizable(width=FALSE, height=FALSE)
        else:
            self._tk_obj.columnconfigure(0, weight=1)
            self._tk_obj.rowconfigure(0, weight=1)

        if bool(show_menu):
            self.__create_menu()

    def __create_menu(self):
        """
        Create menu bar
        """
        self.__logger.info('CreateMenuBar')

        menu_bar = Menu(self._tk_obj)
        self._tk_obj.config(menu=menu_bar)

        # File
        file_menu = Menu(menu_bar)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Close", command=self.quit_app)

        # Help
        help_menu = Menu(menu_bar)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.__create_about_window)
        help_menu.add_command(label="Help", command=self.__create_help_window)

    def __create_about_window(self):
        """
        Create about window
        """
        window_about = Toplevel(self._tk_obj)
        window_about.title("About " + str(self.__window_title))
        window_about.geometry("200x400")

        about_ety = Label(window_about, text="lorem ipsum dolor sit amet...")
        about_ety.pack()

    def __create_help_window(self):
        """
        Create help window
        """
        window_help = Toplevel(self._tk_obj)
        window_help.title(str(self.__window_title) + " Help")
        window_help.geometry("200x400")

        help_ety = Label(window_help, text="lorem ipsum dolor sit amet...")
        help_ety.pack()

    def run_app(self):
        """
        Start tkinter application mainloop
        """
        self.__logger.info('StartMainloop')
        self._tk_obj.mainloop()

    def build_frames(self):
        """
        Build all tkinter frames and start mainloop
        """
        pass

    def quit_app(self):
        """
        Stop tkinter application
        """
        self._tk_obj.quit()

from tkrfcat.TkApplicationUi import ApplicationUi


class Application(ApplicationUi):

    def __init__(self, window_title, window_resizable, bg_color, show_menu):
        """
        Overwrite base tkinter object

        :type window_title: str
        :param window_title: set window title
        :type window_resizable: bool
        :param window_resizable: set windows resizeable true or false
        :type bg_color: str
        :param bg_color: color code ('#ddd')
        :type show_menu: bool
        :param show_menu: set menu visible true or false
        """
        ApplicationUi.__init__(self, window_title, window_resizable, bg_color, show_menu)

    def start_rfcat_ui(self):
        """
        Start to build all frames
        """
        self.build_frames()

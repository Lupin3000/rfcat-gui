import logging
from datetime import datetime
from tkinter import (Frame, OptionMenu, Spinbox, Checkbutton, Button, Entry, Text, Label,
                     StringVar, IntVar, W, E, END, SUNKEN, SOLID, DISABLED, NORMAL)
from tkinter.scrolledtext import ScrolledText
from rflib import *
from tkrfcat.TkBaseUi import BaseUi


class ApplicationUi(BaseUi):

    __FONT_HEADLINE = ('verdana', 13, 'bold')
    __FONT_STYLE = ('verdana', 11, 'normal')
    __MODULATION_OPTIONS = ['Please select', 'MOD_2FSK', 'MOD_GFSK', 'MOD_ASK_OOK', 'MOD_MSK']

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
        # initialize logging and set logging level
        self.__logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

        # all needed variables
        self.__sample_list = []
        self.rf_object = RfCat()
        self._selected_modulation = None
        self._selected_channel = None
        self._selected_sync_mode = None
        self._ety_frequency = None
        self._ety_baud = None
        self._ety_deviation = None
        self._ety_channel_bandwidth = None
        self._ety_sync_word = None
        self._ety_channel_spacing = None
        self._cbx_manchester_value = None
        self._btn_save_settings = None
        self._ety_message_to_send = None
        self._sbx_repeats = None
        self._btn_send = None
        self._txt_send_status = None
        self._cbx_max_power_value = None
        self._cbx_lowball_value = None
        self._stx_receive_status = None
        self._btn_copy = None
        self._btn_receive = None

        BaseUi.__init__(self, window_title, window_resizable, bg_color, show_menu)

    def __add_message_hex_to_list(self, value):
        """
        Split message HEX values into list
        """
        for element in value:
            self.__sample_list.append(element)

    def __set_btn_disabled(self):
        """
        Set all button state to disabled
        """
        self._btn_send.configure(state=DISABLED)
        self._btn_save_settings.configure(state=DISABLED)
        self._btn_receive.configure(state=DISABLED)
        self._btn_copy.configure(state=DISABLED)

    def __set_btn_normal(self):
        """
        Set all button state to normal
        """
        self._btn_send.configure(state=NORMAL)
        self._btn_save_settings.configure(state=NORMAL)
        self._btn_receive.configure(state=NORMAL)
        self._btn_copy.configure(state=NORMAL)

    def __action_clear_message(self):
        """
        Delete values from tkinter box
        """
        self._ety_message_to_send.delete(0, END)

    def __action_store_settings(self):
        """
        Store values from tkinter items on rfcat dongle
        """
        self.__set_btn_disabled()

        # frequency
        frequency = int(self._ety_frequency.get())
        self.__logger.info('Frequency:%i', frequency)
        if frequency in range(300000000, 928000000):
            self.rf_object.setFreq(frequency)

        # modulation
        modulation = str(self._selected_modulation.get())
        self.__logger.info('Modulation:%s', modulation)
        if modulation == 'MOD_2FSK':
            self.rf_object.setMdmModulation(MOD_2FSK)
        elif modulation == 'MOD_GFSK':
            self.rf_object.setMdmModulation(MOD_GFSK)
        elif modulation == 'MOD_ASK_OOK':
            self.rf_object.setMdmModulation(MOD_ASK_OOK)
        elif modulation == 'MOD_MSK':
            self.rf_object.setMdmModulation(MOD_MSK)
        else:
            self.rf_object.setMdmModulation(MOD_2FSK)

        # channel
        channel = int(self._selected_channel.get())
        self.__logger.info('Channel:%i', channel)
        if channel in range(0, 10):
            self.rf_object.setChannel(channel)

        # baud rate
        baud_rate = int(self._ety_baud.get())
        self.__logger.info('BaudRate:%i', baud_rate)
        if baud_rate in range(210, 250000):
            self.rf_object.setMdmDRate(baud_rate)

        # deviation
        deviation = int(self._ety_deviation.get())
        self.__logger.info('Deviation:%i', deviation)

        # channel bandwidth
        channel_bandwidth = int(self._ety_channel_bandwidth.get())
        self.__logger.info('ChannelBandwidth:%i', channel_bandwidth)

        # sync mode
        sync_mode = int(self._selected_sync_mode.get())
        self.__logger.info('SyncMode:%i', sync_mode)
        if sync_mode in range(0, 8):
            self.rf_object.setMdmSyncMode(sync_mode)

        # sync word
        sync_word = self._ety_sync_word.get()
        self.__logger.info('SyncWord:%s', sync_word)

        # channel spacing
        channel_spacing = int(self._ety_channel_spacing.get())
        self.__logger.info('ChannelSpacing:%i', channel_spacing)

        # manchester encoding
        manchester_encoding = int(self._cbx_manchester_value.get())
        self.__logger.info('ManchesterEncoding:%i', manchester_encoding)

        self.__set_btn_normal()

    def __action_send_signal(self):
        """
        Send rfcat dongle signal
        """
        self.__set_btn_disabled()
        self._txt_send_status.configure(state='normal')
        self._txt_send_status.delete('0.0', END)

        rf_message = str(self._ety_message_to_send.get()).strip()

        if not rf_message:
            self.__logger.info('No message found')
            self._txt_send_status.insert(END, 'No message to send?')
        else:
            self.__logger.info('Message:%s', rf_message)
            self._txt_send_status.insert(END, 'Message: ' + rf_message)

            # text to binary
            rf_bin_message = ' '.join(format(ord(x), 'b') for x in rf_message)
            self._txt_send_status.insert(END, "\nBinary: " + rf_bin_message)

            # text to hex
            rf_hex_message = rf_message.encode().hex()
            self._txt_send_status.insert(END, "\nHEX: " + rf_hex_message)

            # add hex to list and count bytes
            self.__add_message_hex_to_list(re.findall('..', rf_hex_message))
            byte_count = len(self.__sample_list)
            self._txt_send_status.insert(END, "\nBytes: " + str(byte_count))

            rf_repeats = int(self._sbx_repeats.get())
            self.__logger.info('Repeats:%i', rf_repeats)
            self._txt_send_status.insert(END, "\nRepeats: " + str(rf_repeats))

            rf_datetime = datetime.now()
            self.__logger.info('Date/Time:%s', rf_datetime)
            self._txt_send_status.insert(END, "\nDate: " + str(rf_datetime))

            # convert hex to bytes and start transmit
            send_message = bytes.fromhex(rf_hex_message)
            self.rf_object.RFxmit(data=send_message, repeat=int(rf_repeats))
            self.__logger.info('Transmit of message done (%i)', int(rf_repeats))

            self.rf_object.setModeIDLE()
            self.__logger.info('set USB dongle into idle state')

            self._txt_send_status.insert(END, "\nResult: transmit done, USB dongle set to idle")

            self.__sample_list = []

        self._txt_send_status.configure(state='disabled')
        self.__set_btn_normal()

    def __action_receive_signal(self):
        """
        Store settings and start receive signal
        """
        self.__set_btn_disabled()
        self._stx_receive_status.delete(0.0, END)

        # @ToDo: store settings of lowball/max power

        # @ToDo: run signal receiving into ScrolledText incl press key to stop loop
        output = self.rf_object.discover()
        print(output)

        self.__set_btn_normal()

    def __action_copy_to_clipboard(self):
        """
        Copy content of received signal field to clipboard
        """
        self.__set_btn_disabled()

        field_value = self._stx_receive_status.get("1.0", 'end-1c')

        if not field_value:
            self.__logger.info('NoValueForClipboard')
        else:
            self._tk_obj.clipboard_clear()
            self._tk_obj.clipboard_append(field_value)

        self.__set_btn_normal()

    def build_frames(self):
        """
        Build all tkinter frames and start mainloop
        """
        self.__logger.info('BuildAllFrames')

        self.__top_frame()
        self.__middle_frame()
        self.__bottom_frame()

        self.run_app()

    def __top_frame(self):
        """
        Create top frame content
        """
        self._selected_modulation = StringVar(self._tk_obj)
        self._selected_channel = StringVar(self._tk_obj)
        self._selected_sync_mode = StringVar(self._tk_obj)
        self._cbx_manchester_value = IntVar(self._tk_obj)

        frame = Frame(self._tk_obj, borderwidth=1, relief=SUNKEN, bg='#fff')
        frame.grid(column=0, row=0, padx=15, pady=15, sticky=W+E)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # headline
        lab_section = Label(frame, text="Default RF Settings")
        lab_section.grid(columnspan=6, row=0, padx=5, pady=5, sticky=W+E)
        lab_section.configure(font=self.__FONT_HEADLINE)

        # frequency
        lab_frequency = Label(frame, text='Frequency')
        lab_frequency.grid(column=0, row=1, padx=5, pady=5, sticky=E)
        lab_frequency.configure(font=self.__FONT_STYLE)

        self._ety_frequency = Entry(frame)
        self._ety_frequency.grid(column=1, row=1, padx=5, pady=5, sticky=W)
        self._ety_frequency.configure(font=self.__FONT_STYLE)
        value_frequency = self.rf_object.getFreq()
        self._ety_frequency.insert(0, int(value_frequency[0]))

        # modulation
        lab_modulation = Label(frame, text='Modulation')
        lab_modulation.grid(column=0, row=2, padx=5, pady=5, sticky=E)
        lab_modulation.configure(font=self.__FONT_STYLE)

        opm_modulation = OptionMenu(frame, self._selected_modulation, *self.__MODULATION_OPTIONS)
        opm_modulation.grid(column=1, row=2, padx=5, pady=5, sticky=W)
        opm_modulation.configure(font=self.__FONT_STYLE)
        value_modulation = self.rf_object.getMdmModulation()
        if value_modulation == 0:
            self._selected_modulation.set(self.__MODULATION_OPTIONS[1])
        elif value_modulation == 16:
            self._selected_modulation.set(self.__MODULATION_OPTIONS[2])
        elif value_modulation == 48:
            self._selected_modulation.set(self.__MODULATION_OPTIONS[3])
        elif value_modulation == 112:
            self._selected_modulation.set(self.__MODULATION_OPTIONS[4])
        else:
            self._selected_modulation.set(self.__MODULATION_OPTIONS[0])

        # channel
        lab_channel = Label(frame, text='Channel')
        lab_channel.grid(column=0, row=3, padx=5, pady=5, sticky=E)
        lab_channel.configure(font=self.__FONT_STYLE)

        sbx_channel = Spinbox(frame, state='readonly')
        sbx_channel.grid(column=1, row=3, padx=5, pady=5, sticky=W)
        sbx_channel.configure(font=self.__FONT_STYLE)
        self._selected_channel.set(self.rf_object.getChannel())
        sbx_channel.configure(from_=0, to=10, increment=1, textvariable=self._selected_channel)

        # baud rate
        lab_baud = Label(frame, text='Baud Rate')
        lab_baud.grid(column=2, row=1, padx=5, pady=5, sticky=E)
        lab_baud.configure(font=self.__FONT_STYLE)

        self._ety_baud = Entry(frame)
        self._ety_baud.grid(column=3, row=1, padx=5, pady=5, sticky=W)
        self._ety_baud.configure(font=self.__FONT_STYLE)
        self._ety_baud.insert(0, int(self.rf_object.getMdmDRate()))

        # deviation
        lab_deviation = Label(frame, text='Deviation')
        lab_deviation.grid(column=2, row=2, padx=5, pady=5, sticky=E)
        lab_deviation.configure(font=self.__FONT_STYLE)

        self._ety_deviation = Entry(frame)
        self._ety_deviation.grid(column=3, row=2, padx=5, pady=5, sticky=W)
        self._ety_deviation.configure(font=self.__FONT_STYLE)
        self._ety_deviation.insert(0, int(self.rf_object.getMdmDeviatn()))
        self._ety_deviation.configure(state='readonly')

        # channel bandwidth
        lab_channel_bandwidth = Label(frame, text='Channel BW')
        lab_channel_bandwidth.grid(column=2, row=3, padx=5, pady=5, sticky=E)
        lab_channel_bandwidth.configure(font=self.__FONT_STYLE)

        self._ety_channel_bandwidth = Entry(frame)
        self._ety_channel_bandwidth.grid(column=3, row=3, padx=5, pady=5, sticky=W)
        self._ety_channel_bandwidth.configure(font=self.__FONT_STYLE)
        self._ety_channel_bandwidth.insert(0, int(self.rf_object.getMdmChanBW()))
        self._ety_channel_bandwidth.configure(state='readonly')

        # sync mode
        lab_sync_mode = Label(frame, text='Sync Mode')
        lab_sync_mode.grid(column=4, row=1, padx=5, pady=5, sticky=E)
        lab_sync_mode.configure(font=self.__FONT_STYLE)

        sbx_sync_mode = Spinbox(frame, state='readonly')
        sbx_sync_mode.grid(column=5, row=1, padx=5, pady=5, sticky=W)
        sbx_sync_mode.configure(font=self.__FONT_STYLE)
        self._selected_sync_mode.set(self.rf_object.getMdmSyncMode())
        sbx_sync_mode.configure(from_=0, to=7, increment=1, textvariable=self._selected_sync_mode)

        # sync word
        lab_sync_word = Label(frame, text='Sync Word')
        lab_sync_word.grid(column=4, row=2, padx=5, pady=5, sticky=E)
        lab_sync_word.configure(font=self.__FONT_STYLE)

        self._ety_sync_word = Entry(frame)
        self._ety_sync_word.grid(column=5, row=2, padx=5, pady=5, sticky=W)
        self._ety_sync_word.configure(font=self.__FONT_STYLE)
        self._ety_sync_word.insert(0, self.rf_object.getMdmSyncWord())
        self._ety_sync_word.configure(state='readonly')

        # channel spacing
        lab_channel_spacing = Label(frame, text='Channel Spacing')
        lab_channel_spacing.grid(column=4, row=3, padx=5, pady=5, sticky=E)
        lab_channel_spacing.configure(font=self.__FONT_STYLE)

        self._ety_channel_spacing = Entry(frame)
        self._ety_channel_spacing.grid(column=5, row=3, padx=5, pady=5, sticky=W)
        self._ety_channel_spacing.configure(font=self.__FONT_STYLE)
        value_channel_spacing = self.rf_object.getMdmChanSpc()
        self._ety_channel_spacing.insert(0, int(value_channel_spacing))
        self._ety_channel_spacing.configure(state='readonly')

        # enable manchester
        lab_manchester = Label(frame, text='Enable Manchester')
        lab_manchester.grid(column=0, row=4, padx=5, pady=5, sticky=E)
        lab_manchester.configure(font=self.__FONT_STYLE)

        cbx_manchester = Checkbutton(frame)
        cbx_manchester.grid(column=1, row=4, padx=5, pady=5, sticky=W)
        if self.rf_object.getEnableMdmManchester() == 1:
            self._cbx_manchester_value.set(1)
        else:
            self._cbx_manchester_value.set(0)
        cbx_manchester.configure(onvalue=1, offvalue=0, variable=self._cbx_manchester_value)

        # save settings
        self._btn_save_settings = Button(frame, text='Save all Settings', command=self.__action_store_settings)
        self._btn_save_settings.grid(column=5, row=4, padx=5, pady=5)
        self._btn_save_settings.configure(font=self.__FONT_STYLE)
        self._btn_save_settings.bind("<Enter>", lambda event: event.widget.config(fg='indian red'))
        self._btn_save_settings.bind("<Leave>", lambda event: event.widget.config(fg='black'))

    def __middle_frame(self):
        """
        Create middle frame content
        """
        frame = Frame(self._tk_obj, borderwidth=1, relief=SUNKEN, bg='#fff')
        frame.grid(column=0, row=1, padx=15, pady=15, sticky=W+E)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # headline
        lab_section = Label(frame, text="Transmit RF Settings")
        lab_section.grid(columnspan=6, row=0, padx=5, pady=5, sticky=W+E)
        lab_section.configure(font=self.__FONT_HEADLINE)

        # message
        lab_message_to_send = Label(frame, text='Message')
        lab_message_to_send.grid(column=0, row=1, padx=5, pady=5, sticky=E)
        lab_message_to_send.configure(font=self.__FONT_STYLE)

        self._ety_message_to_send = Entry(frame, width=50)
        self._ety_message_to_send.grid(column=1, row=1, padx=5, pady=5, sticky=W)
        self._ety_message_to_send.configure(font=self.__FONT_STYLE)

        btn_clear = Button(frame, text='Clear message', command=self.__action_clear_message)
        btn_clear.grid(column=2, row=1, padx=5, pady=5)
        btn_clear.configure(font=self.__FONT_STYLE)

        # repeats
        lab_repeats = Label(frame, text='Repeats')
        lab_repeats.grid(column=3, row=1, padx=5, pady=5, sticky=E)
        lab_repeats.configure(font=self.__FONT_STYLE)

        self._sbx_repeats = Spinbox(frame, width=10)
        self._sbx_repeats.grid(column=4, row=1, padx=5, pady=5, sticky=W)
        self._sbx_repeats.configure(from_=0, to=50, increment=5, state='readonly')
        self._sbx_repeats.configure(font=self.__FONT_STYLE)

        # button send
        self._btn_send = Button(frame, text='Start transmit', command=self.__action_send_signal)
        self._btn_send.grid(column=5, row=1, padx=5, pady=5, sticky=E)
        self._btn_send.configure(font=self.__FONT_STYLE)
        self._btn_send.bind("<Enter>", lambda event: event.widget.config(fg='indian red'))
        self._btn_send.bind("<Leave>", lambda event: event.widget.config(fg='black'))

        self._txt_send_status = Text(frame, height=10)
        self._txt_send_status.grid(columnspan=6, row=2, padx=5, pady=5, sticky=W+E)
        self._txt_send_status.configure(state='disabled', borderwidth=1, relief=SOLID)

    def __bottom_frame(self):
        """
        Create bottom frame content
        """
        self._cbx_max_power_value = IntVar(self._tk_obj)
        self._cbx_lowball_value = IntVar(self._tk_obj)

        frame = Frame(self._tk_obj, borderwidth=1, relief=SUNKEN, bg='#fff')
        frame.grid(column=0, row=2, padx=15, pady=15, sticky=W+E)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # headline
        txt_section = Label(frame, text="Receive RF Settings")
        txt_section.grid(columnspan=6, row=0, padx=5, pady=5, sticky=W+E)
        txt_section.configure(font=self.__FONT_HEADLINE)

        # lowball
        lab_lowball = Label(frame, text='Lowball')
        lab_lowball.grid(column=0, row=1, padx=5, pady=5, sticky=E)
        lab_lowball.configure(font=self.__FONT_STYLE)

        # @ToDo: implementation lowball
        cbx_lowball = Checkbutton(frame, state='disabled')
        cbx_lowball.grid(column=1, row=1, padx=5, pady=5, sticky=W)
        cbx_lowball.configure(onvalue=1, offvalue=0, variable=self._cbx_lowball_value)

        # max power
        lab_max_power = Label(frame, text='max Power')
        lab_max_power.grid(column=2, row=1, padx=5, pady=5, sticky=E)
        lab_max_power.configure(font=self.__FONT_STYLE)

        # @ToDo: implementation of max power
        cbx_max_power = Checkbutton(frame, state='disabled')
        cbx_max_power.grid(column=3, row=1, padx=5, pady=5, sticky=W)
        cbx_max_power.configure(onvalue=1, offvalue=0, variable=self._cbx_max_power_value)

        # receive signal
        self._btn_receive = Button(frame, text='Start receive', command=self.__action_receive_signal)
        self._btn_receive.grid(column=4, row=1, padx=5, pady=5)
        self._btn_receive.configure(font=self.__FONT_STYLE)
        self._btn_receive.bind("<Enter>", lambda event: event.widget.config(fg='indian red'))
        self._btn_receive.bind("<Leave>", lambda event: event.widget.config(fg='black'))

        # copy to clipboard
        self._btn_copy = Button(frame, text='Copy to clipboard', command=self.__action_copy_to_clipboard)
        self._btn_copy.grid(column=5, row=1, padx=5, pady=5)
        self._btn_copy.configure(font=self.__FONT_STYLE)
        self._btn_copy.bind("<Enter>", lambda event: event.widget.config(fg='indian red'))
        self._btn_copy.bind("<Leave>", lambda event: event.widget.config(fg='black'))

        # status
        self._stx_receive_status = ScrolledText(frame)
        self._stx_receive_status.grid(columnspan=6, row=2, padx=5, pady=5, sticky=W+E)
        self._stx_receive_status.configure(height=12, font=self.__FONT_STYLE, borderwidth=1, relief=SOLID)

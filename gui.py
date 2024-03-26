import tkinter as tk
from bluetooz import DiscoverDevices


class BluetoothSettings(tk.Toplevel):
    def __init__(self, parent, side):
        super().__init__(parent.root)
        self.parent = parent
        self.side = side
        if side == 'l':
            self.amp_lbl = self.parent.amp_name_l
            self.wear_lbl = self.parent.wear_name_l
        else:
            self.amp_lbl = self.parent.amp_name_r
            self.wear_lbl = self.parent.wear_name_r
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.w = 500
        self.h = 150
        self.title("Bluetooth")
        self.geometry(str(self.w) + "x" + str(self.h) + "+"
                      + str(int((screen_width - self.w) / 2)) + "+" + str(int((screen_height - self.h) / 2) - 20))
        self.resizable(False, False)
        self.lbl_amplifier = tk.Label(self, text="Усилитель:")
        self.lbl_amplifier.place(x=20, y=20)
        self.pnl_amplifier = tk.LabelFrame(self, width=400, height=30)
        self.pnl_amplifier.place(x=20, y=40)
        self.amplifier_mac = tk.Label(self.pnl_amplifier, textvariable=self.amp_lbl)
        self.amplifier_mac.place(x=5, y=3)
        self.btn_amplifier = tk.Button(self, text="..", command=lambda: self.open_list('amp'))
        self.btn_amplifier.place(x=440, y=40)

        self.lbl_wear = tk.Label(self, text="Браслет:")
        self.lbl_wear.place(x=20, y=80)
        self.pnl_wear = tk.LabelFrame(self, width=400, height=30)
        self.pnl_wear.place(x=20, y=100)
        self.wear_mac = tk.Label(self.pnl_wear, textvariable=self.wear_lbl)
        self.wear_mac.place(x=5, y=3)
        self.btn_wear = tk.Button(self, text="..", command=lambda: self.open_list('wear'))
        self.btn_wear.place(x=440, y=100)

    def open_list(self, device_type):
        bluetooth_list = BluetoothList(self, self.parent, self.side, device_type)
        bluetooth_list.grab_set()


class BluetoothList(tk.Toplevel):
    def __init__(self, parent, main, side, device_type):
        super().__init__(parent)
        self.parent = parent
        self.main = main
        self.side = side
        self.discover_devices = DiscoverDevices(self)
        self.device_type = device_type

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.w = 500
        self.h = 360
        self.title("Список устройств")
        self.geometry(str(self.w) + "x" + str(self.h) + "+"
                      + str(int((screen_width - self.w) / 2)) + "+" + str(int((screen_height - self.h) / 2) - 20))
        self.resizable(False, False)
        self.protocol('WM_DELETE_WINDOW', self.window_close)

        self.status = tk.StringVar()
        self.status.set('...')
        self.lbl_status = tk.Label(self, textvariable=self.status)
        self.lbl_status.place(x=20, y=20)

        self.list = tk.Listbox(self, width=75,  height=12)
        self.list.config(selectmode=tk.SINGLE)
        self.list.place(x=20, y=50)

        self.discover_devices = DiscoverDevices(self)
        self.discover_devices.start()

        self.btn_search = tk.Button(self, text="Обновить", command=self.start_search)
        self.btn_search.place(x=20, y=280)

        self.btn_connect = tk.Button(self, text="Подключить", command=self.connect)
        self.btn_connect.place(x=20, y=320)

        self.btn_close = tk.Button(self, text="Закрыть", command=self.window_close)
        self.btn_close.place(x=150, y=320)

    def connect(self):
        if self.device_type == 'amp':
            selection = self.list.curselection()
            device = self.list.get(selection[0])
            self.parent.amp_lbl.set(device)
            if self.side == 'l':
                self.main.start_read_amp_l(device[-1-len('00:00:00:00:00:00'): -1])
            else:
                self.main.start_read_amp_r(device[-1-len('00:00:00:00:00:00'): -1])
        else:
            # selection = self.list.curselection()
            # device = self.list.get(selection[0])
            # TODO: устройство
            # self.parent.wear_lbl.set(device)
            self.parent.wear_lbl.set("---")
            if self.side == 'l':
                self.main.start_send_l("---")  # device[-1-len('00:00:00:00:00:00'): -1])
            else:
                self.main.start_send_r("---")  # device[-1 - len('00:00:00:00:00:00'): -1])
        self.window_close()

    def start_search(self):
        self.discover_devices = DiscoverDevices(self)
        self.discover_devices.start()

    def list_refresh(self, data):
        self.list.delete(0, tk.END)
        i = 0
        for name, addr in data:
            self.list.insert(i, "%s (%s)" % (addr, name))
            i += 1
        self.update_status("Поиск завершен")

    def update_status(self, status):
        self.status.set(status)

    def window_close(self):
        self.discover_devices.stop()
        self.destroy()


class CommandSettings(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent.root)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.w = 300
        self.h = 300
        self.title("Настройка команд")
        self.geometry(str(self.w) + "x" + str(self.h) + "+"
                      + str(int((screen_width - self.w) / 2)) + "+" + str(int((screen_height - self.h) / 2) - 20))
        self.resizable(False, False)


class GraphSettings(tk.Toplevel):
    def __init__(self, parent, side, num_of_channels, active_graphs):
        super().__init__(parent.root)
        self.parent = parent
        self.side = side
        self.active_graphs = active_graphs

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.w = 300
        self.h = 550
        self.title("Выбор каналов")
        self.geometry(str(self.w) + "x" + str(self.h) + "+"
                      + str(int((screen_width - self.w) / 2)) + "+" + str(int((screen_height - self.h) / 2) - 20))
        self.resizable(False, False)

        self.num_of_channels = tk.IntVar()

        self.active_channels_8 = [tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(),
                                  tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()]
        self.active_channels_4 = [tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()]

        self.chbtns_4c = []
        self.chbtns_8c = []

        self.pnl_4c = tk.Frame(self, width=self.w - 40, height=400)
        self.pnl_8c = tk.Frame(self, width=self.w - 40, height=400)

        for i in range(0, 4):
            self.chbtns_4c.append(tk.Checkbutton(self.pnl_4c, text=self.parent.graph_names_4c[i],
                                                 variable=self.active_channels_4[i],
                                                 onvalue=1, offvalue=0, padx=15, pady=10))
            if len(active_graphs) == 4:
                if self.active_graphs[i] == 1:
                    self.chbtns_4c[i].select()
            else:
                self.chbtns_4c[i].select()
            self.chbtns_4c[i].grid(row=i, column=0, sticky=tk.W)

        for i in range(0, 8):
            self.chbtns_8c.append(tk.Checkbutton(self.pnl_8c, text=self.parent.graph_names_8c[i],
                                                 variable=self.active_channels_8[i],
                                                 onvalue=1, offvalue=0, padx=15, pady=10))
            if len(active_graphs) == 8:
                if self.active_graphs[i] == 1:
                    self.chbtns_8c[i].select()
            else:
                self.chbtns_8c[i].select()
            self.chbtns_8c[i].grid(row=i, column=0, sticky=tk.W)

        self.rb_4c = tk.Radiobutton(self, text="4 канала", value=4, variable=self.num_of_channels,
                                    command=self.change_channels, padx=15, pady=10)
        self.rb_4c.grid(row=1, column=0, sticky=tk.W)
        self.rb_8c = tk.Radiobutton(self, text="8 каналов", value=8, variable=self.num_of_channels,
                                    command=self.change_channels, padx=15, pady=10)
        self.rb_8c.grid(row=2, column=0, sticky=tk.W)

        if num_of_channels == 4:
            self.rb_4c.select()
        else:
            self.rb_8c.select()
        self.change_channels()

        self.btn_apply = tk.Button(self, text="Применить", command=self.apply)
        self.btn_apply.place(x=85, y=500)
        self.btn_close = tk.Button(self, text="Закрыть", command=self.destroy)
        self.btn_close.place(x=200, y=500)

    def apply(self):
        if self.num_of_channels.get() == 4:
            if self.side == "l":
                self.parent.num_of_channels_l = 4
                self.parent.active_graphs_l = [1, 1, 1, 1]
                for i in range(0, 4):
                    self.parent.active_graphs_l[i] = self.active_channels_4[i].get()
            if self.side == "r":
                self.parent.num_of_channels_r = 4
                self.parent.active_graphs_r = [1, 1, 1, 1]
                for i in range(0, 4):
                    self.parent.active_graphs_r[i] = self.active_channels_4[i].get()
        else:
            if self.side == "l":
                self.parent.num_of_channels_l = 8
                self.parent.active_graphs_l = [1, 1, 1, 1, 1, 1, 1, 1]
                for i in range(0, 8):
                    self.parent.active_graphs_l[i] = self.active_channels_8[i].get()
            if self.side == "r":
                self.parent.num_of_channels_r = 8
                self.parent.active_graphs_r = [1, 1, 1, 1, 1, 1, 1, 1]
                for i in range(0, 8):
                    self.parent.active_graphs_r[i] = self.active_channels_8[i].get()
        self.parent.draw_graphs()

    def change_channels(self):
        if self.num_of_channels.get() == 4:
            self.pnl_4c.place(x=20, y=100)
            self.pnl_8c.place_forget()
        else:
            self.pnl_8c.place(x=20, y=100)
            self.pnl_4c.place_forget()

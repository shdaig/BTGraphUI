import tkinter as tk
from bluetooz import GetData, SendData
from graph import Graph
from gui import GraphSettings, CommandSettings, BluetoothSettings
from PIL import ImageTk, Image


class MainWindow:
    def __init__(self):
        self.data_queue_l = [[], [], [], [], [], [], [], []]
        self.data_queue_r = [[], [], [], [], [], [], [], []]
        self.commands_l = [0, 0, 0, 0]
        self.commands_r = [0, 0, 0, 0]

        self.num_of_channels_l = 4
        self.num_of_channels_r = 4
        self.num_of_graphs_l = 0
        self.num_of_graphs_r = 0
        self.active_graphs_l = [1, 1, 1, 1]
        self.active_graphs_r = [1, 1, 1, 1]
        self.names_l = []
        self.names_r = []

        self.graph_names_8c = ["1_8", "2_8", "3_8", "4_8", "5_8", "6_8", "7_8", "8_8"]
        self.graph_names_4c = ["1_4", "2_4", "3_4", "4_4"]

        # self.get_data_thread_l = GetData(4, self.data_queue_l, 1, '0', '0')
        # self.get_data_thread_r = GetData(4, self.data_queue_r, 1, '0', '0')
        self.send_data_thread_l = SendData('0', '0')
        self.send_data_thread_r = SendData('0', '0')
        self.w = 1800
        self.h = 1000

        self.root = tk.Tk()
        self.amp_name_l = tk.StringVar()
        self.amp_name_r = tk.StringVar()
        self.wear_name_l = tk.StringVar()
        self.wear_name_r = tk.StringVar()
        self.amp_name_l.set('... (00:00:00:00:00:00)')
        self.amp_name_r.set('... (00:00:00:00:00:00)')
        self.wear_name_l.set('... (00:00:00:00:00:00)')
        self.wear_name_r.set('... (00:00:00:00:00:00)')
        self.root.protocol('WM_DELETE_WINDOW', self.main_window_was_closed)
        self.root.resizable(False, False)
        self.root.title("GraphUI")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # TODO: убрать +40 под Windows
        self.root.geometry(str(self.w) + "x" + str(self.h) + "+"
                           + str(int((screen_width - self.w) / 2)) + "+" + str(int((screen_height - self.h) / 2) - 35))

        self.wp = self.w / 2
        self.panel_left = tk.LabelFrame(self.root, width=self.wp, height=self.h, bg='#cccccc')
        self.panel_right = tk.LabelFrame(self.root, width=self.wp, height=self.h, bg='#cccccc')
        self.panel_left.place(x=0, y=0)
        self.panel_right.place(x=self.w / 2, y=0)

        self.btn_w = (self.wp-80)/3
        self.btn_h = 40
        self.btn_l_one = tk.Button(self.panel_left, text='Выбор каналов',
                                   command=lambda: self.open_graph_settings("l"))
        self.btn_l_two = tk.Button(self.panel_left, text='Настройка команд', command=self.open_command_settings)
        self.btn_l_three = tk.Button(self.panel_left, text='Bluetooth',
                                     command=lambda: self.open_bluetooth_settings('l'))
        self.btn_l_one.place(x=self.wp / 2 - self.btn_w - self.btn_w / 2 - 20, y=self.h - 40 - 20, width=self.btn_w,
                             height=self.btn_h)
        self.btn_l_two.place(x=self.wp / 2 - self.btn_w / 2, y=self.h - 40 - 20, width=self.btn_w, height=self.btn_h)
        self.btn_l_three.place(x=self.wp / 2 + self.btn_w / 2 + 20, y=self.h - 40 - 20, width=self.btn_w,
                               height=self.btn_h)
        self.btn_r_one = tk.Button(self.panel_right, text='Выбор каналов',
                                   command=lambda: self.open_graph_settings("r"))
        self.btn_r_two = tk.Button(self.panel_right, text='Настройка команд', command=self.open_command_settings)
        self.btn_r_three = tk.Button(self.panel_right, text='Bluetooth',
                                     command=lambda: self.open_bluetooth_settings('r'))
        self.btn_r_one.place(x=self.wp / 2 - self.btn_w - self.btn_w / 2 - 20, y=self.h - 40 - 20, width=self.btn_w,
                             height=self.btn_h)
        self.btn_r_two.place(x=self.wp / 2 - self.btn_w / 2, y=self.h - 40 - 20, width=self.btn_w, height=self.btn_h)
        self.btn_r_three.place(x=self.wp / 2 + self.btn_w / 2 + 20, y=self.h - 40 - 20, width=self.btn_w,
                               height=self.btn_h)

        self.graph_l = []
        self.graph_r = []

        self.draw_graphs()

        # Индикаторы команд
        self.lamps_left = tk.Frame(self.panel_left, height=90, width=500, bg='#cccccc')
        self.lamps_left.place(x=200, y=self.h - 160)
        self.lamps_right = tk.Frame(self.panel_right, height=90, width=500, bg='#cccccc')
        self.lamps_right.place(x=200, y=self.h - 160)

        img_lamp_off_raw = Image.open('pictures/lamp_off.png')
        img_lamp_on_raw = Image.open('pictures/lamp_on.png')
        k = img_lamp_off_raw.height / 39
        img_lamp_off_raw = img_lamp_off_raw.resize((int(img_lamp_off_raw.width / k),
                                                    int(img_lamp_off_raw.height / k)), Image.ANTIALIAS)
        img_lamp_on_raw = img_lamp_on_raw.resize((int(img_lamp_on_raw.width / k),
                                                  int(img_lamp_on_raw.height / k)), Image.ANTIALIAS)
        self.img_lamp_off = ImageTk.PhotoImage(img_lamp_off_raw)
        self.img_lamp_on = ImageTk.PhotoImage(img_lamp_on_raw)

        self.image_labels_left = []
        self.image_labels_right = []

        self.btns_test_left = []
        self.btns_test_right = []

        step = (500 - 40) / 3
        i = 0
        for command in self.commands_l:
            img = None
            if command:
                img = self.img_lamp_on
            else:
                img = self.img_lamp_off
            self.image_labels_left.append(tk.Label(self.lamps_left, image=img, bg='#cccccc'))
            self.image_labels_left[i].place(x=step * i, y=0)

            self.btns_test_left.append(tk.Button(self.lamps_left, text=''))
            self.btns_test_left[i].place(x=step * i, y=50, height=20, width=40)
            i += 1

        self.btns_test_left[0].config(command=lambda: self.test_command_was_pressed(self.image_labels_left[0],
                                                                                    self.btns_test_left[0], "l", "red"))
        self.btns_test_left[1].config(command=lambda: self.test_command_was_pressed(self.image_labels_left[1],
                                                                                    self.btns_test_left[1], "l", "yellow"))
        self.btns_test_left[2].config(command=lambda: self.test_command_was_pressed(self.image_labels_left[2],
                                                                                    self.btns_test_left[2], "l", "green"))
        self.btns_test_left[3].config(command=lambda: self.test_command_was_pressed(self.image_labels_left[3],
                                                                                    self.btns_test_left[3], "l", "blue"))
        i = 0
        for command in self.commands_r:
            img = None
            if command:
                img = self.img_lamp_on
            else:
                img = self.img_lamp_off
            self.image_labels_right.append(tk.Label(self.lamps_right, image=img, bg='#cccccc'))
            self.image_labels_right[i].place(x=step * i, y=0)

            self.btns_test_right.append(tk.Button(self.lamps_right, text=''))
            self.btns_test_right[i].place(x=step * i, y=50, height=20, width=40)
            i += 1

        self.btns_test_right[0].config(command=lambda: self.test_command_was_pressed(self.image_labels_right[0],
                                                                                     self.btns_test_right[0], "r", "red"))
        self.btns_test_right[1].config(command=lambda: self.test_command_was_pressed(self.image_labels_right[1],
                                                                                     self.btns_test_right[1], "r", "yellow"))
        self.btns_test_right[2].config(command=lambda: self.test_command_was_pressed(self.image_labels_right[2],
                                                                                     self.btns_test_right[2], "r", "green"))
        self.btns_test_right[3].config(command=lambda: self.test_command_was_pressed(self.image_labels_right[3],
                                                                                     self.btns_test_right[3], "r", "blue"))
        # Запуск потоков чтения
        # self.get_data_thread_l.start()
        # self.get_data_thread_r.start()

    def open_bluetooth_settings(self, side):
        if side == 'l':
            bluetooth_settings = BluetoothSettings(self, 'l')
            bluetooth_settings.grab_set()
        else:
            bluetooth_settings = BluetoothSettings(self, 'r')
            bluetooth_settings.grab_set()

    def start_read_amp_l(self, addr):
        self.get_data_thread_l = GetData(self.num_of_channels_l, self.data_queue_l, 1, addr, 'L')
        self.get_data_thread_l.start()

    def start_read_amp_r(self, addr):
        self.get_data_thread_r = GetData(self.num_of_channels_r, self.data_queue_r, 1, addr, 'R')
        self.get_data_thread_r.start()

    def start_send_l(self, addr):
        self.send_data_thread_l = SendData(addr, 'L')
        self.send_data_thread_l.start()

    def start_send_r(self, addr):
        self.send_data_thread_r = SendData(addr, 'R')
        self.send_data_thread_r.start()

    def main_window_was_closed(self):
        self.send_data_thread_l.stop()
        self.send_data_thread_r.stop()
        self.get_data_thread_l.stop()
        self.get_data_thread_r.stop()
        self.root.destroy()

    def test_command_was_pressed(self, lamp_label, btn, side, command):
        lamp_label.config(image=self.img_lamp_on)
        btn["state"] = tk.DISABLED
        lamp_label.after(1000, lambda: lamp_label.config(image=self.img_lamp_off))
        btn.after(1000, lambda: self.enable_btn(btn))
        if side == 'l':
            self.send_data_thread_l.change_command(command)
        else:
            self.send_data_thread_r.change_command(command)

    def enable_btn(self, btn):
        btn["state"] = tk.NORMAL

    def open_command_settings(self):
        command_settings = CommandSettings(self)
        command_settings.grab_set()

    def open_graph_settings(self, side):
        if side == "l":
            graph_settings = GraphSettings(self, side, self.num_of_channels_l, self.active_graphs_l)
            graph_settings.grab_set()
        else:
            graph_settings = GraphSettings(self, side, self.num_of_channels_r, self.active_graphs_r)
            graph_settings.grab_set()

    def draw_graphs(self):
        self.num_of_graphs_l = 0
        self.num_of_graphs_r = 0

        for graph in self.graph_l:
            if graph:
                graph.remove()

        for graph in self.graph_r:
            if graph:
                graph.remove()

        for active in self.active_graphs_l:
            self.num_of_graphs_l += active
        for active in self.active_graphs_r:
            self.num_of_graphs_r += active

        if self.num_of_channels_l == 8:
            self.names_l = self.graph_names_8c
        else:
            self.names_l = self.graph_names_4c

        if self.num_of_channels_r == 8:
            self.names_r = self.graph_names_8c
        else:
            self.names_r = self.graph_names_4c

        graph_height_l = int((self.h - 26 * self.num_of_graphs_l - 200) / self.num_of_graphs_l)
        graph_height_r = int((self.h - 26 * self.num_of_graphs_r - 200) / self.num_of_graphs_r)
        self.graph_l = []
        i = 0
        j = 0
        for active_graph in self.active_graphs_l:
            if active_graph:
                self.graph_l.append(Graph(self.panel_left, self.names_l[j], 20, 26 * (i + 1) + graph_height_l * i,
                                          graph_height_l, 860, 10000, 100, 25, self.data_queue_l[i]))
                i += 1
            else:
                self.graph_l.append(None)
            j += 1

        self.graph_r = []
        i = 0
        j = 0
        for active_graph in self.active_graphs_r:
            if active_graph:
                self.graph_r.append(Graph(self.panel_right, self.names_r[j], 20, 26 * (i + 1) + graph_height_r * i,
                                          graph_height_r, 860, 10000, 100, 25, self.data_queue_r[i]))
                i += 1
            else:
                self.graph_l.append(None)
            j += 1

        for graph in self.graph_l:
            if graph:
                graph.start_read_data()

        for graph in self.graph_r:
            if graph:
                graph.start_read_data()


if __name__ == '__main__':
    main_window = MainWindow()
    main_window.root.mainloop()

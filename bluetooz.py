import threading
from collections import deque
import bluetooth
from bluetooth import Protocols
import array
import datetime
from time import sleep


class DiscoverDevices(threading.Thread):
    def __init__(self, parent):
        super().__init__()
        self.socket = bluetooth.BluetoothSocket(Protocols.RFCOMM)
        self.device_list = []
        self.parent = parent
        self.running = True

    def run(self):
        self.parent.update_status("Поиск устройств...")
        self.device_list = bluetooth.discover_devices(lookup_names=True)

        for name, addr in self.device_list:
            print("%s - %s" % (addr, name))

        if self.running:
            self.parent.list_refresh(self.device_list)

    def stop(self):
        self.running = False


class SendData(threading.Thread):
    def __init__(self, addr, side):
        super().__init__()
        self.wear_mac_addr = addr
        self.running = True
        self.error = False
        self.side = side
        if side == "L":
            self.uuid = "..."
        else:
            self.uuid = "..."
        self.name = "SampleServer" + self.side
        self.socket = None
        self.command = "none"

    def run(self):
        try:
            self.socket = bluetooth.BluetoothSocket(Protocols.RFCOMM)
            self.socket.bind(("", bluetooth.PORT_ANY))
            self.socket.listen(5)
            print(self.uuid)
            print(self.name)
            bluetooth.advertise_service(self.socket, self.name, service_id=self.uuid,
                                        service_classes=[self.uuid, bluetooth.SERIAL_PORT_CLASS],
                                        profiles=[bluetooth.SERIAL_PORT_PROFILE])
            print("open")
            print("wait for client")
            client, client_info = self.socket.accept()
            print("got client")
            # client.send("Hello")
            # print(self.wear_mac_addr)
            # bluetooth.find_service("")
            # self.socket.connect((self.wear_mac_addr, 2))
            # self.socket.send("fgd")

            # i = 0
            while not self.error and self.running:
                try:
                    if self.command != "none":
                        client.send(self.command)
                        self.command = "none"
                    sleep(1)
            #         i += 1
                except:
                    self.error = True
        except:
            self.error = True
            print('Подключиться к Bluetooth-устройству не удалось!')
            return

    def change_command(self, command):
        self.command = command

    def close_connection(self):
        if self.socket is not None:
            self.socket.close()

    def stop(self):
        self.running = False
        self.close_connection()


class GetData(threading.Thread):
    def __init__(self, channel_count, data_queue, port, addr, side):
        super().__init__()
        self.data_queue = data_queue
        self.amp_mac_addr = addr
        self.port = port
        self.buffer_size = 100
        self.running = True
        self.channel_count = channel_count
        self.len_package = self.channel_count * 2
        self.buff = deque(maxlen=self.buffer_size)
        self.package = []
        self.chunk = ''
        self.error = False
        self.socket = bluetooth.BluetoothSocket()
        self.do_save = True
        if side == '0':
            self.do_save = False
        self.data_file_name = "data/sig_" + side + "_" + str(datetime.datetime.now()).replace(':', '.') + ".dat"
        self.data = array.array('f')

    def run(self):
        try:
            # print(bluetooth.discover_devices())
            self.socket.connect((self.amp_mac_addr, self.port))
        except:
            self.error = True
            print('Подключиться к Bluetooth-устройству не удалось!')
            return

        # Read signal
        # self.file = open("some.dat", "w")
        # self.file.close()

    def close_connection(self):
        self.socket.close()
        if self.do_save:
            self.save_data()

    def save_data(self):
        f = open(self.data_file_name, 'wb')
        self.data.tofile(f)
        f.close()

    def stop(self):
        self.running = False
        self.close_connection()

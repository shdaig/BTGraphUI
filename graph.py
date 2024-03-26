import tkinter as tk


class Graph:
    def __init__(self, parent, name, x, y, height, width, time, graph_update_freq, data_update_freq, data_queue):
        self.parent = parent
        self.name = name
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.time = time
        self.graph_update_freq = graph_update_freq
        self.data_update_freq = data_update_freq
        self.data_queue = data_queue

        self.exist = True

        self.step = int((self.width - 40) * data_update_freq / self.time)
        self.len_graph_buf = int(self.time / data_update_freq)
        self.deviation = int(((self.width - 40) - ((self.len_graph_buf - 1) * self.step)) / 2)
        self.current_value = 0
        self.previous_value = 0
        self.graph_queue = []
        for i in range(0, self.len_graph_buf):
            self.graph_queue.append(0)

        self.root = tk.LabelFrame(self.parent, height=self.height+23, width=self.width+6, text=self.name, bg='#cccccc')
        self.root.place(x=self.x, y=self.y)
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg='white')
        self.canvas.place(x=0, y=0)
        self.canvas.create_line(20 + self.deviation, 10, 20 + self.deviation, self.height - 10)
        self.canvas.create_line(self.width - 20 - self.deviation, 10,
                                self.width - 20 - self.deviation, self.height - 10)
        self.canvas.create_line(20 + self.deviation, self.height / 2,
                                self.width - 20 - self.deviation, self.height / 2)

    def start_read_data(self):
        self.do_asyncio()

    def do_asyncio(self):
        self.root.after(50, self.refresh_data)

    def refresh_data(self):
        if self.exist:
            self.canvas.delete("all")

            self.canvas.create_line(20 + self.deviation, 20,
                                    self.width - 20 - self.deviation, 20, fill="lightgray")
            self.canvas.create_line(20 + self.deviation, self.height - 20,
                                    self.width - 20 - self.deviation, self.height - 20, fill="lightgray")

            self.canvas.create_line(20 + self.deviation, (self.height / 2 + 20) / 2,
                                    self.width - 20 - self.deviation, (self.height / 2 + 20) / 2, fill="lightgray")
            self.canvas.create_line(20 + self.deviation, self.height - (self.height / 2 + 20) / 2,
                                    self.width - 20 - self.deviation, self.height - (self.height / 2 + 20) / 2,
                                    fill="lightgray")

            self.canvas.create_line(20 + self.deviation, 10, 20 + self.deviation, self.height - 10)
            self.canvas.create_line(self.width - 20 - self.deviation, 10,
                                    self.width - 20 - self.deviation, self.height - 10)
            self.canvas.create_line(20 + self.deviation, self.height / 2,
                                    self.width - 20 - self.deviation, self.height / 2)

            while not len(self.data_queue) == 0:
                self.graph_queue.append(self.data_queue.pop(0) * int(self.height / 2 - 10))
                self.graph_queue.pop(0)

            j = len(self.graph_queue) - 1
            self.current_value = self.graph_queue[j]
            i = 0

            max = 1e-7
            for g in self.graph_queue:
                if abs(g) > max:
                    max = abs(g)

            self.canvas.create_text(2 + self.deviation, 20, text=str(round(max, 1)), font=("Calibri", 5))
            self.canvas.create_text(2 + self.deviation, self.height - 20, text=str(-round(max, 1)),
                                    font=("Calibri", 5))

            self.canvas.create_text(2 + self.deviation, (self.height / 2 + 20) / 2, text=str(round(max / 2, 1)),
                                    font=("Calibri", 5))
            self.canvas.create_text(2 + self.deviation, self.height - (self.height / 2 + 20) / 2,
                                    text=str(-round(max / 2, 1)), font=("Calibri", 5))

            mScale = (int(self.height / 2) - 20) / max

            for j in range(self.len_graph_buf - 2, -1, -1):
                self.previous_value = self.current_value
                self.current_value = self.graph_queue[j]
                self.canvas.create_line(i + 20 + self.deviation,
                                        int(-self.previous_value * mScale) + int(self.height / 2),
                                        i + self.step + 20 + self.deviation,
                                        int(-self.current_value * mScale) + int(self.height / 2),
                                        fill="red")
                i += self.step

            self.root.after(self.graph_update_freq, self.refresh_data)

    def remove(self):
        self.exist = False
        self.root.destroy()

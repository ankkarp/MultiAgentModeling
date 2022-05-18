import random
import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
# import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class PR8(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.n = tk.StringVar(value="256")
        self.period = tk.StringVar(value="30")
        self.it_duration = tk.StringVar(value='2000')
        self.day = 0
        self.frame = StartFrame(self)
        self.frame.pack()
        self.switch_frame = master.switch_frame
        self.vcmd = master.vcmd
        self.log_data = []
        # scrollbar = tk.Scrollbar(self, orient="vertical")
        self.table = Table(self)
        self.table.pack(side='left', fill=tk.Y)
        # scrollbar.config(command=self.table.xview)
        # scrollbar.pack(side='left', fill=tk.Y)


class Table(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.update()

    def update(self):
        if self.master.log_data:
            for i, k in enumerate(self.master.log_data[0].keys()):
                tk.Label(self, text=k, borderwidth=1, relief=tk.RIDGE, width=len(k)).grid(row=0, column=i)
        for row, data in enumerate(self.master.log_data):
            for column, (k, v) in enumerate(data.items()):
                tk.Label(self, text=v, borderwidth=1, relief=tk.RIDGE, width=len(k)).grid(row=row + 1, column=column)
        if len(self.master.log_data) < int(self.master.period.get()):
            self.after(int(self.master.it_duration.get()), self.update)


class StartFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Кол-во дней").pack(side='top', fill=tk.X)
        tk.Entry(self, validate='key', validatecommand=(master.master.vcmd, '%P'),
                 textvariable=master.period).pack(side='top', fill=tk.X)
        tk.Label(self, text="Длина дня (мс)").pack(side='top', fill=tk.X)
        tk.Entry(self, validate='key', validatecommand=(master.master.vcmd, '%P'),
                 textvariable=master.it_duration).pack(side='top', fill=tk.X)
        tk.Label(self, text="Население").pack()
        values = [str(i ** 2) for i in range(10, 101)]
        tk.ttk.Combobox(self, state="readonly", textvariable=master.n, values=values).pack()
        tk.Button(self, text='Старт', command=lambda: master.switch_frame(master, PlotFrame)).pack()


class InfoFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.infectivity = tk.StringVar(value="10")
        self.day_label = tk.Label(self, text=f"День {self.master.day}/{int(master.period.get())}")
        self.day_label.pack(side='top', fill=tk.X)
        self.update()
        tk.Label(self, text=f"Популяция из {int(master.n.get())} челоовек").pack(side='top', fill=tk.X)
        tk.Label(self, text="Заразность").pack(side='top', fill=tk.X)
        tk.Entry(self, validate='key', validatecommand=(master.vcmd, '%P'),
                 textvariable=self.infectivity).pack(side='top', fill=tk.X)
        self.incubation_t = tk.StringVar(value="5")
        tk.Label(self, text="Инкубационный период").pack(side='top', fill=tk.X)
        tk.Entry(self, validate='key', validatecommand=(master.vcmd, '%P'),
                 textvariable=self.incubation_t).pack(side='top', fill=tk.X)
        self.sick_t = tk.StringVar(value="5")
        tk.Label(self, text="Длительность болезни").pack(side='top', fill=tk.X)
        tk.Entry(self, validate='key', validatecommand=(master.vcmd, '%P'),
                 textvariable=self.sick_t).pack(side='top', fill=tk.X)
        tk.Button(self, text='Выйти', command=lambda: master.switch_frame(master, PlotFrame)).pack()

    def update(self):
        self.day_label['text'] = f"День {self.master.day}/{int(self.master.period.get())}"
        if self.master.day < int(self.master.period.get()):
            self.day_label.after(int(self.master.it_duration.get()), self.update)


class PlotFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.info_frame = InfoFrame(master)
        self.info_frame.pack(side='right')
        self.popul = np.zeros((int(master.n.get()),), dtype=int)
        # print(self.popul)
        self.popul[0] = 1
        self.fig = plt.Figure()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)  # A tk.DrawingArea.
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.update()

    def update(self):
        print(self.popul)
        if not self.info_frame.incubation_t.get():
            self.info_frame.incubation_t.set('0')
        if not self.info_frame.sick_t.get():
            self.info_frame.sick_t.set('0')
        if not self.info_frame.infectivity.get():
            self.info_frame.infectivity.set('0')
        if not self.info_frame.infectivity.get():
            self.info_frame.infectivity.set('0')
        fills = ['#324C3D', '#4BB32E']
        self.master.day += 1
        infective = (self.popul < (int(self.info_frame.incubation_t.get()) + int(self.info_frame.sick_t.get()))).sum()
        new_infected = np.random.randint(low=0, high=len(self.popul),
                                         size=(int(infective*int(self.info_frame.infectivity.get())/100)))
        # print(self.popul)
        for i, p in enumerate(self.popul):
            if p != 0:
                self.popul[i] += 1
            if i in new_infected and p == 0:
                self.popul[i] = 1
        infected = (self.popul < int(self.info_frame.incubation_t.get())).sum() - (self.popul == 0).sum()
        sick = (self.popul < (int(self.info_frame.sick_t.get())) + int(self.info_frame.incubation_t.get())).sum() \
               - (self.popul == 0).sum() - infected
        self.master.log_data.append({"День": self.master.day,
                                     "Здоровые": (self.popul == 0).sum(),
                                     "Зараженные": infected,
                                     "Больные": sick,
                                     "Переболевшие": (self.popul > (int(self.info_frame.sick_t.get()))
                                                      + int(self.info_frame.incubation_t.get())).sum()})
        log_df = pd.DataFrame(self.master.log_data)
        self.fig.clear()
        # for i, state in enumerate(log_df):
            # plot = log_df.plot()
        ax = self.fig.add_subplot(111)
        ax.plot(log_df, label=log_df.columns)
        ax.legend(loc="upper right")
        self.canvas.draw_idle()
        if self.master.day <= int(self.master.period.get()):
            self.after(int(self.master.it_duration.get()), self.update)
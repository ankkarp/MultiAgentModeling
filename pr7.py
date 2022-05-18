import random
import tkinter as tk
import tkinter.ttk as ttk
import numpy as np


class PR7(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.n = tk.StringVar(value="256")
        self.period = tk.StringVar(value="30")
        self.it_duration = tk.StringVar(value='2000')
        self.day = 1
        self.frame = StartFrame(self)
        self.frame.pack()
        self.switch_frame = master.switch_frame
        self.vcmd = master.vcmd
        self.log_data = []
        self.table = Table(self)
        self.table.pack(side='bottom', fill=tk.X)


class Table(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.update()

    def update(self):
        if self.master.log_data:
            tk.Label(self, text="День", borderwidth=1, relief=tk.RIDGE, width=15).grid(row=0, column=0)
            tk.Label(self, text="Не пользователи", borderwidth=1, relief=tk.RIDGE, width=15).grid(row=1, column=0)
            tk.Label(self, text="Пользователи", borderwidth=1, relief=tk.RIDGE, width=15).grid(row=2, column=0)
        for i, data in enumerate(self.master.log_data):
            tk.Label(self, text=str(i+1), borderwidth=1, relief=tk.RIDGE,
                     width=len(self.master.n.get())).grid(row=0, column=i+1)
            tk.Label(self, text=str(data['potential']), borderwidth=1, relief=tk.RIDGE,
                     width=len(self.master.n.get())).grid(row=1, column=i+1)
            tk.Label(self, text=str(data['users']), borderwidth=1, relief=tk.RIDGE,
                     width=len(self.master.n.get())).grid(row=2, column=i+1)
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
        self.consumers_per_day = tk.StringVar(value="10")
        self.day_label = tk.Label(self, text=f"День {self.master.day}/{int(master.period.get())}")
        self.day_label.pack(side='top', fill=tk.X)
        self.update()
        tk.Label(self, text=f"Популяция из {int(master.n.get())} челоовек").pack(side='top', fill=tk.X)
        tk.Label(self, text="Процент потребителей в день").pack(side='top', fill=tk.X)
        tk.Entry(self, validate='key', validatecommand=(master.vcmd, '%P'),
                 textvariable=self.consumers_per_day).pack(side='top', fill=tk.X)
        self.best_before = tk.StringVar(value="5")
        tk.Label(self, text="Срок годности продукта (дни)").pack(side='top', fill=tk.X)
        tk.Entry(self, validate='key', validatecommand=(master.vcmd, '%P'),
                 textvariable=self.best_before).pack(side='top', fill=tk.X)
        tk.Button(self, text='Выйти', command=lambda: master.switch_frame(master, PlotFrame)).pack()

    def update(self):
        self.day_label['text'] = f"День {self.master.day}/{int(self.master.period.get())}"
        if self.master.day < int(self.master.period.get()):
            self.day_label.after(int(self.master.it_duration.get()), self.update)


class PlotFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.n = int(master.n.get())
        self.m = np.sqrt(self.n)
        self.cell_size = 700 / self.m
        self.info_frame = InfoFrame(master)
        self.info_frame.pack(side='right')
        self.popul = np.zeros(self.n)
        self.user_count = 0
        self.plot = tk.Canvas(self, width=1500, height=700)
        self.update_plot()
        self.plot.grid(row=0, column=0)


    def update_plot(self):
        if not self.info_frame.best_before.get():
            self.info_frame.best_before.set('0')
        if not self.info_frame.consumers_per_day.get():
            self.info_frame.consumers_per_day.set('0')

        fills = ['#324C3D', '#4BB32E']
        self.master.day += 1

        users_to_be = random.sample(list(np.arange(len(self.popul))),
                                    int(int(self.info_frame.consumers_per_day.get()) / 100 * len(self.popul)
                                    + self.user_count))
        for i in range(len(self.popul)):
            if i in users_to_be:
                self.popul[i] = 1
            elif self.popul[i] > int(self.info_frame.best_before.get()):
                self.popul[i] = 0
            elif self.popul[i] > 0:
                self.popul[i] += 1
            self.plot.create_rectangle(i // self.m * self.cell_size, i % self.m * self.cell_size,
                                       (i // self.m + 1) * self.cell_size, (i % self.m + 1) * self.cell_size,
                                       fill=fills[bool(self.popul[i])])
        bar_width = 600 / int(self.master.period.get())
        day = self.master.day - 2
        self.plot.create_rectangle(720 + day * bar_width, 700,
                                   720 + (day+0.5)*bar_width, 700*(1-(self.popul == 0).sum()/len(self.popul)),
                                   fill=fills[0])
        self.plot.create_rectangle(720 +  (day+0.5)*bar_width, 700,
                                   720 + (day+1) * bar_width, 700*(1-(self.popul != 0).sum()/len(self.popul)),
                                   fill=fills[1])
        self.master.log_data.append({'potential': (self.popul == 0).sum(), 'users': (self.popul != 0).sum()})
        if self.master.day <= int(self.master.period.get()):
            self.plot.after(int(self.master.it_duration.get()), self.update_plot)
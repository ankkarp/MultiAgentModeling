import random
import tkinter as tk
import tkinter.ttk as ttk

import numpy as np


def validate(P):
    if str.isdigit(P) and len(P) < 4 or P == "":
        return True
    else:
        return False

        # frame_info = tk.Frame(master=window, width=1000, height=700)
        # frame_info.pack(side=tk.RIGHT)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.plot_size = 800
        self.geometry("1900x1000")
        self.n = tk.StringVar(value="100")
        self.vcmd = (self.register(validate))
        self.n_choice = tk.ttk.Combobox(textvariable=self.n,
                                        values=["100", "400"]).place(x=1300, y=50)
        self.n_label = tk.Label(text="Число людей в популяции").place(x=1300, y=30)
        self.consumers_per_day = tk.StringVar(value="10")
        self.consumers_per_day_input = tk.Entry(validate='key', validatecommand=(self.vcmd, '%P'),
                                                textvariable=self.consumers_per_day).place(x=1300, y=100)
        self.consumers_per_day_label = tk.Label(text="Процент потребителей в день").place(x=1300, y=80)
        self.best_before = tk.StringVar(value="5")
        self.best_before_input = tk.Entry(validate='key', validatecommand=(self.vcmd, '%P'),
                                          textvariable=self.best_before).place(x=1300, y=150)
        self.best_before_label = tk.Label(text="Срок сохранности продукта в днях").place(x=1300, y=130)
        # frame_plot = tk.Frame(master=window, width=500, height=700)
        # frame_plot.pack(side=tk.RIGHT)
        # print(type(self.m))
        self.popul = np.zeros(int(self.n.get()), dtype=int)
        self.plot = tk.Canvas(width=self.plot_size, height=self.plot_size, bg='white')
        self.update_plot()
        self.plot.pack(side=tk.LEFT)
        self.mainloop()

    def update_plot(self):
        n = int(self.n.get())
        m = np.sqrt(n)
        cell_size = np.sqrt(800 * 800 / n)
        fills = ['white', 'yellow', 'green']
        for i, state in enumerate(self.popul):
            self.plot.create_rectangle(i // m * cell_size, i % m * cell_size, (i // m + 1) * cell_size,
                                       (i % m + 1) * cell_size, outline="black", fill=fills[random.randint(0, 2)])
        self.plot.after(1000, self.update_plot)


if __name__ == '__main__':
    app = App()
    app.mainloop()

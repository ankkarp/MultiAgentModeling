import random
import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
from pr7 import PR7
from pr8 import PR8
from pr9 import PR9


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('1500x1000')
        self.tabControl = ttk.Notebook(self)
        self.vcmd = (self.register(self.validate))
        self.pr7 = PR7(self)
        self.pr8 = PR8(self)
        self.pr9 = PR9(self)
        self.tabControl.add(self.pr7, text='Практическая работа 7')
        self.tabControl.add(self.pr8, text='Практическая работа 8')
        self.tabControl.add(self.pr9, text='Практическая работа 9')
        self.tabControl.pack(expand=True, fill=tk.BOTH)


    def validate(self, P):
        return str.isdigit(P) and len(P) < 4 or P == ''

    def switch_frame(self, master, new_frame, destroy_frames=None):
        """Destroys current frame and replaces it with a new one."""
        try:
            master.frame.destroy()
            for frame in destroy_frames:
                frame.destroy()
        except Exception as e:
            print(e)
        master.frame = new_frame(master)
        master.frame.pack()

    def num(self, var):
        val = var.get()
        return 0 if val == '' else int(val)


if __name__ == '__main__':
    app = App()
    app.mainloop()
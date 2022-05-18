import tkinter as tk
import random
import numpy as np


class PR9(tk.Canvas):
    def __init__(self, master):
        tk.Canvas.__init__(self, master)
        self.width = 1500
        self.height = 1000
        self.boat = {'x': 200, 'move': 100}
        # self.p_img = tk.PhotoImage(file='person.png')
        self.people = np.array([])
        self.update()

    def update(self):
        self.create_rectangle(0, 0, self.width, self.height, fill='white')
        self.create_rectangle(0, self.height / 2, 200, self.height, fill='#E0997E')
        self.create_rectangle(self.width - 200, self.height / 2, self.width, self.height, fill='#E0997E')
        self.create_rectangle(200, self.height / 2 + 10, self.width - 200, self.height, fill='#6674E0')
        self.create_rectangle(self.boat['x'], self.height / 2, self.boat['x'] + 100, self.height / 2 + 10, fill='black')
        if len(self.people) < 4 and random.randint(0, 5) == 0:
            self.people = np.append(self.people,
                                    {'x': random.randint(self.width - 200, self.width), 'status': 'waiting'})
        for p in self.people:
            self.create_rectangle(p['x'], self.height / 2, p['x'] + 5, self.height / 2 - 15, fill='grey')
        self.people = [p for p in self.people if p['status'] != 'leaving']
        if self.boat['x'] == self.width - 300 and self.boat['move'] > 0:
            self.boat['move'] *= -1
            for p in self.people:
                if p['status'] == 'waiting':
                    p['status'] = 'boarded'
                    p['x'] = self.boat['x'] + random.randint(0, 95)
        elif self.boat['x'] == 200 and self.boat['move'] < 0:
            self.boat['move'] *= -1
            for p in self.people:
                if p['status'] == 'boarded':
                    p['status'] = 'leaving'
                    p['x'] = random.randint(0, 200)
        else:
            self.boat['x'] += self.boat['move']
            for p in self.people:
                if p['status'] == 'boarded':
                    p['x'] += self.boat['move']
        self.after(1000, self.update)

# --- clock.py ---
#!/usr/bin/python3
#A simple clock implementation

import sys, os, select, time, threading, datetime
import tkinter as tk
from tkinter import ttk

class Clock:
    def __init__(self):
        self.colors = ("white", "black", "red", "blue", "green", "yellow", "cyan", "magenta")
        self.curClockColor = 1
        self.curBackgroundColor = 0
        self.globalTime = False
        self.separator = ":"
        self.clock_font_size = 70
        self.system_time = datetime.datetime.now()

    def colorChange(self):
        if self.curClockColor+1 >= len(self.colors):
            self.curClockColor = 0
        else:
            self.curClockColor += 1

        self.clock_label.config(foreground = self.colors[self.curClockColor])

    def backgroundChange(self):
        if self.curBackgroundColor+1 >= len(self.colors):
            self.curBackgroundColor = 0
        else:
            self.curBackgroundColor += 1

        self.root.config(background = self.colors[self.curBackgroundColor])
        self.clock_label.config(background = self.colors[self.curBackgroundColor])

    def increseTextSize(self):
        self.clock_font_size += 10
        self.clock_label.configure(font = ('calibri', self.clock_font_size, 'bold'))

    def decreseTextSize(self):
        self.clock_font_size -= 10
        self.clock_label.configure(font = ('calibri', self.clock_font_size, 'bold'))

    def clock(self):
        self.root = tk.Tk()
        self.root.geometry('700x500')
        self.root.resizable(True, True)
        self.root.iconbitmap('icons/clock.ico')
        style = ttk.Style(self.root)
        style.configure('root.TButton', font = ('calibri', 20, 'bold'))
        self.root.title('Clock')

        self.am_pm_button = ttk.Button(self.root, text="12Hr time", style = 'root.TButton', command=lambda: self.time_style(12))
        self.am_pm_button.pack(fill = 'both', expand=True, anchor='w')
        self.global_time_button = ttk.Button(self.root, text="24 Hr time", style = 'root.TButton', command=lambda: self.time_style(24))
        self.global_time_button.pack(fill = 'both', expand=True, anchor='e')

        self.clock_label = ttk.Label(self.root, text="00:00:00", font = ('calibri', self.clock_font_size, 'bold'), foreground="black",  wraplength=700)

        self.color_change_button = ttk.Button(self.root, text="Color", style = 'root.TButton', command=self.colorChange, width=5)
        self.background_color_change_button = ttk.Button(self.root, text="Background", style = 'root.TButton', command=self.backgroundChange, width=10)
        self.plus_size = ttk.Button(self.root, text="+", style = 'root.TButton', command=self.increseTextSize, width=2)
        self.minus_size = ttk.Button(self.root, text="-", style = 'root.TButton', command=self.decreseTextSize, width=2)

        self.root.mainloop()

    def time_style(self, hour_setting):
        if hour_setting == 12: self.globalTime = False
        else: self.globalTime = True

        self.am_pm_button.destroy()
        self.global_time_button.destroy()
        self.clock_label.place(relx=0.5, rely=0.5, anchor='center')
        self.color_change_button.pack(side = 'left', anchor='s')
        self.background_color_change_button.pack(side = 'left', anchor='s')
        self.plus_size.pack(side = 'right', anchor='s')
        self.minus_size.pack(side = 'right', anchor='s')

        self.count()

    def count(self):

        self.system_time = datetime.datetime.now()

        if int(self.system_time.strftime("%S")) % 2 == 0:
            self.separator = ":"
        else:
            self.separator = " "

        if self.globalTime == True:
            self.clock_label.configure(text = (self.system_time.strftime("%H" + self.separator + "%M" + self.separator + "%S")), font = ('calibri', self.clock_font_size, 'bold'), wraplength=self.root.winfo_width())
        else:
            self.clock_label.configure(text = (self.system_time.strftime("%I" + self.separator + "%M" + self.separator + "%S %p")), font = ('calibri', self.clock_font_size, 'bold'), wraplength=self.root.winfo_width())

        self.clock_label.after(1000, self.count)

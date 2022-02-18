# --- stopwatch.py ---
#!/usr/bin/python3
#A simple stopwatch implementation

import sys, os, select, time, threading
import tkinter as tk
from tkinter import ttk

def sleep(sleep_time):
	time.sleep(sleep_time)

class Stopwatch:
    def __init__(self):
        self.laps = []
        self.timerIncrement = 1
        self.currentSeconds = 0
        self.currentMinutes = 0
        self.currentHours = 0
        self.separator = ":"
        self.newOutput = ""
        self.currentOutput = ""

    def addLap(self):
        self.laps.append(self.currentOutput)

    def stopwatch(self):
        self.root = tk.Tk()
        self.root.geometry('500x500')
        self.root.resizable(False, False)
        self.root.iconbitmap('stopwatch.ico')
        style = ttk.Style(self.root)
        style.configure('root.TButton', font = ('calibri', 20, 'bold'))
        self.root.title('Stopwatch')

        name = ttk.Label(self.root, text="Stopwatch", font = ('calibri', 40, 'bold', 'underline'))
        name.pack()

        self.pretty_laps = "Lap(s): "
        self.stopwatch_ = ttk.Label(self.root, text=self.currentOutput, font = ('calibri', 40, 'bold'))
        self.stopwatch_.pack()

        addlap_ = ttk.Button(self.root, text="Add Lap", width=100, style = 'root.TButton', command=self.addLap)
        addlap_.pack()

        self.laps_ = ttk.Label(self.root, text=self.pretty_laps, font = ('calibri', 30, 'bold'), wraplength=500, justify="center")
        self.laps_.pack()

        self.count()
        self.root.mainloop()


    def count(self):
        if self.currentSeconds >= 59:
            self.currentMinutes = self.currentMinutes + 1
            self.currentSeconds = 0
        else:
            self.currentSeconds += 1

        if self.currentMinutes >= 59:
            self.currentHours = self.currentHours + 1
            self.currentMinutes = 0

        if self.currentHours < 10:
            self.newOutput += ("0" + str(self.currentHours) + self.separator)
        else:
            self.newOutput += (str(self.currentHours) + self.separator)

        if self.currentMinutes < 10:
                self.newOutput += ("0" + str(self.currentMinutes) + self.separator)
        else:
            self.newOutput += (str(currentMinutes) + self.separator)

        if self.currentSeconds < 10:
            self.newOutput += ("0" + str(self.currentSeconds))
        else:
            self.newOutput += (str(self.currentSeconds))

        self.currentOutput = self.newOutput
        self.stopwatch_['text'] = self.currentOutput
        self.newOutput = ""

        self.pretty_laps = "Lap(s): "
        for i in self.laps:
            if i != self.laps[0]:
                self.pretty_laps += ", " + i
            else: self.pretty_laps += i
        self.laps_['text'] = self.pretty_laps

        self.stopwatch_.after(1000, self.count)

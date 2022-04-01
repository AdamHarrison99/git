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
		self.currentMilliSeconds = 0
		self.currentSeconds = 0
		self.currentMinutes = 0
		self.currentHours = 0
		self.separator = ":"
		self.newOutput = ""
		self.currentOutput = ""
		self.miliOutput = ""
		self.pretty_laps = "Lap(s): "

	def addLap(self):
		self.laps.append(self.currentOutput)

	def stopwatch(self):
		#init tk
		self.root = tk.Tk()
		x = 500
		y = 500
		self.root.geometry(str(x) + "x" + str(y))
		self.root.resizable(False, True)
		self.root.iconbitmap('icons/stopwatch.ico')
		style = ttk.Style(self.root)
		style.configure('root.TButton', font = ('calibri', 20, 'bold'))
		self.root.title('Stopwatch')

		name = ttk.Label(self.root, text="Stopwatch", font = ('calibri', 30, 'bold', 'underline'))
		name.pack()

		#Create stopwatch and MilliSeconds lables. pack them into a frame so they center properly
		self.stopwatch_containter = ttk.Frame(self.root)
		self.stopwatch_ = ttk.Label(self.stopwatch_containter, text=self.newOutput, font = ('calibri', 40, 'bold'), padding=0)
		self.stopwatch_.pack(side='left', anchor='n')
		self.stopwatch_mili = ttk.Label(self.stopwatch_containter, text=self.miliOutput, font = ('calibri', 20, 'bold'), padding=0)
		self.stopwatch_mili.pack(side='left', anchor='n', pady='23')
		self.stopwatch_containter.pack()

		#lap Button
		addlap_ = ttk.Button(self.root, text="Add Lap", width=100, style = 'root.TButton', command=self.addLap)
		addlap_.pack()

		self.laps_ = ttk.Label(self.root, text=self.pretty_laps, font = ('calibri', 30, 'bold'), wraplength=500, justify="center")
		self.laps_.pack()

		#start count and mainloop
		self.count()
		self.root.mainloop()


	def count(self):
		#all the math for the stopwatch
		self.currentMilliSeconds += 1
		if self.currentMilliSeconds >= 99:
			self.currentSeconds += 1
			self.currentMilliSeconds = 0

		if self.currentSeconds >= 59:
			self.currentMinutes += 1
			self.currentSeconds = 0

		if self.currentMinutes >= 59:
			self.currentHours += 1
			self.currentMinutes = 0

		#output formating
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

		if self.currentMilliSeconds < 10:
			self.miliOutput += ("0" + str(self.currentMilliSeconds))
		else:
			self.miliOutput += (str(self.currentMilliSeconds))

		self.currentOutput = self.newOutput + "." + self.miliOutput

		#change the lables to reflect new time and clear buffer time variables
		self.stopwatch_['text'] = self.newOutput
		self.stopwatch_mili['text'] = self.miliOutput
		self.newOutput = ""
		self.miliOutput = ""

		#"pretty" lap formating
		self.pretty_laps = "Lap(s): "
		for i in self.laps:
			if i != self.laps[0]:
				self.pretty_laps += ", " + i
			else: self.pretty_laps += i
		self.laps_['text'] = self.pretty_laps

		#do it again
		self.stopwatch_.after(10, self.count)

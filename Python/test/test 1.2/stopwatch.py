# --- stopwatch.py ---
#!/usr/bin/python3
#A simple stopwatch implementation

import sys, os, select, time, threading
from pynput import keyboard

def clearTerm():
    os.system('cls' if os.name == 'nt' else 'clear')
    print()

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
        self.laps.append(self.newOutput)

    def on_press(self, key):
        if key == keyboard.Key.enter:
            self.addLap()

        elif key == keyboard.Key.esc:
            print("\nDone")
            os._exit(0) 

    def stopwatch(self):
    	listener = keyboard.Listener(on_press=self.on_press)
    	listener.start()  # start to listen on a separate thread
    	clearTerm()

    	while True:
            if self.currentSeconds >= 59:
                self.currentMinutes = self.currentMinutes + 1
                self.currentSeconds = 0
            else:
                self.currentSeconds += 1

            if self.currentMinutes >= 59:
                self.currentHours = self.currentHours + 1
                self.currentMinutes = 0

            clearTerm()

            if self.currentSeconds % 2 == 0:
                self.separator = ":"
            else:
                self.separator = " "

            print("Hr:Min:Sec")

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
            print(self.currentOutput)
            if len(self.laps) != 0:
                print("Lap(s):", end="")
                for i in self.laps:
                    print(i + ", ", end="")
            sleep(self.timerIncrement)
            self.newOutput = ""

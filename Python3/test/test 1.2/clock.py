# --- clock.py ---
#!/usr/bin/python3
#A simple clock implementation

import sys, os, select, time, threading, datetime
from pynput import keyboard
from colorama import Fore, Style

def clearTerm():
    os.system('cls' if os.name == 'nt' else 'clear')
    print()

def sleep(sleep_time):
	time.sleep(sleep_time)

class Clock:
    def __init__(self):
        self.colors = (Fore.CYAN, Fore.WHITE, Fore.RED, Fore.BLUE, Fore.GREEN, Fore.YELLOW, Fore.MAGENTA)
        self.curColor = 0
        self.globalTime = False
        self.clockSleepTime = 1
        self.separator = ":"

    def on_press(self, key):
        if key == keyboard.Key.enter:
            self.colorChange()

        elif key == keyboard.Key.esc:
            print("\nDone")
            os._exit(0) 

    def colorChange(self):
        if self.curColor+1 >= len(self.colors):
            self.curColor = 0

        else:
            self.curColor += 1

    def clock(self):
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()  # start to listen on a separate thread

        hour_setting = input("Type '12' for 12HR time, or '24' for 24HR time ")
        if hour_setting == "12": globalTime = False
        else: globalTime = True

        while(True):
            clearTerm()
            system_time = datetime.datetime.now()

            if int(system_time.strftime("%S")) % 2 == 0:
                self.separator = ":"
            else:
                self.separator = " "

            if globalTime == True:
                print(self.colors[self.curColor], system_time.strftime("%H" + self.separator + "%M" + self.separator + "%S"))
            else:
                print(self.colors[self.curColor], system_time.strftime("%I" + self.separator + "%M" + self.separator + "%S %p"))
            sleep(self.clockSleepTime)

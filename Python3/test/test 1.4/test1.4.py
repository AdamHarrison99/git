# --- main.py ---
#!/usr/bin/python3
#A simple python demo

__author__="Adam Harrison"
__copyright__="None"
__license__="Public Domain"
__version__="1.3"
__date__="2-18-22"
__OS__="GNU/Linux & Windows"
__requirements__ ="requirements.txt"

"""
v1.4 Planned updates: TODO
Clock
	Analoge clock option
	Add 'File' and 'Options' dropdown menus
		Options-AM/PM or Global: Able to set AM/PM or Global time (no more using big buttons)
		File-Save: Save Config options (color, size, AM/PM or Global)
Stopwatch
	Pause, reset buttons for Stopwatch
	Make stopwatch resizeable
	Use dropdown menus
Maybe?
	Put clearTerm, sleep, on_press functions into helper file so each separate class doesn't need a new one

v1.4 Updates:
Stopwatch
	Added miliseconds (again)
"""

import sys, os, select, time, random, threading
from colorama import Back, Style
from pynput import keyboard
from stopwatch import *
from clock import *

def on_press(key):
	if key == keyboard.Key.esc:
		print("\nDone")
		os._exit(0)

def clearTerm():
	os.system('cls' if os.name == 'nt' else 'clear')

def sleep(sleep_time):
	time.sleep(sleep_time)

def count(sleepDir):
	print("Give me something to count ")
	word = input("Type Here: ")
	print("How many", word + "(s) are there? ")
	number = input("Type Here: ")
	print()

	for i in range(1, int(number) + 1):
		sleep(sleepDir)
		if i != 1:
			print(i, word + "s")
		else:
			print(i, word)

	sleep(sleepDir)

def dance(sleepDir):
	listener = keyboard.Listener(on_press=on_press)
	listener.start()  # start to listen on a separate thread
	while True:
		clearTerm()
		print(" \(* *)/")
		sleep(sleepDir)

		clearTerm()
		print(" /(* * )/")
		sleep(sleepDir)

		clearTerm()
		print(" \(* *)/")
		sleep(sleepDir)

		clearTerm()
		print("\( * *)\\")
		sleep(sleepDir)

def partymode(sleepDir):
	listener = keyboard.Listener(on_press=on_press)
	listener.start()  # start to listen on a separate thread
	outputs = (Back.RED, Back.GREEN, Back.BLUE, Back.YELLOW, Back.BLACK, Back.WHITE, Back.MAGENTA, Back.CYAN)
	while(True):
		selection = random.randrange(len(outputs))
		clearTerm()
		print(outputs[selection], "PARTYYYYYYYY!!!")
		sleep(sleepDir)

def danceparty(sleepDir):
	listener = keyboard.Listener(on_press=on_press)
	listener.start()  # start to listen on a separate thread

	#creating threads
	t1 = threading.Thread(target=partymode, args=(sleepDir,))
	t2 = threading.Thread(target=dance, args=(sleepDir,))

	#starting thread 1
	t1.start()
    #starting thread 2
	t2.start()

def math(sleepDir):
	listener = keyboard.Listener(on_press=on_press)
	listener.start()  # start to listen on a separate thread
	clearTerm()
	outputs = "1234567890+=-/*%^.()xyz\n "
	print("Time to do some math!\n")
	sleep(sleepDir)

	while True:
		selection = random.randrange(len(outputs))
		print (outputs[selection], end="")
		sleep(sleepDir)

if __name__ == "__main__":
	#basic info
	if len(sys.argv) == 1:
		print("A simple python demo\n")
		if os.name == 'nt': print("Usage: python3.exe " + sys.argv[0] + " -[args]")
		else: print("Usage: python3 " + sys.argv[0] + " -[args]")
		print("-h for Help\n")

		f = open("requirements.txt", "r")
		print("Dependencies:\n" + f.read() ,"\nrun 'pip install -r requirements.txt'\n")

	#arguments
	elif str(sys.argv[1]) == "-h":
		print("--info : Display program information\n")
		print("--count : Count a given word a specified number of times\n")
		print("--math : A VERY VERY intelligent algorithm that creates math equations: \n\tpress 'Esc' to exit\n")
		print("--stopwatch : Start a stopwatch: \n")
		print("--clock : Start a clock: \n")
		print("--dance : Pretty self explanatory: \n\tpress 'Esc' to exit\n")
		print("--partymode : Hours of fun (SEIZURE WARNING): \n\tpress 'Esc' to exit\n")
		print("--danceparty : Hours of fun + dancing (SEIZURE WARNING): \n\tpress 'Esc' to exit\n")

	elif str(sys.argv[1]) == "--info":
		print("Tested on", __OS__, "\n")
		print("Author:", __author__, "\nCopyright:", __copyright__, "\nLicense:", __license__, "\nVersion:", __version__, "\nModified date:", __date__)

	#Broken due to Enter key listener
	elif str(sys.argv[1]) == "--count":
		count(1)

	#prints 1 of 3 "frames" of the dancing man each 0.3 seconds
	elif str(sys.argv[1]) == "--dance":
		dance(0.3)

	#selects a random character from given string outputs and prints it to the terminal
	elif str(sys.argv[1]) == "--math":
		math(0.1)

	#A basic stopwatch implementation
	#Added Laps as of v1.2
	elif str(sys.argv[1]) == "--stopwatch":
		watch = Stopwatch()
		watch.stopwatch()

	#A basic clock implementation
	elif str(sys.argv[1]) == "--clock":
		time = Clock()
		time.clock()

	#dance and partymode together
	elif str(sys.argv[1]) == "--danceparty":
		danceparty(0.35)

	#picks a random color and sets the character backgroud to the selected color
	elif str(sys.argv[1]) == "--partymode":
		partymode(0.35)

	else:
		print("Error, Argument(s) invalid:")
		for i, j in enumerate(sys.argv):
			if i == 0: continue
			else: print("\t" + str(i) + ":", j)

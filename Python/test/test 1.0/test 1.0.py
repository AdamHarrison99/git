#!/usr/bin/python3

__author__="Adam Harrison"
__copyright__="None"
__license__="Public Domain"
__version__="1.0"
__date__="2-2-22"

import sys, os, select, time, random
from colorama import Back, Style

#basic info
if len(sys.argv) == 1:
	print("Made for GNU/Linux systems\n\nUsage: ./test.py -args\n-h for Help\n")
	print("Author:", __author__, "\nCopyright:", __copyright__, "\nLicense:", __license__, "\nVersion:", __version__, "\nModified date:", __date__)

#arguments
elif str(sys.argv[1]) == "-h":
	print("--count : Count a given word a specified number of times")
	print("--math : A VERY VERY intelligent algorithm that creates math equations; press 'ENTER' to exit")
	print("--stopwatch : Start a stopwatch; press 'ENTER' to exit")
	print("--dance : Pretty self explanatory; press 'ENTER' to exit")
	print("--partymode : Hours of fun (SEIZURE WARNING); press 'ENTER' to exit")
	print("--danceparty : Hours of fun + dancing (SEIZURE WARNING); press 'ENTER' to exit")

elif str(sys.argv[1]) == "--count":
	sleepDir = 1
	print("Give me something to count ")
	word = input("Type Here: ")
	print("How many", word + "(s) are there? ")
	number = input("Type Here: ")
	print()

	for i in range(1, int(number) + 1):
		time.sleep(sleepDir)
		if i != 1:
			print(i, word + "s")
		else:
			print(i, word)

	time.sleep(sleepDir)

#prints 1 of 3 "frames" of the dancing man each 0.3 seconds
elif str(sys.argv[1]) == "--dance":
	sleepDir = 0.3

	while True:
		os.system('clear')
		print(" \(* *)/")
		time.sleep(sleepDir)

		os.system('clear')
		print(" /(* * )/")
		time.sleep(sleepDir)

		os.system('clear')
		print(" \(* *)/")
		time.sleep(sleepDir)

		os.system('clear')
		print("\( * *)\\")
		time.sleep(sleepDir)

		if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
			os.system('clear')
			break

#selects a random character from given string outputs and prints it to the terminal
elif str(sys.argv[1]) == "--math":
	os.system('clear')
	sleepDir = 0.1
	outputs = "1234567890+=-/*%^.()xyz\n "
	print("Time to do some math!\n")
	time.sleep(1)

	while True:
		selection = random.randrange(len(outputs))
		print (outputs[selection], end="")
		time.sleep(sleepDir)
		if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
			print("\n\nTotally just solved the Reimann hypothesis")
			break

#A basic stopwatch implementation
elif str(sys.argv[1]) == "--stopwatch":
	os.system('clear')
	timerIncrement = 1
	currentSeconds = 0
	currentMinutes = 0
	currentHours = 0

	while True:
		time.sleep(timerIncrement)
		if currentSeconds >= 59:
			currentMinutes = currentMinutes + 1
			currentSeconds = 0
		else:
			currentSeconds = currentSeconds + 1
		if currentMinutes >= 59:
			currentHours = currentHours + 1
			currentMinutes = 0

		os.system('clear')

		if currentHours < 10:
			print("0" + str(currentHours) + ":", end="")
		else:
			print(str(currentHours) + ":", end="")

		if currentMinutes < 10:
			print("0" + str(currentMinutes) + ":", end="")
		else:
			print(str(currentMinutes) + ":", end="")

		if currentSeconds < 10:
			print("0" + str(currentSeconds))
		else:
			print(str(currentSeconds))

		if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
			break

#dance and partymode together
elif str(sys.argv[1]) == "--danceparty":
	sleepDir = 0.35
	outputs = (Back.RED, Back.GREEN, Back.BLUE, Back.YELLOW, Back.BLACK, Back.WHITE, Back.MAGENTA, Back.CYAN)
	while(True):

		selection = random.randrange(len(outputs))
		os.system('clear')
		print(outputs[selection], " \(* *)/")
		time.sleep(sleepDir)

		selection = random.randrange(len(outputs))
		os.system('clear')
		print(outputs[selection], " /(* * )/")
		time.sleep(sleepDir)

		selection = random.randrange(len(outputs))
		os.system('clear')
		print(outputs[selection], " \(* *)/")
		time.sleep(sleepDir)

		selection = random.randrange(len(outputs))
		os.system('clear')
		print(outputs[selection], "\( * *)\\")
		time.sleep(sleepDir)

		if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
			break

#picks a random color and sets the character backgroud to the selected color
elif str(sys.argv[1]) == "--partymode":
	sleepDir = 0.35
	outputs = (Back.RED, Back.GREEN, Back.BLUE, Back.YELLOW, Back.BLACK, Back.WHITE, Back.MAGENTA, Back.CYAN)
	while(True):
		selection = random.randrange(len(outputs))
		os.system('clear')
		print(outputs[selection], "PARTYYYYYYYY!!!")
		time.sleep(sleepDir)

		if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
			break

else:
	print("Bro, I have no idea what to do with this")
	for i, j in enumerate(sys.argv):
		if i == 0: continue
		else: print("\t" + str(i) + ":", j)

print("\nDone")

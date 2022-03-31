# --- main.py ---
#!/usr/bin/python3
#A simple python demo

__author__="Adam Harrison"
__copyright__="None"
__license__="Public Domain"
__version__="1.0"
__date__="3-31-22"
__OS__="GNU/Linux & Windows"
#__requirements__ =""

"""
UNFINISHED
TODO: Fix non square grid in window_dressing
    Fix body tracking and tail removal in move func
        -not sure of issue atm
    Tweak boarder detection
    Fix some unknown issue with fruit handler

Add: Game over when head colides with body
"""

import sys, os, time, random
from pynput import keyboard


def main():
    game = Game()
    game.init_board()

class Game:
    def __init__(self):
        self.board = []
        self.xSize = 0
        self.ySize = 0
        self.fruitX = 0
        self.fruitY = 0
        self.headX = 0
        self.headY = 0
        self.body = []
        self.points = 0
        self.curDir = "up"
        self.dead = False

    def init_board(self):
        if len(sys.argv) >= 2:
            self.xSize = int(sys.argv[1])
            self.ySize = int(sys.argv[2])
        else:
            self.xSize = int(input("Define size x "))
            self.ySize = int(input("Define size y "))

        for i in range(0,self.xSize):
            self.board.append([])
            self.board[i].append("\n")

            for j in range(0,self.ySize):
                self.board[i].append(" . ")

        self.headX = int(self.xSize/2)+1
        self.headY = int(self.ySize/2)+1

        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()  # start to listen on a separate thread

        self.window_dressing()
        self.fruit_handler_init()

        while(True):
            if self.dead == True:
                break
            #self.clearTerm()
            self.fruit_handler()
            self.print_board()
            self.print_points()
            self.move()
            print(self.curDir)
            self.sleep(1)

        print("Game Over")
    def window_dressing(self):
        horDressing = ["\n "]
        for i in range(0, self.xSize*3):
            horDressing.append("_")

        self.board.insert(0,horDressing)
        self.board.append(horDressing)

        vertDressing = "|"
        for j in range(1,len(self.board)-1):
            self.board[j].insert(1,vertDressing)
            self.board[j].append(vertDressing)

    def print_board(self):
        for i in self.board:
            for j in i:
                print(j, end="")

    def print_points(self):
        print("\nPoints:" + str(self.points))

    def fruit_handler_init(self):
        self.fruitX = random.randrange(2, self.xSize-1)
        self.fruitY = random.randrange(2, self.ySize-1)
        self.board[self.fruitX][self.fruitY] = " o "
        self.fruit_handler()

    def fruit_handler(self):
        if self.fruitX == self.headX:
            if self.fruitY == self.headY:
                self.add_point()
                self.fruit_handler_init()

    #Weird issue with tracking body and removing old parts
    def move(self):
        print(self.headX, self.headY)
        print(self.body)

        if self.curDir == "up":
            self.body.append((self.headX + self.points, self.headY))
            self.headX -= 1

        elif self.curDir == "down":
            self.body.append((self.headX - self.points, self.headY))
            self.headX += 1

        elif self.curDir == "left":
            self.body.append((self.headX, self.headY + self.points))
            self.headY -= 1

        elif self.curDir == "right":
            self.body.append((self.headX, self.headY - self.points))
            self.headY += 1

        if self.headX == 0 or self.headX == self.xSize or self.headY == 0 or self.headY == self.ySize:
            self.game_over()

        if len(self.body) > self.points + 1:
            self.board[self.body[0][0]][self.body[0][1]] = " . "
            self.body.pop(0)
        else:
            self.board[self.body[0][0]][self.body[0][1]] = " . "

        self.board[self.headX][self.headY] = " \u25A1 "

    def add_point(self):
        self.points += 1

    def game_over(self):
        self.dead = True

    def on_press(self, key):
        if key == keyboard.Key.esc:
            print("\nExiting")
            os._exit(0)
        elif key == keyboard.Key.up:
            self.curDir = "up"
        elif key == keyboard.Key.down:
            self.curDir = "down"
        elif key == keyboard.Key.left:
            self.curDir = "left"
        elif key == keyboard.Key.right:
            self.curDir = "right"

    def clearTerm(self):
    	os.system('cls' if os.name == 'nt' else 'clear')

    def sleep(self, sleep_time):
    	time.sleep(sleep_time)

if __name__ =="__main__":
    main()

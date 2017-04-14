from Tkinter import *
import sys, argparse
from math import *
from time import *
from random import *
from copy import deepcopy


class Board(object):
    def __init__(self, in_screen):
        # White goes first (0 is white and player,1 is black and computer)
        self.screen = in_screen
        self.player = 0

        self.ttl_score=0
        self.computer_score=0
        self.player_score=0

        # Initializing an empty board
        self.array = []
        for x in range(8):
            self.array.append([])
            for y in range(8):
                self.array[x].append(None)

        # Initializing center values
        self.array[3][3] = "w"
        self.array[3][4] = "b"
        self.array[4][3] = "b"
        self.array[4][4] = "w"

        # Initializing old values
        self.oldarray = self.array

        # Drawing the intermediate lines
        for i in range(7):
            lineShift = 50 + 50 * (i + 1)

            # Horizontal line
            self.screen.create_line(50, lineShift, 450, lineShift, fill="#111")

            # Vertical line
            self.screen.create_line(lineShift, 50, lineShift, 450, fill="#111")

        self.update()

        # Checks if a move is valid for a given array.

    def valid(self, array, player, x, y):
        # Sets player colour
        if player == 0:
            colour = "w"
        else:
            colour = "b"

        # If there's already a piece there, it's an invalid move
        if array[x][y] != None:
            return False

        else:
            # Generating the list of neighbours
            neighbour = False
            neighbours = []
            for i in range(max(0, x - 1), min(x + 2, 8)):
                for j in range(max(0, y - 1), min(y + 2, 8)):
                    if array[i][j] != None:
                        neighbour = True
                        neighbours.append([i, j])
            # If there's no neighbours, it's an invalid move
            if not neighbour:
                return False
            else:
                # Iterating through neighbours to determine if at least one line is formed
                valid = False
                for neighbour in neighbours:

                    neighX = neighbour[0]
                    neighY = neighbour[1]

                    # If the neighbour colour is equal to your colour, it doesn't form a line
                    # Go onto the next neighbour
                    if array[neighX][neighY] == colour:
                        continue
                    else:
                        # Determine the direction of the line
                        deltaX = neighX - x
                        deltaY = neighY - y
                        tempX = neighX
                        tempY = neighY

                        while 0 <= tempX <= 7 and 0 <= tempY <= 7:
                            # If an empty space, no line is formed
                            if array[tempX][tempY] == None:
                                break
                            # If it reaches a piece of the player's colour, it forms a line
                            if array[tempX][tempY] == colour:
                                valid = True
                                break
                            # Move the index according to the direction of the line
                            tempX += deltaX
                            tempY += deltaY
                return valid

    def get_action(self, player):
        action = []
        for x in range(8):
            for y in range(8):

                if self.valid(self.array, player, x, y):
                    action.append([x, y])
        return action

        # Updating the board to the screen

    def update(self):
        self.screen.delete("highlight")
        self.screen.delete("tile")
        for x in range(8):
            for y in range(8):
                # Could replace the circles with images later, if I want
                if self.oldarray[x][y] == "w":
                    self.screen.create_oval(54 + 50 * x, 54 + 50 * y, 96 + 50 * x, 96 + 50 * y,
                                            tags="tile {0}-{1}".format(x, y), fill="#aaa", outline="#aaa")
                    self.screen.create_oval(54 + 50 * x, 52 + 50 * y, 96 + 50 * x, 94 + 50 * y,
                                            tags="tile {0}-{1}".format(x, y), fill="#fff", outline="#fff")

                elif self.oldarray[x][y] == "b":
                    self.screen.create_oval(54 + 50 * x, 54 + 50 * y, 96 + 50 * x, 96 + 50 * y,
                                            tags="tile {0}-{1}".format(x, y), fill="#000", outline="#000")
                    self.screen.create_oval(54 + 50 * x, 52 + 50 * y, 96 + 50 * x, 94 + 50 * y,
                                            tags="tile {0}-{1}".format(x, y), fill="#111", outline="#111")
        # Animation of new tiles
        self.screen.update()
        for x in range(8):
            for y in range(8):
                # Could replace the circles with images later, if I want
                if self.array[x][y] != self.oldarray[x][y] and self.array[x][y] == "w":
                    self.screen.delete("{0}-{1}".format(x, y))
                    # 42 is width of tile so 21 is half of that
                    # Shrinking
                    for i in range(21):
                        self.screen.create_oval(54 + i + 50 * x, 54 + i + 50 * y, 96 - i + 50 * x, 96 - i + 50 * y,
                                                tags="tile animated", fill="#000", outline="#000")
                        self.screen.create_oval(54 + i + 50 * x, 52 + i + 50 * y, 96 - i + 50 * x, 94 - i + 50 * y,
                                                tags="tile animated", fill="#111", outline="#111")
                        if i % 3 == 0:
                            sleep(0.01)
                        self.screen.update()
                        self.screen.delete("animated")
                    # Growing
                    for i in reversed(range(21)):
                        self.screen.create_oval(54 + i + 50 * x, 54 + i + 50 * y, 96 - i + 50 * x, 96 - i + 50 * y,
                                                tags="tile animated", fill="#aaa", outline="#aaa")
                        self.screen.create_oval(54 + i + 50 * x, 52 + i + 50 * y, 96 - i + 50 * x, 94 - i + 50 * y,
                                                tags="tile animated", fill="#fff", outline="#fff")
                        if i % 3 == 0:
                            sleep(0.01)
                        self.screen.update()
                        self.screen.delete("animated")
                    self.screen.create_oval(54 + 50 * x, 54 + 50 * y, 96 + 50 * x, 96 + 50 * y, tags="tile",
                                            fill="#aaa",
                                            outline="#aaa")
                    self.screen.create_oval(54 + 50 * x, 52 + 50 * y, 96 + 50 * x, 94 + 50 * y, tags="tile",
                                            fill="#fff",
                                            outline="#fff")
                    self.screen.update()

                elif self.array[x][y] != self.oldarray[x][y] and self.array[x][y] == "b":
                    self.screen.delete("{0}-{1}".format(x, y))
                    # 42 is width of tile so 21 is half of that
                    # Shrinking
                    for i in range(21):
                        self.screen.create_oval(54 + i + 50 * x, 54 + i + 50 * y, 96 - i + 50 * x, 96 - i + 50 * y,
                                                tags="tile animated", fill="#aaa", outline="#aaa")
                        self.screen.create_oval(54 + i + 50 * x, 52 + i + 50 * y, 96 - i + 50 * x, 94 - i + 50 * y,
                                                tags="tile animated", fill="#fff", outline="#fff")
                        if i % 3 == 0:
                            sleep(0.01)
                        self.screen.update()
                        self.screen.delete("animated")
                    # Growing
                    for i in reversed(range(21)):
                        self.screen.create_oval(54 + i + 50 * x, 54 + i + 50 * y, 96 - i + 50 * x, 96 - i + 50 * y,
                                                tags="tile animated", fill="#000", outline="#000")
                        self.screen.create_oval(54 + i + 50 * x, 52 + i + 50 * y, 96 - i + 50 * x, 94 - i + 50 * y,
                                                tags="tile animated", fill="#111", outline="#111")
                        if i % 3 == 0:
                            sleep(0.01)
                        self.screen.update()
                        self.screen.delete("animated")

                    self.screen.create_oval(54 + 50 * x, 54 + 50 * y, 96 + 50 * x, 96 + 50 * y, tags="tile",
                                            fill="#000",
                                            outline="#000")
                    self.screen.create_oval(54 + 50 * x, 52 + 50 * y, 96 + 50 * x, 94 + 50 * y, tags="tile",
                                            fill="#111",
                                            outline="#111")
                    self.screen.update()

        # Drawing of highlight circles
        for x in range(8):
            for y in range(8):
                if self.player == 0:
                    if self.valid(self.array, self.player, x, y):
                        self.screen.create_oval(68 + 50 * x, 68 + 50 * y, 32 + 50 * (x + 1), 32 + 50 * (y + 1),
                                                tags="highlight", fill="#008000", outline="#008000")


        # Draw the scoreboard and update the screen
        self.drawScoreBoard()
        self.screen.update()


    def mustPass(self, player):
        must_pass = True
        for x in range(8):
            for y in range(8):
                if self.valid(self.array, player, x, y  ):
                    must_pass = False
        return must_pass

    def drawScoreBoard(self):

        # Deleting prior score elements
        self.screen.delete("score")

        # Scoring based on number of tiles
        player_score = 0
        computer_score = 0
        for x in range(8):
            for y in range(8):
                if self.array[x][y] == "w":
                    player_score += 1
                elif self.array[x][y] == "b":
                    computer_score += 1

        if self.player == 0:
            player_colour = "green"
            computer_colour = "gray"
        else:
            player_colour = "gray"
            computer_colour = "green"

        self.screen.create_oval(5, 540, 25, 560, fill=player_colour, outline=player_colour)
        self.screen.create_oval(380, 540, 400, 560, fill=computer_colour, outline=computer_colour)

        # Pushing text to screen
        self.screen.create_text(30, 550, anchor="w", tags="score", font=("Consolas", 50), fill="white",
                                text=player_score)
        self.screen.create_text(400, 550, anchor="w", tags="score", font=("Consolas", 50), fill="black",
                                text=computer_score)
        self.computer_score=computer_score
        self.player_score=player_score
        self.ttl_score= computer_score + player_score

    def move(self, passedArray, x, y):
        # Must copy the passedArray so we don't alter the original
        array = deepcopy(passedArray)
        # Set colour and set the moved location to be that colour
        if self.player == 0:
            colour = "w"

        else:
            colour = "b"
        array[x][y] = colour

        # Determining the neighbours to the square
        neighbours = []
        for i in range(max(0, x - 1), min(x + 2, 8)):
            for j in range(max(0, y - 1), min(y + 2, 8)):
                if array[i][j] != None:
                    neighbours.append([i, j])

        # Which tiles to convert
        convert = []

        # For all the generated neighbours, determine if they form a line
        # If a line is formed, we will add it to the convert array
        for neighbour in neighbours:
            neighX = neighbour[0]
            neighY = neighbour[1]
            # Check if the neighbour is of a different colour - it must be to form a line
            if array[neighX][neighY] != colour:
                # The path of each individual line
                path = []

                # Determining direction to move
                deltaX = neighX - x
                deltaY = neighY - y

                tempX = neighX
                tempY = neighY

                # While we are in the bounds of the board
                while 0 <= tempX <= 7 and 0 <= tempY <= 7:
                    path.append([tempX, tempY])
                    value = array[tempX][tempY]
                    # If we reach a blank tile, we're done and there's no line
                    if value == None:
                        break
                    # If we reach a tile of the player's colour, a line is formed
                    if value == colour:
                        # Append all of our path nodes to the convert array
                        for node in path:
                            convert.append(node)
                        break
                    # Move the tile
                    tempX += deltaX
                    tempY += deltaY

        # Convert all the appropriate tiles
        for node in convert:
            array[node[0]][node[1]] = colour

        return array

    def boardMove(self, x, y):

        # Move and update screen
        self.oldarray = self.array
        self.oldarray[x][y] = "w"
        self.array = self.move(self.array, x, y)

        # Switch Player
        self.player = 1 - self.player
        self.update()


class DumbAgent(object):
    def get_action(self,board):
        actions=board.get_action(1)
        return actions[0] if len(actions)!=0 else None

def clickHandle(event):
    global agent,board
    if board.mustPass(0)==True and board.mustPass(1)==True:
        if board.player_score>board.computer_score:
            over_text="You Win"
        elif board.player_score<board.computer_score:
            over_text="Computer Win"
        else:
            over_text="Balance"

        board.screen.create_text(250, 550, anchor="c", font=("Consolas", 15), text=over_text)

    # print board.player
    assert board.player == 0, "not your move?"
    print board.get_action(0)
    if board.mustPass(0)==True:
        print "You Have No Choose"
        board.player=1-board.player
    else:
        # Delete the highlights
        x = int((event.x - 50) / 50)
        y = int((event.y - 50) / 50)
        # Determine the grid index for where the mouse was clicked

        # If the click is inside the bounds and the move is valid, move to that location
        if 0 <= x <= 7 and 0 <= y <= 7:
            if board.valid(board.array, board.player, x, y):
                board.boardMove(x, y)

    assert  board.player==1,"not computer move?"
    if board.mustPass(1)==True:
        board.player = 1 - board.player
        print "Computer No Choose"
    else:
        action=agent.get_action(board)
        board.boardMove(*action)



if __name__ == "__main__":
    root = Tk()
    main_screen = Canvas(root, width=500, height=600, background="#555")
    main_screen.pack()

    agent = DumbAgent()

    # Binding, setting
    main_screen.bind("<Button-1>", clickHandle)
    # main_screen.bind("<Key>", keyHandle)
    main_screen.focus_set()

    board = Board(main_screen)
    root.wm_title("Reversi")
    root.mainloop()

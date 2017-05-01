# from __future__ import division
from Tkinter import *
import  argparse,math,cPickle
import os,sys
import glob
from math import *
from time import *
from random import *
from copy import deepcopy
import numpy as np
import pprint
from main import Config

class DumbAgent(object):
    def agent_get_action(self, board, player=None):
        actions = board.get_action(board.player)
        return actions[0] if len(actions) != 0 else None


class GUI(object):
    def __init__(self, screen, board):
        self.screen = screen
        self.init(board)

    def handle_finish(self, board):
        if board.must_pass(0) == True and board.must_pass(1) == True:
            print "Game Finish"
            if board.white_score > board.black_score:
                over_text = "You Win"
            elif board.white_score < board.black_score:
                over_text = "Computer Win"
            else:
                over_text = "Balance"
            self.screen.create_text(250, 550, anchor="c", font=("Consolas", 15), text=over_text)

    def init(self, board):
        # Drawing the intermediate lines
        for i in range(7):
            lineShift = 50 + 50 * (i + 1)

            # Horizontal line
            self.screen.create_line(50, lineShift, 450, lineShift, fill="#111")

            # Vertical line
            self.screen.create_line(lineShift, 50, lineShift, 450, fill="#111")

        self.update(board)

        # Checks if a move is valid for a given array.

    def update(self, board):
        self.screen.delete("highlight")
        self.screen.delete("tile")
        for x in range(8):
            for y in range(8):
                # Could replace the circles with images later, if I want
                if board.oldarray[x][y] == "w":
                    self.screen.create_oval(54 + 50 * x, 54 + 50 * y, 96 + 50 * x, 96 + 50 * y,
                                            tags="tile {0}-{1}".format(x, y), fill="#aaa", outline="#aaa")
                    self.screen.create_oval(54 + 50 * x, 52 + 50 * y, 96 + 50 * x, 94 + 50 * y,
                                            tags="tile {0}-{1}".format(x, y), fill="#fff", outline="#fff")

                elif board.oldarray[x][y] == "b":
                    self.screen.create_oval(54 + 50 * x, 54 + 50 * y, 96 + 50 * x, 96 + 50 * y,
                                            tags="tile {0}-{1}".format(x, y), fill="#000", outline="#000")
                    self.screen.create_oval(54 + 50 * x, 52 + 50 * y, 96 + 50 * x, 94 + 50 * y,
                                            tags="tile {0}-{1}".format(x, y), fill="#111", outline="#111")
        # Animation of new tiles
        self.screen.update()
        for x in range(8):
            for y in range(8):
                # Could replace the circles with images later, if I want
                if board.array[x][y] != board.oldarray[x][y] and board.array[x][y] == "w":
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

                elif board.array[x][y] != board.oldarray[x][y] and board.array[x][y] == "b":
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
                if board.player == Config.player_color:
                    if board.valid(board.array, board.player, x, y):
                        self.screen.create_oval(68 + 50 * x, 68 + 50 * y, 32 + 50 * (x + 1), 32 + 50 * (y + 1),
                                                tags="highlight", fill="#008000", outline="#008000")

        # Draw the scoreboard and update the screen
        self.draw_score_board(board)
        self.screen.update()

    def draw_score_board(self, board):
        board.update_score()
        # Deleting prior score elements
        self.screen.delete("score")

        # Scoring based on number of tiles

        # if board.player == 0:
        player_colour = "black"
        computer_colour = "white"
        # else:
        #     player_colour = "gray"
        #     computer_colour = "green"

        self.screen.create_oval(5, 540, 25, 560, fill=player_colour, outline=player_colour)
        self.screen.create_oval(380, 540, 400, 560, fill=computer_colour, outline=computer_colour)

        # Pushing text to screen
        self.screen.create_text(30, 550, anchor="w", tags="score", font=("Consolas", 50), fill="black",
                                text=board.black_score)
        self.screen.create_text(400, 550, anchor="w", tags="score", font=("Consolas", 50), fill="white",
                                text=board.white_score)


class CLI(object):
    def __init__(self, board):

        self.init(board)

    def handle_finish(self, board):
        # global result
        if board.must_pass(0) == True and board.must_pass(1) == True:
            print "Game Finish"
            if board.white_score > board.black_score:
                over_text = "You Win"
            elif board.white_score < board.black_score:
                over_text = "Computer Win"
            else:
                over_text = "Balance"
            print over_text
            # print result
            # exit(1)
            return "Exit"

    def init(self, board):
        # pprint.pprint(board.array)
        self.update(board)

    def update(self, board):
        pprint.pprint(board.array)
        self.draw_score_board(board)

    def draw_score_board(self, board):
        board.update_score()
        print "white has ", board.white_score, " black has ", board.black_score


class Board(object):
    def __init__(self):
        # White goes first (0 is white and player,1 is black and computer)
        self.player = 0

        self.ttl_score = 0
        self.black_score = 0
        self.white_score = 0
        self._next_action = None
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
        self.oldarray = deepcopy(self.array)

    def update_score(self):
        white_score = 0
        black_score = 0
        for x in range(8):
            for y in range(8):
                if self.array[x][y] == "w":
                    white_score += 1
                elif self.array[x][y] == "b":
                    black_score += 1
        self.black_score = black_score
        self.white_score = white_score
        self.ttl_score = self.black_score + self.white_score

    @staticmethod
    def valid(array, player, x, y):
        # Sets player colour
        if player == 0:
            colour = "b"
        else:
            colour = "w"

        # If there's already a piece there, it's an invalid move
        if array[x][y] is not None:
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

    def get_action(self, player=None):
        if player is None:
            player = self.player
        # if self._next_action is None:
        action = []
        for x in range(8):
            for y in range(8):

                if self.valid(self.array, player, x, y):
                    action.append([x, y])
        self._next_action = action
        return action
        # else:
        #     return self._next_action
        # Updating the board to the screen

    def must_pass(self, player):
        must_pass = True
        for x in range(8):
            for y in range(8):
                if self.valid(self.array, player, x, y):
                    must_pass = False
        return must_pass

    def self_move(self, x, y):
        self.oldarray = deepcopy(self.array)
        if self.player == 0:
            self.oldarray[x][y] = "b"
        else:
            self.oldarray[x][y] = "w"
        self.array = self.move(self.array, x, y)

        # Switch Player
        self.player = 1 - self.player

    def move(self, passedArray, x, y):
        # Must copy the passedArray so we don't alter the original
        array = deepcopy(passedArray)
        # Set colour and set the moved location to be that colour
        if self.player == 0:
            colour = "b"
        else:
            colour = "w"
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


class TreeNode(object):
    def __init__(self, *args, **kwargs):
        self.child = []
        self._next_action = []
        self.next_action_visited = set()

        self.parent = None
        self.last_action = None

        self.board = deepcopy(kwargs.get('board', None))
        self.n_visited = 0
        self.n_win = 0

    def get_next_action(self):
        # if not self._next_action:
        action = self.board.get_action()
        # self._next_action = action
        return action  # self._next_action

    def move_2_next_state(self, action):
        next_node = TreeNode(board=self.board)
        next_node.board.array = next_node.board.move(self.board.array, *action)
        next_node.board.player = 1 - self.board.player
        next_node.last_action = action
        next_node.parent = self
        return next_node


# class Tree(object):
#     def __init__(self, *args, **kwargs):
#         if len(kwargs) == 0:
#             self.root = TreeNode()
#         elif len(kwargs) == 1 and kwargs.get('board', None) is not None:
#             self.root = TreeNode(kwargs.get('board'))
#         elif len(kwargs) == 1 and kwargs.get('tree_node', None) is not None:
#             self.root = kwargs.get('tree_node')


class MTCSAgent(object):
    def __init__(self):
        self.mtcs_root_node = None

    def expand(self, tree_node):
        next_actions = tree_node.get_next_action()
        for i in range(len(next_actions)):
            if i in tree_node.next_action_visited:
                continue
            action = next_actions[i]
            next_node = tree_node.move_2_next_state(action)
            tree_node.child.append(next_node)
            tree_node.next_action_visited.add(i)
            return next_node
            # must can return

    def is_final(self, tree_node):
        now_board = tree_node.board
        return (now_board.must_pass(0) and now_board.must_pass(1))

    def tree_policy(self, tree_node):
        while not self.is_final(tree_node):
            if len(tree_node.child) < len(tree_node.get_next_action()):
                next_node = self.expand(tree_node)
                return next_node, False
            elif len(tree_node.child) != 0:
                tree_node = self.best_child(tree_node)
            else:
                # no chess to put
                next_node = deepcopy(tree_node)
                next_node.parent = tree_node
                next_node.board.player = 1 - tree_node.board.player
                return next_node, False

        return tree_node, True  # All Node is explored

    def default_policy(self, tree_node_in):
        tree_node = deepcopy(tree_node_in)  # avoid modify tree_node_in
        while not self.is_final(tree_node):
            actions = tree_node.get_next_action()
            if not actions:
                tree_node.board.player = 1 - tree_node.board.player
            else:
                action = actions[np.random.randint(0, len(actions))]
                tree_node = tree_node.move_2_next_state(action)
        tree_node.board.update_score()
        if tree_node_in.board.player == 0:  # 0 is white and 1 is black
            prob_4_curr_player = tree_node.board.white_score * 1. / tree_node.board.ttl_score
        else:
            prob_4_curr_player = tree_node.board.black_score * 1. / tree_node.board.ttl_score
        return prob_4_curr_player

    def back_up(self, tree_node, prob):
        while tree_node is not None:
            tree_node.n_visited += 1
            tree_node.n_win += prob
            prob = 1 - prob
            tree_node = tree_node.parent

    def best_child(self, tree_node):
        best_child = tree_node.child[0]  # assert there is at least a child
        best_val = -1
        for child in tree_node.child:
            assert child.n_visited != 0, "zero division error"
            t_val = child.n_win * 1. / child.n_visited + \
                    math.sqrt(2. * math.log(tree_node.n_visited) / child.n_visited)

            if t_val > best_val:
                best_child = child

        return best_child

    def agent_get_action(self, board):
        # assert board.player == 1, "1 computer black temporarily"
        # mtcs_tree = Tree(board)
        self.mtcs_root_node = TreeNode(board=board)
        tic = time()  # in seconds
        i = 0
        while True:
            i += 1
            mtcs_tree_node, can_end = self.tree_policy(self.mtcs_root_node)
            # Note: do not affect mtcs_tree_node
            prob = self.default_policy(mtcs_tree_node)
            # print prob
            self.back_up(mtcs_tree_node, prob)
            toc = time()
            if (toc - tic > Config.rollout_time or can_end):
                break
        print time() - tic
        print i
        result = self.best_child(self.mtcs_root_node)
        return result.last_action


if __name__ == "__main__":
    root = Tk()
    main_screen = Canvas(root, width=500, height=600, background="#555")
    main_screen.pack()

    agent = DumbAgent()

    main_screen.focus_set()

    board = Board()
    gui = GUI(screen=main_screen, board=board)
    root.wm_title("Reversi")
    # root.mainloop()
    node1 = TreeNode(board=board)
    node2 = TreeNode(board=board)
    print node1.board.array
    node2.board.array[0][0] = 100
    print node1.board.array

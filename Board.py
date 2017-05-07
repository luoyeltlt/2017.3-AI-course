# from __future__ import division
from Tkinter import *
import argparse, math, cPickle, os, sys, glob, time
from random import *
import copy
import numpy
import pprint, socket, json, threading, thread, pp, subprocess


class DumbAgent(object):
    def agent_get_action(self, board, player=None):
        actions = board.get_action(board.player)
        return actions[0] if len(actions) != 0 else None


class Config(object):
    BLACK = 0
    WHITE = 1

    def __init__(self, first_color, first, second, use_cli, rollout_time):
        self.player_color = first_color
        # 0 is black first
        # 1 is white second
        self.first = first
        self.second = second
        self.rollout_time = rollout_time
        self.use_cli = use_cli


class ComInterface(object):
    def handle_finish(self, board):
        over_text = None
        if board.must_pass(0) == True and board.must_pass(1) == True:
            print "Game Finish"
            if board.white_score < board.black_score:
                over_text = "black Win"
            elif board.white_score > board.black_score:
                over_text = "white Win"
            else:
                over_text = "Balance"
            print over_text

        return over_text


class GUI(ComInterface):
    def __init__(self, tk_screen, tk_root, board):
        self.screen = tk_screen
        self.root = tk_root
        self.input = None
        self.init(board)

    def handle_finish(self, board):
        over_text = super(GUI, self).handle_finish(board)
        self.screen.create_text(
            250, 550,
            anchor="c", font=("Consolas", 15), text=over_text)
        return "Exit" if over_text is not None else None

    def get_input(self, board):
        self.screen.bind("<Button-1>", self.get_input_callback)
        while True:
            self.root.mainloop()
            x, y = self.input
            if board.valid(board.array, board.player, x, y):
                break
            else:
                print "illegal input!"
        return self.input

    def get_input_callback(self, event):
        x = int((event.x - 50) / 50)
        y = int((event.y - 50) / 50)
        if 0 <= x <= 7 and 0 <= y <= 7:
            self.input = [x, y]
            self.root.quit()

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
        # self.screen.update()
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
                            time.sleep(0.01)
                        self.screen.update()
                        self.screen.delete("animated")
                    # Growing
                    for i in reversed(range(21)):
                        self.screen.create_oval(54 + i + 50 * x, 54 + i + 50 * y, 96 - i + 50 * x, 96 - i + 50 * y,
                                                tags="tile animated", fill="#aaa", outline="#aaa")
                        self.screen.create_oval(54 + i + 50 * x, 52 + i + 50 * y, 96 - i + 50 * x, 94 - i + 50 * y,
                                                tags="tile animated", fill="#fff", outline="#fff")
                        if i % 3 == 0:
                            time.sleep(0.01)
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
                            time.sleep(0.01)
                        self.screen.update()
                        self.screen.delete("animated")
                    # Growing
                    for i in reversed(range(21)):
                        self.screen.create_oval(54 + i + 50 * x, 54 + i + 50 * y, 96 - i + 50 * x, 96 - i + 50 * y,
                                                tags="tile animated", fill="#000", outline="#000")
                        self.screen.create_oval(54 + i + 50 * x, 52 + i + 50 * y, 96 - i + 50 * x, 94 - i + 50 * y,
                                                tags="tile animated", fill="#111", outline="#111")
                        if i % 3 == 0:
                            time.sleep(0.01)
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
                if board.player == board.config.player_color:
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


class CLI(ComInterface):
    def __init__(self, board):
        self.init(board)

    def handle_finish(self, board):
        over_text = super(CLI, self).handle_finish(board=board)
        return "Exit" if over_text is not None else None

    def init(self, board):
        # pprint.pprint(board.array)
        self.update(board)

    def update(self, board):
        pprint.pprint(board.array)
        self.draw_score_board(board)

    def draw_score_board(self, board):
        board.update_score()
        print "white has ", board.white_score, " black has ", board.black_score


class SOI(ComInterface):
    def __init__(self, config, client=True, local=True):
        if config.second == "socket" or config.first=="socket":
            if client:
                HOST = '10.214.211.10'
                PORT = 6000
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.settimeout(None)
                while True:
                    # try:
                    errno = self.s.connect_ex((HOST, PORT))
                    if errno == 0:
                        break
                    else:
                        print "No connection"
                        time.sleep(1)
            # elif client and not local:
            #     HOST = '10.214.211.205'
            #     PORT = 8888
            #     self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #     self.s.settimeout(None)
            #     i=0
            #     while i<5 and True:
            #         # try:
            #         i+=1
            #         errno = self.s.connect_ex((HOST, PORT))
            #         if errno == 0:
            #             break
            #         else:
            #             print "No connection"
            #             time.sleep(1)
            # elif not client:
            #     HOST = '10.214.211.205'
            #     PORT = 8888
            #     self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #     self.s.settimeout(None)
            #     self.s.bind((HOST,PORT))
            #     self.s.listen(5)
        else:
            self.s = None

    def _get_input(self):
        # return self.data
        if not self.s:
            return
        data = self.s.recv(1024)
        print "recieve:", data
        data = json.loads(data)
        return data

    def get_data_input(self):
        if not self.s:
            return
        data = self._get_input()
        return [data['x'], data['y']]

    def get_config_input(self):
        if not self.s:
            return
        data = self._get_input()
        if 'White' in data.keys():
            return data
        else:
            return None

    def send_data(self, action):
        if not self.s:
            return
        # str="{" + '"x": {0[0]};  "y": {0[1]}'.format(action)  + "}"
        action = {'x': action[0], 'y': action[1]}
        str = json.dumps(action)
        self.s.send(str)


class Board(object):
    def __init__(self, config):
        # White goes first (0 is black and player,1 is white and computer)
        self.config = config
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
        self.oldarray = copy.deepcopy(self.array)

    def to_array(self):
        save_array = copy.deepcopy(self.array)
        for i, val1 in enumerate(save_array):
            for j, val2 in enumerate(val1):
                if val2 is None:
                    save_array[i][j] = 0
                elif val2 == 'w':
                    save_array[i][j] = -1
                else:
                    save_array[i][j] = 1
        save_array = numpy.array(save_array, dtype=numpy.int32)
        if self.player == Config.BLACK:
            mul = 1
        else:
            mul = -1
        save_player = numpy.ones_like(save_array) * mul
        return numpy.stack((save_player, save_array))

    def change_player(self):
        self.player = 1 - self.player
        self.cache_action()

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
        # self.cache_action()
        if player is None:
            player = self.player
        if self._next_action is None:
            self.cache_action()
        return self._next_action

    def cache_action(self, player=None):
        if player is None:
            player = self.player
        action = []
        for x in range(8):
            for y in range(8):
                if self.valid(self.array, player, x, y):
                    action.append([x, y])
        self._next_action = action

    def must_pass(self, player):
        must_pass = True
        for x in range(8):
            for y in range(8):
                if self.valid(self.array, player, x, y):
                    must_pass = False
        return must_pass

    def self_move(self, x, y):
        if x == -1 and y == -1:
            self.change_player()
        else:
            self.oldarray = copy.deepcopy(self.array)
            if self.player == 0:
                self.oldarray[x][y] = "b"
            else:
                self.oldarray[x][y] = "w"
            self.array = self.move(self.array, x, y)

            # Switch Player
            self.change_player()

    def move(self, passedArray, x, y):
        # Must copy the passedArray so we don't alter the original
        array = copy.deepcopy(passedArray)
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
    def __init__(self, board=None):
        self.child = []
        # self._next_action = []
        self.next_action_visited = set()

        self.parent = None
        self.last_action = None
        self.board = copy.deepcopy(board)
        self.n_visited = 0
        self.n_win = 0

    def get_next_action(self):
        # if not self._next_action:
        return self.board.get_action()
        #     self._next_action = action
        # # else:
        # return self._next_action

    def move_2_next_node(self, action):
        next_node = TreeNode(board=self.board)
        next_node.board.array = next_node.board.move(self.board.array, *action)
        next_node.board.change_player()
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
            next_node = tree_node.move_2_next_node(action)
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
                # next_node = copy.deepcopy(tree_node)
                next_node = TreeNode(board=tree_node.board)
                next_node.parent = tree_node
                next_node.board.change_player()
                next_node.last_action = [-1, -1]
                return next_node, False

        return tree_node, True  # All Node is explored

    def default_policy(self, tree_node_in):
        tree_node = copy.deepcopy(tree_node_in)  # avoid modify tree_node_in

        while not self.is_final(tree_node):
            actions = tree_node.get_next_action()
            if not actions:
                tree_node.board.change_player()
                tree_node.last_action = [-1, -1]
            else:
                action = actions[numpy.random.randint(0, len(actions))]
                tree_node = tree_node.move_2_next_node(action)
        tree_node.board.update_score()
        if tree_node_in.board.player == 0:  # 0 is black and 1 is white
            # prob_4_curr_player = tree_node.board.black_score * 1. / tree_node.board.ttl_score
            prob_4_curr_player = tree_node.board.black_score > tree_node.board.white_score
        else:
            # prob_4_curr_player = tree_node.board.white_score * 1. / tree_node.board.ttl_score
            prob_4_curr_player = tree_node.board.black_score < tree_node.board.white_score
        return int(prob_4_curr_player)

    def back_up(self, tree_node, win, ttl=None):
        if ttl == None:
            ttl = 1
        while tree_node is not None:
            tree_node.n_visited += ttl
            tree_node.n_win += win
            win = ttl - win
            tree_node = tree_node.parent

    def best_child(self, tree_node, info=None, use_uct=True):
        childs = tree_node.child
        val = [1. - child.n_win * 1. / child.n_visited + math.sqrt(2. * math.log(tree_node.n_visited) / child.n_visited)
               for child in tree_node.child]
        prob = [1. - child.n_win * 1. / (child.n_visited * 1.) for child in tree_node.child]
        actions = [child.last_action for child in tree_node.child]
        val_ind = numpy.argmax(val)
        prob_ind = numpy.argmax(prob)
        if info == "show_info":
            if use_uct:
                print "among ", val \
                    , "\n       ", actions \
                    , "\nchoose", val[val_ind] \
                    , "\n     ", actions[val_ind]
            else:
                print "among ", prob, \
                    "\n      ", actions, \
                    "\nchoose", prob[prob_ind], \
                    "\n     ", actions[prob_ind]
        return childs[val_ind] if use_uct else childs[prob_ind]

        # best_child = tree_node.child[0]  # assert there is at least a child
        # best_val = -1
        # for child in tree_node.child:
        #     assert child.n_visited != 0, "zero division error"
        #     t_val = child.n_win * 1. / child.n_visited + \
        #             math.sqrt(2. * math.log(tree_node.n_visited) / child.n_visited)
        #
        #     if t_val > best_val:
        #         best_child = child

        # return best_child

    def go_down(self, action):
        actions = [child.last_action for child in self.mtcs_root_node.child]
        if not actions:
            return False
        for ind, val in enumerate(actions):
            if val == action:
                break
        print "--"
        assert val == action
        assert self.mtcs_root_node.board.player != self.mtcs_root_node.child[ind].board.player
        self.mtcs_root_node = self.mtcs_root_node.child[ind]
        return True
        # if action==[-1,-1]:

    def agent_get_action(self, board, first_action=None, second_action=None):

        # if first_action is None or second_action is None:
        #     self.mtcs_root_node = TreeNode(board=board)
        #
        # else:
        #     if self.go_down(first_action) \
        #             and self.go_down(second_action):
        #         # print "----"
        #         assert self.mtcs_root_node.board.array == board.array
        #         assert self.mtcs_root_node.board.player==board.player
        #
        #     else:
        #         self.mtcs_root_node = TreeNode(board=board)
        self.mtcs_root_node = TreeNode(board=board)

        tic = time.time()  # in seconds
        i = 0
        job_sever = pp.Server(ppservers=())
        while True:
            i += 1
            mtcs_tree_node, can_end = self.tree_policy(self.mtcs_root_node)
            # Note: do not affect mtcs_tree_node

            if 'jobs' in locals():
                del jobs[:]
            jobs = []
            # tic_default=time.time()
            n_cpus = job_sever.get_ncpus()
            for i in range(n_cpus ):#+ 4
                jobs.append(job_sever.submit(self.default_policy,
                                             (mtcs_tree_node,),
                                             (self.mtcs_root_node.get_next_action,
                                              self.mtcs_root_node.board.change_player,
                                              self.mtcs_root_node.move_2_next_node,
                                              self.mtcs_root_node.board.update_score),
                                             ("copy", "numpy")
                                             )
                            )
            win_lose = [job() for job in jobs]
            win = sum(win_lose)
            ttl = len(win_lose)
            # print time.time()-tic_default
            # prob = self.default_policy(mtcs_tree_node)
            # print prob
            self.back_up(mtcs_tree_node, win, ttl)
            toc = time.time()
            # toc=tic
            if (toc - tic > board.config.rollout_time or can_end):
                break
        print "spend time", time.time() - tic, " run ", i
        result = self.best_child(self.mtcs_root_node, "show_info", use_uct=False)
        job_sever.destroy()
        return result.last_action

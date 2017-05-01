from Board import *
import cPickle
import os,sys
import glob

class Config(object):
    player_white = 0
    player_computer = False
    use_cli = False
    rollout_time=0.5

def clickHandle(event):
    # global agent,board
    # White goes first (0 is white player first,1 is black computer second)
    if interface_factory.handle_finish(board)=="Exit":
        result.append([[board.white_score-board.black_score]])
        print result

        os.chdir("output")
        files = glob.glob("*.pkl")
        files = [int(file.split('.')[0]) for file in files]
        files = np.sort(files)
        print files
        file = files[-1] + 1
        print file
        with open(str(file) + ".pkl", "w") as f:
            cPickle.dump(result, f)

        exit(1)

    assert board.player == 0, "now should be player!"

    if board.must_pass(0) == True:
        print "You Have No Choose"
        board.player = 1 - board.player
        action = None
    else:
        if not Config.player_computer:
            while True:
                # Delete the highlights
                x = int((event.x - 50) / 50)
                y = int((event.y - 50) / 50)
                # Determine the grid index for where the mouse was clicked
                # If the click is inside the bounds and the move is valid, move to that location
                if 0 <= x <= 7 and 0 <= y <= 7:
                    if board.valid(board.array, board.player, x, y):
                        action=[x,y]
                        board.self_move(x, y)
                        interface_factory.update(board)
                        break
                print "Your input error, input again: "
        else:
            action = agent.agent_get_action(board)
            board.self_move(*action)
            interface_factory.update(board)
    result.append([[0], [action], [board.array]])
    assert board.player == 1, "now should be computer"
    if board.must_pass(1) == True:
        board.player = 1 - board.player
        print "Computer No Choose"
        interface_factory.update(board)
        action = None
    else:
        action = agent.agent_get_action(board)
        board.self_move(*action)
        interface_factory.update(board)
    result.append([[1], [action], [board.array]])

    print "player has ", board.get_action(0)
    if interface_factory.handle_finish(board)=="Exit":
        print result
        # exit(1)

def clickHandle2(event):
    # global agent,board
    # White goes first (0 is white player first,1 is black computer second)
    interface_factory.handle_finish(board)

    assert board.player == 0, "now should be player!"

    if board.must_pass(0) == True:
        print "You Have No Choose"
        board.player = 1 - board.player

    else:
        while True:
            # Delete the highlights
            x = int((event.x - 50) / 50)
            y = int((event.y - 50) / 50)
            # Determine the grid index for where the mouse was clicked
            # If the click is inside the bounds and the move is valid, move to that location
            if 0 <= x <= 7 and 0 <= y <= 7:
                if board.valid(board.array, board.player, x, y):
                    board.self_move(x, y)
                    interface_factory.update(board)
                    break
            print "Your input error, input again: "

    assert board.player == 1, "now should be computer"
    if board.must_pass(1) == True:
        board.player = 1 - board.player
        print "Computer No Choose"
        interface_factory.update(board)
    else:
        action = agent.agent_get_action(board)
        board.self_move(*action)
        interface_factory.update(board)

    print "player has ", board.get_action(0)
    interface_factory.handle_finish(board)


if __name__ == "__main__":
    # global board, interface_factory, result, agent

    result=[]
    if not Config.use_cli:
        root = Tk()
        main_screen = Canvas(root, width=500, height=600, background="#555")
        main_screen.pack()

        # agent = DumbAgent()
        agent = MTCSAgent()
        # Binding, setting
        main_screen.bind("<Button-1>", clickHandle)
        # main_screen.bind("<Key>", keyHandle)
        main_screen.focus_set()

        board = Board()
        interface_factory = GUI(screen=main_screen, board=board)
        root.wm_title("Reversi")
        root.mainloop()
    else:
        board = Board()
        interface_factory = CLI(board=board)
        agent = MTCSAgent()
        while True:
            clickHandle(None)
            # print result



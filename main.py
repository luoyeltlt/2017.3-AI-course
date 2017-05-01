from Board import *

class Config(object):
    player_color = 0
    # 0 is black first
    # 1 is white second
    player_computer = True
    use_cli = True
    rollout_time=0.5

def clickHandle(event):
    # global agent,board
    if interface_factory.handle_finish(board)=="Exit":
        result.append([[board.white_score,board.black_score]])
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
        if board.white_score-board.black_score>=0:
            exit(1)
        elif board.white_score-board.black_score==0:
            exit(2)
        else:
            exit(3)

    action = None
    assert board.player == 0,"now be black"

    if board.must_pass(0):
        print "black Have No Choose"
        board.player = 1 - board.player
    else:
        if not Config.player_computer and Config.player_color==0:
            # Delete the highlights
            x = int((event.x - 50) / 50)
            y = int((event.y - 50) / 50)
            # Determine the grid index for where the mouse was clicked
            # If the click is inside the bounds and the move is valid, move to that location
            if 0 <= x <= 7 and 0 <= y <= 7 and board.valid(board.array, board.player, x, y):
                action=[x,y]
                board.self_move(x, y)
                interface_factory.update(board)
            else:
                print "Your input error, input again: "
                return
        else:
            action = agent.agent_get_action(board)
            board.self_move(*action)
            interface_factory.update(board)
    result.append([[0], [action], [board.array]])

    assert board.player == 1,"now white"

    if board.must_pass(1) == True:
        board.player = 1 - board.player
        print "white No Choose"
        interface_factory.update(board)
        action = None
    else:
        if not Config.player_computer and Config.player_color==1:
            # Delete the highlights
            x = int((event.x - 50) / 50)
            y = int((event.y - 50) / 50)
            # Determine the grid index for where the mouse was clicked
            # If the click is inside the bounds and the move is valid, move to that location
            if 0 <= x <= 7 and 0 <= y <= 7:
                if board.valid(board.array, board.player, x, y):
                    action = [x, y]
                    board.self_move(x, y)
                    interface_factory.update(board)
            if action is None:
                print "Your input error, input again: "
                return
        else:
            action = agent2.agent_get_action(board) # agent2
            board.self_move(*action)
            interface_factory.update(board)
    result.append([[1], [action], [board.array]])

    print "black has ", board.get_action(0)
    if interface_factory.handle_finish(board)=="Exit":
        print result
        # exit(1)


def clickHandle2(event):
    # global agent,board
    # White goes first (0 is black player first,1 is white computer second)
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
    action = None

    assert board.player == 1,"now white"

    if board.must_pass(1):
        board.player = 1 - board.player
        print "white No Choose"
        interface_factory.update(board)
        action = None
    else:
        if not Config.player_computer and Config.player_color==1:
            # Delete the highlights
            x = int((event.x - 50) / 50)
            y = int((event.y - 50) / 50)
            if 0 <= x <= 7 and 0 <= y <= 7:
                if board.valid(board.array, board.player, x, y):
                    action = [x, y]
                    board.self_move(x, y)
                    interface_factory.update(board)
            if action is None:
                print "Your input error, input again: "
                return
        else:
            action = agent.agent_get_action(board)
            board.self_move(*action)
            interface_factory.update(board)
    result.append([[1], [action], [board.array]])


    assert board.player == 0,"now black"

    if board.must_pass(0):
        print "black Have No Choose"
        board.player = 1 - board.player
        interface_factory.update(board)
    else:
        if not Config.player_computer and Config.player_color==0:
            # Delete the highlights
            x = int((event.x - 50) / 50)
            y = int((event.y - 50) / 50)
            if 0 <= x <= 7 and 0 <= y <= 7 and board.valid(board.array, board.player, x, y):
                action=[x,y]
                board.self_move(x, y)
                interface_factory.update(board)
            else:
                print "Your input error, input again: "
                return
        else:
            action = agent.agent_get_action(board)
            board.self_move(*action)
            interface_factory.update(board)
    result.append([[0], [action], [board.array]])

    print "white has ", board.get_action(1)
    if interface_factory.handle_finish(board)=="Exit":
        print result
        # exit(1)


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
        if Config.player_color==0:
            main_screen.bind("<Button-1>", clickHandle)
        else:
            main_screen.bind("<Button-1>",clickHandle2)


        main_screen.focus_set()

        board = Board()
        interface_factory = GUI(screen=main_screen, board=board)
        root.wm_title("Reversi")
        if Config.player_color==1:
            action = agent.agent_get_action(board)
            board.self_move(*action)
            interface_factory.update(board)
        root.mainloop()
    else:
        board = Board()
        interface_factory = CLI(board=board)
        agent = MTCSAgent()
        agent2=DumbAgent()
        while True:
            clickHandle(None)
            # print result



from Board import *


def clickHandle(event):
    # global agent,board
    if player_interface.handle_finish(board)== "Exit":
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
                player_interface.update(board)
            else:
                print "Your input error, input again: "
                return
        else:
            action = agent.agent_get_action(board)
            board.self_move(*action)
            player_interface.update(board)
    result.append([[0], [action], [board.array]])

    assert board.player == 1,"now white"

    if board.must_pass(1) == True:
        board.player = 1 - board.player
        print "white No Choose"
        player_interface.update(board)
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
                    player_interface.update(board)
            if action is None:
                print "Your input error, input again: "
                return
        else:
            action = agent2.agent_get_action(board) # agent2
            board.self_move(*action)
            player_interface.update(board)
    result.append([[1], [action], [board.array]])

    print "black has ", board.get_action(0)
    if player_interface.handle_finish(board)== "Exit":
        print result
        # exit(1)

def m_main_loop():

    while True:
        if player_interface.handle_finish(board) == "Exit":
            # exit(1)
            return
        assert board.player == 0, "now be black"
        if board.must_pass(0):
            print "black no choose"
            board.player=1-board.player
            so_interface.send_data([-1,-1])
        else:
            # action=player_interface.get_input(board)
            action=agent.agent_get_action(board)
            board.self_move(*action)
            player_interface.update(board)
            so_interface.send_data(action)

        assert board.player==1,"now white"

        if board.must_pass(1):
            print "white no choose"
            action = so_interface.get_data_input()
            board.player=1-board.player
            if config.use_socket:
                assert action==[-1,-1],"action must be [-1,-1]"
        else:
            if config.use_socket:
                action = so_interface.get_data_input()
            else:
                action=agent2.agent_get_action(board)
            board.self_move(*action)
            player_interface.update(board)


if __name__ == "__main__":
    # global board, interface_factory, result, agent
    result = []
    config = Config(player_color=0,
                    player_computer=False ,
                    rollout_time=0.1,
                    use_socket=False)

    agent=MTCSAgent()
    agent2 = DumbAgent()
    root=Tk()
    root.wm_title('Reversi')
    screen= Canvas(root, width=500, height=600, background="#555")
    screen.pack()
    screen.focus_set()
    board=Board(config)
    player_interface=GUI(screen, root, board)

    so_interface=SOI(config=config)

    config_data = so_interface.get_config_input()
    data = so_interface.get_data_input()

    m_main_loop()




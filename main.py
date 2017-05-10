from Board import *
import paramiko

def clickHandle(event):
    # global agent,board
    if gui_cli.handle_finish(board) == "Exit":
        result.append([[board.white_score, board.black_score]])
        print result
        os.chdir("output")
        files = glob.glob("*.pkl")
        files = [int(file.split('.')[0]) for file in files]
        files = numpy.sort(files)
        print files
        file = files[-1] + 1
        print file
        with open(str(file) + ".pkl", "w") as f:
            cPickle.dump(result, f)
        if board.white_score - board.black_score >= 0:
            exit(1)
        elif board.white_score - board.black_score == 0:
            exit(2)
        else:
            exit(3)

    action = None
    assert board.player == 0, "now be black"

    if board.must_pass(0):
        print "black Have No Choose"
        board.player = 1 - board.player
    else:
        if not Config.player_computer and Config.player_color == 0:
            # Delete the highlights
            x = int((event.x - 50) / 50)
            y = int((event.y - 50) / 50)
            # Determine the grid index for where the mouse was clicked
            # If the click is inside the bounds and the move is valid, move to that location
            if 0 <= x <= 7 and 0 <= y <= 7 and board.valid(board.array, board.player, x, y):
                action = [x, y]
                board.self_move(x, y)
                gui_cli.update(board)
            else:
                print "Your input error, input again: "
                return
        else:
            action = mtcs_agent.agent_get_action(board)
            board.self_move(*action)
            gui_cli.update(board)
    result.append([[0], [action], [board.array]])

    assert board.player == 1, "now white"

    if board.must_pass(1) == True:
        board.player = 1 - board.player
        print "white No Choose"
        gui_cli.update(board)
        action = None
    else:
        if not Config.player_computer and Config.player_color == 1:
            # Delete the highlights
            x = int((event.x - 50) / 50)
            y = int((event.y - 50) / 50)
            # Determine the grid index for where the mouse was clicked
            # If the click is inside the bounds and the move is valid, move to that location
            if 0 <= x <= 7 and 0 <= y <= 7:
                if board.valid(board.array, board.player, x, y):
                    action = [x, y]
                    board.self_move(x, y)
                    gui_cli.update(board)
            if action is None:
                print "Your input error, input again: "
                return
        else:
            action = dumb_agent.agent_get_action(board)  # agent2
            board.self_move(*action)
            gui_cli.update(board)
    result.append([[1], [action], [board.array]])

    print "black has ", board.get_action(0)
    if gui_cli.handle_finish(board) == "Exit":
        print result
        # exit(1)


def m_main_loop():
    first_action, second_action = None, None
    # result.append([board.to_array()])
    while True:
        if gui_cli.handle_finish(board) == "Exit":
            if board.white_score < board.black_score:
                return 1
            elif board.white_score > board.black_score:
                return -1
            else:
                return 0

        assert board.player == 0, "now be black"
        if board.must_pass(0):
            print "black no choose"
            if config.first=="socket":
                first_action=soi.get_data_input()
            first_action = [-1, -1]

        else:
            if config.first == "gui":
                first_action = gui_cli.get_input(board)

            elif config.first == "mtcs":
                first_action = mtcs_agent.agent_get_action(board, first_action, second_action)
                assert board.player == 0, "now be black"
                possible_actions = board.get_action()
                # print "---"
                assert first_action in possible_actions, "!!"
            elif config.first=="dumb":
                first_action=dumb_agent.agent_get_action(board)
            elif config.first=="socket":
                first_action = soi.get_data_input()

            if config.first!="socket":
                soi.send_data(first_action)

        board.self_move(*first_action)
        gui_cli.update(board)

        # result.append([first_action])
        # result.append([board.to_array()])

        assert board.player == 1, "now white"

        if board.must_pass(1):
            print "white no choose"
            if config.second=="socket":
                soi.get_data_input()
            second_action = [-1, -1]
        else:
            if config.second == "socket":
                second_action = soi.get_data_input()
            elif config.second == "dumb":
                second_action = dumb_agent.agent_get_action(board)
            elif config.second == "mtcs":
                second_action = second_mtcs_agent.agent_get_action(board)
                assert board.player == 1, "now be white"
                possible_actions = board.get_action()
                # print "---"
                assert second_action in possible_actions, "!!"
            if config.second!="socket":
                soi.send_data(second_action)

        board.self_move(*second_action)
        gui_cli.update(board)
        # result.append([first_action])
        # result.append([board.to_array()])


if __name__ == "__main__":
    # while True:
    #     print "OK"
    result = []
    dbg = True
    if not dbg:
        config = Config(first_color=Config.BLACK,
                        first="socket",  # socket mtcs dumb gui
                        second="mtcs",  # socket mtcs dumb
                        use_cli=True,
                        rollout_time=30)
    else:
        config = Config(first_color=Config.BLACK,
                        first="dumb",  # socket mtcs dumb gui
                        second="mtcs",  # socket mtcs dumb
                        use_cli=True,
                        rollout_time=5)

    mtcs_agent = MTCSAgent()
    dumb_agent = DumbAgent()
    second_mtcs_agent = MTCSAgent()
    board = Board(config)
    if not config.use_cli:
        root = Tk()
        root.wm_title('Reversi')
        screen = Canvas(root, width=500, height=600, background="#555")
        screen.pack()
        screen.focus_set()
        gui_cli = GUI(screen, root, board)
    else:
        gui_cli = CLI(board)
    soi = SOI(config=config, client=True, local=True)

    config_data = soi.get_config_input()
    data = soi.get_data_input()
    soi.buf=data
    res = m_main_loop()

    result.append([res])
    print result
    # subprocess.call("mkdir -p output".split(" "))
    # os.chdir("output")
    # files = glob.glob("*.pkl")
    # if not files:
    #     file = 0
    # else:
    #     files = [int(file.split('.')[0]) for file in files]
    #     files = numpy.sort(files)
    #     file = files[-1] + 1

        # print file
        # with open(str(file) + ".pkl", "w") as f:
        #     cPickle.dump(result, f)

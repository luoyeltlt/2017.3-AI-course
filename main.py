from Board import *
import paramiko

def m_main_loop():
    first_action, second_action = None, None
    result.append([board.to_array()])
    while True:
        LOG.info("New round\n=============================\n")
        if gui_cli.handle_finish(board) == "Exit":
            if board.white_score < board.black_score:
                return 1
                # exit(1)
            elif board.white_score > board.black_score:
                return -1
                # exit(-1)
            else:
                return 0
                # exit(0)

        assert board.player == config.first_color, "now be fisrt color"

        if config.first == "gui":
            if board.must_pass(config.first_color):
                first_action=[-1,-1]
            else:
                first_action = gui_cli.get_input(board)
        elif config.first == "mtcs":
            first_action = mtcs_agent.agent_get_action(board, second_action=second_action)
            assert board.player == config.first_color, "now be black"
            assert not board.get_action() or first_action in board.get_action(), "!!"
        elif config.first == "dumb":
            first_action = dumb_agent.agent_get_action(board)
        elif config.first == "socket":
            first_action = soi.get_data_input()

        if config.first != "socket":
            soi.send_data(first_action)

        if board.must_pass(config.first_color):
            print "first color no choose"
            assert  first_action==[-1,-1]


        board.self_move(*first_action)
        gui_cli.update(board)

        result.append([first_action])
        result.append([board.to_array()])

        assert board.player == config.second_color, "now second color"

        if config.second == "socket":
            second_action = soi.get_data_input()
        elif config.second == "dumb":
            second_action = dumb_agent.agent_get_action(board)
        elif config.second == "mtcs":
            second_action = second_mtcs_agent.agent_get_action(board, first_action=first_action)
            assert board.player == config.second_color, "now be second color"
            assert not board.get_action() or second_action in board.get_action(), "!!"
        if config.second != "socket":
            soi.send_data(second_action)

        if board.must_pass(config.second_color):
            print "second color no choose"
            assert second_action==[-1,-1]

        board.self_move(*second_action)
        gui_cli.update(board)

        result.append([first_action])
        result.append([board.to_array()])


if __name__ == "__main__":
    result = []
    dbg = False

    if not dbg:
        config = Config(first_color=Config.BLACK,
                        first="socket",  # socket mtcs dumb gui
                        host='10.214.211.9',
                        port=6000,
                        second="mtcs",  # socket mtcs dumb
                        use_cli=True,
                        rollout_time=30,
                        dbg=dbg)
    else:
        config = Config(first_color=Config.WHITE,
                        first="mtcs",  # socket mtcs dumb gui
                        second="mtcs",  # socket mtcs dumb
                        use_cli=True,
                        rollout_time=numpy.random.randint(20,35,size=1)[0],
                        # rollout_time=0.5,
                        dbg=dbg)
    soi = SOI(config=config, client=True, local=True)
    if config.first == "socket" or config.second == 'socket':
        while len(soi.buf) == 0:
            continue
        config_data = soi.get_config_input()
        if config_data['Black']==0: # black first! black 0
            config.first_color=Config.BLACK # black 0
        else:
            config.first_color=Config.WHITE
        data=soi.get_data_input()
        if data!=[-2,-2]:
            soi.buf.append(data)
        else:
            config.first="mtcs"
            config.second="socket"

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


    res = m_main_loop()

    result.append([res])
    print result

    subprocess.call("mkdir -p output".split(" "))
    os.chdir("output")
    files = glob.glob("*.pkl")
    if not files:
        file = 0
    else:
        files = [int(file.split('.')[0]) for file in files]
        files = numpy.sort(files)
        file = files[-1] + 1

    print file
    with open(str(file) + ".pkl", "w") as f:
        cPickle.dump(result, f)

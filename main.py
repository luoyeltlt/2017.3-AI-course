from Board import *


def clickHandle(event):
    # global agent,board
    # White goes first (0 is black player first,1 is white computer second)
    gui.handle_finish(board)

    assert board.player == 0, "now should be player!"

    if board.must_pass(0) == True:
        print "You Have No Choose"
        board.player = 1 - board.player

    else:
        while(True):
            # Delete the highlights
            x = int((event.x - 50) / 50)
            y = int((event.y - 50) / 50)
            # Determine the grid index for where the mouse was clicked
            # If the click is inside the bounds and the move is valid, move to that location
            if 0 <= x <= 7 and 0 <= y <= 7:
                if board.valid(board.array, board.player, x, y):
                    board.self_move(x,y)
                    gui.update(board)
                    break
            print "Your input error, input again: "

    assert board.player == 1, "now should be computer"
    if board.must_pass(1) == True:
        board.player = 1 - board.player
        print "Computer No Choose"
        gui.update(board)
    else:
        action = agent.agent_get_action(board)
        board.self_move(x, y)
        gui.update(board)

    print "player has ", board.get_action(0)
    gui.handle_finish(board)



def clickHandle2(event):
    # global agent,board
    # White goes first (0 is white and computer,1 is black and player)
    gui.handle_finish(board)

    assert board.player == 0, "now should be white!"

    if board.must_pass(0) == True:
        print "You Have No Choose"
        board.player = 1 - board.player
    else:
        # Delete the highlights
        x = int((event.x - 50) / 50)
        y = int((event.y - 50) / 50)
        # Determine the grid index for where the mouse was clicked

        # If the click is inside the bounds and the move is valid, move to that location
        if 0 <= x <= 7 and 0 <= y <= 7:
            if board.valid(board.array, board.player, x, y):
                gui.draw_board_move(board=board, x=x, y=y)

    assert board.player == 1, "now should be black"
    if board.must_pass(1) == True:
        board.player = 1 - board.player
        print "Computer No Choose"
        gui.update(board)
    else:
        action = agent.agent_get_action(board)
        gui.draw_board_move(board, *action)

    print "player has ", board.get_action(0)
    gui.handle_finish(board)



if __name__ == "__main__":
    # global board,gui,agent
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
    gui = GUI(screen=main_screen, board=board)
    root.wm_title("Reversi")
    root.mainloop()

from Board import *


def clickHandle(event):
    # global agent,board
    # White goes first (0 is white and player,1 is black and computer)
    if board.must_pass(0)==True and board.must_pass(1)==True:
        if board.white_score>board.black_score:
            over_text="You Win"
        elif board.white_score<board.black_score:
            over_text="Computer Win"
        else:
            over_text="Balance"

        board.screen.create_text(250, 550, anchor="c", font=("Consolas", 15), text=over_text)

    assert board.player == 0, "not your move?"

    if board.must_pass(0)==True:
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
                gui.draw_board_move(board=board, x=x, y=y)

    assert board.player == 1, "not computer move?"
    if board.must_pass(1) == True:
        board.player = 1 - board.player
        print "Computer No Choose"
    else:
        action=agent.agent_get_action(board)
        gui.draw_board_move(board, *action)

    print "player has ", board.get_action(0)


if __name__ == "__main__":
    # global board,gui,agent
    root = Tk()
    main_screen = Canvas(root, width=500, height=600, background="#555")
    main_screen.pack()

    # agent = DumbAgent()
    agent=MTCSAgent()
    # Binding, setting
    main_screen.bind("<Button-1>", clickHandle)
    # main_screen.bind("<Key>", keyHandle)
    main_screen.focus_set()

    board = Board()
    gui=GUI(screen=main_screen,board=board)
    root.wm_title("Reversi")
    root.mainloop()

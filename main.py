from Board import *


def clickHandle(event):
    # global agent,board
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
    # global board,agent
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

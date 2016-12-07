from Board import Board
import sys

class BoardView:
    ROWS = 8
    COLUMNS = 9

    def __init__(self):
        print "Nothing"

    def draw_board(self, board):
        for currentRow in reversed(xrange(BoardView.ROWS)):
            sys.stdout.write("%s\t" %abs(currentRow + 1))
            for currentCol in range(0, BoardView.COLUMNS):
                if (board.get_square_resident(currentRow, currentCol) != None):
                    if (board.get_square_resident(currentRow, currentCol).botOperated):
                        sys.stdout.write("C%s%s\t" %(board.get_square_resident(currentRow, currentCol).top, board.get_square_resident(currentRow, currentCol).left))
                    else:
                        sys.stdout.write("H%s%s\t" %(board.get_square_resident(currentRow, currentCol).top, board.get_square_resident(currentRow, currentCol).right))
                else:
                    sys.stdout.write("-\t")
            sys.stdout.write("\n")
        sys.stdout.write("\t1\t2\t3\t4\t5\t6\t7\t8\t9\n\n")
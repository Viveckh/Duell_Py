# coding: utf-8
# BoardView Class
# Draws the updated game board to the console. Also can notify the user about the dices that haven’t been captured and are active on the game board.
#

"""	************************************************************
* Name:			Vivek Pandey								*
* Project:		Duell Python								*
* Class:		CMPS 366									*
* Date:			12/10/2016									*
************************************************************ """

from Board import Board
import sys

class BoardView:
    #Class Variables
    ROWS = 8
    COLUMNS = 9

    """ *********************************************************************
    Function Name: draw_board
    
    Purpose: Draws the game board to the console
    
    Parameters: board, board object to be drawn
    
    Return Value: none
    
    Local Variables: none besides loop counters
    
    Assistance Received: none
    ********************************************************************* """
    # Draws the GameBoard to the console
    def draw_board(self, board):
        print "\n"
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
            sys.stdout.write("\n\n")
        sys.stdout.write("\t1\t2\t3\t4\t5\t6\t7\t8\t9\n\n")
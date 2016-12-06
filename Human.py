from Player import Player
from Board import Board
from BoardView import BoardView

class Human(Player):
    #Validates user's Input, Validates user's move and performs the move as instructed by human player
    def play(self, startRow, startCol, endRow, endCol, board, path=0):
        Player.printNotifications = True

        if (self.index_out_of_bounds(startRow, startCol, endRow, endCol)):
            #Log error here
            #PRINT NOTIFICATIONS
            return False
        
        #Decrementing the input values to match the gameboard internal representation in list
        startRow -= 1
        startCol -= 1
        endRow -= 1
        endCol -= 1

        #Verify the dice is not bot operated so that the dice belongs to human player
        if (board.get_square_resident(startRow, startCol) != None):
            if (not board.get_square_resident(startRow, startCol).botOperated):
                #Checking to see if there is a 90 degree turn
                if (Player.make_a_move(self, startRow, startCol, endRow, endCol, board, False, path)):
                    return True
                else:
                    return False
            else:
                #PRINT NOTIFICATIONS
                return False
        else:
            #PRINT NOTIFICATIONS
            return False
    
    
    #Returns true if any input values are out of bounds, call before decrementing the input values to match the gameboard array indexes
    def index_out_of_bounds(self, startRow, startCol, endRow, endCol):
        if (startRow <= 0 or startRow > 8):
            return True
        if (startCol <= 0 or startCol > 9):
            return True
        if (endRow <= 0 or endRow > 8):
            return True
        if (endCol <= 0 or endCol > 9):
            return True
        return False


#Main at the moment
boa = Board()
bv = BoardView()
player = Human()
bv.draw_board(boa)

player.play(1, 1, 2, 1, boa)
bv.draw_board(boa)
player.play(1, 1, 2, 5, boa)
bv.draw_board(boa)
player.play(1, 9, 2, 5, boa)
bv.draw_board(boa)
player.play(8, 6, 2, 6, boa)
bv.draw_board(boa)
player.play(2, 6, 3, 6, boa)
bv.draw_board(boa)
player.play(1, 7, 2, 6, boa)
bv.draw_board(boa)
player.play(1, 6, 7, 6, boa)
bv.draw_board(boa)
player.play(1, 2, 1, 1, boa)
bv.draw_board(boa)
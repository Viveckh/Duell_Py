from copy import deepcopy
from BoardView import BoardView
from Board import Board

class Player:
    printStatus = True
    printNotifications = True

    def __init__(self):
        self.pathChoice = 0
        self.multiplePathPossible = False
        self.tempStorage1 = 0
        self.tempStorage2 = 0
        self.counterRowsTraversed = 0
        self.counterColumnsTraversed = 0

    def roll_up(self, dice, board):
        self.tempStorage1 = dice.front
        self.tempStorage2 = dice.rear

        dice.front = dice.top
        dice.rear = dice.bottom
        dice.bottom = self.tempStorage1
        dice.top = self.tempStorage2

        #Set the currently occupied square to empty (also capturing the current dice, if in destination), and place our dice in the next square
        board.set_square_resident_dice(dice.row, dice.column, None)
        dice.row = dice.row + 1

        #This capture statement will only be executed at the destination square if path checking is done beforehand
        if (board.get_square_resident(dice.row, dice.column) != None):
            board.set_square_resident_captured(dice.row, dice.column, True)
            #PRINT NOTIFICATIONS
        
        board.set_square_resident_dice(dice.row, dice.column, dice)

    def roll_down(self, dice, board):
        self.tempStorage1 = dice.front
        self.tempStorage2 = dice.rear

        dice.rear = dice.top
        dice.front = dice.bottom
        dice.top = self.tempStorage1
        dice.bottom = self.tempStorage2

        #Set the currently occupied square to empty (also capturing the current dice, if in destination), and place our dice in the next square
        board.set_square_resident_dice(dice.row, dice.column, None)
        dice.row = dice.row - 1

        #This capture statement will only be executed at the destination square if path checking is done beforehand
        if (board.get_square_resident(dice.row, dice.column) != None):
            board.set_square_resident_captured(dice.row, dice.column, True)
            #PRINT NOTIFICATIONS
        
        board.set_square_resident_dice(dice.row, dice.column, dice)

    def roll_left(self, dice, board):
        self.tempStorage1 = dice.left
        self.tempStorage2 = dice.right

        dice.left = dice.top
        dice.right = dice.bottom
        dice.bottom = self.tempStorage1
        dice.top = self.tempStorage2

        #Set the currently occupied square to empty (also capturing the current dice, if in destination), and place our dice in the next square
        board.set_square_resident_dice(dice.row, dice.column, None)
        dice.column = dice.column - 1

        #This capture statement will only be executed at the destination square if path checking is done beforehand
        if (board.get_square_resident(dice.row, dice.column) != None):
            board.set_square_resident_captured(dice.row, dice.column, True)
            #PRINT NOTIFICATIONS
        
        board.set_square_resident_dice(dice.row, dice.column, dice)

    def roll_right(self, dice, board):
        self.tempStorage1 = dice.left
        self.tempStorage2 = dice.right

        dice.right = dice.top
        dice.left = dice.bottom
        dice.top = self.tempStorage1
        dice.bottom = self.tempStorage2

        #Set the currently occupied square to empty (also capturing the current dice, if in destination), and place our dice in the next square
        board.set_square_resident_dice(dice.row, dice.column, None)
        dice.column = dice.column + 1

        #This capture statement will only be executed at the destination square if path checking is done beforehand
        if (board.get_square_resident(dice.row, dice.column) != None):
            board.set_square_resident_captured(dice.row, dice.column, True)
            #PRINT NOTIFICATIONS
        
        board.set_square_resident_dice(dice.row, dice.column, dice)
    
    def is_path_valid(self, origin, gameBoard):
        dice = deepcopy(origin)
        board = deepcopy(gameBoard)


#Main at the moment
board = Board()
bv = BoardView()
player = Player()
bv.draw_board(board)
player.roll_up(board.get_square_resident(0, 0), board)
bv.draw_board(board)
player.roll_right(board.get_square_resident(1, 0), board)
bv.draw_board(board)
player.roll_right(board.get_square_resident(1, 1), board)
bv.draw_board(board)
player.roll_left(board.get_square_resident(1, 2), board)
bv.draw_board(board)
player.roll_left(board.get_square_resident(1, 1), board)
bv.draw_board(board)
player.roll_down(board.get_square_resident(1, 0), board)
bv.draw_board(board)
player.is_path_valid(board.get_square_resident(0, 0), board)
bv.draw_board(board)
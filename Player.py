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
    
    def is_valid_destination(self, origin, dest):
        #Making duplicate copies of function parameters to avoid modifying original reference
        dice = deepcopy(origin)
        destination = deepcopy(dest)

        #Destination square should either be null or contain a dice of different team other than the one moving.
        if ((destination.resident == None) or (destination.resident.botOperated and not dice.botOperated) or (not destination.resident.botOperated and dice.botOperated)):
            #(Destination row - source row) + (Destination col - source col) gives the distance between the source and destination squares
            if (dice.top == abs(destination.row - dice.row) + abs(destination.column - dice.column)):
                return True
            else:
                #PRINT NOTIFICATIONS
                return False
        else:
            #PRINT NOTIFICATIONS
            return False 
        return False

    def is_path_valid(self, origin, dest, gameBoard):
        #The temporary dice jumps from one square to the other and checks if it is already occupied

        #Making duplicate copies of function parameters to avoid modifying original reference
        dice = deepcopy(origin)
        destination = deepcopy(dest)
        board = deepcopy(gameBoard)

        #Resetting values for calculations
        self.counterRowsTraversed = 0
        self.counterColumnsTraversed = 0
        self.pathChoice = 0
        self.multiplePathPossible = False

        """CASE 1
        If both the rows & columns differ in the destination, it means this is a frontal-lateral combined move attempt
        TWO possible paths"""
        if((dice.row != destination.row) and (dice.column != destination.column)):
            
            #Only one path needs to pass
            #Path 1 - First row traversal, then column
            if (self.traversed_rows_without_blockade(dice, destination, board) and self.traversed_columns_without_blockade(dice, destination, board)):
                self.pathChoice = 1

            """In case we need to check the validity of second path, the dice needs to be reverted back to its original spot
            based on the counters gathered while traversing above"""
            dice.row = dice.row - self.counterRowsTraversed
            dice.column = dice.column - self.counterColumnsTraversed

            #Path 2 - First column traversal, then row
            if (self.traversed_columns_without_blockade(dice, destination, board) and self.traversed_columns_without_blockade(dice, destination, board)):
                #If the previous path was valid too, then there are surely two paths
                if (self.pathChoice == 1):
                    self.multiplePathPossible = True
                    return True

                self.pathChoice = 2
                return True

            #If the first path was the only one valid
            if (self.pathChoice == 1):
                return True

            #If both the path couldn't return true, then the path is invalid
            #PRINT NOTIFICATIONS
            return False

        """CASE 2
        If only the rows change in destination, it means this is a frontal/backward move attempt
        ONE possible path"""
        if (dice.row != destination.row):
            if (self.traversed_rows_without_blockade(dice, destination, board)):
                self.pathChoice = 3
                return True
            else:
                #PRINT NOTIFICATIONS
                return False

        """CASE 3
        If only the column change, it means this is a lateral move attempt
        ONE possible path"""
        if (dice.column != destination.column):
            if (self.traversed_columns_without_blockade(dice, destination, board)):
                self.pathChoice = 4
                return True
            else:
                #PRINT NOTIFICATIONS
                return False
        
        #If moving from and to the current location, still true lol
        return True

    def traversed_rows_without_blockade(self, dice, dest, gameBoard):
        #Still passed by reference cause in case of a 90 degree turn, we want the dice state preserved to call traversed_columns_without_blockade

        #Making duplicate copies of function parameters to avoid modifying original reference
        destination = deepcopy(dest)
        board = deepcopy(gameBoard)

        self.counterRowsTraversed = 0
        while True:
            #Increment if destination is in a upper row, decrement if in lower row
            if (dice.row < destination.row):
                dice.row = dice.row + 1
                self.counterRowsTraversed += 1
            else:
                dice.row = dice.row - 1
                self.counterRowsTraversed -= 1
            
            #No need to check on the destination. If it reaches there, the traversal is considered successful
            if ((dice.row == destination.row) and (dice.column == destination.column)):
                return True

            #Check if there is a blockade on the path as you go
            #If yes, the path is invalid
            if (board.get_square_resident(dice.row, dice.column) != None):
                return False

            if (dice.row == destination.row):
                break
        
        #If it gets to this poiont without any false returns, it is a valid path anyway
        return True
    
    def traversed_columns_without_blockade(self, dice, dest, gameBoard):
        #Making duplicate copies of function parameters to avoid modifying original reference
        destination = deepcopy(dest)
        board = deepcopy(gameBoard)

        self.counterColumnsTraversed = 0
        while True:
            #Increment if destination is in right column, decrement if in a left column
            if (dice.column < destination.column):
                dice.column = dice.column + 1
                self.counterColumnsTraversed += 1
            else:
                dice.column = dice.column - 1
                self.counterColumnsTraversed -= 1
            
            #No need to check on the destination. If it reaches there, the traversal is considered successful
            if ((dice.row == destination.row) and (dice.column == destination.column)):
                return True

            #Check if there is a blockade on the path as you go
            #If yes, the path is invalid
            if (board.get_square_resident(dice.row, dice.column) != None):
                return False

            if (dice.column == destination.column):
                break
        
        #If it gets to this poiont without any false returns, it is a valid path anyway
        return True

    def make_a_move(self, startRow, startCol, endRow, endCol, board, helpModeOn, path=0):
        """Check if destination is valid, then if path is valid
        Then, either make the move or log an error
        This can be used for both human or computer after verifying that they are moving their own players.
        Path 1 and 2 need to offset the changes done by the first function, and hence the startRow/startCol has a counter added in the second function"""
        if (self.is_valid_destination(board.get_square_resident(startRow, startCol), board.get_square_at_location(endRow, endCol))):
            if (self.is_path_valid(board.get_square_resident(startRow, startCol), board.get_square_at_location(endRow, endCol), board)):
                #If help mode is on, no need to make the actual move, return true here and print suggestion
                if (helpModeOn):
                    #PRINT NOTIFICATIONS
                    return True
                
                topValueAtStart = board.get_square_resident(startRow, startCol).top
                rightValueAtStart = board.get_square_resident(startRow, startCol).right

                #If user has input a preferred path in case of a 90 degree turn, we need to honor that
                if (path != 0):
                    if (path == 1 and self.pathChoice == 1):
                        self.pathChoice = 1

                    if ((path == 2) and (self.pathChoice == 2 or self.multiplePathPossible)):
                        self.pathChoice = 2
                    
                    #Display a notification if the user's choice of path wasn't valid and had to be overridden by the next best route
                    if (path != self.pathChoice):
                        #PRINT NOTIFICATIONS
                        print "Nothing"
                
                #Start the rolls

                #First Vertically, a 90 degree turn, then laterally
                if (self.pathChoice == 1):
                    self.keep_rolling_vertically(board.get_square_resident(startRow, startCol), board.get_square_at_location(endRow, endCol), board)
                    self.keep_rolling_laterally(board.get_square_resident(startRow + self.counterRowsTraversed, startCol), board.get_square_at_location(endRow, endCol), board)
                    #PRINT NOTIFICATIONS

                #First Laterally, a 90 degree turn, then vertically
                elif (self.pathChoice == 2):
                    self.keep_rolling_laterally(board.get_square_resident(startRow, startCol), board.get_square_at_location(endRow, endCol), board)
                    self.keep_rolling_vertically(board.get_square_resident(startRow, startCol + self.counterColumnsTraversed), board.get_square_at_location(endRow, endCol), board)
                    #PRINT NOTIFICATIONS

                #Vertically only
                elif (self.pathChoice == 3):
                    self.keep_rolling_vertically(board.get_square_resident(startRow, startCol), board.get_square_at_location(endRow, endCol), board)
                    #PRINT NOTIFICATIONS

                #Laterally only
                elif (self.pathChoice == 4):
                    self.keep_rolling_laterally(board.get_square_resident(startRow, startCol), board.get_square_at_location(endRow, endCol), board)
                    #PRINT NOTIFICATIONS

                else:
                    #PRINT NOTIFICATIONS
                    return False
                
                #PRINT NOTIFICATIONS
                return True
        return False

    def keep_rolling_vertically(self, dice, destination, board):
        self.counterRowsTraversed = 0
        while True:
            if (dice.row < destination.row):
                self.roll_up(dice, board)
                self.counterRowsTraversed += 1
            else:
                self.roll_down(dice, board)
                self.counterRowsTraversed -= 1

            if(dice.row == destination.row):
                break 
    
    def keep_rolling_laterally(self, dice, destination, board):
        self.counterColumnsTraversed = 0
        while True:
            if (dice.column < destination.column):
                self.roll_right(dice, board)
                self.counterColumnsTraversed -= 1
            else:
                self.roll_left(dice, board)
                self.counterColumnsTraversed -= 1

            if(dice.column == destination.column):
                break


#Main at the moment
board = Board()
bv = BoardView()
player = Player()
bv.draw_board(board)

"""player.roll_up(board.get_square_resident(0, 0), board)
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
bv.draw_board(board)"""
player.make_a_move(0, 0, 1, 0, board, False)
bv.draw_board(board)
player.make_a_move(0, 0, 1, 4, board, False)
bv.draw_board(board)
player.make_a_move(0, 8, 1, 4, board, False)
bv.draw_board(board)
player.make_a_move(7, 5, 1, 5, board, False)
bv.draw_board(board)
player.make_a_move(1, 5, 2, 5, board, False)
bv.draw_board(board)
player.make_a_move(0, 6, 1, 5, board, False)
bv.draw_board(board)
player.make_a_move(0, 5, 6, 5, board, False)
bv.draw_board(board)
player.make_a_move(0, 1, 0, 0, board, False)
bv.draw_board(board)
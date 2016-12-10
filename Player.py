# coding: utf-8
# Player Class
# Implements the basic set of strategies for any player like traversing the board and determining path choices, validating and processing moves, 
# changing dice orientation based on the rolls, capturing and eliminating opponent dices.
#

"""	************************************************************
* Name:			Vivek Pandey								*
* Project:		Duell Python								*
* Class:		CMPS 366									*
* Date:			12/10/2016									*
************************************************************ """

from copy import deepcopy
from Board import Board
from Notifications import Notifications

class Player:
    #Class Variables
    printStatus = True
    printNotifications = True

    #Default Constructor
    def __init__(self):
        self.pathChoice = 0
        self.multiplePathPossible = False
        self.tempStorage1 = 0
        self.tempStorage2 = 0
        self.counterRowsTraversed = 0
        self.counterColumnsTraversed = 0
        self.notifications = Notifications()

    """
    #
    # NEW SECTION: THESE FUNCTIONS CAN BE USED TO CHANGE STATES EITHER IN A TEMPORARY OR A PERMANENT GAME BOARD
    #
    """

    """ *********************************************************************
    Function Name: roll_up

    Purpose: To Roll up a dice by one row and change the appropriate dice & board values accordingly to reflect changes

    Parameters:
    dice, the dice to be moved (passed by ref)
    board, the board in context (passed by ref)

    Return Value: none

    Local Variables: none

    Assistance Received: none
    ********************************************************************* """
    # Does one up roll of the dice
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
            Player.printNotifications and self.notifications.msg_captured_an_opponent()
        
        board.set_square_resident_dice(dice.row, dice.column, dice)

    """ *********************************************************************
    Function Name: roll_down

    Purpose: To Roll down a dice by one row and change the appropriate dice & board values accordingly to reflect changes

    Parameters:
    dice, the dice to be moved (passed by ref)
    board, the board in context (passed by ref)

    Return Value: none

    Local Variables: none

    Assistance Received: none
    ********************************************************************* """
    # Does one down roll of the dice
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
            Player.printNotifications and self.notifications.msg_captured_an_opponent()
        
        board.set_square_resident_dice(dice.row, dice.column, dice)


    """ *********************************************************************
    Function Name: roll_left

    Purpose: To Roll left a dice by one column and change the appropriate dice & board values accordingly to reflect changes

    Parameters:
    dice, the dice to be moved (passed by ref)
    board, the board in context (passed by ref)

    Return Value: none

    Local Variables: none

    Assistance Received: none
    ********************************************************************* """
    # Does one left roll of the dice
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
            Player.printNotifications and self.notifications.msg_captured_an_opponent()
        
        board.set_square_resident_dice(dice.row, dice.column, dice)


    """ *********************************************************************
    Function Name: roll_right

    Purpose: To Roll right a dice by one column and change the appropriate dice & board values accordingly to reflect changes

    Parameters:
    dice, the dice to be moved (passed by ref)
    board, the board in context (passed by ref)

    Return Value: none

    Local Variables: none

    Assistance Received: none
    ********************************************************************* """
    # Does one right roll of the dice
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
            Player.printNotifications and self.notifications.msg_captured_an_opponent()
        
        board.set_square_resident_dice(dice.row, dice.column, dice)
    
    """
    #
    # NEW SECTION: THE FOLLOWING FUNCTIONS WILL FORM TEMPORARY PASSED-BY-VALUE GAME OBJECTS AND CHECK THE VALIDITY OF ROUTE/DESTINATION
    #
    """

    """ *********************************************************************
    Function Name: is_valid_destination

    Purpose: To check if the given square is a valid destination distance-wise for the given dice

    Parameters:
    origin, the dice as the origin
    dest, the destination square

    Return Value: true if a valid destination, false if not

    Local Variables: none

    Assistance Received: none
    ********************************************************************* """
    # Checks if the destination is a valid one
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
                Player.printNotifications and self.notifications.msg_invalid_move()
        else:
            Player.printNotifications and self.notifications.msg_running_over_own_dice()
        return False

    """ *********************************************************************
    Function Name: is_path_valid
    Purpose: To find an appropriate path, if exists, between the origin and destination
            It sets the pathChoice varible with the proper path number
            1 for vertical & lateral, 2 for lateral & vertical, 3 for vertical only, 4 for lateral only

    Parameters:
    origin, the dice as the origin
    dest, the destination square
    gameBoard, the board in context

    Return Value: true if a path exists, false if not

    Local Variables: none

    Assistance Received: none
    ********************************************************************* """
    # Checks the validity of a path to get from origin to destination square
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
            if (self.traversed_columns_without_blockade(dice, destination, board) and self.traversed_rows_without_blockade(dice, destination, board)):
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
            Player.printNotifications and self.notifications.msg_no_valid_path()
            return False

        """CASE 2
        If only the rows change in destination, it means this is a frontal/backward move attempt
        ONE possible path"""
        if (dice.row != destination.row):
            if (self.traversed_rows_without_blockade(dice, destination, board)):
                self.pathChoice = 3
                return True
            else:
                Player.printNotifications and self.notifications.msg_no_valid_path()
                return False

        """CASE 3
        If only the column change, it means this is a lateral move attempt
        ONE possible path"""
        if (dice.column != destination.column):
            if (self.traversed_columns_without_blockade(dice, destination, board)):
                self.pathChoice = 4
                return True
            else:
                Player.printNotifications and self.notifications.msg_no_valid_path()
                return False
        
        #If moving from and to the current location, still true lol
        return True

    """ *********************************************************************
    Function Name: traversed_rows_without_blockade

    Purpose: To traverse rows and make sure blockade don't exist
            Used in conjunction with is_path_valid() function.
            The passed by reference values are actually the temporary values passed by value in is_path_valid() function

    Parameters:
    The passed by reference values are actually the temporary values passed by value in is_path_valid() function
    dice, the dice as the origin
    dest, the destination square
    gameBoard, the board in context

    Return Value: true if traversal along rows successful without blockade, false otherwise

    Local Variables: none

    Assistance Received: none
    ********************************************************************* """
    # Returns true if traversal is successful without blockade until the destination row (The passed by reference dice is actually a temporary dice itself)
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
    
    """ *********************************************************************
    Function Name: traversed_columns_without_blockade

    Purpose: To traverse columns and make sure blockade don't exist
            Used in conjunction with is_path_valid() function.
            The passed by reference values are actually the temporary values passed by value in is_path_valid() function

    Parameters:
    The passed by reference values are actually the temporary values passed by value in IsPathValid() function
    dice, the dice as the origin
    dest, the destination square
    gameBoard, the board in context

    Return Value: true if traversal along columns successful without blockade, false otherwise

    Local Variables: none

    Assistance Received: none
    ********************************************************************* """
    # Returns true if traversal is successful without blockade until the destination column (The passed by reference dice is actually a temporary dice itself)
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

    """
    #
    # NEW SECTION: THE FOLLOWING FUNCTIONS WILL ACTUALLY MODIFY THE REAL GAMEBOARD.
    #
    """

    """ *********************************************************************
    Function Name: make_a_move

    Purpose: To validate the move from and to the given coordinates, and process it if valid

    Parameters:
    startRow, integer value of start row coordinate
    startCol, integer value of start column coordinate
    endRow, integer value of end row coordinate
    endCol, integer value of end Column coordinate
    board, the board in context where the move is to be made (passed by ref)
    helpModeOn, boolean value determining whether the function is being called by Help Mode to act accordingly
    path, the path selected by the human player in case of a 90 degree turn, if any

    Return Value: true if move successful, false otherwise

    Local Variables:
    topValueAtStart, the top value of the dice at starting coordinate
    rightValueAtStart, the right value of the dice at starting coordinate

    Assistance Received: none
    ********************************************************************* """
    # Checks the validity of a given move, and performs it on the gameboard if valid
    def make_a_move(self, startRow, startCol, endRow, endCol, board, helpModeOn, path=0):
        """Check if destination is valid, then if path is valid
        Then, either make the move or log an error
        This can be used for both human or computer after verifying that they are moving their own players.
        Path 1 and 2 need to offset the changes done by the first function, and hence the startRow/startCol has a counter added in the second function"""
        if (self.is_valid_destination(board.get_square_resident(startRow, startCol), board.get_square_at_location(endRow, endCol))):
            if (self.is_path_valid(board.get_square_resident(startRow, startCol), board.get_square_at_location(endRow, endCol), board)):
                #If help mode is on, no need to make the actual move, return true here and print suggestion
                if (helpModeOn):
                    self.notifications.msg_helpmode_recommended_move(startRow + 1, startCol + 1, endRow + 1, endCol + 1, self.pathChoice)
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
                        Player.printNotifications and self.notifications.msg_90degree_path_selection_not_processed()
                
                #Start the rolls

                #First Vertically, a 90 degree turn, then laterally
                if (self.pathChoice == 1):
                    self.keep_rolling_vertically(board.get_square_resident(startRow, startCol), board.get_square_at_location(endRow, endCol), board)
                    self.keep_rolling_laterally(board.get_square_resident(startRow + self.counterRowsTraversed, startCol), board.get_square_at_location(endRow, endCol), board)
                    self.notifications.msg_nature_of_path_taken("VERTICAL & LATERAL")

                #First Laterally, a 90 degree turn, then vertically
                elif (self.pathChoice == 2):
                    self.keep_rolling_laterally(board.get_square_resident(startRow, startCol), board.get_square_at_location(endRow, endCol), board)
                    self.keep_rolling_vertically(board.get_square_resident(startRow, startCol + self.counterColumnsTraversed), board.get_square_at_location(endRow, endCol), board)
                    self.notifications.msg_nature_of_path_taken("LATERAL & VERTICAL")

                #Vertically only
                elif (self.pathChoice == 3):
                    self.keep_rolling_vertically(board.get_square_resident(startRow, startCol), board.get_square_at_location(endRow, endCol), board)
                    self.notifications.msg_nature_of_path_taken("VERTICAL")

                #Laterally only
                elif (self.pathChoice == 4):
                    self.keep_rolling_laterally(board.get_square_resident(startRow, startCol), board.get_square_at_location(endRow, endCol), board)
                    self.notifications.msg_nature_of_path_taken("LATERAL")

                else:
                    Player.printNotifications and self.notifications.msg_crashed_while_making_the_move()
                    return False
                
                self.notifications.msg_move_description(startRow + 1, startCol + 1, endRow + 1, endCol + 1, topValueAtStart, rightValueAtStart, board.get_square_resident(endRow, endCol).top, board.get_square_resident(endRow, endCol).right, board.get_square_resident(endRow, endCol).botOperated)	# +1 To compensate for 1 offset in the array indexes
                return True
        return False

    #These two following functions will modify the actual gameboard. So pass the real game objects
    # Make sure you check the validity of the path beforehand. Cause they won't do the checking

    """ *********************************************************************
    Function Name: keep_rolling_vertically

    Purpose: To continue the move vertically until the dice reaches the destination row
            Used in conjunction with the make_a_move() function
            This modifies the actually gameboard in context, so be careful while using it

    Parameters:
    dice, the dice of origin
    destination, the destination square to be reached
    board, the board in context (will be modified permanently)

    Return Value: none

    Local Variables: none

    Assistance Received: none
    ********************************************************************* """
    # Rolls the dice vertically until it is in the destination row
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
    

    """ *********************************************************************
    Function Name: keep_rolling_laterally

    Purpose: To continue the move laterally until the dice reaches the destination column
    Used in conjunction with the make_a_move() function
    This modifies the actually gameboard in context, so be careful while using it

    Parameters:
    dice, the dice of origin
    destination, the destination square to be reached
    board, the board in context (will be modified permanently)

    Return Value: none

    Local Variables: none

    Assistance Received: none
    ********************************************************************* """
    # Rolls the die laterally until it is in the destination column
    def keep_rolling_laterally(self, dice, destination, board):
        self.counterColumnsTraversed = 0
        while True:
            if (dice.column < destination.column):
                self.roll_right(dice, board)
                self.counterColumnsTraversed += 1
            else:
                self.roll_left(dice, board)
                self.counterColumnsTraversed -= 1

            if(dice.column == destination.column):
                break

# coding: utf-8
# Computer Class
# Implements Computer strategies to evaluate, prioritize, select and initiate the best move on behalf of the computer.
#

"""	************************************************************
* Name:			Vivek Pandey								*
* Project:		Duell Python								*
* Class:		CMPS 366									*
* Date:			12/10/2016									*
************************************************************ """

from copy import deepcopy
from Player import Player
from Board import Board
from Notifications import Notifications

class Computer(Player):
    #Default Constructor
    def __init__(self):
        Player.__init__(self)
        self.TEAMSIZE = 9
        self.helpModeOn = False
        self.ownDiceList = None
        self.opponentDiceList = None
        self.ownKingSquare = None
        self.ownKeySquare = None
        self.opponentKingSquare = None
        self.opponentKeySquare = None
        self.notifications = Notifications()
    
    """ *********************************************************************
    Function Name: play

    Purpose: Calculate the best move on behalf of the Computer Player and process the move

    Parameters: 
    board, the current state of the board where the move needs to be made
    helpModeOn, Boolean value to determine whether the function call is made by human under help mode

    Return Value: true if a move is made successfully, false if no move made

    Local Variables: 
    calculationBoard, a copy of current board to use for move calculation purposes
    ownKingSquare, a copy of the king square of the calling team
    ownKeySquare, a copy of the key square of the calling team
    opponentKingSquare, a copy of king square of passive team
    opponentKeySquare, a copy of key square of passive team
    index & jindex, counter for loops
    bestMoveCoordinates, list to store start and end coordinates of the best move calculated so far
    minDistance, integer to store the minimum distance of a move so far
    distanceFromFinalDestination,  integer to store the distance from key pieces in current calculated move

    Assistance Received: none
    ********************************************************************* """
    #Prioritizes, calculates and makes proper move for Computer on its turn
    def play(self, board, helpModeOn):
        self.helpModeOn = helpModeOn
        Player.printNotifications = False

        #Moving contents to a temporary board to prevent unintentional modification of actual gameboard during calculations
        calculationBoard = deepcopy(board)
        
        #If help mode on, the algorithm will work favorably for human and against the Computer
        if (self.helpModeOn):
            #Setting Human as the owner and bot as the opponent
            self.ownDiceList = deepcopy(calculationBoard.humans)
            self.opponentDiceList = deepcopy(calculationBoard.bots)
            self.ownKingSquare = deepcopy(calculationBoard.get_square_at_location(calculationBoard.get_human_king().row, calculationBoard.get_human_king().column))
            self.ownKeySquare = deepcopy(calculationBoard.get_square_at_location(0, 4))
            self.opponentKingSquare = deepcopy(calculationBoard.get_square_at_location(calculationBoard.get_bot_king().row, calculationBoard.get_bot_king().column))
            self.opponentKeySquare = deepcopy(calculationBoard.get_square_at_location(7, 4))
        else:
            #Setting Bot as the owner and human as the opponent
            self.ownDiceList = deepcopy(calculationBoard.bots)
            self.opponentDiceList = deepcopy(calculationBoard.humans)
            self.ownKingSquare = deepcopy(calculationBoard.get_square_at_location(calculationBoard.get_bot_king().row, calculationBoard.get_bot_king().column))
            self.ownKeySquare = deepcopy(calculationBoard.get_square_at_location(7, 4))
            self.opponentKingSquare = deepcopy(calculationBoard.get_square_at_location(calculationBoard.get_human_king().row, calculationBoard.get_human_king().column))
            self.opponentKeySquare = deepcopy(calculationBoard.get_square_at_location(0, 4))

        self.notifications.botsthink_trying_to_capture_opponentkeys()
        #STEP 1: Check if the opponent's king or key square can be captured. If yes, go for it
        for index in range(0, self.TEAMSIZE):
            if (not self.ownDiceList[index].captured):
                #Try to capture the king die
                if (Player.make_a_move(self, self.ownDiceList[index].row, self.ownDiceList[index].column, self.opponentKingSquare.row, self.opponentKingSquare.column, board, self.helpModeOn, 0)):
                    return True
                #Try to capture the key square by the king die
                if (self.ownDiceList[index].king):
                    if (Player.make_a_move(self, self.ownDiceList[index].row, self.ownDiceList[index].column, self.opponentKeySquare.row, self.opponentKeySquare.column, board, self.helpModeOn, 0)):
                        return True

        self.notifications.botsthink_checking_king_keysquare_safety()
        #STEP 2: Check if own king or keysquare is under potential attack. If yes, Save em
        for index in range(0, self.TEAMSIZE):
            if (not self.opponentDiceList[index].captured):
                #If both kingSquare and keySquare are under threat, then blocking is the best way to go about iter

                #Check if kingSquare is under imminent threat
                if (Player.is_valid_destination(self, self.opponentDiceList[index], self.ownKingSquare)):
                    if (Player.is_path_valid(self, self.opponentDiceList[index], self.ownKingSquare, calculationBoard)):
                        #King is under imminent threat
                        self.notifications.botsthink_keythreat_detected("King")

                        #First, try capturing the hostile opponent
                        if (self.try_capturing_the_hostile_opponent(self.opponentDiceList[index], board)):
                            not self.helpModeOn and self.notifications.botsthink_hostile_opponent_captured("King")
                            return True
                        else:
                            self.notifications.botsthink_hostile_opponent_uncapturable("King")

                        #Second, try blocking the hostile opponent
                        if (self.try_blocking_attack(self.opponentDiceList[index], self.ownKingSquare, board)):
                            not self.helpModeOn and self.notifications.botsthink_blocking_move_made()
                            return True
                        else:
                            self.notifications.botsthink_blocking_move_not_possible()
                        
                        #Third, try moving the king as a last resort and make sure the new position is safe
                        if (self.try_moving_king(self.ownKingSquare, board)):
                            not self.helpModeOn and self.notifications.botsthink_king_moved()
                            return True
                        else:
                            self.notifications.botsthink_unsafe_to_move_king()
                        
        
        """SAFETY OF THE KEY SQUARE HAS BEEN TAKEN CARE IN ABOVE STEPS ALREADY
        Opponent king is the only threat to the key square and capture of opponent king has already been tried above,
        Blocking the hostile king can't really be done since it will be right next to the keysquare if a threat"""

        """STEP 3: Try to capture any vulnerable opponent dice in the game board
        We will not send king to capture opponents to make sure king is safe from opponent's trap
        king will only capture opponent king which is faciliated above"""
        
        self.notifications.botsthink_trying_to_capture_opponent_dice()
        for index in range(0, self.TEAMSIZE):
            #Use the die to hunt only if it is not a king and hasn't been captured yet
            if (not self.ownDiceList[index].king and not self.ownDiceList[index].captured):
                for jindex in range (0, self.TEAMSIZE):
                    if (not self.opponentDiceList[jindex].captured):
                        if (Player.make_a_move(self, self.ownDiceList[index].row, self.ownDiceList[index].column, self.opponentDiceList[jindex].row, self.opponentDiceList[jindex].column, board, self.helpModeOn, 0)):
                            not self.helpModeOn and self.notifications.botsthink_captured_opponent_dice()
                            return True


        #STEP 4: Protect any own dice that might be potentially captured by the opponent in the next step
        self.notifications.botsthink_protect_dices_from_potential_captures()
        # For all uncaptured opponent dice
        for index in range (0, self.TEAMSIZE):
            if (not self.opponentDiceList[index].captured):
                #Go through all of own uncaptured dice and check chances of hostile takeover
                for counter in range (0, self.TEAMSIZE):
                    if (not self.ownDiceList[counter].captured):
                        if (Player.is_valid_destination(self, self.opponentDiceList[index], calculationBoard.get_square_at_location(self.ownDiceList[counter].row, self.ownDiceList[counter].column))):
                            if (Player.is_path_valid(self, self.opponentDiceList[index], calculationBoard.get_square_at_location(self.ownDiceList[counter].row, self.ownDiceList[counter].column), calculationBoard)):
                                if (self.protect_the_dice(calculationBoard.get_square_at_location(self.ownDiceList[counter].row, self.ownDiceList[counter].column), board)):
                                    return True


        #STEP 5: Go through the remaining possibilities and move a die with intentions of getting it closer to the king or key square
        #Variables to store the best combination of origin and destination coordinates for a move, and also the minDistance that has been attained
        minDistance = 99
        distanceFromFinalDestination = 99
        bestMoveCoordinates = []

        self.notifications.botsthink_searching_ordinary_move()
        #For each of the die, go through every square in the gamboard and find the most optimal square to move in current state
        for index in range(0, self.TEAMSIZE):
            if(not self.ownDiceList[index].king and not self.ownDiceList[index].captured):        #For every uncaptured soldier die
                for row in range(0, 8):                                               #Go through the entire board and                                                                                   
                    for col in range(0, 9):
                        if (Player.is_valid_destination(self, self.ownDiceList[index], calculationBoard.get_square_at_location(row, col))):        #Check if valid dest
                            if (Player.is_path_valid(self, self.ownDiceList[index], calculationBoard.get_square_at_location(row, col), board)):    #Check if valid path
                                if (not self.is_in_danger(board.get_square_at_location(row, col), board)):                              #Check if safe
                                    #Compare distance to get to the king square from new location
                                    distanceFromFinalDestination = abs(self.opponentKingSquare.row - row) + abs(self.opponentKingSquare.column - col)
                                    if (distanceFromFinalDestination < minDistance):                                            #Check if distance to king becomes minimum and assign
                                        minDistance = distanceFromFinalDestination
                                        bestMoveCoordinates = [self.ownDiceList[index].row, self.ownDiceList[index].column, row, col]     #Stored in format startRow, startCol, endRow, endCol

                                    #Compare distance to get to the key square from new location
                                    distanceFromFinalDestination = abs(self.opponentKeySquare.row - row) + abs(self.opponentKeySquare.column - col)
                                    if (distanceFromFinalDestination < minDistance):                                            #Check if distance to key becomes minimum and assign
                                        minDistance = distanceFromFinalDestination
                                        bestMoveCoordinates = [self.ownDiceList[index].row, self.ownDiceList[index].column, row, col]     #Stored in format startRow, startCol, endRow, endCol
        
        #If a better path was found from the above intensive checking
        if (minDistance < 99):
            if (Player.make_a_move(self, bestMoveCoordinates[0], bestMoveCoordinates[1], bestMoveCoordinates[2], bestMoveCoordinates[3], board, self.helpModeOn, 0)):
                return True
        
        #It won't ever come to this, but return true anyway lol
        return True
    

    """ *********************************************************************
    Function Name: try_blocking_attack

    Purpose: To attempt to make a blocking move on a hostile dice

    Parameters:
    hostileOne, a Dice object that needs to be blocked
    victim, the square to be protected from hostile dice
    board, the board where the blocking needs to be done (passed by ref)

    Return Value: true if blocking move successful, false if unsuccessful

    Local Variables:
    path, integer to store the potential path that will be used by the hostile dice to get to squareToProtect

    Assistance Received: none
    ********************************************************************* """
    # Attempts to block the path of an opponent who is a potential threat
    def try_blocking_attack(self, hostileOne, victim, board):
        #Duplicating some function params to prevent the modification of original ReferenceError
        hostileDice = deepcopy(hostileOne)
        squareToProtect = deepcopy(victim)

        #Get the path choice first
        Player.is_path_valid(self, hostileDice, squareToProtect, board)
        path = self.pathChoice

        #Then based on that path, check which coordinate is best suited to jam the route
        #First vertically, a 90 degree turn, then laterally
        if (path == 1):
            if (self.find_block_point_vertically(hostileDice, squareToProtect, board)):
                return True
            if (self.find_block_point_laterally(hostileDice, squareToProtect, board)):
                return True
        
        #First laterally, a 90 degree turn, then vertically
        elif (path == 2):
            if (self.find_block_point_laterally(hostileDice, squareToProtect, board)):
                return True
            if (self.find_block_point_vertically(hostileDice, squareToProtect, board)):
                return True
        
        #Vertically only
        elif (path == 3):
            if (self.find_block_point_vertically(hostileDice, squareToProtect, board)):
                return True

        #Laterally only
        elif (path == 4):
            if (self.find_block_point_laterally(hostileDice, squareToProtect, board)):
                return True
        
        #No path found
        else:
            return False

    
    """ *********************************************************************
    Function Name: find_block_point_vertically

    Purpose: To Find a block point in vertical direction to block a hostile dice
            Called in conjunction with above try_blocking_attack() function

    Parameters:
    Normally Passed by reference from the above function of TryBlockingAttack
    hostileDice, a Dice object that needs to be blocked (passed by ref)
    squareToProtect, the square to be protected from hostile dice (passed by ref)
    board, the board where the blocking needs to be done (passed by ref)

    Return Value: true if blocking successful, false if unsuccessful

    Local Variables: none

    Assistance Received: none
    ********************************************************************* """
    # Finds a co-ordinate to place blocking dice on the vertical route
    def find_block_point_vertically(self, hostileDice, squareToProtect, board):
        while True:
            #Bump up/down the coordinates to check first
            if (hostileDice.row < squareToProtect.row):
                hostileDice.row = hostileDice.row + 1
            else:
                hostileDice.row = hostileDice.row - 1

            #See if any of the own dies can take that spot and block
            for i in range(0, self.TEAMSIZE):
                if (not self.ownDiceList[i].king and not self.ownDiceList[i].captured):
                    if (Player.make_a_move(self, self.ownDiceList[i].row, self.ownDiceList[i].column, hostileDice.row, hostileDice.column, board, self.helpModeOn, 0)):
                        return True

            #Condition to break while loop
            if (hostileDice.row == squareToProtect.row):
                break
        
        #If it can't find a block point even after traversing through all the legal rows, return False
        return False


    """ *********************************************************************
    Function Name: find_block_point_laterally

    Purpose: To Find a block point in lateral direction to block a hostile dice
    Called in conjunction with above try_blocking_attack() function

    Parameters:
    Normally Passed by reference from the above function of TryBlockingAttack
    hostileDice, a Dice object that needs to be blocked (passed by ref)
    squareToProtect, the square to be protected from hostile dice (passed by ref)
    board, the board where the blocking needs to be done (passed by ref)

    Return Value: true if blocking successful, false if unsuccessful

    Local Variables: none

    Assistance Received: none
    ********************************************************************* """
    # Finds a co-ordinate to place blocking dice on the lateral route
    def find_block_point_laterally(self, hostileDice, squareToProtect, board):
        while True:
            #Bump up/down the coordinates to check first
            if (hostileDice.column < squareToProtect.column):
                hostileDice.column = hostileDice.column + 1
            else:
                hostileDice.column = hostileDice.column - 1

            #See if any of the own dies can take that spot and block
            for i in range(0, self.TEAMSIZE):
                if (not self.ownDiceList[i].king and not self.ownDiceList[i].captured):
                    if (Player.make_a_move(self, self.ownDiceList[i].row, self.ownDiceList[i].column, hostileDice.row, hostileDice.column, board, self.helpModeOn, 0)):
                        return True

            #Condition to break while loop
            if (hostileDice.column == squareToProtect.column):
                break
        
        #If it can't find a block point even after traversing through all the legal columns, return False
        return False

    """ *********************************************************************
    Function Name: try_capturing_the_hostile_opponent

    Purpose: To try and capture a hostile opponent

    Parameters:
    hostileOne, the hostile dice that needs to be captured
    board, the game board in context (passed by ref)

    Return Value: true if capture successful, false if unsuccessful

    Local Variables: none

    Assistance Received: none
    ********************************************************************* """
    # Tries capturing a hostile opponent who is a potential threat
    def try_capturing_the_hostile_opponent(self, hostileOne, board):
        #Duplicating function params to prevent modification of the original params
        hostileDice = deepcopy(hostileOne)

        for i in range(0, self.TEAMSIZE):
            if (not self.ownDiceList[i].captured):
                #try to capture the hostile die
                if (Player.make_a_move(self, self.ownDiceList[i].row, self.ownDiceList[i].column, hostileDice.row, hostileDice.column, board, self.helpModeOn, 0)):
                    return True
        
        return False
    
    """ *********************************************************************
    Function Name: try_moving_king

    Purpose: To move the king to protect from opponent attack

    Parameters:
    king, the square where the king is located
    board, the game board in context

    Return Value: true if the move successful, false if unsuccessful

    Local Variables: none

    Assistance Received: none
    ********************************************************************* """
    # Tries moving the king to a secure position
    def try_moving_king(self, king, board):
        kingSquare = deepcopy(king)

        #Check if it is possible/safe to move the king upwards in the board
        if (kingSquare.row < 7):
            if (Player.is_valid_destination(self, kingSquare.resident, board.get_square_at_location(kingSquare.row + 1, kingSquare.column))):
                if (not self.is_in_danger(board.get_square_at_location(kingSquare.row + 1, kingSquare.column), board)):
                    if (Player.make_a_move(self, kingSquare.row, kingSquare.column, kingSquare.row + 1, kingSquare.column, board, self.helpModeOn, 0)):
                        return True

        #Check if it is possible/safe to move the king downwards in the board
        if (kingSquare.row > 0):
            if (Player.is_valid_destination(self, kingSquare.resident, board.get_square_at_location(kingSquare.row - 1, kingSquare.column))):
                if (not self.is_in_danger(board.get_square_at_location(kingSquare.row - 1, kingSquare.column), board)):
                    if (Player.make_a_move(self, kingSquare.row, kingSquare.column, kingSquare.row - 1, kingSquare.column, board, self.helpModeOn, 0)):
                        return True

        #Check if it is possible/safe to move the king rightwards in the board
        if (kingSquare.column < 8):
            if (Player.is_valid_destination(self, kingSquare.resident, board.get_square_at_location(kingSquare.row, kingSquare.column + 1))):
                if (not self.is_in_danger(board.get_square_at_location(kingSquare.row, kingSquare.column + 1), board)):
                    if (Player.make_a_move(self, kingSquare.row, kingSquare.column, kingSquare.row, kingSquare.column + 1, board, self.helpModeOn, 0)):
                        return True

        #Check if it is possible/safe to move the king leftwards in the board
        if (kingSquare.column > 0):
            if (Player.is_valid_destination(self, kingSquare.resident, board.get_square_at_location(kingSquare.row, kingSquare.column - 1))):
                if (not self.is_in_danger(board.get_square_at_location(kingSquare.row, kingSquare.column - 1), board)):
                    if (Player.make_a_move(self, kingSquare.row, kingSquare.column, kingSquare.row, kingSquare.column - 1, board, self.helpModeOn, 0)):
                        return True

        return False
    
    """ *********************************************************************
    Function Name: protect_the_dice

    Purpose: To move a dice under threat to a safe location

    Parameters:
    potentialVictim, the square that needs to be moved to a safe location
    board, the game board in context (passed by ref)

    Return Value: true if move successful, false if unsuccessful

    Local Variables: none

    Assistance Received: none
    ********************************************************************* """
    # Tries protecting a dice under threat
    def protect_the_dice(self, potentialVictim, board):
        #Making duplicate copies of necessary function params for modification
        squareAtRisk = deepcopy(potentialVictim)

        #Go through the entire game board, find a location where the squareAtRisk will be safe and move it there
        for row in range(0, 8):
            for col in range(0, 9):
                if (Player.is_valid_destination(self, squareAtRisk.resident, board.get_square_at_location(row, col))):
                    if (Player.is_path_valid(self, squareAtRisk.resident, board.get_square_at_location(row, col), board)):
                        if (not self.is_in_danger(board.get_square_at_location(row, col), board)):
                            if (Player.make_a_move(self, squareAtRisk.row, squareAtRisk.column, row, col, board, self.helpModeOn, 0)):
                                return True
        
        return False
    
    """ *********************************************************************
    Function Name: is_in_danger

    Purpose: To check and see if the given square is at risk in the given gameboard

    Parameters:
    potentialVictim, the square that needs to be checked if it is in danger
    gameBoard, the game board in context

    Return Value: true if square at risk, false if safe

    Local Variables: none

    Assistance Received: none
    ********************************************************************* """
    # Checks if a given square is at risk from opponent dices
    def is_in_danger(self, potentialVictim, gameBoard):
        #Making duplicate copies of function params that were supposed to be passed by Value 
        squareAtRisk = deepcopy(potentialVictim)
        board = deepcopy(gameBoard)

        for index in range(0, self.TEAMSIZE):
            #This even considers threat from the king and just not normal soldier attacks
            if (not self.opponentDiceList[index].captured):
                if (Player.is_valid_destination(self, self.opponentDiceList[index], squareAtRisk)):
                    if (Player.is_path_valid(self, self.opponentDiceList[index], squareAtRisk, board)):
                        return True
        
        return False



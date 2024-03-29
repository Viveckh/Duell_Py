
# coding: utf-8
# Game Class
# Implements the necessary details to run a game like conducting initial toss, getting user input for moves, displaying updated game board and turn notifications.
#

"""	************************************************************
* Name:			Vivek Pandey								*
* Project:		Duell Python								*
* Class:		CMPS 366									*
* Date:			12/10/2016									*
************************************************************ """

from msvcrt import getche
from random import randint

from Board import Board
from BoardView import BoardView
from Computer import Computer
from Human import Human
from Notifications import Notifications

class Game:

    #Default Constructor
    def __init__(self):
        #GameBoard, display and notification objects
        self.board = Board()
        self.boardView = BoardView()
        self.notifications = Notifications()
        #Player objects
        self.human = Human()
        self.computer = Computer()
        #Toss Variables
        self.humanDieToss = 0
        self.computerDieToss = 0
        #Control variables
        self.humanTurn = False
        self.computerTurn = False
        #Variables to store user input of coordinates
        self.startRow = 0
        self.startCol = 0
        self.endRow = 0
        self.endCol = 0
        #1 for vertical first, 2 for lateral first
        self.path = 0

    """ *********************************************************************
    Function Name: implement_game

    Purpose: Runs a full game until someone wins or user requests serialization

    Parameters:
    restoringGame, boolean value stating whether a restore of previous game was requested by user
    nextPlayer, a string that contains who's turn is next (if restoring) (Computer or Human)

    Return Value: 'c' if bot wins, 'h' if human wins, 'S' if serialization requested during bot turn, 's' if serialization requested during human turn

    Local Variables: none

    Assistance Received: none
    ********************************************************************* """
    #Implements a Round.
    #Return value is 'h' for human winner, 'c' for computer winner, 'S' for serializing during computer's turn, 's' for serializing during human's turn
    def implement_game(self, restoringGame, nextPlayer=""):
        #Set the turns if restoring a game from saved state
        if restoringGame:
            if (nextPlayer == "Computer"):
                self.computerTurn = True
            if (nextPlayer == "Human"):
                self.humanTurn = True
        
        #Draw Initial Board
        self.boardView.draw_board(self.board)

        #Conduct a toss if the controls haven't been assigned while restoring 
        if (not self.humanTurn and not self.computerTurn):
            self.toss_to_begin()

        #Continue the loop until one of the king is captured, one of the key squares gets occupied or user chooses to serialize and quit
        while True:
            refresh = False
            #If it is computer's turn
            if self.computerTurn:
                self.notifications.msg_turns("COMPUTER'S TURN")
                if (self.computer.play(self.board, False)):
                    #Transfer Controls
                    self.computerTurn = False
                    self.humanTurn = True
                    self.notifications.msg_turns("BOARD AFTER COMPUTER'S MOVE")
                    refresh = True  #Using this boolean to prevent human's loop from running immediately
                else:
                    continue

            #If it is human's Turn
            if not refresh:
                if self.humanTurn:
                    self.notifications.msg_turns("YOUR TURN")
                    if self.turn_help_mode_on():
                        self.notifications.msg_helpmode_on()
                        #Calling computer Play in Help Mode
                        self.computer.play(self.board, True)

                    self.get_user_input()
                    if (self.human.play(self.startRow, self.startCol, self.endRow, self.endCol, self.board, self.path)):
                        self.humanTurn = False
                        self.computerTurn = True    #Transferring controls
                        self.notifications.msg_turns("BOARD AFTER HUMAN'S MOVE")
                    else:
                        self.notifications.msg_invalid_move()
                        continue
            
            #After the move is made
            #Re-draw the board after each move
            self.boardView.draw_board(self.board)

            #If game over condition met
            if(self.game_over_condition_met()):
                #Whoever just received the control is the one who lost
                if self.humanTurn:
                    self.notifications.msg_game_over("COMPUTER")
                    return 'c'  #Bot Winner
                else:
                    self.notifications.msg_game_over("HUMAN")
                    return 'h'  #Human Winner

            """Stop the game and return if user wants to serialize
            return 'S' if serializing during computer's turn, 's' if serializing during human's turn"""
            if self.user_wants_to_serialize():
                if self.computerTurn:
                    return 'S'
                if self.humanTurn:
                    return 's'
    
    
    """ *********************************************************************
    Function Name: turn_help_mode_on

    Purpose: Ask human player if they want to turn help mode on

    Parameters: none

    Return Value: true if user requests help mode, false otherwise

    Local Variables: none

    Assistance Received: none
    ********************************************************************* """
    # Receives user input on whether they want to turn on help mode
    def turn_help_mode_on(self):
        #Continue asking user for input until they press 'y' or 'n'
        while True:
            self.notifications.msg_help_mode_prompt()
            input = getche()
            if (input == 'y' or input == 'Y'):
                return True
            if (input == 'n' or input == 'N'):
                return False
            self.notifications.msg_improper_input()

    """ *********************************************************************
    Function Name: user_wants_to_serialize

    Purpose: Ask human player if they want to serialize

    Parameters: none

    Return Value: true if user requests serialization, false otherwise

    Local Variables: none

    Assistance Received: none
    ********************************************************************* """
    # Asks if user wants to serialize & returns true if user wants to serialize
    def user_wants_to_serialize(self):
        #Continue asking user for input until they press 'y' or 'n'
        while True:
            self.notifications.msg_serialize_prompt()
            input = getche()
            if (input == 'y' or input == 'Y'):
                return True
            if (input == 'n' or input == 'N'):
                return False
            self.notifications.msg_improper_input()
    
    """ *********************************************************************
    Function Name: game_over_condition_met

    Purpose: To check if the condition for game over has been met

    Parameters: none

    Return Value: true if condition met for game to be over, false otherwise

    Local Variables: none

    Assistance Received: none
    ********************************************************************* """
    # Checks if the condition to end the game has been met
    def game_over_condition_met(self):
        #If one of the kings captured
        if (self.board.get_human_king().captured or self.board.get_bot_king().captured):
            return True

        #If the human key square is occupied by the bots king die    
        if (self.board.get_square_resident(0, 4) != None):
            if (self.board.get_square_resident(0, 4).botOperated):
                if (self.board.get_square_resident(0, 4).king):
                    return True

        #If the computer key square is occupied by the Human king die
        if (self.board.get_square_resident(7, 4) != None):
            if (not self.board.get_square_resident(7, 4).botOperated):
                if (self.board.get_square_resident(7, 4).king):
                    return True

        #If none of the game over conditions are met
        return False
    
    """ *********************************************************************
    Function Name: get_user_input

    Purpose: To get user input for coordinates

    Parameters: none

    Return Value: none

    Local Variables: none

    Assistance Received: none
    ********************************************************************* """
    # Gets user input for coordinates if it is a human's turn
    def get_user_input(self):
        self.startRow = 0
        self.startCol = 0
        self.endRow = 0
        self.endCol = 0
        self.path = 0

        #Continue asking user for input until they press all the digits        
        #Ask for origin row
        while True:
            self.notifications.msg_enter_origin_row()
            input = getche()
            try:
                self.startRow = int(input)
                break
            except ValueError:
                self.notifications.msg_improper_input()
        
        #Ask for origin column
        while True:
            self.notifications.msg_enter_origin_column()
            input = getche()
            try:
                self.startCol = int(input)
                break
            except ValueError:
                self.notifications.msg_improper_input()
        
        #Ask for destination row
        while True:
            self.notifications.msg_enter_destination_row()
            input = getche()
            try:
                self.endRow = int(input)
                break
            except ValueError:
                self.notifications.msg_improper_input()

        #Ask for destination column
        while True:
            self.notifications.msg_enter_destination_column()
            input = getche()
            try:
                self.endCol = int(input)
                break
            except ValueError:
                self.notifications.msg_improper_input()

        #In case of a 90 degree turn, ask the path preference as well
        if ((self.startRow != self.endRow) and (self.startCol != self.endCol)):
            while True:
                self.notifications.msg_90degree_path_selection()
                input = getche()
                try:
                    if (int(input) == 1 or int(input) == 2):
                        self.path = int(input)
                        break
                except ValueError:
                    self.notifications.msg_improper_input()

    
    """ *********************************************************************
    Function Name: toss_to_begin

    Purpose: To conduct a toss and set the turn of appropriate player to true

    Parameters: none

    Return Value: none

    Local Variables: none

    Assistance Received: none
    ********************************************************************* """
    # Does a toss to determine which team will start the game
    def toss_to_begin(self):

        #Continue until both have different toss results
        while True:
            self.humanDieToss = randint(1, 6)
            self.computerDieToss = randint(1, 6)

            if (self.humanDieToss != self.computerDieToss):
                break

        #Whoever has the highest number on top - wins the toss
        if (self.humanDieToss > self.computerDieToss):
            self.humanTurn = True
            self.notifications.msg_toss_results("You", self.humanDieToss, self.computerDieToss)
        else:
            self.computerTurn = True
            self.notifications.msg_toss_results("Computer", self.humanDieToss, self.computerDieToss)



# coding: utf-8
# Tournament Class
# Runs a series of games, maintains the score for human and computer player, processes game serialization/restoration requests & declares winner.
#

"""	************************************************************
* Name:			Vivek Pandey								*
* Project:		Duell Python								*
* Class:		CMPS 366									*
* Date:			12/10/2016									*
************************************************************ """

from msvcrt import getche
from copy import deepcopy

from Game import Game
from Notifications import Notifications
from Serializer import Serializer
from Board import Board

class Tournament:

    #Default Constructor
    def __init__(self):
        #Serializer components
        self.serializer = Serializer()
        self.restoreFilePath = None

        #Tournament details
        self.humanScore = 0
        self.botScore = 0
        self.nextPlayer = None
        self.gameResult = None
        
        #Booleans for decision making
        self.quit = False
        self.restoringGame = False
        
        #Notifications purposes
        self.notifications = Notifications()

    """ *********************************************************************
    Function Name: play_tournament

    Purpose: Runs a series of games and maintains score until user serializes or quits

    Parameters: none

    Return Value: none

    Local Variables: none

    Assistance Received: none
    ********************************************************************* """
    # Runs a Tournament
    def play_tournament(self):
        #Ask user if they want to restore the tournament from existing file
        self.notifications.msg_restore_from_file()
        if self.wants_to_continue():
            self.restoringGame = True
            self.notifications.msg_enter_file_path()
            self.restoreFilePath = raw_input()

        #Start the tournament and keep going until user chooses to quit or serialize
        while True:
            #Implement a fresh game
            game = Game()

            #Modify the board and other tournament, game objects from serialization file here if one is provided
            if self.restoringGame:
                pkg = {}
                pkg['board'] = Board()
                pkg['botWins'] = None
                pkg['humanWins'] = None
                pkg['nextPlayer'] = None

                #Exit the game if restore failed
                if not self.serializer.read_from_file(self.restoreFilePath, pkg):
                    self.notifications.msg_serialized("FAILED")
                    return
                game.board = deepcopy(pkg['board'])
                self.botScore = pkg['botWins']
                self.humanScore = pkg['humanWins']
                self.nextPlayer = pkg['nextPlayer']

                self.gameResult = game.implement_game(self.restoringGame, self.nextPlayer)
                self.restoringGame = False
            else:
                self.gameResult = game.implement_game(self.restoringGame)

            #If a player has won the game
            if self.gameResult == 'h':
                self.humanScore += 1
            if self.gameResult == 'c':
                self.botScore += 1

            # 'S' refers to serialize during computer's turn and 's' refers to serialize during human's turn
            if (self.gameResult == 'S' or self.gameResult == 's'):
                self.serialize_game(game)
                return True
            
            #Ask if user wants to continue to next round
            self.notifications.msg_want_to_play_again()
            if not self.wants_to_continue():
                self.quit = True

            self.notifications.draw_divider()

            #If user chooses to quit, stop the tournament
            if self.quit:
                break

        #Displaying the tournament results
        self.notifications.msg_display_results(self.botScore, self.humanScore)


    """ *********************************************************************
    Function Name: serialize_game

    Purpose: Processes the serialization request from the human player

    Parameters: game, the current game object

    Return Value: none

    Local Variables: none

    Assistance Received: none
    ********************************************************************* """
    # Serializes a Tournament state
    def serialize_game(self, game):
        #Store the next player in a string
        if self.gameResult == 'S':
            self.nextPlayer = "Computer"        
        else:
            self.nextPlayer = "Human"

        #Write the serialized output to a file and exit
        if (self.serializer.write_to_file(game.board, self.botScore, self.humanScore, self.nextPlayer)):
            self.notifications.msg_serialized("SUCCESSFUL")
        else:
            self.notifications.msg_serialized("FAILED")

    """ *********************************************************************
    Function Name: wants_to_continue

    Purpose: To Ask user if they want to continue. At any given time

    Parameters: none

    Return Value: True if user picks yes, False otherwise

    Local Variables: none

    Assistance Received: none
    ********************************************************************* """
    # Gets user's choice on whether to continue to another round
    def wants_to_continue(self):
        #Continue asking user for input until they press 'y' or 'n'
        while True:
            input = getche()
            if (input == 'y' or input == 'Y'):
                return True
            if (input == 'n' or input == 'N'):
                return False

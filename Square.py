# coding: utf-8
# Square Class
# Stores and maintains the location and occupancy status of a square in the game board. A square can be occupied by a dice object only.
#

"""	************************************************************
* Name:			Vivek Pandey								*
* Project:		Duell Python								*
* Class:		CMPS 366									*
* Date:			12/10/2016									*
************************************************************ """

from Dice import Dice

class Square:
    #Default Constructor
    def __init__(self, row=None, column=None):
        self.row = row
        self.column = column
        self.resident = None
    
    #Sets the coordinates of the square in the board context. Pass row and column integers as parameters
    def set_coordinates(self, row, column):
        self.row = row
        self.column = column
        
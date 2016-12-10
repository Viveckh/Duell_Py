# coding: utf-8
# Dice Class
# Implements the properties of a dice object used in the game. 
# The class consists of variables and functions to store and modify a dice’s face values, its coordinates within a game board, 
# its controller (human or computer), its capture status, and whether it is a king. 
#

"""	************************************************************
* Name:			Vivek Pandey								*
* Project:		Duell Python								*
* Class:		CMPS 366									*
* Date:			12/10/2016									*
************************************************************ """

class Dice:
    #Class Variables
    SUM_OF_OPPOSITE_SIDES = 7
    counterClockwiseDiceOrder1 = (1, 2, 6, 5, 1, 2, 6, 5)
    counterClockwiseDiceOrder2 = (3, 1, 4, 6, 3, 1, 4, 6)
    counterClockwiseDiceOrder3 = (2, 3, 5, 4, 2, 3, 5, 4)

    #Default Constructor
    def __init__(self):
        
        self.row = 0
        self.column = 0
        self.top = 1
        self.left = 2
        self.rear = 3
        self.bottom = Dice.SUM_OF_OPPOSITE_SIDES - self.top
        self.right = Dice.SUM_OF_OPPOSITE_SIDES - self.left
        self.front = Dice.SUM_OF_OPPOSITE_SIDES - self.rear
        self.king = False
        self.botOperated = False
        self.captured = False

    """ *********************************************************************
    Function Name: set_beginning_orientation

    Purpose: To set the remaining sides of a dice based on known sides at the beginning of game
    
    Parameters:
    top, the top integer value of the dice
    isBot, boolean value stating if the dice is bot operated
    
    Return Value: none

    Local Variables: none besides loop counters

    Assistance Received: none
    ********************************************************************* """
    #Calculates & Sets the beginning orientation with face values of a dice in the home row
    def set_beginning_orientation(self, top, isBot):
        #Values given in program specs
        self.top = top
        self.bottom = Dice.SUM_OF_OPPOSITE_SIDES - self.top

        #Since the dice are arranged facing each other in two opposite directions
        if (isBot):
            self.front = 3
            self.rear = Dice.SUM_OF_OPPOSITE_SIDES - self.front
        else:
            self.rear = 3
            self.front = Dice.SUM_OF_OPPOSITE_SIDES - self.rear

        """"Since the given dice is oriented in a counterclockwise direction and 3 is always facing the rear,
	    the top-left-bottom-right values are always in some 1-2-6-5 order pattern.
	    This means, for a human, the left value is always next to the top value in the given 1-2-6-5 order.
        For a bot, the reverse is true, i.e. right value is always next to the top value in the 1-2-6-5 order. """

        #Searching through the counter clockwise dice pattern to find the top value
        for index in range(0, 4):
            #If index has the top value, index+1 will have the left value for human, and right value for a bottom
            if (Dice.counterClockwiseDiceOrder1[index] == top):
                if (isBot):
                    self.right = Dice.counterClockwiseDiceOrder1[index + 1]
                    self.left = Dice.SUM_OF_OPPOSITE_SIDES - self.right
                else:
                    self.left = Dice.counterClockwiseDiceOrder1[index + 1]
                    self.right = Dice.SUM_OF_OPPOSITE_SIDES - self.left


    """ *********************************************************************
    Function Name: set_remaining_sides

    Purpose: To set the remaining sides of a dice based on the known two (top-right for humans, top-left for bots)
    
    Parameters:
    arg1, the top value of dice
    arg2, the right value if a human dice, the left value if a bot dice
    
    Return Value: none
    
    Local Variables: none
    
    Assistance Received: had a discussion with Sujil Maharjan on how to approach this situation
    ********************************************************************* """
    #Calculates & Sets the remaining sides of a dice given the Top-left or Top-Right sides
    def set_remaining_sides(self, arg1, arg2):
        #The first parameter is the top, the second one can either be left (for computer) or right (for human)
        self.bottom = Dice.SUM_OF_OPPOSITE_SIDES - arg1

        #for computer the given arg2 is left whereas for human the given arg2 is right value
        if (self.botOperated):
            self.right = Dice.SUM_OF_OPPOSITE_SIDES - arg2
        else:
            self.left = Dice.SUM_OF_OPPOSITE_SIDES - arg2

        self.front = self.rear = 0  #resetting before calculating a new one

        """From this point, it doesn't matter whether it is human or computer die because both are saved in the model in the same way
        above we had to be careful to meet our model's specs because the computer's right given in the serialization file is actually left in our overall board model"""
        for index in range(0, 7):
            if (Dice.counterClockwiseDiceOrder1[index] == self.top and Dice.counterClockwiseDiceOrder1[index + 1] == self.right):
                #take higher out of the remaining two not in the array as the rear value
                self.rear = 4
                self.front = Dice.SUM_OF_OPPOSITE_SIDES - self.rear
                break

            if (Dice.counterClockwiseDiceOrder1[index] == self.right and Dice.counterClockwiseDiceOrder1[index + 1] == self.top):
                #take lower out of the remaining two not in the array as the rear value
                self.rear = 3
                self.front = Dice.SUM_OF_OPPOSITE_SIDES - self.rear
                break
            
            if (Dice.counterClockwiseDiceOrder2[index] == self.top and Dice.counterClockwiseDiceOrder2[index + 1] == self.right):
                #take higher out of the remaining two not in the array as the rear value
                self.rear = 5
                self.front = Dice.SUM_OF_OPPOSITE_SIDES - self.rear
                break

            if (Dice.counterClockwiseDiceOrder2[index] == self.right and Dice.counterClockwiseDiceOrder2[index + 1] == self.top):
                #take lower out of the remaining two not in the array as the rear value
                self.rear = 2
                self.front = Dice.SUM_OF_OPPOSITE_SIDES - self.rear
                break

            if (Dice.counterClockwiseDiceOrder3[index] == self.top and Dice.counterClockwiseDiceOrder3[index + 1] == self.right):
                #take higher out of the remaining two not in the array as the rear value
                self.rear = 6
                self.front = Dice.SUM_OF_OPPOSITE_SIDES - self.rear
                break

            if (Dice.counterClockwiseDiceOrder3[index] == self.right and Dice.counterClockwiseDiceOrder3[index + 1] == self.top):
                #take lower out of the remaining two not in the array as the rear value
                self.rear = 1
                self.front = Dice.SUM_OF_OPPOSITE_SIDES - self.rear
                break

    #Sets the values of faces if the given dice is a king. Pass True or False as function parameter
    def set_king(self, value):
        self.king = value
        if (value == True):
            self.top = self.bottom = self.front = self.rear = self.left = self.right = 1
    
    # Sets the dice coordinates. Pass integer value for row and column as parameters
    def set_coordinates(self, row, column):
        self.row = row
        self.column = column




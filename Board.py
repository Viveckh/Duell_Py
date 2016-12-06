from Dice import Dice
from Square import Square

class Board:
    ROWS = 8
    COLUMNS = 9
    STARTING_TOP_VALUES_OF_DICES = (5, 1, 2, 6, 1, 6, 2, 1, 5)

    def __init__(self):
        #Declaring the player lists
        self.humans = [Dice]*Board.COLUMNS
        self.bots = [Dice for dice in range(0, Board.COLUMNS)]

        #Initializing and filling up values in the indexes in the player lists
        for index in range(0, Board.COLUMNS):
            self.humans[index] = Dice()
            self.bots[index] = Dice()
            if (index == 4):
                self.humans[index].set_king(True)
                self.bots[index].set_king(True)
            else:
                self.humans[index].set_beginning_orientation(Board.STARTING_TOP_VALUES_OF_DICES[index], False)
                self.bots[index].set_beginning_orientation(Board.STARTING_TOP_VALUES_OF_DICES[index], True)
        
        #Declaring and initializing the game board
        self.gameBoard = [[Square for x in range(0, Board.COLUMNS)] for y in range(0, Board.ROWS)]
        for currentRow in range (0, Board.ROWS):
            for currentCol in range (0, Board.COLUMNS):
                self.gameBoard[currentRow][currentCol] = Square()
                self.gameBoard[currentRow][currentCol].set_coordinates(currentRow, currentCol)

                #Humans Home row
                if (currentRow == 0):
                    self.gameBoard[currentRow][currentCol].resident = self.humans[currentCol]
                    self.humans[currentCol].set_coordinates(currentRow, currentCol)
                    self.humans[currentCol].botOperated = False
                
                #Computers Home row
                if (currentRow == 7):
                    self.gameBoard[currentRow][currentCol].resident = self.bots[currentCol]
                    self.bots[currentCol].set_coordinates(currentRow, currentCol)
                    self.bots[currentCol].botOperated = True

    #Gets square resident if rows and column coordinates within the board is given
    def get_square_resident(self, row, col):
        return self.gameBoard[row][col].resident

    #Gets square at a given location within the Board
    def get_square_at_location(self, row, col):
        return self.gameBoard[row][col]

    def get_human_king(self):
        return self.humans[4]

    def get_bot_king(self):
        return self.bots[4]
    
    #Sets square resident, dice can be null if the square has to be set vacant
    def set_square_resident_dice(self, row, col, dice):
        self.gameBoard[row][col].resident = dice

    #Sets square resident as captured or uncaptured based on the boolean value passed to the captured parameter
    def set_square_resident_captured(self, row, col, captured):
        self.gameBoard[row][col].resident.captured = captured

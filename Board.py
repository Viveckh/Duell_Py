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

    def get_square_resident(self, row, col):
            return self.gameBoard[row][col].resident
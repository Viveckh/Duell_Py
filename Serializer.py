import re
from Board import Board

class Serializer:
    ROWS = 8
    COLUMNS = 9

    def __init__(self):
        self.fileName = "C:/Duell_LastGameSerialization.txt"

        #Declaring and initializign the serialized game board
        self.serializedGameBoard = [[None for x in range(0, Serializer.COLUMNS)] for y in range(0, Serializer.ROWS)]
        for currentRow in range (0, Serializer.ROWS):
            for currentCol in range (0, Serializer.COLUMNS):
                self.serializedGameBoard[currentRow][currentCol] = None

    
    def write_to_file(self, board, botWins, humanWins, nextPlayer):
        #Update the multidimensional string array for serialization first
        self.update_serialized_board(board)
        
        try:
            #Opening the file
            loadFile = open(self.fileName, 'w')
            
            #Writing the contents of the board
            loadFile.write("Board\n")
            for currentRow in reversed(xrange(Serializer.ROWS)):
                for currentCol in range (0, Serializer.COLUMNS):
                    loadFile.write("%s\t" %(self.serializedGameBoard[currentRow][currentCol]))
                loadFile.write("\n")
            
            #Writing the number of wins and next Player
            loadFile.write("Computer Wins:\t%s\n" %(str(botWins)))
            loadFile.write("Human Wins:\t%s\n" %(str(humanWins)))
            loadFile.write("Next Player:\t%s\n" %(nextPlayer))
            loadFile.close()
            return True
        except:
            print "An error has occurred while writing to the file."
        return False

    #pkg is a dictionary object with entries of board, botWins, humanWins, nextPlayer
    def read_from_file(self, filepath, pkg):
        try:
            #Opening the file
            loadFile = open(filepath, 'r')

            #Step 1: Reading the line with the Board Text
            loadFile.readline()

            #Step 2: Reading the gameboard and populating the multidimensional string list
            #The topmost row in the file is actually the 8th row in the model, so read inverted
            for currentRow in reversed(xrange(Serializer.ROWS)):
                #Parse the board contents, one line at a time
                line = loadFile.readline()
                line = line.strip()     #Stripping from leading and trailing whitespaces
                listOfValues = line.split()     #Splits automatically on all whitespaces

                #Populate the row on the multidimensional string list
                for currentCol in range(0, Serializer.COLUMNS):
                    self.serializedGameBoard[currentRow][currentCol] = listOfValues[currentCol]
            
            #Set the board model
            self.set_board(pkg['board'])

            #Step 3: Reading the human and computer scores and the next player
            while True:
                line = loadFile.readline()
                #Break the reading loop if this is the end of file
                if line == "":
                    break
                
                #Continue if the line is not empty
                if line:
                    #Parse number of computer wins
                    if re.match("(\\s*)[Cc]omputer(\\s+)[Ww]ins(.*)", line):
                        pkg['botWins'] = int(re.sub("[\\D]", "", line))

                    #Parse number of human wins
                    if re.match("(\\s*)[Hh]uman(\\s+)[Ww]ins(.*)", line):
                        pkg['humanWins'] = int(re.sub("[\\D]", "", line))
                    
                    #Parse the next player
                    if re.match("(\\s*)[Nn]ext(\\s+)[Pp]layer(.*)", line):
                        if re.match("(.*):(.*)[Cc]omputer(.*)", line):
                            pkg['nextPlayer'] = "Computer"
                        else:
                            pkg['nextPlayer'] = "Human"
            
            #Closing file and returning
            loadFile.close()
            return True
        except:
            print "An error has occurred while reading the file. File Format not acceptable."
            return False

    def set_board(self, board):
        #This one is for going through the Human's player dices
        humanCount = 0
        botCount = 0

        #This one is for temporary purposes
        tempHumanIndex = 0
        tempBotIndex = 0

        #Go through every index of the serializedGameBoard list and update the actual game board
        for row in range(0, Serializer.ROWS):
            for col in range (0, Serializer.COLUMNS):
                board.set_square_resident_dice(row, col, None)
                cell = self.serializedGameBoard[row][col]

                #If the square is empty
                if (cell[0] == '0'):
                    continue

                #If the square is occupied by computer dice 
                if (cell[0] == 'C'):
                    #Check if the dice at hand is a king, and determine the index accordingly
                    if (cell[1] == '1' and cell[2] == '1'):
                        #it is the king, so assign the king index
                        tempBotIndex = 4
                    else:
                        tempBotIndex = botCount
    
                    #Setting bot properties
                    board.bots[tempBotIndex].botOperated = True
                    board.bots[tempBotIndex].captured = False
                    board.bots[tempBotIndex].set_coordinates(row, col)
                    board.bots[tempBotIndex].top = int(cell[1])
                    board.bots[tempBotIndex].left = int(cell[2])

                    if (board.bots[tempBotIndex].top == 1 and board.bots[tempBotIndex].left == 1):
                        board.bots[tempBotIndex].set_king(True)
                    else:
                        board.bots[tempBotIndex].set_remaining_sides(board.bots[tempBotIndex].top, board.bots[tempBotIndex].left)
                    
                    #Setting square properties
                    board.set_square_resident_dice(row, col, board.bots[tempBotIndex])

                    #Incrementing counts
                    if tempBotIndex != 4:
                        botCount += 1
                    if botCount == 4:   #This index is occupied for the king
                        botCount += 1
                    continue

                #If the square is occupied by Human dice 
                if (cell[0] == 'H'):
                    #Check if the dice at hand is a king, and determine the index accordingly
                    if (cell[1] == '1' and cell[2] == '1'):
                        #it is the king, so assign the king index
                        tempHumanIndex = 4
                    else:
                        tempHumanIndex = humanCount
    
                    #Setting human properties
                    board.humans[tempHumanIndex].botOperated = False
                    board.humans[tempHumanIndex].captured = False
                    board.humans[tempHumanIndex].set_coordinates(row, col)
                    board.humans[tempHumanIndex].top = int(cell[1])
                    board.humans[tempHumanIndex].right = int(cell[2])

                    if (board.humans[tempHumanIndex].top == 1 and board.humans[tempHumanIndex].right == 1):
                        board.humans[tempHumanIndex].set_king(True)
                    else:
                        board.humans[tempHumanIndex].set_remaining_sides(board.humans[tempHumanIndex].top, board.humans[tempHumanIndex].right)
                    
                    #Setting square properties
                    board.set_square_resident_dice(row, col, board.humans[tempHumanIndex])

                    #Incrementing counts
                    if tempHumanIndex != 4:
                        humanCount += 1
                    if humanCount == 4:   #This index is occupied for the king
                        humanCount += 1
                    continue

        # The dices not found are definitely captured, so set the flags
        while botCount != 9:
            if botCount != 4:
                board.bots[botCount].captured = True
            botCount += 1
        
        while humanCount != 9:
            if humanCount != 4:
                board.humans[humanCount].captured = True
            humanCount += 1


    def update_serialized_board(self, board):
        for row in reversed(xrange(Serializer.ROWS)):
            for col in range(0, Serializer.COLUMNS):
                self.serializedGameBoard[row][col] = "0"
                if (board.get_square_resident(row, col) != None):
                    #If the square is occupied by a bot
                    if (board.get_square_resident(row, col).botOperated):
                        self.serializedGameBoard[row][col] = "C"
                        #Append the top and left value of the occupying die
                        self.serializedGameBoard[row][col] += str(board.get_square_resident(row, col).top)
                        self.serializedGameBoard[row][col] += str(board.get_square_resident(row, col).left) #Since computer's left is the board's right
                    #If the square is occupied by a human
                    else:
                        self.serializedGameBoard[row][col] = "H"
                        #Append the top and left value of the occupying die
                        self.serializedGameBoard[row][col] += str(board.get_square_resident(row, col).top)
                        self.serializedGameBoard[row][col] += str(board.get_square_resident(row, col).right)

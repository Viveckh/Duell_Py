from Dice import Dice

class Square:
    def __init__(self, row=None, column=None):
        self.row = row
        self.column = column
        self.resident = None

    def set_coordinates(self, row, column):
        self.row = row
        self.column = column
        
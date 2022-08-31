"""
Sudoku Class for Sudoku backtracking algorithm
Date: 2022-08-14
"""


class Sudoku:
    """
    Sudoku class, containing methods to manipulate and check conditions on sudoku board

    Attributes:
    - board: (list) 2d array representing sudoku puzzle
    - blanks: (tuple) all xy pairs of empty squares in puzzle

    Methods:
    sudoku tests:
    - get_row(num): (set) gets all values in a given row/column/block (0-8)
    - get_column(num): (set)
    - get_block(num): (set) note: blocks are numbered 0-8 in order that you read
    NOTE: for uncertain squares (many possible values) the first value in list is used (most likely smallest)
    - is_solved(): (bool)

    getter methods:
    - get_blanks(): (tuple)
    - see_board(): (none)
    - get_board(): (list)
    - get_square(x, y): (str) if value is fixed or blank or (list) if square is filled

    setter methods:
    - set_square(x, y, values): (none) replaces a zero or list in the board with a list of possible values
    """

    def __init__(self, board):
        """
        class init function
        :param board: (str) len 81 string using only numerals 1-9 for values 0 for blanks to represent
        sudoku board from top left to bottom right (default order)
        """
        self.__board = []
        for i in range(9):
            self.__board.append(list(board[i * 9:i * 9 + 9]))
        # board is a 2d array (board[y][x])

        self.__blanks = []
        for y in range(9):
            for x in range(9):
                if self.__board[y][x] == '0':
                    self.__blanks.append((x, y))
        self.__blanks = tuple(self.__blanks)

    def get_board(self):
        return self.__board

    def see_board(self):
        """
        outputs the board in ascii art
        :return: (none)
        """
        print("+---+---+---+")
        for idx, val in enumerate(self.__board):
            row = val.copy()
            for jdx, elem in enumerate(row):
                if type(elem) is list:
                    row[jdx] = elem[0]
            row = ''.join(row)
            if idx == 3 or idx == 6:
                print("+---+---+---+")
            print(f"|{row[0:3]}|{row[3:6]}|{row[6:9]}|")
        print("+---+---+---+")

    def get_blanks(self):
        """
        returns xy coords of every blank square in default order
        :return: (list)
        """
        return self.__blanks

    def get_row(self, x):
        """
        gets all the different values present in a row
        :param x: (int) [0-8]
        :return: (set)
        """
        output = list(self.__board[x])
        for idx, val in enumerate(output):
            if type(val) is list:
                output[idx] = val[0]
        return {i for i in output if i != '0'}  # get rid of repeats and zeros

    def get_column(self, y):
        """
        :param y: (int) [0-8]
        :return: (set)
        """
        output = []
        for i in range(9):
            output.append(self.__board[i][y])

        for idx, val in enumerate(output):
            if type(val) is list:
                output[idx] = val[0]
        return {i for i in output if i != '0'}

    def get_block(self, x, y):
        """
        uses x and y values to find which block the coordinates are in
        then calls method to return all elements in the block
        :param x, y: (int) [0-8]
        :return: (set)
        """
        if y < 3:
            if x < 3:
                return self.get_block_from_number(0)
            elif x < 6:
                return self.get_block_from_number(1)
            else:
                return self.get_block_from_number(2)
        elif y < 6:
            if x < 3:
                return self.get_block_from_number(3)
            elif x < 6:
                return self.get_block_from_number(4)
            else:
                return self.get_block_from_number(5)
        else:
            if x < 3:
                return self.get_block_from_number(6)
            elif x < 6:
                return self.get_block_from_number(7)
            else:
                return self.get_block_from_number(8)

    def get_block_from_number(self, num):
        """
        adds values from a given block number to a set
        :param num: (int) [0-8]
        :return: (set)
        """
        output = []
        if num < 3:
            for i in range(3):
                for j in range(3):
                    output.append(self.__board[j][i + num * 3])
        elif num < 6:
            num -= 3
            for i in range(3):
                for j in range(3):
                    output.append(self.__board[j + 3][i + num * 3])
        else:
            num -= 6
            for i in range(3):
                for j in range(3):
                    output.append(self.__board[j + 6][i + num * 3])

        for idx, val in enumerate(output):
            if type(val) is list:
                output[idx] = val[0]
        return {i for i in output if i != '0'}

    def get_square(self, x, y):
        """
        :param x: (int) [0-8]
        :param y: (int) [0-8]
        :return: (str) OR (list)
        """
        return self.__board[y][x]

    def set_square(self, x, y, val):
        """
        :param x: (int) [0-8]
        :param y: (int) [0-8]
        :param val: (list) OR (str) OR (tuple)
        :return: (bool) success?
        """
        if self.__board[y][x] == '0' or type(self.__board[y][x]) is list:
            if type(val) is str and val != '0':
                return False
            self.__board[y][x] = list(val)
            return True
        else:
            return False

    def is_solved(self):
        for i in range(9):
            if len(self.get_row(i)) != 9 or len(self.get_column(i)) != 9 or len(self.get_block_from_number(i)) != 9:
                return False
        return True

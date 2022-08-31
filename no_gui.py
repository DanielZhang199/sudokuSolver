"""
Sudoku solver using backtracking (but no GUI) to better showcase algorithm
more comments (yay!)
date: 2022-08-31
"""
from Sudoku_puzzle import Sudoku
from time import perf_counter


def get_puzzle():  # replaces the graphic interface
    """
    gets a puzzle from the console
    :return: (str)
    """
    test = input("Enter a Sudoku Puzzle (81 number string): ")
    while 42 == 42:
        if test.isnumeric() and len(test) == 81:
            return test
        elif test.lower().startswith('h'):
            print("""
            Input Sudoku board from top left to bottom right, row by row, as one would read a book.
            The input must be 81 characters long and contains only characters 0-9.
            '0' represents a blank space, and other numbers represent the permanent values on a Sudoku puzzle.
            """)
            test = input("Enter a Sudoku Puzzle (81 number string): ")
        else:
            test = input("Invalid format for board, try again or type help: ")


def main():
    puzzle = Sudoku(get_puzzle())
    blanks = puzzle.get_blanks()

    # using iterative approach, we need to keep track of indexes as we traverse the board (no recursion gang)
    current = 0
    total = len(blanks) - 1

    print("Inputted Board:")
    puzzle.see_board()  # outputs to console
    print()

    start = perf_counter()  # start solving
    while current <= total:
        pos = blanks[current]

        # get set of values in corresponding row, column, and block
        row = puzzle.get_row(pos[1])
        column = puzzle.get_column(pos[0])
        block = puzzle.get_block(pos[0], pos[1])  # find block uses both x and y values
        combined = set().union(*[row, column, block])  # union of three sets

        values = [i for i in '123456789' if i not in combined]  # list of possible values
        if values:  # as long as a value exists we can continue
            current += 1
            puzzle.set_square(pos[0], pos[1], values)  # values is list: first value will be used as the value in sudoku

        else:
            while True:  # loop because we may need to do this multiple times until we are done backtracking
                current -= 1  # go back one square and remove the last value we were using from list of possible values
                pos = blanks[current]
                square = puzzle.get_square(pos[0], pos[1])
                del square[0]  # remove first value, as it does not lead to a valid solution
                if square:  # same as before; as long as one valid value exists
                    puzzle.set_square(pos[0], pos[1], square)
                    current += 1
                    break
                else:  # otherwise square has no possible values so we can reset it and go back further
                    puzzle.set_square(pos[0], pos[1], '0')
    end = perf_counter()

    if puzzle.is_solved():
        print(f"Puzzle Solved ({round(end - start, 4)} seconds)")
        puzzle.see_board()
    else:
        print("Puzzle Not Solved (probably due to input error)")


if __name__ == "__main__":
    main()

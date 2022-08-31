"""
deterministic backtracking sudoku solver with realtime pygame display because who cares about speed
date: 2022-08-14
todo:
- have a proper loop so that the window doesnt need to reboot when restarting
- buttons instead of key presses
- make code that finds blocks more readable
"""
from Sudoku_puzzle import Sudoku
from display import Display
import pygame
from time import perf_counter


def main():

    pygame.init()
    done = False
    window = Display(720, "Sudoku Solver")

    while not done:  # loop 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                mouse = pygame.mouse.get_pos()
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    window.edit_board(mouse[0], mouse[1], '1')
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    window.edit_board(mouse[0], mouse[1], '2')
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    window.edit_board(mouse[0], mouse[1], '3')
                elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    window.edit_board(mouse[0], mouse[1], '4')
                elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    window.edit_board(mouse[0], mouse[1], '5')
                elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    window.edit_board(mouse[0], mouse[1], '6')
                elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    window.edit_board(mouse[0], mouse[1], '7')
                elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    window.edit_board(mouse[0], mouse[1], '8')
                elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    window.edit_board(mouse[0], mouse[1], '9')
                elif event.key == pygame.K_0 or event.key == pygame.K_BACKSPACE or event.key == pygame.K_KP0:
                    window.edit_board(mouse[0], mouse[1], '0')
                elif event.key == pygame.K_RETURN:
                    done = True
        window.update(30)

    puzzle = Sudoku(window.get_board())
    blanks = puzzle.get_blanks()
    current_idx = 0
    total = len(blanks) - 1
    update_screen = True
    print("Inputted Board:")
    puzzle.see_board()
    print()

    start = perf_counter()  # start solving
    while current_idx <= total:
        pos = blanks[current_idx]
        row = puzzle.get_row(pos[1])  # y value
        column = puzzle.get_column(pos[0])  # x value
        block = puzzle.get_block(pos[0], pos[1])
        combined = set().union(*[row, column, block])  # union of three sets
        values = [i for i in '123456789' if i not in combined]
        if values:
            current_idx += 1
            puzzle.set_square(pos[0], pos[1], values)
            if update_screen:
                window.edit_board(pos[0], pos[1], values[0], False)
        else:
            done = False
            while not done:
                current_idx -= 1
                pos = blanks[current_idx]
                square = puzzle.get_square(pos[0], pos[1])
                del square[0]
                if square:
                    puzzle.set_square(pos[0], pos[1], square)
                    if update_screen:
                        window.edit_board(pos[0], pos[1], square[0], False)
                    current_idx += 1
                    done = True
                else:
                    puzzle.set_square(pos[0], pos[1], '0')
                    if update_screen:
                        window.edit_board(pos[0], pos[1], '0', False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if update_screen:
                    update_screen = False
                else:
                    for y in range(9):
                        for x in range(9):
                            if type(puzzle.get_square(x, y)) is list:
                                window.edit_board(x, y, puzzle.get_square(x, y)[0], False)
                                window.update(0)
                    update_screen = True
        if update_screen:
            window.update(0)  # window doesnt update at fps, but asap

    end = perf_counter()

    if not update_screen:
        for y in range(9):
            for x in range(9):
                if type(puzzle.get_square(x, y)) is list:
                    window.edit_board(x, y, puzzle.get_square(x, y)[0], False)
                    window.update(0)

    if puzzle.is_solved():
        print(f"Puzzle Solved ({round(end - start, 4)} seconds)")
        puzzle.see_board()
    else:
        print("Puzzle Not Solved (either code is bugged or sudoku is invalid)")

    print("Exit window to end or press any key to run program again")
    wait = True
    while wait:  # keep window open until closed
        window.update(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                pygame.quit()
                wait = False


if __name__ == "__main__":
    print("\nSudoku Solving Algorithm Visualizer with Pygame:")
    print("""   1. Enter puzzle by hovering over squares and press a number to fill in grid
    2. Press enter to start solving
    3. Solving time may range significantly (as with all brute force searches), but is non-random
    4. Updating the window slows the speed by a few orders of magnitude; press enter if you only want to find solution
    5. Press enter to restart program
        """)
    while True:
        main()
        
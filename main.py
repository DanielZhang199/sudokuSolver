"""
main program code for sudoku solver
with realtime pygame display because who cares about speed
date: 2022-08-14
"""
from Sudoku_puzzle import Sudoku
from display import Display
import pygame


def find_block(x, y):
    """
    finds the sudoku block a xy value is in
    :param x: (int) [0-8]
    :param y: (int) [0-8]
    :return: (int) [0-8]
    """
    if y < 3:
        if x < 3:
            return 0
        elif x < 6:
            return 1
        else:
            return 2
    elif y < 6:
        if x < 3:
            return 3
        elif x < 6:
            return 4
        else:
            return 5
    else:
        if x < 3:
            return 6
        elif x < 6:
            return 7
        else:
            return 8


if __name__ == "__main__":
    print("\nSudoku Solving Algorithm Visualizer with Pygame:")
    print("""1. Enter puzzle by hovering over squares and press a number to fill in grid
2. Press enter to start solving
3. Solving time may range from instant to  the heat death of the universe depending on luck
4. Updating the window slows the speed by a few orders of magnitude so press enter again to disable window updating
    """)
    from time import perf_counter, sleep

    pygame.init()
    done = False
    Window = Display(720, 30)

    while not done:  # loop 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                mouse = pygame.mouse.get_pos()
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    Window.edit_board(mouse[0], mouse[1], '1')
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    Window.edit_board(mouse[0], mouse[1], '2')
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    Window.edit_board(mouse[0], mouse[1], '3')
                elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    Window.edit_board(mouse[0], mouse[1], '4')
                elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    Window.edit_board(mouse[0], mouse[1], '5')
                elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    Window.edit_board(mouse[0], mouse[1], '6')
                elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    Window.edit_board(mouse[0], mouse[1], '7')
                elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    Window.edit_board(mouse[0], mouse[1], '8')
                elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    Window.edit_board(mouse[0], mouse[1], '9')
                elif event.key == pygame.K_0 or event.key == pygame.K_BACKSPACE or event.key == pygame.K_KP0:
                    Window.edit_board(mouse[0], mouse[1], '0')
                elif event.key == pygame.K_RETURN:
                    done = True
        Window.update()

    Puzzle = Sudoku(Window.get_board())
    Blanks = Puzzle.get_blanks()
    CurrentIdx = 0
    TOTAL = len(Blanks) - 1
    update_screen = True
    print("Inputted Board:")
    Puzzle.see_board()
    print()

    start = perf_counter()  # start solving
    while CurrentIdx <= TOTAL:
        pos = Blanks[CurrentIdx]
        row = Puzzle.get_row(pos[1])  # y value
        column = Puzzle.get_column(pos[0])  # x value
        block = Puzzle.get_block(find_block(pos[0], pos[1]))
        combined = set().union(*[row, column, block])  # union of three sets
        Values = [i for i in '123456789' if i not in combined]
        if Values:
            CurrentIdx += 1
            Puzzle.set_square(pos[0], pos[1], Values)
            if update_screen:
                Window.edit_board(pos[0], pos[1], Values[0], False)
        else:
            Done = False
            while not Done:
                CurrentIdx -= 1
                pos = Blanks[CurrentIdx]
                square = Puzzle.get_square(pos[0], pos[1])
                del square[0]
                if square:
                    Puzzle.set_square(pos[0], pos[1], square)
                    if update_screen:
                        Window.edit_board(pos[0], pos[1], square[0], False)
                    CurrentIdx += 1
                    Done = True
                else:
                    Puzzle.set_square(pos[0], pos[1], '0')
                    if update_screen:
                        Window.edit_board(pos[0], pos[1], '0', False)
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
                            Window.edit_board(x, y, Puzzle.get_square(x, y)[0], False)
                            Window.update(False)
                    update_screen = True
        if update_screen:
            Window.update(False)  # window doesnt update at fps, but asap

    end = perf_counter()

    if not update_screen:
        for y in range(9):
            for x in range(9):
                Window.edit_board(x, y, Puzzle.get_square(x, y)[0], False)
                Window.update()

    if Puzzle.is_solved():
        print(f"Puzzle Solved ({round(end-start, 4)} seconds)")
        Puzzle.see_board()
    else:
        print("Puzzle Not Solved (either code is bugged or sudoku is invalid)")

    while True:  # keep window open until closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        sleep(0.1)

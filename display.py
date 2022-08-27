"""
Sudoku Board Display with pygame
date: 2022-08-17
"""
import pygame


class Display:
    """
    sudoku display made using pygame
    Attributes:
        BOARD: (list) of (tuple): (character (str), colour (tuple))
        WIDTH: (int)
        HEIGHT: (int)
        FPS: (int)
        DIMENSIONS: (tuple)
        CLOCK: (pygame.time.Clock)
        SCREEN: (pygame.Surface)
        BACKGROUND: (pygame.Surface)
        NFONT: (pygame.Font) font used for numbers
        MFONT: font used for misc purposes

    Methods:
        update(): (none)
        clear(): (none)
        get_screen(): (pygame.Surface)
        get_width(): (int)
        get_height(): (int)
        edit_board(x, y, val): (none)
        get_board(): (string)
    """

    def __init__(self, size, fps, caption):
        """
        :param size: (int) pixel size of sudoku board
        :param fps: (int)
        :param caption: (str)
        """
        self.__FPS = fps
        self.__WIDTH = size
        self.__HEIGHT = size
        self.__DIMENSIONS = (self.__WIDTH, self.__HEIGHT)
        self.__CLOCK = pygame.time.Clock()
        self.__SCREEN = pygame.display.set_mode(self.__DIMENSIONS)
        pygame.display.set_caption(caption)
        self.__BACKGROUND = pygame.Surface(self.__DIMENSIONS, pygame.SRCALPHA, 32)
        self.__BACKGROUND.fill((230, 230, 230))
        self.__BOARD = [list('000000000') for _ in range(9)]
        pygame.font.init()
        self.__NFONT = pygame.font.SysFont('franklingothicmedium', 70)
        self.__MFONT = pygame.font.SysFont('Segoe UI', 14)

    # --- MODIFIERS --- #

    def update(self, restrict=True):
        """
        Updates the entire screen
        to be honest, due to the number of updates needed and the requirement to go asap,
        this code should be optimized quite a bit to not update the entire screen
        :param restrict: (bool) whether the fps should be unlimited
        :return:
        """
        self.__SCREEN.blit(self.__BACKGROUND, (0, 0))  # clears screen

        for i in range(1, 9):  # draw lines
            if i == 3 or i == 6:
                width = 3
            else:
                width = 1
            pygame.draw.line(self.__SCREEN, (0, 0, 0), (self.__WIDTH / 9 * i, self.__HEIGHT), (self.__WIDTH / 9 * i, 0),
                             width)
            pygame.draw.line(self.__SCREEN, (0, 0, 0), (self.__WIDTH, self.__HEIGHT / 9 * i),
                             (0, self.__HEIGHT / 9 * i), width)

        for y, row in enumerate(self.__BOARD):  # draw board
            for x, val in enumerate(row):
                if val[0] == '0':
                    pass
                else:
                    try:
                        text = self.__NFONT.render(val[0], True, val[1])
                        self.__SCREEN.blit(text, (self.__WIDTH / 9 * x + self.__WIDTH / 36, self.__HEIGHT / 9 * y))
                    except TypeError:
                        pass

        fps_text = self.__MFONT.render("FPS: " + str(int(self.__CLOCK.get_fps())), True, (10, 10, 10))

        self.__SCREEN.blit(fps_text, (10, 0))

        if restrict:  # during solving we don't want fps <= 30
            self.__CLOCK.tick(self.__FPS)
        else:
            self.__CLOCK.tick()
        pygame.display.flip()  # updates screen

    def edit_board(self, x, y, val, pixels=True):
        """
        edits one square on the board
        :param x: (float) location on screen
        :param y: (float) location on screen
        :param val: (str)
        :param pixels: (bool) whether the function looks at pixels or index position
        :return: (none)
        """
        if pixels:
            ix = None
            iy = None
            cutoff = [self.__WIDTH/9 * (i+1) for i in range(9)]
            for idx, num in enumerate(cutoff):
                if x < num:
                    ix = idx
                    break
            for idx, num in enumerate(cutoff):
                if y < num:
                    iy = idx
                    break
            self.__BOARD[iy][ix] = (val, (10, 10, 10))
        else:
            self.__BOARD[y][x] = (val, (90, 90, 90))

    # --- ACCESSORS -- #

    def get_screen(self):
        return self.__SCREEN

    def get_width(self):
        return self.__WIDTH

    def get_height(self):
        return self.__HEIGHT

    def get_board(self):
        string = ''
        for j in range(9):
            string += ''.join([i if isinstance(i, str) else i[0] for i in self.__BOARD[j]])
        return string

# Sabin Dheke
# CMPS 5443 
# Advance topic: 2D Games
# Assignment 1
# Word Cited: https://projectgurukul.org/create-sudoku-game-python/

import sys
import pygame as pg
from gameLogic import Sudoku

# Initialize pygame
pg.init()

# Declare all constants here.
CELL_SIZE = 70
MINOR_GRID_SIZE = 1
MAJOR_GRID_SIZE = 3
BUFFER = 5

# Button properties
BUTTON_HEIGHT = 50
BUTTON_WIDTH = 120
BUTTON_BORDER = 1

# Calculate width and height
WIDTH = CELL_SIZE * 9 + MINOR_GRID_SIZE * 6 + MAJOR_GRID_SIZE * 4 + BUFFER * 2
HEIGHT = CELL_SIZE * 9 + MINOR_GRID_SIZE * 6 + MAJOR_GRID_SIZE * 4 + BUTTON_HEIGHT + BUFFER * 3 + BUTTON_BORDER * 2

# button color
INACTIVE_BUTTON = 0, 175, 0
INACTIVE_RESET_BUTTON = 200, 0, 0
ACTIVE_BUTTON = 255, 255, 255

# Button size
SIZE = WIDTH, HEIGHT

# Colors
WHITE = 255, 255, 255
BLACK = 0, 0, 0
GRAY = 236, 255, 154
GREEN = 0, 175, 0
RED = 200, 0, 0

"""adding custom icon and and title to pygame"""
screen = pg.display.set_mode(SIZE)
img = pg.image.load('./game.png')
pg.display.set_icon(img)
pg.display.set_caption('Sudoku Game')


class RectCell(pg.Rect):
    """
    Represent individual cells in the game
    """

    def __init__(self, left, top, row, col):
        super().__init__(left, top, CELL_SIZE, CELL_SIZE)
        self.row = row
        self.col = col


class Draw:
    def __init__(self):
        """Initial the drawing properties"""
        self.cells = [[] for _ in range(9)]
        self.row = 0
        self.col = 0

    def createCells(self):
        """Creates all 81 cells with RectCell class."""
        left = BUFFER + MAJOR_GRID_SIZE
        top = BUFFER + MAJOR_GRID_SIZE

        """Generates and creates cells for a 9x9 grid, with the cells being positioned and spaced according to specified grid sizes. The position of each cell is calculated based on its row and column, with values updated for the next cell iteration."""
        while self.row < 9:
            while self.col < 9:
                self.cells[self.row].append(RectCell(left, top, self.row, self.col))
                """Updating the attributes for next RectCell"""
                left += CELL_SIZE + MINOR_GRID_SIZE
                if self.col != 0 and (self.col + 1) % 3 == 0:
                    left = left + MAJOR_GRID_SIZE - MINOR_GRID_SIZE
                self.col += 1

            """Updating the attributes for next RectCell"""
            top += CELL_SIZE + MINOR_GRID_SIZE
            if self.row != 0 and (self.row + 1) % 3 == 0:
                top = top + MAJOR_GRID_SIZE - MINOR_GRID_SIZE
            left = BUFFER + MAJOR_GRID_SIZE
            self.col = 0
            self.row += 1

        return self.cells

    @staticmethod
    def drawGrid():
        """Draws the major and minor grid lines for Sudoku."""
        draw_lines = 0
        position = BUFFER + MAJOR_GRID_SIZE + CELL_SIZE

        """Draws red lines on screen for a grid of cells with alternating major and minor line sizes. Loop stops at 6 iterations."""
        while draw_lines < 6:
            pg.draw.line(screen, RED, (position, BUFFER),
                             (position, WIDTH - BUFFER - 1), MINOR_GRID_SIZE)
            pg.draw.line(screen, RED, (BUFFER, position),
                             (WIDTH - BUFFER - 1, position), MINOR_GRID_SIZE)

            # Update number of draw line
            draw_lines += 1

            # Update pos for next lines
            position += CELL_SIZE + MINOR_GRID_SIZE
            if draw_lines % 2 == 0:
                position += CELL_SIZE + MAJOR_GRID_SIZE

        """Draws green major grid lines on screen with a set interval and buffer size. The lines are drawn horizontally and vertically."""
        for position in range(BUFFER + MAJOR_GRID_SIZE // 2, WIDTH,
                              CELL_SIZE * 3 + MINOR_GRID_SIZE * 2 + MAJOR_GRID_SIZE):
            pg.draw.line(screen, GREEN, (position, BUFFER),
                             (position, WIDTH - BUFFER - 1), MAJOR_GRID_SIZE)
            pg.draw.line(screen, GREEN, (BUFFER, position),
                             (WIDTH - BUFFER - 1, position), MAJOR_GRID_SIZE)

    @staticmethod
    def fillCells(cells, board):
        """Fills in all the numbers for the game."""
        font = pg.font.Font(None, 36)

        """Renders text in the cells of the board, filling in black bold font and user entered values in green or red depending on if the move is valid. Centers text in cell."""
        # Fill in all cells with correct value
        for row in range(9):
            for col in range(9):
                if board.board[row][col].value is None:
                    continue

                """Filling the board with values in bold font"""
                if not board.board[row][col].editable:
                    font.bold = True
                    text = font.render(f'{board.board[row][col].value}', True, BLACK)

                # Filling values in the board by the user
                else:
                    font.bold = False
                    if board.check_move(board.board[row][col], board.board[row][col].value):
                        text = font.render(
                            f'{board.board[row][col].value}', True, GREEN)
                    else:
                        text = font.render(
                            f'{board.board[row][col].value}', True, RED)

                # Center the text in cell
                x_pos, y_pos = cells[row][col].center
                textbox = text.get_rect(center=(x_pos, y_pos))
                screen.blit(text, textbox)

    @staticmethod
    def drawBtn(left, top, width, height, border, color, border_color, text, text_color):
        """Creates a button with a border for reset."""
        # Draw the border as outer rect
        pg.draw.rect(
            screen,
            border_color,
            (left, top, width + border * 2, height + border * 2),
        )

        # Draw the inner button
        button = pg.Rect(
            left + border,
            top + border,
            width,
            height
        )
        pg.draw.rect(screen, color, button)
        # Set the text
        font = pg.font.Font(None, 26)
        text = font.render(text, True, text_color)
        x_pos, y_pos = button.center
        textbox = text.get_rect(center=(x_pos, y_pos))
        screen.blit(text, textbox)

        return button

    def drawBoard(self, active_cell, cells, _game):
        """Draws the board with all elements."""
        # Draws grid and cells
        self.drawGrid()
        if active_cell is not None:
            pg.draw.rect(screen, GRAY, active_cell)

        # Fill cells values with predifined numbers
        self.fillCells(cells, _game)


class Game:
    def __init__(self):
        """Contains all the functionality for playing a game of Sudoku."""

        """Creating the board with grid and cells also the reset button"""
        self.draw = Draw()
        self.reset_btn = self.draw.drawBtn(
            WIDTH - BUFFER - BUTTON_BORDER * 2 - BUTTON_WIDTH,
            HEIGHT - BUTTON_HEIGHT - BUTTON_BORDER * 2 - BUFFER,
            BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_BORDER, INACTIVE_RESET_BUTTON, BLACK, 'Reset', BLACK
        )

        """The difficulty level sudoku board and predefined numbers"""
        easy = [
            [1, 0, 0, 9, 4, 0, 0, 3, 2],
            [3, 5, 6, 0, 2, 0, 0, 4, 0],
            [2, 0, 4, 0, 0, 3, 1, 0, 6],
            [0, 7, 0, 0, 5, 1, 0, 2, 0],
            [0, 3, 1, 0, 6, 0, 0, 5, 7],
            [5, 0, 9, 0, 0, 0, 6, 0, 0],
            [4, 1, 0, 0, 0, 2, 0, 7, 8],
            [7, 6, 3, 0, 0, 5, 4, 0, 0],
            [9, 2, 8, 0, 0, 4, 0, 0, 1]
        ]

        """Calling the sudoku from gameLogic"""
        self.game = Sudoku(easy)
        self.cells = self.draw.createCells()
        self.active_cell = None
        self.solve_rect = pg.Rect(
            BUFFER, HEIGHT - BUTTON_HEIGHT - BUTTON_BORDER * 2 - BUFFER,
                    BUTTON_WIDTH + BUTTON_BORDER * 2, BUTTON_HEIGHT + BUTTON_BORDER * 2
        )
    """All the logics and all the events are checking here from the beginning till quit."""
    def play(self):

        while True:

            # iterating through the events and exit if the event is quit
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()

                # Checking mouse click
                if event.type == pg.MOUSEBUTTONUP:
                    mouse_pos = pg.mouse.get_pos()

                    # Checking reset button is pressed or not
                    if self.reset_btn.collidepoint(mouse_pos):
                        self.game.reset()

                    # Test if point in any cell of any row
                    for row in self.cells:
                        for cell in row:
                            if cell.collidepoint(mouse_pos):
                                self.active_cell = cell

                    # Test if active cell is empty
                    if self.active_cell and not self.game.board[self.active_cell.row][self.active_cell.col].editable:
                        self.active_cell = None

                """Process keypress events to input numbers in active cell of sudoku board and clear values with backspace/delete."""
                if event.type == pg.KEYUP:
                    if self.active_cell is not None:

                        """Input number based on key press"""
                        if event.key == pg.K_0 or event.key == pg.K_KP0:
                            self.game.board[self.active_cell.row][self.active_cell.col].value = 0
                        if event.key == pg.K_1 or event.key == pg.K_KP1:
                            self.game.board[self.active_cell.row][self.active_cell.col].value = 1
                        if event.key == pg.K_2 or event.key == pg.K_KP2:
                            self.game.board[self.active_cell.row][self.active_cell.col].value = 2
                        if event.key == pg.K_3 or event.key == pg.K_KP3:
                            self.game.board[self.active_cell.row][self.active_cell.col].value = 3
                        if event.key == pg.K_4 or event.key == pg.K_KP4:
                            self.game.board[self.active_cell.row][self.active_cell.col].value = 4
                        if event.key == pg.K_5 or event.key == pg.K_KP5:
                            self.game.board[self.active_cell.row][self.active_cell.col].value = 5
                        if event.key == pg.K_6 or event.key == pg.K_KP6:
                            self.game.board[self.active_cell.row][self.active_cell.col].value = 6
                        if event.key == pg.K_7 or event.key == pg.K_KP7:
                            self.game.board[self.active_cell.row][self.active_cell.col].value = 7
                        if event.key == pg.K_8 or event.key == pg.K_KP8:
                            self.game.board[self.active_cell.row][self.active_cell.col].value = 8
                        if event.key == pg.K_9 or event.key == pg.K_KP9:
                            self.game.board[self.active_cell.row][self.active_cell.col].value = 9
                        if event.key == pg.K_BACKSPACE or event.key == pg.K_DELETE:
                            self.game.board[self.active_cell.row][self.active_cell.col].value = None

            screen.fill(WHITE)
            # Draw board
            self.draw.drawBoard(self.active_cell, self.cells, self.game)

            # Create buttons
            reset_btn = self.draw.drawBtn(
                WIDTH - BUFFER - BUTTON_BORDER * 2 - BUTTON_WIDTH,
                HEIGHT - BUTTON_HEIGHT - BUTTON_BORDER * 2 - BUFFER,
                BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_BORDER, INACTIVE_RESET_BUTTON, GREEN, 'RESET', WHITE
            )

            # Check if mouse over either button
            if reset_btn.collidepoint(pg.mouse.get_pos()):
                self.reset_btn = self.draw.drawBtn(
                    WIDTH - BUFFER - BUTTON_BORDER * 2 - BUTTON_WIDTH,
                    HEIGHT - BUTTON_HEIGHT - BUTTON_BORDER * 2 - BUFFER,
                    BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_BORDER, WHITE, BLACK, 'RESET', BLACK
                )

            # Check if game is complete
            if not self.game.get_empty_cell():
                if self.__check_sudoku(self.game):
                    # Set the text
                    font = pg.font.Font(None, 36)
                    text = font.render('Sudoku Solved!', True, RED)
                    textbox = text.get_rect(center=self.solve_rect.center)
                    screen.blit(text, textbox)
            # Update screen
            pg.display.flip()

    @staticmethod
    def __check_sudoku(sudoku):
        """
        Takes a complete instance of Sudoku and
        returns whether the solution is valid.
        """
        # Ensure all cells are filled
        if sudoku.get_empty_cell():
            raise ValueError('Game is not complete')

        # Will hold values for each row, column, and box
        row_sets = [set() for _ in range(9)]
        col_sets = [set() for _ in range(9)]
        box_sets = [set() for _ in range(9)]

        """checks if a value in the sudoku board is unique in its row, column, and box. If a duplicate is found, it returns False. Otherwise, it adds the value to the corresponding set of unique values for that row, column, and box"""
        for row in range(9):
            for col in range(9):
                box = (row // 3) * 3 + col // 3
                value = sudoku.board[row][col].value

                # Check if number already encountered in row, column, or box
                if value in row_sets[row] or value in col_sets[col] or value in box_sets[box]:
                    return False
                # Add value to corresponding set
                row_sets[row].add(value)
                col_sets[col].add(value)
                box_sets[box].add(value)
        # All rows, columns, and boxes are valid
        return True


# Program run from here.
if __name__ == '__main__':
    # Initialize Sudoko game
    game = Game()
    # run this game
    game.play()

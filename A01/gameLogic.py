# Sabin Dheke
# CMPS 5443 
# Advance topic: 2D Games
# Assignment 1
# Word Cited: https://projectgurukul.org/create-sudoku-game-python/


class Cell:
    """This represents a cell within a game of Sudoku"""

    def __init__(self, row, col, value, editable):
        """Initialize cell attribute"""
        self.row = row
        self.col = col
        self.value = value
        self._editable = editable

    @property
    def row(self):
        """Getter method for row"""
        return self._row

    @row.setter
    def row(self, row):
        """Setter method for row"""
        if row < 0 or row > 8:
            raise AttributeError('Row must be between 0 and 8.')
        else:
            self._row = row

    @property
    def col(self):
        """Getter method for column"""
        return self._col

    @col.setter
    def col(self, col):
        """Setter method for column"""
        if col < 0 or col > 8:
            raise AttributeError('Col must be between 0 and 8.')
        else:
            self._col = col

    @property
    def value(self):
        """Getter method for value."""
        return self._value

    @property
    def editable(self):
        """Getter method for editable."""
        return self._editable

    def __repr__(self):
        return f'{self.__class__.__name__}({self.value})'

    @value.setter
    def value(self, value):
        """Setter method for value."""
        if value is not None and (value < 1 or value > 9):
            raise AttributeError('Value must be between 1 to 9.')
        else:
            self._value = value

"""Represents a game/board of Sudoku."""
class Sudoku:

    """Initializes Sudoku game """
    def __init__(self, board):
        self.board = []
        for row in range(9):
            self.board.append([])
            for col in range(9):
                if board[row][col] == 0:
                    val = None
                    editable = True
                else:
                    val = board[row][col]
                    editable = False
                self.board[row].append(Cell(row, col, val, editable))

    
    """Returns whether a number is a valid move for a cell."""
    def check_move(self, cell, num):
        # Check if the number is valid for the row
        for col in range(9):
            if self.board[cell.row][col].value == num and col != cell.col:
                return False

        # Check if the number is valid for the column
        for row in range(9):
            if self.board[row][cell.col].value == num and row != cell.row:
                return False

        # Check if the number is valid in its box
        for row in range(cell.row // 3 * 3, cell.row // 3 * 3 + 3):
            for col in range(cell.col // 3 * 3, cell.col // 3 * 3 + 3):
                if (
                    self.board[row][col].value == num
                    and row != cell.row
                    and col != cell.col
                ):
                    return False
        # Move is valid
        return True

    """Returns an empty cell & returns False if all cells are filled in."""
    def get_empty_cell(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col].value is None:
                    return self.board[row][col]

        return False

    """
    Solves the game from current state using backtracking algorithm.
    Returns True if successful and False if it is not possible to solve.
    """
    def solve(self):
        
        cell = self.get_empty_cell()

        # Board is complete if cell is False
        if not cell:
            return True

        # Check each possible value in cell
        for val in range(1, 10):

            # Check if the value is a valid move
            if not self.check_move(cell, val):
                continue

            # Place value in board
            cell.value = val

            # If all recursive calls return True then board is solved
            if self.solve():
                return True
            # Undo move is solve was unsuccessful
            cell.value = None
        # No moves were successful
        return False

    """Get the value of the row and column up to 9th position"""
    def __get_board(self):
        return [[self.board[row][col].value for col in range(9)] for row in range(9)]

    """Checks if the current configuration is solvable."""
    def test_solve(self):
        current_board = self.__get_board()
        solvable = self.solve()

        # Reset board to state before solve check
        for row in range(9):
            for col in range(9):
                self.board[row][col].value = current_board[row][col]

        return solvable

    """Resets the game to the starting point."""
    def reset(self):
        """Reset all the cells that is editible"""
        for row in self.board:
            for cell in row:
                if cell.editable:
                    cell.value = None

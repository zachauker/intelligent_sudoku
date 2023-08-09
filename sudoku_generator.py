import random
import pandas as pd
import copy


class SudokuPuzzle:
    def __init__(self, grid):
        self.grid = grid
        self.initial_puzzle = [row[:] for row in grid]

    def get_value(self, row, col):
        return self.grid[row][col]

    def set_value(self, row, col, value):
        self.grid[row][col] = value

    def is_editable(self, row, col):
        return self.initial_puzzle[row][col] == 0
    
    def copy(self):
        return SudokuPuzzle([row[:] for row in self.grid])
    
    def is_valid_number(self, row, col, num):
        # Check if the number exists in the same row
        if num in self.grid[row]:
            return False

        # Check if the number exists in the same column
        for i in range(9):
            if self.grid[i][col] == num:
                return False

        # Check if the number exists in the same 3x3 subgrid
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.grid[i][j] == num:
                    return False

        return True
    
    def get_possible_values(self, row, col):
        possible_values = []
        for value in range(1, 10):
            if self.is_valid_number(row, col, value):
                possible_values.append(value)
        return possible_values
    
    def is_initial_value(self, row, col):
        return self.initial_puzzle[row][col] != 0
    
    def is_solved(self):
        # Check rows, columns, and subgrids
        for i in range(9):
            if not self.is_unit_valid(self.grid[i]):  # Check row
                return False
            # Check column
            if not self.is_unit_valid([self.grid[j][i] for j in range(9)]):
                return False
            if not self.is_unit_valid(self.get_subgrid(i // 3, i % 3)):  # Check subgrid
                return False
        return True

    def is_unit_valid(self, unit):
        # Check if a row, column, or subgrid is valid (contains numbers 1 to 9 exactly once)
        return sorted(unit) == list(range(1, 10))

    def get_subgrid(self, row, col):
        # Get the values of the 3x3 subgrid at the specified row and column
        return [self.grid[3 * row + i][3 * col + j] for i in range(3) for j in range(3)]
    
    def is_valid(self):
        # Check rows and columns for duplicates
        for i in range(9):
            row_values = set()
            col_values = set()
            for j in range(9):
                row_val = self.get_value(i, j)
                col_val = self.get_value(j, i)
                if row_val in row_values or col_val in col_values:
                    return False
                if row_val != 0:
                    row_values.add(row_val)
                if col_val != 0:
                    col_values.add(col_val)

        # Check 3x3 subgrids for duplicates
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                subgrid_values = set()
                for x in range(i, i + 3):
                    for y in range(j, j + 3):
                        val = self.get_value(x, y)
                        if val in subgrid_values:
                            return False
                        if val != 0:
                            subgrid_values.add(val)

        return True

    def solve_sudoku(self):
        # Find the next empty cell
        row, col = find_empty_cell(self.grid)

        # If no empty cells are found, the Sudoku is solved
        if row == -1 and col == -1:
            return True

        # Try different numbers in the empty cell
        for num in range(1, 10):
            if self.is_valid_number(row, col, num):
                self.set_value(row, col, num)

                # Recursively solve the Sudoku
                if self.solve_sudoku():
                    return True

                # If the number is not part of the solution, backtrack and try a different number
                self.set_value(row, col, 0)
        

    def remove_numbers(self, difficulty):
        # Determine the number of cells to remove based on the difficulty level
        if difficulty == "Easy":
            num_cells_to_remove = 40
        elif difficulty == "Medium":
            num_cells_to_remove = 50
        elif difficulty == "Hard":
            num_cells_to_remove = 60
        else:
            num_cells_to_remove = 50

        # Remove numbers from the grid
        cells_removed = 0
        while cells_removed < num_cells_to_remove:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if self.get_value(row, col) != 0:
                self.set_value(row, col, 0)
                cells_removed += 1
  
def generate_sudoku(difficulty):
    # Create an empty Sudoku grid
    grid = [[0] * 9 for _ in range(9)]

    # Instantiate SudokuPuzzle class object with generated grid.
    puzzle = SudokuPuzzle(grid)

    # Solve the Sudoku grid
    puzzle.solve_sudoku()

    # Remove numbers based on the difficulty level
    puzzle.remove_numbers(difficulty)

    ready_puzzle = SudokuPuzzle(puzzle.grid)

    return ready_puzzle

def find_empty_cell(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return row, col
    return -1, -1

def get_hint(puzzle):
    # Get a list of all empty cells
    empty_cells = [(row, col) for row in range(9)
                   for col in range(9) if puzzle.get_value(row, col) == 0]

    # Sort the empty cells based on the number of conflicts they have
    sorted_cells = sorted(empty_cells, key=lambda cell: count_conflicts(
        puzzle, cell[0], cell[1]), reverse=True)

    # Attempt constraint propagation on each cell until a valid hint is found
    for cell in sorted_cells:
        row, col = cell

        original_value = puzzle.get_value(row, col)
        possible_values = puzzle.get_possible_values(row, col)

        for value in possible_values:
            # Temporarily set the cell value to the possible value
            puzzle.set_value(row, col, value)

            # Check if the puzzle remains valid after setting the value
            if puzzle.is_valid():
                # Resets grid value back to original so that hint callback can handle setting hint value.
                puzzle.set_value(row, col, original_value)
                return row, col, value

            # Reset the cell value to its original value and continue through loop
            puzzle.set_value(row, col, original_value)

    # If no valid hint is found, return None
    return None, None, None


def find_most_difficult_cell(puzzle):
    max_conflicts = 1
    most_difficult_cell = None

    for row in range(9):
        for col in range(9):
            if puzzle.get_value(row, col) == 0:
                conflicts = count_conflicts(puzzle, row, col)
                if conflicts > max_conflicts:
                    max_conflicts = conflicts
                    most_difficult_cell = (row, col)
                    return most_difficult_cell

def count_conflicts(grid, row, col):
    conflicts = 0
    num = grid.get_value(row, col)

    # Count conflicts in the row and column
    for i in range(9):
        if grid.get_value(row, i) == num:
            conflicts += 1
        if grid.get_value(i, col) == num:
            conflicts += 1

    # Count conflicts in the 3x3 subgrid
    start_row, start_col = (row // 3) * 3, (col // 3) * 3
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if grid.get_value(i, j) == num:
                conflicts += 1

    return conflicts


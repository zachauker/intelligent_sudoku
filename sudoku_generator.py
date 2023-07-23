import random
import pandas as pd

class SudokuPuzzle:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.initial_puzzle = [row[:] for row in puzzle]

    def get_value(self, row, col):
        return self.puzzle[row][col]

    def set_value(self, row, col, value):
        self.puzzle[row][col] = value

    def is_editable(self, row, col):
        return self.initial_puzzle[row][col] == 0

    def copy(self):
        return SudokuPuzzle([row[:] for row in self.puzzle])
    
    def is_initial_value(self, row, col):
        return self.initial_puzzle[row][col] != 0
    
def generate_sudoku(difficulty):
    # Create an empty Sudoku grid
    grid = [[0] * 9 for _ in range(9)]

    # Solve the Sudoku grid
    solve_sudoku(grid)

    # Remove numbers based on the difficulty level
    remove_numbers(grid, difficulty)

    # Convert the grid to a Pandas DataFrame
    puzzle = SudokuPuzzle(grid)

    return puzzle

def solve_sudoku(grid):
    # Find the next empty cell
    row, col = find_empty_cell(grid)

    # If no empty cells are found, the Sudoku is solved
    if row == -1 and col == -1:
        return True

    # Try different numbers in the empty cell
    for num in range(1, 10):
        if is_valid_number(grid, row, col, num):
            grid[row][col] = num

            # Recursively solve the Sudoku
            if solve_sudoku(grid):
                return True

            # If the number is not part of the solution, backtrack and try a different number
            grid[row][col] = 0

    return False

def find_empty_cell(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return row, col
    return -1, -1

def is_valid_number(grid, row, col, num):
    # Check if the number exists in the same row
    if num in grid[row]:
        return False

    # Check if the number exists in the same column
    for i in range(9):
        if grid[i][col] == num:
            return False

    # Check if the number exists in the same 3x3 subgrid
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if grid[i][j] == num:
                return False

    return True

def remove_numbers(grid, difficulty):
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
        if grid[row][col] != 0:
            grid[row][col] = 0
            cells_removed += 1

def get_hint(puzzle):
    # Find the most difficult cell to fill
    row, col = find_most_difficult_cell(puzzle)

    # Perform constraint propagation to find a valid value for the cell
    if row is not None and col is not None:
        value = puzzle.get_value(row, col)
        valid_values = constraint_propagation(puzzle.puzzle, row, col)
        if value == 0 and valid_values:
            valid_value = random.choice(valid_values)
            puzzle.puzzle[row][col] = valid_value

def constraint_propagation(grid, row, col):
    valid_values = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    # Remove values already present in the same row and column
    for i in range(9):
        if grid[row][i] in valid_values:
            valid_values.remove(grid[row][i])
        if grid[i][col] in valid_values:
            valid_values.remove(grid[i][col])

    # Remove values already present in the 3x3 subgrid
    start_row, start_col = (row // 3) * 3, (col // 3) * 3
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if grid[i][j] in valid_values:
                valid_values.remove(grid[i][j])

    return list(valid_values)

def find_most_difficult_cell(puzzle):
    max_conflicts = -1
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


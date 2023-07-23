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

def generate_hint(puzzle):
    # Implement AI hint generator logic here
    # Analyze the puzzle to find a cell with a conflict or incorrect value
    # Use backtracking or constraint propagation to find a valid value for the cell
    # Return the hint as (row, col, value) or None if no hint is available
    max_conflicts = -1
    hint_cell = None

    for row in range(9):
        for col in range(9):
            # Skip cells with initial puzzle values
            if not puzzle.is_editable(row, col):
                continue

            # Count conflicts for each cell
            conflicts = count_conflicts(puzzle, row, col)

            if conflicts > max_conflicts:
                max_conflicts = conflicts
                hint_cell = (row, col)

    if hint_cell is None:
        return None

    row, col = hint_cell

def count_conflicts(puzzle, row, col):
    conflicts = 0

    # Check conflicts in the row
    conflicts += len(set(puzzle.loc[row, :])) - len(puzzle.loc[row, :].replace(0, pd.NA).dropna())

    # Check conflicts in the column
    conflicts += len(set(puzzle.loc[:, col])) - len(puzzle.loc[:, col].replace(0, pd.NA).dropna())

    # Check conflicts in the 3x3 subgrid
    start_row, start_col = (row // 3) * 3, (col // 3) * 3
    subgrid_values = puzzle.loc[start_row:start_row + 2, start_col:start_col + 2]
    conflicts += len(set(subgrid_values.values.flatten())) - len(subgrid_values.values.flatten().replace(0, pd.NA).dropna())

    return conflicts

def get_empty_cell(puzzle):
    # Find the empty cell with the fewest legal values (MRV heuristic)
    empty_cells = []
    for row in range(9):
        for col in range(9):
            if puzzle.loc[row, col] == 0:
                num_legal_values = len(get_legal_values(puzzle, row, col))
                empty_cells.append(((row, col), num_legal_values))
    empty_cells.sort(key=lambda cell: cell[1])
    return empty_cells[0][0] if empty_cells else None

def get_legal_values(puzzle, row, col):
    # Get the set of legal values for the given cell
    legal_values = set(range(1, 10))

    # Remove values that conflict in the row, column, and 3x3 subgrid
    legal_values -= set(puzzle.loc[row, :])
    legal_values -= set(puzzle.loc[:, col])
    start_row, start_col = (row // 3) * 3, (col // 3) * 3
    subgrid_values = puzzle.loc[start_row:start_row + 2, start_col:start_col + 2]
    legal_values -= set(subgrid_values.values.flatten())

    return legal_values

def backtracking(puzzle, row, col):
    if row == 9:
        return puzzle  # The puzzle is solved

    if puzzle.loc[row, col] != 0:
        return backtracking(puzzle, *get_next_cell(row, col))

    for value in get_legal_values(puzzle, row, col):
        puzzle.loc[row, col] = value
        if is_valid_solution(puzzle):
            next_cell = get_next_cell(row, col)
            if backtracking(puzzle, *next_cell) is not None:
                return puzzle
        puzzle.loc[row, col] = 0

    return None

def get_next_cell(row, col):
    if col < 8:
        return row, col + 1
    else:
        return row + 1, 0

def is_valid_solution(puzzle):
    # Check if the puzzle is a valid solution
    return all(len(set(puzzle.loc[row, :])) == 9 for row in range(9)) \
           and all(len(set(puzzle.loc[:, col])) == 9 for col in range(9)) \
           and all(len(set(puzzle.loc[start_row:start_row + 2, start_col:start_col + 2].values.flatten())) == 9
                   for start_row in (0, 3, 6) for start_col in (0, 3, 6))

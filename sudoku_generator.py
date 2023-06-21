import random
import pandas as pd

def generate_sudoku(difficulty):
    # Create an empty Sudoku grid
    grid = [[0] * 9 for _ in range(9)]

    # Solve the Sudoku grid
    solve_sudoku(grid)

    # Remove numbers based on the difficulty level
    remove_numbers(grid, difficulty)

    # Convert the grid to a Pandas DataFrame
    puzzle = pd.DataFrame(grid)

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

import numpy as np
from sudoku_generator import count_conflicts, find_empty_cell
from collections import deque

def backtracking(puzzle):
    # Find the next empty cell
    row, col = find_empty_cell(puzzle.grid)

    for temp_row in range(9):
        for temp_col in range(9):
            if puzzle.grid[row][col] == 0:
                row, col = temp_row, temp_col

    # If no empty cells are found, the Sudoku is solved
    if row == -1 and col == -1:
        return True

    # Try different numbers in the empty cell
    for num in range(1, 10):
        if puzzle.is_valid_number(row, col, num):
            puzzle.set_value(row, col, num)

            # Recursively solve the Sudoku
            if puzzle.solve_sudoku():
                return True

            # If the number is not part of the solution, backtrack and try a different number
            puzzle.set_value(row, col, 0)

def constraint_propagation(puzzle):
    # Get a list of all empty cells
    empty_cells = [(row, col) for row in range(9)
                   for col in range(9) if puzzle.get_value(row, col) == 0]

    # Sort the empty cells based on the number of conflicts they have
    sorted_cells = sorted(empty_cells, key=lambda cell: count_conflicts(
        puzzle, cell[0], cell[1]), reverse=True)

    progress_made = False

    for cell in sorted_cells:
        row, col = cell

        original_value = puzzle.get_value(row, col)
        possible_values = puzzle.get_possible_values(row, col)

        for value in possible_values:
            # Temporarily set the cell value to the possible value
            puzzle.set_value(row, col, value)

            # Check if the puzzle remains valid after setting the value
            if puzzle.is_valid():
                progress_made = True
                # If value is valid then break loop and continue to next grid marker.
                break

            # Reset the cell value to its original value
            puzzle.set_value(row, col, original_value)

        if not progress_made:
            break
    
    return puzzle.is_solved()


def solve_sudoku_bfs(puzzle):
    queue = deque([(puzzle, 0, 0)])

    while queue:
        current_puzzle, row, col = queue.popleft()

        if current_puzzle.is_solved():
            return current_puzzle # Solution found

        for num in range(1, 10):
            if current_puzzle.is_valid_number(row, col, num):
                new_puzzle = current_puzzle.copy()
                new_puzzle.set_value(row, col, num)
                new_row, new_col = find_empty_cell(new_puzzle.grid)
                queue.append((new_puzzle, new_row, new_col))

    return None
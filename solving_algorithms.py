import numpy as np
from sudoku_generator import count_conflicts, find_empty_cell
from collections import deque
import heapq

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

def solve_sudoku_dfs(puzzle):
    empty_cell = find_empty_cell(puzzle.grid)

    if puzzle.is_solved():
        return puzzle  # Puzzle is solved

    row, col = empty_cell

    for num in range(1, 10):
        if puzzle.is_valid_number(row, col, num):
            new_puzzle = puzzle.copy()
            new_puzzle.set_value(row, col, num)

            # Recursive call 
            result = solve_sudoku_dfs(new_puzzle)
            if result:
                return result  # Puzzle is solved

    return None  # No valid solution found

def solve_sudoku_ids(puzzle):
    depth_limit = 1

    while True:
        result = depth_limited_search(puzzle, depth_limit)
        if result is not None:
            return result
        depth_limit += 1

def depth_limited_search(puzzle, depth_limit):
    return dls_recursive(puzzle, depth_limit)

def dls_recursive(puzzle, depth_limit, current_depth=0):
    if current_depth == depth_limit:
        return None

    if puzzle.is_solved():
        return puzzle

    empty_cell = find_empty_cell(puzzle.grid)
    row, col = empty_cell

    for num in range(1, 10):
        if puzzle.is_valid_number(row, col, num):
            new_puzzle = puzzle.copy()
            new_puzzle.set_value(row, col, num)

            result = dls_recursive(new_puzzle, depth_limit, current_depth + 1)
            if result is not None:
                return result

    return None

class SudokuNode:
    def __init__(self, puzzle, row, col):
        self.puzzle = puzzle
        self.row = row
        self.col = col
        self.g = 0  # Cost to reach this node from the start
        self.h = self.heuristic()  # Heuristic estimation of remaining cost
        self.f = self.g + self.h  # Combined cost

    def heuristic(self):
        # Calculate the number of empty cells in the puzzle
        empty_cells = sum(
            1 for row in self.puzzle.grid for value in row if value == 0)
        return empty_cells

    def expand(self):
        # Generate child nodes by trying all possible numbers in the current cell
        children = []
        possible_values = self.puzzle.get_possible_values(self.row, self.col)

        for value in possible_values:
            new_puzzle = self.puzzle.copy()
            new_puzzle.set_value(self.row, self.col, value)
            new_row, new_col = find_empty_cell(new_puzzle.grid)
            children.append(SudokuNode(new_puzzle, new_row, new_col))

        return children

    def __lt__(self, other):
        return self.f < other.f

def solve_sudoku_astar(puzzle):
    start_row, start_col = find_empty_cell(puzzle.grid)
    start_node = SudokuNode(puzzle, start_row, start_col)

    open_list = [start_node]
    closed_set = set()

    while open_list:
        current_node = heapq.heappop(open_list)

        if current_node.puzzle.is_solved():
            return current_node.puzzle

        closed_set.add(current_node.puzzle)

        for child_node in current_node.expand():
            if child_node.puzzle not in closed_set:
                child_node.g = current_node.g + 1
                child_node.f = child_node.g + child_node.h
                heapq.heappush(open_list, child_node)

    return None

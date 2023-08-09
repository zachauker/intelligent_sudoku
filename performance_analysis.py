import time
import sudoku_generator
from solving_algorithms import backtracking, constraint_propagation, solve_sudoku_dfs, solve_sudoku_bfs, solve_sudoku_ids, solve_sudoku_astar
import psutil

# Number of puzzles to generate and solve
num_puzzles = 100

# List of solver functions
solver_functions = [
    backtracking,
    constraint_propagation,
    solve_sudoku_dfs,
    solve_sudoku_bfs,
    solve_sudoku_ids,
    solve_sudoku_astar
]

dificulties = [
    "Easy",
    "Medium",
    "Hard"
]

def analyze_algorithm_speed(solving_function, difficulty):
    # Generate and solve puzzles
    for solver_function in solver_functions:
        total_time = 0
        for _ in range(num_puzzles):
            puzzle = sudoku_generator.generate_sudoku(difficulty)
            start_time = time.time()
            solving_function(puzzle)
            end_time = time.time()
            total_time += end_time - start_time
        avg_time = total_time / num_puzzles
        print(f"{solver_function.__name__}: Average Time: {avg_time:.6f} seconds")

def analyze_algorithm_performance(solving_function, difficulty):
    for _ in range(num_puzzles):
        puzzle = sudoku_generator.generate_sudoku(difficulty)
        process = psutil.Process()
        start_time = time.time()
        solving_function(puzzle)
        end_time = time.time()

        cpu_usage = process.cpu_percent()
        memory_usage = process.memory_info().rss / 1024 / 1024  # in MB

        print(f"{solving_function} CPU Usage: {cpu_usage}%")
        print(f"{solving_function} Memory Usage: {memory_usage:.2f} MB")
        print(f"{solving_function} Time taken: {end_time - start_time:.6f} seconds")

def analyze_algorithmn_accuracy(solving_function, difficulty):
    total_correct = 0
    total_time = 0
    for _ in range(num_puzzles):
        puzzle = sudoku_generator.generate_sudoku(difficulty)
        start_time = time.time()
        solving_function(puzzle)
        end_time = time.time()

        is_solution_correct = puzzle.is_solved()
        total_correct += is_solution_correct
        total_time += end_time - start_time

    accuracy = (total_correct / num_puzzles) * 100
    average_time = total_time / num_puzzles

    print(f"Algorithm: {solving_function}")
    print(f"Accuracy: {accuracy:.2f}%")
    print(f"Average Time: {average_time:.6f} seconds")
    print("-----------------------------")

def main():
    # analyze_algorithm_speed()
    # analyze_algorithm_performance()
    analyze_algorithmn_accuracy(backtracking, "Easy")
    exit

if __name__ == "__main__":
    main()

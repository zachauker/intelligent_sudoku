import time
import sudoku_generator
from solving_algorithms import backtracking, constraint_propagation, solve_sudoku_dfs, solve_sudoku_bfs, solve_sudoku_ids, solve_sudoku_astar
import psutil
import pandas as pd
import matplotlib.pyplot as plt

# Number of puzzles to generate and solve
num_puzzles = 10

# List of solver functions
solver_functions = [
    backtracking,
    constraint_propagation,
    solve_sudoku_dfs,
    solve_sudoku_bfs,
    solve_sudoku_ids,
    solve_sudoku_astar
]

def analyze_algorithms(solving_function, difficulty):
        total_time = 0
        total_mem = 0
        total_cpu = 0
        total_correct = 0

        for _ in range(num_puzzles):
            process = psutil.Process()
            puzzle = sudoku_generator.generate_sudoku(difficulty)
            start_time = time.time()
            solved = solving_function(puzzle)
            end_time = time.time()

            is_solution_correct = solved.is_solved()
            total_correct += is_solution_correct

            elapsed_time = end_time - start_time
            total_time += elapsed_time

            cpu_usage = process.cpu_percent(interval=elapsed_time)
            total_mem += process.memory_info().rss / 1024 / 1024  # in MB
            total_cpu += cpu_usage

        avg_cpu = total_cpu / num_puzzles
        avg_mem = total_mem / num_puzzles
        avg_time = total_time / num_puzzles
        accuracy = (total_correct / num_puzzles) * 100

        print(f"Algorithm: {solving_function.__name__}")
        print("Average Time: {avg_time:.6f} seconds")
        print("CPU Usage: {avg_cpu}%")
        print("Memory Usage: {avg_mem:.2f} MB")
        print(f"Accuracy: {accuracy:.2f}%")
        print("-----------------------------")

        return {
            "algorithm": solving_function.__name__,
            "average_cpu": avg_cpu,
            "average_mem": avg_mem,
            "avg_time": avg_time,
            "accuracy": accuracy
        }
        
def analyze_algorithm_speed(solving_function, difficulty):
    total_time = 0
    for _ in range(num_puzzles):
        puzzle = sudoku_generator.generate_sudoku(difficulty)
        start_time = time.time()
        solving_function(puzzle)
        end_time = time.time()

        elapsed_time = end_time - start_time
        total_time += elapsed_time

    avg_time = total_time / num_puzzles

    print(f"Algorithm: {solving_function.__name__}")
    print(f"{solving_function.__name__}: Average Time: {avg_time:.6f} seconds")
    print("-----------------------------")

    return {
        "algorithm": solving_function.__name__,
        "average_time": avg_time
    }

def analyze_algorithm_performance(solving_function, difficulty):
    total_mem = 0
    total_cpu = 0
    for _ in range(num_puzzles):
        puzzle = sudoku_generator.generate_sudoku(difficulty)
        process = psutil.Process()
        start_time = time.time()
        solving_function(puzzle)
        end_time = time.time()

        elapsed_time = end_time - start_time
        cpu_usage = process.cpu_percent(interval=elapsed_time)

        total_mem += process.memory_info().rss / 1024 / 1024  # in MB
        total_cpu += cpu_usage
    
    avg_cpu = total_cpu / num_puzzles
    avg_mem = total_mem / num_puzzles

    print(f"Algorithm: {solving_function.__name__}")
    print(f"{solving_function.__name__} CPU Usage: {avg_cpu}%")
    print(f"{solving_function.__name__} Memory Usage: {avg_mem:.2f} MB")
    print("-----------------------------")

    return {
        "algorithm": solving_function.__name__,
        "average_cpu": avg_cpu,
        "average_mem": avg_mem
    }

def analyze_algorithmn_accuracy(solving_function, difficulty):
    total_correct = 0
    for _ in range(num_puzzles):
        puzzle = sudoku_generator.generate_sudoku(difficulty)
        start_time = time.time()
        solving_function(puzzle)
        end_time = time.time()

        is_solution_correct = puzzle.is_solved()
        total_correct += is_solution_correct

    accuracy = (total_correct / num_puzzles) * 100

    print(f"Algorithm: {solving_function.__name__}")
    print(f"Accuracy: {accuracy:.2f}%")
    print("-----------------------------")

    return {
        "algorithm": solving_function.__name__,
        "accuracy": accuracy
    }

def process_performance_results(performance):
    df = pd.DataFrame(performance)
    # Create subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # Plot for Algorithm vs Average CPU
    df.plot(kind='bar', x='algorithm', y='average_cpu', ax=ax1)
    ax1.set_xlabel('Algorithms')
    ax1.set_ylabel('Average CPU Performance')
    ax1.set_title('Algorithm vs Avg CPU Performance')
    ax1.tick_params(axis='x', rotation=45)

    # Plot for Algorithm vs Average Memory
    df.plot(kind='bar', x='algorithm', y='average_mem', color='orange', ax=ax2)
    ax2.set_xlabel('Algorithms')
    ax2.set_ylabel('Average Memory Usage')
    ax2.set_title('Algorithm vs Avg Memory Usage')
    ax2.tick_params(axis='x', rotation=45)

    # Adjust layout
    plt.tight_layout()

    # Show the plots
    plt.show()

def main():
    # Run performance analysis and add results for each algorithm to list.
    performance_results = []
    for solving_function in solver_functions:
        results = analyze_algorithms(solving_function, "Easy")
    
    exit

if __name__ == "__main__":
    main()

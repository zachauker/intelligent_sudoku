import time
import sudoku_generator
from solving_algorithms import backtracking, constraint_propagation, solve_sudoku_dfs, solve_sudoku_bfs, solve_sudoku_ids, solve_sudoku_astar
import psutil
import pandas as pd
import matplotlib.pyplot as plt

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
        print(f"Average Time: {avg_time:.6f} seconds")
        print(f"CPU Usage: {avg_cpu}%")
        print(f"Memory Usage: {avg_mem:.2f} MB")
        print(f"Accuracy: {accuracy:.2f}%")
        print("-----------------------------")

        return {
            "algorithm": solving_function.__name__,
            "average_cpu": avg_cpu,
            "average_mem": avg_mem,
            "avg_time": avg_time,
            "accuracy": accuracy,
            "difficulty": difficulty
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


def generate_visualizations(data, difficulty):
    # Create subplots
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    # Plot average CPU usage
    axs[0, 0].bar([entry["algorithm"] for entry in data], [
                  entry["average_cpu"] for entry in data])
    axs[0, 0].set_title(f"Average CPU Usage ({difficulty})")
    axs[0, 0].set_ylabel("Usage (%)")
    axs[0, 0].tick_params(axis='x', rotation=40)

    # Plot average memory consumption
    axs[0, 1].bar([entry["algorithm"] for entry in data], [
                  entry["average_mem"] for entry in data])
    axs[0, 1].set_title(f"Average Memory Consumption ({difficulty})")
    axs[0, 1].set_ylabel("Memory (MB)")
    axs[0, 1].tick_params(axis='x', rotation=40)
    axs[0, 1].set_ylim(78, 86)

    # Plot average solving time
    axs[1, 0].bar([entry["algorithm"] for entry in data],
                  [entry["avg_time"] for entry in data])
    axs[1, 0].set_title(f"Average Solving Time ({difficulty})")
    axs[1, 0].set_ylabel("Time (s)")
    axs[1, 0].tick_params(axis='x', rotation=40)

    # Plot accuracy
    axs[1, 1].bar([entry["algorithm"] for entry in data],
                  [entry["accuracy"] for entry in data])
    axs[1, 1].set_title(f"Accuracy ({difficulty})")
    axs[1, 1].set_ylabel("Accuracy")
    axs[1, 1].tick_params(axis='x', rotation=40)

    # Adjust layout
    plt.tight_layout()

    # Show plots
    plt.show()

def main():
    # Run performance analysis and add results for each algorithm to list.
    # easy_performance_results = []
    # for solving_function in solver_functions:
    #     easy_results = analyze_algorithms(solving_function, "Easy")
    #     easy_performance_results.append(easy_results)
    # generate_visualizations(easy_performance_results, "Easy")

    medium_performance_results = []
    for solving_function in solver_functions:
        medium_results = analyze_algorithms(solving_function, "Medium")
        medium_performance_results.append(medium_results)
    generate_visualizations(medium_performance_results, "Medium")
    
    # hard_performance_results = []
    # for solving_function in solver_functions:
    #     hard_results = analyze_algorithms(solving_function, "Hard")
    #     hard_performance_results.append(hard_results)
    
    exit

if __name__ == "__main__":
    main()

import pygame
import sys
import pandas as pd
from sudoku_generator import generate_sudoku, get_hint
import solving_algorithms

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Initialize Pygame
pygame.init()

# Set up the window
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 800
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Sudoku")

# Set up fonts
FONT_LARGE = pygame.font.Font(None, 48)
FONT_MEDIUM = pygame.font.Font(None, 32)
FONT_SMALL = pygame.font.Font(None, 24)

# Define cell sizes and margins
CELL_SIZE = 60
CELL_MARGIN = 10

# Define difficulty levels
DIFFICULTY_EASY = "Easy"
DIFFICULTY_MEDIUM = "Medium"
DIFFICULTY_HARD = "Hard"
PLAYER_HINT = "Hint"
SOLVE_PUZZLE = "Solve"

# Define Sudoku puzzle grid position and size
# Calculate the grid position to center it in the window
GRID_SIZE = CELL_SIZE * 9 + CELL_MARGIN * 10
GRID_X = (WINDOW_WIDTH - GRID_SIZE) // 2
GRID_Y = (WINDOW_HEIGHT - GRID_SIZE) // 2

# Generate a Sudoku puzzle with medium difficulty by default
difficulty = DIFFICULTY_MEDIUM
puzzle = generate_sudoku(difficulty)

# Selected cell and number
selected_cell = None
selected_number = None

# Define the key mappings
KEY_MAPPING = {
    pygame.K_1: 1,
    pygame.K_2: 2,
    pygame.K_3: 3,
    pygame.K_4: 4,
    pygame.K_5: 5,
    pygame.K_6: 6,
    pygame.K_7: 7,
    pygame.K_8: 8,
    pygame.K_9: 9,
    pygame.K_BACKSPACE: None
}

# Define the Button class
class Button:
    def __init__(self, text, position, width, height, color, hover_color, callback):
        self.text = text
        self.position = position
        self.width = width
        self.height = height
        self.color = color
        self.hover_color = hover_color
        self.callback = callback

    def draw(self, surface):
        if self.is_hovered():
            pygame.draw.rect(surface, self.hover_color, (self.position[0], self.position[1], self.width, self.height))
        else:
            pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], self.width, self.height))
        font = FONT_SMALL
        text = font.render(self.text, True, BLACK)
        text_rect = text.get_rect(center=(self.position[0] + self.width // 2, self.position[1] + self.height // 2))
        surface.blit(text, text_rect)

    def is_hovered(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.position[0] <= mouse_pos[0] <= self.position[0] + self.width \
               and self.position[1] <= mouse_pos[1] <= self.position[1] + self.height

# Difficulty button callbacks
def easy_button_callback():
    global puzzle, difficulty
    difficulty = DIFFICULTY_EASY
    puzzle = generate_sudoku(difficulty)
    reset_selection()

def medium_button_callback():
    global puzzle, difficulty
    difficulty = DIFFICULTY_MEDIUM
    puzzle = generate_sudoku(difficulty)
    reset_selection()

def hard_button_callback():
    global puzzle, difficulty
    difficulty = DIFFICULTY_HARD
    puzzle = generate_sudoku(difficulty)
    reset_selection()

# Hint button callback function
def hint_button_callback():
    global hint_button
    hint_row, hint_col, hint_value = get_hint(puzzle)
    # Display hint on the user interface
    puzzle.set_value(hint_row, hint_col, hint_value)
    hint_row, hint_col, hint_value = None, None, None
    reset_selection()

def solve_button_callback():
    global puzzle, show_dialog
    show_dialog = True
    if show_dialog:
        for button in dialog.buttons:
            if button.is_hovered() and pygame.mouse.get_pressed()[0]:
                algorithm_selected = button.text  # This will store the selected algorithm
                show_dialog = False  # Close the dialog
    # puzzle.solve_sudoku()

def backtracking_callback():
    global show_dialog
    solving_algorithms.backtracking(puzzle)
    show_dialog = False

def constraint_callback():
    global show_dialog
    solving_algorithms.constraint_propagation(puzzle)
    show_dialog = False

def bfs_callback():
    global show_dialog
    solved = solving_algorithms.solve_sudoku_bfs(puzzle)

    # Iterate over each cell in the solved grid and update the puzzle's grid
    for row in range(9):
        for col in range(9):
            value = solved.get_value(row, col)
            puzzle.set_value(row, col, value)

    show_dialog = False

def dfs_callback():
    global show_dialog
    solved = solving_algorithms.solve_sudoku_dfs(puzzle)

    for row in range(9):
        for col in range(9):
            value = solved.get_value(row, col)
            puzzle.set_value(row, col, value)
    
    show_dialog = False

def ids_callback():
    global show_dialog
    solved = solving_algorithms.solve_sudoku_ids(puzzle)

    for row in range(9):
        for col in range(9):
            value = solved.get_value(row, col)
            puzzle.set_value(row, col, value)

    show_dialog = False

        
# Define difficulty button size.
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40
BUTTON_MARGIN = 20

# Create the main UI buttons
buttons = [
    Button(DIFFICULTY_EASY, (0, 0), BUTTON_WIDTH, BUTTON_HEIGHT, GRAY, GREEN, easy_button_callback),
    Button(DIFFICULTY_MEDIUM, (0, 0), BUTTON_WIDTH, BUTTON_HEIGHT, GRAY, GREEN, medium_button_callback),
    Button(DIFFICULTY_HARD, (0, 0), BUTTON_WIDTH, BUTTON_HEIGHT, GRAY, GREEN, hard_button_callback),
    Button(PLAYER_HINT, (0, 0), BUTTON_WIDTH, BUTTON_HEIGHT, GRAY, GREEN, hint_button_callback),
    Button(SOLVE_PUZZLE, (0, 0), BUTTON_WIDTH, BUTTON_HEIGHT, GRAY, GREEN, solve_button_callback)
]

# To Do see if there is a better way to do this - feels corny 
hint_button = buttons[3]
solve_button = buttons[4]

# Calculate the total buttons' width and margin to center them horizontally
total_buttons_width = (BUTTON_WIDTH + BUTTON_MARGIN) * \
    len(buttons) - BUTTON_MARGIN
buttons_start_x = (WINDOW_WIDTH - total_buttons_width) // 2

# Calculate the buttons' Y position based on the grid size
BUTTON_Y = GRID_Y + GRID_SIZE + 20

# Calculate the buttons' X position based on the start position and index
for i, button in enumerate(buttons):
    BUTTON_X = buttons_start_x + (BUTTON_WIDTH + BUTTON_MARGIN) * i
    button.position = (BUTTON_X, BUTTON_Y)

class Dialog:
    def __init__(self, title, options):
        self.title = title
        self.options = options
        self.buttons = []

        for idx, option in enumerate(options):
            button_x = WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2
            button_y = WINDOW_HEIGHT // 2 + idx * \
                (BUTTON_HEIGHT + BUTTON_MARGIN)
            button = Button(option["text"], (button_x, button_y),
                            BUTTON_WIDTH, BUTTON_HEIGHT, GRAY, GREEN, option["callback"])
            self.buttons.append(button)

    def show(self, surface):
        dialog_rect = pygame.Rect(
            WINDOW_WIDTH // 4, WINDOW_HEIGHT // 4, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        pygame.draw.rect(surface, GRAY, dialog_rect)

        title_text = FONT_LARGE.render(self.title, True, BLACK)
        title_rect = title_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
        surface.blit(title_text, title_rect)

        for button in self.buttons:
            button.draw(surface)

dialog = Dialog("Select Solve Algorithm", [
        {"text": "Backtracking", "callback": backtracking_callback},
        {"text":"Constraint Propagation", "callback": constraint_callback},
        {"text": "BFS Algorithm", "callback": bfs_callback},
        {"text": "DFS Algorithm", "callback": dfs_callback},
        {"text": "IDS Algorithm", "callback": ids_callback}
    ])

# Function to get the clicked cell
def get_clicked_cell(pos):
    x, y = pos
    if GRID_X <= x <= GRID_X + GRID_SIZE and GRID_Y <= y <= GRID_Y + GRID_SIZE:
        col = (x - GRID_X - CELL_MARGIN) // (CELL_SIZE + CELL_MARGIN)
        row = (y - GRID_Y - CELL_MARGIN) // (CELL_SIZE + CELL_MARGIN)
        if 0 <= col < 9 and 0 <= row < 9:
            return row, col
    return None

# Function to reset the selected cell and number
def reset_selection():
    global selected_cell, selected_number
    selected_cell = None
    selected_number = None

# Function to draw the Sudoku grid
def draw_grid():
    for row in range(9):
        for col in range(9):
            cell_x = GRID_X + col * (CELL_SIZE + CELL_MARGIN)
            cell_y = GRID_Y + row * (CELL_SIZE + CELL_MARGIN)

            # Draw the cell background
            pygame.draw.rect(
                window, WHITE, (cell_x, cell_y, CELL_SIZE, CELL_SIZE))

            # Draw the main grid lines
            if row % 3 == 0 and row != 0:
                pygame.draw.line(window, BLACK, (GRID_X, cell_y),
                                 (GRID_X + GRID_SIZE, cell_y), 3)
            if col % 3 == 0 and col != 0:
                pygame.draw.line(window, BLACK, (cell_x, GRID_Y),
                                 (cell_x, GRID_Y + GRID_SIZE), 3)

            # Draw the lighter cell grid lines
            if row != 0:
                pygame.draw.line(window, GRAY, (cell_x, cell_y),
                                 (cell_x + CELL_SIZE, cell_y), 1)
            if col != 0:
                pygame.draw.line(window, GRAY, (cell_x, cell_y),
                                 (cell_x, cell_y + CELL_SIZE), 1)

            # Draw the selected cell
            if selected_cell == (row, col):
                pygame.draw.rect(
                    window, GREEN, (cell_x, cell_y, CELL_SIZE, CELL_SIZE), 3)

            value = puzzle.get_value(row, col)

            # Determine the color for the number
            if (row, col) == selected_cell:
                number_color = BLUE  # Selected number color
            elif puzzle.is_initial_value(row, col):
                number_color = RED  # Initial puzzle value color
            else:
                number_color = BLACK  # Editable cell number color or user-entered value color

            # Draw the numbers
            if value != 0:
                cell_text = FONT_LARGE.render(str(value), True, number_color)
                text_rect = cell_text.get_rect(
                    center=(cell_x + CELL_SIZE // 2, cell_y + CELL_SIZE // 2))
                window.blit(cell_text, text_rect)

            # Draw the selected number
            if selected_cell == (row, col) and selected_number is not None:
                number_color = RED if puzzle.is_initial_value(row, col) else BLACK
                number_text = FONT_SMALL.render(
                    str(selected_number), True, RED)
                number_rect = number_text.get_rect(
                    center=(cell_x + CELL_SIZE // 2, cell_y + CELL_SIZE // 2))
                window.blit(number_text, number_rect)

hint_row, hint_col, hint_value = None, None, None
running = True
show_dialog = False

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:  # Left mouse button
                pos = pygame.mouse.get_pos()
                clicked_cell = get_clicked_cell(pos)
                if clicked_cell is not None:
                    selected_cell = clicked_cell
                    selected_number = None
                # Click handling for all generated buttons on main window.
                for button in buttons:
                    if button.is_hovered() and pygame.mouse.get_pressed()[0]:
                        button.callback()
                if show_dialog and dialog:
                    for button in dialog.buttons:
                        if button.is_hovered() and pygame.mouse.get_pressed()[0]:
                            button.callback()
            elif pygame.mouse.get_pressed()[2]:  # Right mouse button
                pos = pygame.mouse.get_pos()
                clicked_cell = get_clicked_cell(pos)
                if clicked_cell is not None:
                    selected_cell = clicked_cell
                    selected_number = puzzle.get_value(clicked_cell[0], clicked_cell[1])
        # Keyboard events
        elif event.type == pygame.KEYDOWN:
            if event.key in KEY_MAPPING:
                if selected_cell is not None:
                    selected_number = KEY_MAPPING[event.key]
                    if puzzle.get_value(selected_cell[0], selected_cell[1]) != 0:
                        selected_number = None
            elif event.key == pygame.K_RETURN:
                if selected_cell is not None and selected_number is not None:
                    puzzle.set_value(selected_cell[0], selected_cell[1], selected_number)
                    reset_selection()
            elif event.key == pygame.K_ESCAPE:
                # Close the dialog if Escape key is pressed
                show_dialog = False
    
    # Fill the pygame canavs white.
    window.fill(WHITE)
    
    # Draws Sudoku grid and writes in initial numbers. 
    draw_grid()

    # Draw the buttons
    for button in buttons:
        button.draw(window)
    
    # Checks if dialog window should be shown and if so renders it. 
    if show_dialog and dialog is not None:
        dialog.show(window)

    pygame.display.flip()

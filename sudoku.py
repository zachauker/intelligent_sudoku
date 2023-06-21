import pygame
import sys
import random
import pandas as pd
from sudoku_generator import generate_sudoku

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

# Define Sudoku puzzle grid position and size
GRID_X = CELL_MARGIN
GRID_Y = CELL_MARGIN
GRID_SIZE = CELL_SIZE * 9 + CELL_MARGIN * 10

# Define difficulty button position and size
BUTTON_X = 160
BUTTON_Y = 620
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40
BUTTON_MARGIN = 20

# Generate a Sudoku puzzle with medium difficulty by default
difficulty = DIFFICULTY_MEDIUM
puzzle = generate_sudoku(difficulty)

# Selected cell and number
selected_cell = None
selected_number = None

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

# Create the difficulty buttons
buttons = [
    Button(DIFFICULTY_EASY, (BUTTON_X, BUTTON_Y), BUTTON_WIDTH, BUTTON_HEIGHT, GRAY, GREEN, easy_button_callback),
    Button(DIFFICULTY_MEDIUM, (BUTTON_X + BUTTON_WIDTH + BUTTON_MARGIN, BUTTON_Y), BUTTON_WIDTH, BUTTON_HEIGHT, GRAY, GREEN, medium_button_callback),
    Button(DIFFICULTY_HARD, (BUTTON_X + 2 * (BUTTON_WIDTH + BUTTON_MARGIN), BUTTON_Y), BUTTON_WIDTH, BUTTON_HEIGHT, GRAY, GREEN, hard_button_callback)
]

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
            pygame.draw.rect(window, WHITE, (cell_x, cell_y, CELL_SIZE, CELL_SIZE))
            if selected_cell == (row, col):
                pygame.draw.rect(window, GREEN, (cell_x, cell_y, CELL_SIZE, CELL_SIZE), 3)
            value = puzzle.loc[row, col]
            if value != 0:
                if (row, col) == selected_cell:
                    cell_text = FONT_LARGE.render(str(value), True, BLUE)
                else:
                    cell_text = FONT_LARGE.render(str(value), True, BLACK)
                text_rect = cell_text.get_rect(center=(cell_x + CELL_SIZE // 2, cell_y + CELL_SIZE // 2))
                window.blit(cell_text, text_rect)
            if selected_cell == (row, col) and selected_number is not None:
                number_text = FONT_SMALL.render(str(selected_number), True, RED)
                number_rect = number_text.get_rect(center=(cell_x + CELL_SIZE // 2, cell_y + CELL_SIZE // 2))
                window.blit(number_text, number_rect)

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
    pygame.K_DELETE: None,
    pygame.K_BACKSPACE: None
}

# Main game loop
while True:
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
            elif pygame.mouse.get_pressed()[2]:  # Right mouse button
                pos = pygame.mouse.get_pos()
                clicked_cell = get_clicked_cell(pos)
                if clicked_cell is not None:
                    selected_cell = clicked_cell
                    selected_number = puzzle.loc[clicked_cell[0], clicked_cell[1]]
        elif event.type == pygame.KEYDOWN:
            if event.key in KEY_MAPPING:
                if selected_cell is not None:
                    selected_number = KEY_MAPPING[event.key]
                    if puzzle.loc[selected_cell[0], selected_cell[1]] != 0:
                        selected_number = None
            elif event.key == pygame.K_RETURN:
                if selected_cell is not None and selected_number is not None:
                    puzzle.loc[selected_cell[0], selected_cell[1]] = selected_number
                    reset_selection()

    window.fill(WHITE)

    draw_grid()

    # Draw the difficulty buttons
    for button in buttons:
        button.draw(window)
        if button.is_hovered() and pygame.mouse.get_pressed()[0]:
            button.callback()

    pygame.display.flip()

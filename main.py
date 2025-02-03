import pygame
import sys
from board import Board

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((640, 640))
pygame.display.set_caption("Chess")

# Load piece images
IMAGES = {}
for piece in ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']:
    IMAGES[piece] = pygame.transform.scale(pygame.image.load(f'images/{piece}.png'), (80, 80))

board = Board()
selected_square = None

def get_square(pos):
    x, y = pos
    return y // 80, x // 80

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            row, col = get_square(pygame.mouse.get_pos())
            if selected_square:
                board.handle_move(selected_square, (row, col))
                selected_square = None
            else:
                if board.get_piece((row, col)):
                    selected_square = (row, col)

    board.draw(screen, IMAGES)
    pygame.display.flip()

# main.py
import pygame
import sys
from board import create_initial_board, draw_board, draw_pieces

# Constants
WIDTH, HEIGHT = 640, 640
SQUARE_SIZE = WIDTH // 8

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

# Load Images
IMAGES = {}
PIECES = ["b_pawn", "b_rook", "b_knight", "b_bishop", "b_queen", "b_king",
          "w_pawn", "w_rook", "w_knight", "w_bishop", "w_queen", "w_king"]

for piece in PIECES:
    IMAGES[piece] = pygame.transform.scale(
        pygame.image.load(f"images/{piece}.png"), (SQUARE_SIZE, SQUARE_SIZE)
    )

# Game State
board = create_initial_board()
selected_square = None


def get_square_under_mouse(pos):
    x, y = pos
    return y // SQUARE_SIZE, x // SQUARE_SIZE


def main():
    global selected_square
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col = get_square_under_mouse(pygame.mouse.get_pos())
                if selected_square:
                    start_row, start_col = selected_square
                    board[row][col] = board[start_row][start_col]
                    board[start_row][start_col] = " "
                    selected_square = None
                else:
                    if board[row][col] != " ":
                        selected_square = (row, col)

        draw_board(screen)
        draw_pieces(screen, board, IMAGES)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()

# board.py
import pygame

WHITE = (232, 235, 239)
BLACK = (125, 135, 150)
SQUARE_SIZE = 80
ROWS, COLS = 8, 8


def create_initial_board():
    return [
        ["b_rook", "b_knight", "b_bishop", "b_queen", "b_king", "b_bishop", "b_knight", "b_rook"],
        ["b_pawn"] * 8,
        [" "] * 8,
        [" "] * 8,
        [" "] * 8,
        [" "] * 8,
        ["w_pawn"] * 8,
        ["w_rook", "w_knight", "w_bishop", "w_queen", "w_king", "w_bishop", "w_knight", "w_rook"]
    ]


def draw_board(screen):
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_pieces(screen, board, images):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != " ":
                screen.blit(images[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))

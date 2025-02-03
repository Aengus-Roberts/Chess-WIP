# board.py
import pygame
from pieces import Pawn, Rook, Knight, Bishop, Queen, King

WHITE = (232, 235, 239)
BLACK = (125, 135, 150)
SQUARE_SIZE = 80
ROWS, COLS = 8, 8


class Board:
    def __init__(self):
        self.grid = self.create_initial_board()
        self.turn = "w"  # 'w' for white's turn, 'b' for black
        self.last_move = None  # Stores the last move as ((start_row, start_col), (end_row, end_col))

    def create_initial_board(self):
        # Set up pieces on the board
        return [
            [Rook('b'), Knight('b'), Bishop('b'), Queen('b'), King('b'), Bishop('b'), Knight('b'), Rook('b')],
            [Pawn('b') for _ in range(8)],
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [Pawn('w') for _ in range(8)],
            [Rook('w'), Knight('w'), Bishop('w'), Queen('w'), King('w'), Bishop('w'), Knight('w'), Rook('w')]
        ]

    def get_piece(self, position):
        row, col = position
        return self.grid[row][col]

    def handle_move(self, start, end):
        piece = self.get_piece(start)
        if piece and piece.color == self.turn:
            legal_moves = piece.get_legal_moves(start, self.grid)
            if end in legal_moves:
                # Simulate the move
                captured_piece = self.grid[end[0]][end[1]]
                self.grid[end[0]][end[1]] = piece
                self.grid[start[0]][start[1]] = None

                if self.is_in_check(self.turn):
                    # Undo move if it leaves the king in check
                    self.grid[start[0]][start[1]] = piece
                    self.grid[end[0]][end[1]] = captured_piece
                    print("Illegal move: You cannot put your king in check!")
                    return

                # Track the last move
                self.last_move = (start, end)

                # Move is valid
                self.turn = 'b' if self.turn == 'w' else 'w'

                # Check for checkmate after the move
                if self.is_checkmate(self.turn):
                    print(f"Checkmate! {piece.color.upper()} wins!")
                    return  # Game over
                if self.is_stalemate(self.turn):
                    print("Stalemate! It's a draw.")
                    return  # Game over
            else:
                print("Illegal move!")
        else:
            print("Not your turn or no piece selected!")

    def draw(self, screen, images):
        # Drawing board squares
        colors = [(240, 217, 181), (181, 136, 99)]  # Light and dark squares

        if self.last_move:
            (start_row, start_col), (end_row, end_col) = self.last_move
            highlight_color = pygame.Color(246, 246, 105)  # Light yellow highlight

            square_size = screen.get_width() // 8

            # Highlight the start square
            pygame.draw.rect(screen, highlight_color,
                             pygame.Rect(start_col * square_size, start_row * square_size, square_size, square_size))

            # Highlight the end square
            pygame.draw.rect(screen, highlight_color,
                             pygame.Rect(end_col * square_size, end_row * square_size, square_size, square_size))


        # Draw the rest of the board
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                square_size = screen.get_width() // 8

                # Avoid overwriting the highlighted squares
                if not self.last_move or (row, col) not in self.last_move:
                    pygame.draw.rect(screen, color,
                                     pygame.Rect(col * square_size, row * square_size, square_size, square_size))

                # Draw the pieces
                piece = self.grid[row][col]
                if piece:
                    screen.blit(piece.image, (col * square_size, row * square_size))

    def is_in_check(self, color):
        # 1. Find the king's position
        king_pos = None
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece and piece.color == color and isinstance(piece, King):
                    king_pos = (row, col)
                    break
            if king_pos:
                break

        # 2. Check if any enemy piece can attack the king
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece and piece.color != color:
                    moves = piece.get_legal_moves((row, col), self.grid)
                    if king_pos in moves:
                        return True  # King is under attack
        return False  # King is safe

    def is_checkmate(self, color):
        if not self.is_in_check(color):
            return False  # Not checkmate if the king isn't in check

        # Check if the player has ANY legal move to escape check
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece and piece.color == color:
                    legal_moves = piece.get_legal_moves((row, col), self.grid)
                    for move in legal_moves:
                        # Simulate each move
                        captured_piece = self.grid[move[0]][move[1]]
                        self.grid[move[0]][move[1]] = piece
                        self.grid[row][col] = None

                        if not self.is_in_check(color):  # King is safe after this move
                            # Undo the move
                            self.grid[row][col] = piece
                            self.grid[move[0]][move[1]] = captured_piece
                            return False  # Not checkmate, there’s a valid move

                        # Undo move if it doesn't help
                        self.grid[row][col] = piece
                        self.grid[move[0]][move[1]] = captured_piece

        return True  # No legal moves found, it's checkmate!

    def is_stalemate(self, color):
        if self.is_in_check(color):
            return False  # Not stalemate if the king is in check

        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece and piece.color == color:
                    legal_moves = piece.get_legal_moves((row, col), self.grid)
                    for move in legal_moves:
                        # Simulate move
                        captured_piece = self.grid[move[0]][move[1]]
                        self.grid[move[0]][move[1]] = piece
                        self.grid[row][col] = None

                        if not self.is_in_check(color):
                            # Undo move
                            self.grid[row][col] = piece
                            self.grid[move[0]][move[1]] = captured_piece
                            return False  # Found a legal move

                        # Undo move
                        self.grid[row][col] = piece
                        self.grid[move[0]][move[1]] = captured_piece

        return True  # No legal moves and not in check = stalemate

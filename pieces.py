import pygame

SQUARE_SIZE = 80

class Piece:
    def __init__(self, color):
        self.color = color
        self.symbol = self.__class__.symbol  # Ensure each subclass defines 'symbol'
        self.image = self.load_image()

    def load_image(self):
        color_prefix = 'w' if self.color == 'w' else 'b'  # For white or black pieces

        # Use the symbol as the file name, e.g., 'w_R.png' for a white rook
        path = f"images/{color_prefix}{self.symbol}.png"
        try:
            image = pygame.image.load(path)
            image = pygame.transform.smoothscale(image, (SQUARE_SIZE, SQUARE_SIZE))
            return image
        except pygame.error:
            print(f"Image not found for {path}")
            return None

    def get_legal_moves(self, position, board):
        raise NotImplementedError("This method should be implemented by subclasses.")


def slide_moves(position, board, directions, color):
    moves = []
    row, col = position

    for d_row, d_col in directions:
        r, c = row + d_row, col + d_col
        while 0 <= r < 8 and 0 <= c < 8:
            target = board[r][c]
            if target is None:
                moves.append((r, c))
            elif target.color != color:
                moves.append((r, c))
                break
            else:
                break
            r += d_row
            c += d_col
    return moves


class Pawn(Piece):
    symbol = "P"

    def get_legal_moves(self, position, board):
        moves = []
        row, col = position
        direction = -1 if self.color == 'w' else 1

        # Move forward
        if 0 <= row + direction < 8 and board[row + direction][col] is None:
            moves.append((row + direction, col))

            # Double move from starting position
            if (self.color == 'w' and row == 6) or (self.color == 'b' and row == 1):
                if board[row + 2 * direction][col] is None:
                    moves.append((row + 2 * direction, col))

        # Captures
        for dx in [-1, 1]:
            new_col = col + dx
            if 0 <= new_col < 8 and 0 <= row + direction < 8:
                target = board[row + direction][new_col]
                if target and target.color != self.color:
                    moves.append((row + direction, new_col))

        return moves


class Rook(Piece):
    symbol = "R"

    def get_legal_moves(self, position, board):
        return slide_moves(position, board, [(-1, 0), (1, 0), (0, -1), (0, 1)], self.color)


class Bishop(Piece):
    symbol = "B"

    def get_legal_moves(self, position, board):
        return slide_moves(position, board, [(-1, -1), (-1, 1), (1, -1), (1, 1)], self.color)


class Queen(Piece):
    symbol = "Q"

    def get_legal_moves(self, position, board):
        return slide_moves(position, board, [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)],
                           self.color)


class Knight(Piece):
    symbol = "N"

    def get_legal_moves(self, position, board):
        moves = []
        row, col = position
        knight_moves = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]

        for dr, dc in knight_moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if target is None or target.color != self.color:
                    moves.append((r, c))
        return moves


class King(Piece):
    symbol = "K"

    def get_legal_moves(self, position, board):
        moves = []
        row, col = position
        king_moves = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for dr, dc in king_moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if target is None or target.color != self.color:
                    moves.append((r, c))

        return moves

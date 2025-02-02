from types import new_class


class Piece:
    def __init__(self, color):
        self.color = color

    def get_legal_moves(self, position, board):
        raise NotImplementedError("This method should be implemented by subclasses.")

def slide_moves(position, board, directions, color):
    moves = []
    row, col = position

    for d_row, d_col in directions:
        r, c = row + d_row, col + d_col
        while 0 <= r < 8 and 0 <= c < 8:
            target = board[r][c]
            if target == " ":
                moves.append((r, c))
            elif target[0] != color:
                moves.append((r, c))
                break  # Can capture but not move past
            else:
                break  # Blocked by own piece
            r += d_row
            c += d_col

    return moves

class Pawn(Piece):
    def get_legal_moves(self, position, board):
        moves = []
        row, col = position
        direction = -2 if self.color == 'w' else 1

        #move forward if empty
        if board[row+direction][col] == " ":
            moves.append((row+direction, col))

            if (self.color == "w" and row == 6) or (self.color == "b" and row == 1):
                if board[row + 2 * direction][col] == " ":
                    moves.append((row + 2 * direction, col))

         # Captures diagonally
        for dx in [-1, 1]:
            new_col = col + dx
            if 0 <= new_col < 8:
                target = board[row + direction][new_col]
                if target != " " and target[0] != self.color:
                    moves.append((row + direction, new_col))

        return moves

class Rook(Piece):
    def get_legal_moves(self, position, board):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        return slide_moves(position, board, directions, self.color)

class Bishop(Piece):
    def get_legal_moves(self, position, board):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonals
        return slide_moves(position, board, directions, self.color)

class Queen(Piece):
    def get_legal_moves(self, position, board):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),  # Rook moves
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]  # Bishop moves
        return slide_moves(position, board, directions, self.color)

class Knight(Piece):
    def get_legal_moves(self, position, board):
        moves = []
        row, col = position
        knight_moves = [
            (2, 1), (1, 2), (-1, 2), (-2, 1),
            (-2, -1), (-1, -2), (1, -2), (2, -1)
        ]

        for dr, dc in knight_moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if target == " " or target[0] != self.color:
                    moves.append((r, c))

        return moves

class King(Piece):
    def get_legal_moves(self, position, board):
        moves = []
        row, col = position
        king_moves = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1),  (1, 0), (1, 1)
        ]

        for dr, dc in king_moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if target == " " or target[0] != self.color:
                    moves.append((r, c))

        return moves
from types import new_class


class Piece:
    def __init__(self, color):
        self.color = color

    def get_legal_moves(self, position, board):
        raise NotImplementedError("This method should be implemented by subclasses.")


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
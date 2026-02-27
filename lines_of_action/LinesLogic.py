"""
Author: Adam Klepáč
Date: Feb 26, 2026.
Board class.
Board data:
  1=black, -1=white, 0=empty
  first dim is column , 2nd is row:
     stones[1][7] is the square in column 2,
     at the opposite end of the board in row 8.
Squares are stored and manipulated as (x,y) tuples.
x is the column, y is the row.
"""

import numpy as np


class Board:
    # list of all 8 directions on the board, as (x,y) offsets
    __directions = [
        (1, 1),
        (1, 0),
        (1, -1),
        (0, -1),
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, 1),
    ]

    def __init__(self, n):
        "Set up initial board configuration."

        self.n = n
        # Create the empty board array.
        self.stones = np.zeros(shape=(n, n))

        # Set up the initial stones.abs
        for x in range(1, n - 1):
            self.stones[x, 0] = 1
            self.stones[x, n - 1] = 1

        for y in range(1, n - 1):
            self.stones[0, y] = -1
            self.stones[n - 1, y] = -1

    # add [][] indexer syntax to the Board
    def __getitem__(self, index):
        return self.stones[index]

    def countDiff(self, color):
        """Counts the # pieces of the given color
        (1 for black, -1 for white, 0 for empty spaces)"""
        count = 0
        for y in range(self.n):
            for x in range(self.n):
                if self[x, y] == color:
                    count += 1
                if self[x, y] == -color:
                    count -= 1
        return count

    def get_legal_moves(self, color):
        """Returns all the legal moves for the given color.
        (1 for black, -1 for white)
        """
        moves = set()  # stores the legal moves.

        # Get all the squares with pieces of the given color.
        for y in range(self.n):
            for x in range(self.n):
                if self[x, y] == color:
                    newmoves = self.get_moves_for_square((x, y))
                    moves.update(newmoves)
        return list(moves)

    def has_legal_moves(self, color):
        for y in range(self.n):
            for x in range(self.n):
                if self[x, y] == color:
                    newmoves = self.get_moves_for_square((x, y))
                    if len(newmoves) > 0:
                        return True
        return False

    def get_moves_for_square(self, square):
        """Returns all the legal moves that use the given square as a base."""
        x, y = square

        # determine the color of the piece.
        color = self[x, y]

        # skip empty source squares.
        if color == 0:
            return None

        moves = set()

        # Get sum for all directions.
        hor_sum = np.sum(np.absolute(self.stones[:, y]), dtype=int)
        ver_sum = np.sum(np.absolute(self.stones[x]), dtype=int)
        main_diag_sum = np.sum(np.absolute(self.stones.diagonal(y - x)), dtype=int)
        aux_diag_sum = np.sum(
            np.absolute(np.flipud(self.stones).diagonal(x + y - self.n + 1)), dtype=int
        )

        # Calculate jump lengths for direction
        jumps_for_direction = {
            (0, -1): ver_sum,
            (1, -1): aux_diag_sum,
            (1, 0): hor_sum,
            (1, 1): main_diag_sum,
            (0, 1): ver_sum,
            (-1, 1): aux_diag_sum,
            (-1, 0): hor_sum,
            (-1, -1): main_diag_sum,
        }

        # Check directions for blocking enemy stones
        for dir, jump_length in jumps_for_direction.items():
            viable = True
            tmp_x, tmp_y = x, y
            for j in range(jump_length):
                tmp_x += dir[0]
                tmp_y += dir[1]
                if not (0 <= tmp_x < self.n and 0 <= tmp_y < self.n):
                    viable = False
                    break

                if self[tmp_x, tmp_y] == -color and j != jump_length - 1:
                    viable = False
                    break
            if viable and self[tmp_x, tmp_y] != color:
                moves.add(((x, y), (tmp_x, tmp_y)))

        # return the generated move list
        return moves

    def execute_move(self, move, color):
        """Perform the given move on the board.
        Color gives the color of the piece to play (1=black,-1=white)
        """

        source, target = move
        self.stones[*source] = 0
        self.stones[*target] = color

from __future__ import print_function
import sys

sys.path.append("..")
from Game import Game
from .LinesLogic import Board
import numpy as np
from collections import deque


class LinesGame(Game):
    square_content = {1: "", +0: "-", -1: ""}

    @staticmethod
    def getSquarePiece(stone):
        return LinesGame.square_content[stone]

    def __init__(self, n):
        self.n = n

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(self.n)
        return b.stones

    @property
    def board_size(self):
        # (a,b) tuple
        return (self.n, self.n)

    def getBoardSize(self):
        return self.board_size

    @property
    def action_size(self):
        # return number of actions
        return (self.n * self.n) ** 2

    def getActionSize(self):
        return self.action_size

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        source = (action % self.n, (action // self.n) % self.n)
        target = ((action // self.n**2) % self.n, action // self.n**3)

        b = Board(self.n)
        b.stones = np.copy(board)
        # action must be valid
        valid_moves = b.get_legal_moves(player)
        if (source, target) not in valid_moves:
            return (board, -player)

        move = (source, target)
        b.execute_move(move, player)
        return (b.stones, -player)

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0] * self.action_size
        b = Board(self.n)
        b.stones = np.copy(board)
        legalMoves = b.get_legal_moves(player)
        for source, target in legalMoves:
            sx, sy = source
            tx, ty = target
            valids[sx + sy * self.n + tx * self.n**2 + ty * self.n**3] = 1
        return np.array(valids)

    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        b = Board(self.n)
        b.stones = np.copy(board)

        if b.has_connected_stones(player):
            return 1
        elif b.has_connected_stones(-player):
            return -1
        else:
            return 0

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        return player * board

    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert len(pi) == self.action_size
        pi_board = np.reshape(pi, (self.n**2, self.n**2))
        l = []

        for i in range(1, 5):
            for j in [True, False]:
                newB = np.rot90(board, i)
                newPi = np.copy(pi_board)

                pi_subarray = newPi[0:self.n, 0:self.n]
                new_subarray = np.rot90(pi_subarray, i)
                newPi[0:self.n, 0:self.n] = pi_subarray

                pi_subarray = newPi[self.n:, self.n:]
                new_subarray = np.rot90(pi_subarray, i)
                newPi[self.n:, self.n:] = pi_subarray
                if j:
                    newB = np.fliplr(newB)
                    newPi = np.copy(pi_board)
                    pi_subarray = newPi[0:self.n, 0:self.n]
                    new_subarray = np.fliplr(pi_subarray)
                    newPi[0:self.n, 0:self.n] = pi_subarray

                    pi_subarray = newPi[self.n:, self.n:]
                    new_subarray = np.fliplr(pi_subarray)
                    newPi[self.n:, self.n:] = pi_subarray
                l += [(newB, list(newPi.ravel()))]
        return l

    def stringRepresentation(self, board):
        return np.array2string(board)

    def stringRepresentationReadable(self, board):
        board_s = "".join(
            self.square_content[square] for row in board for square in row
        )
        return board_s

    @staticmethod
    def display(board):
        n = board.shape[0]
        print("   ", end="")
        for y in range(n):
            print(y, end=" ")
        print("")
        print("-----------------------")
        for y in range(n):
            print(y, "|", end="")  # print the row #
            for x in range(n):
                piece = board[x][y]  # get the piece to print
                print(LinesGame.square_content[piece], end=" ")
            print("|")

        print("-----------------------")

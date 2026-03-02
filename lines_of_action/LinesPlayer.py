import numpy as np
import subprocess
from collections import defaultdict


class RandomPlayer:
    def __init__(self, game):
        self.game = game

    def play(self, board):
        a = np.random.randint(self.game.action_size)
        valids = self.game.getValidMoves(board, 1)
        while valids[a] != 1:
            a = np.random.randint(self.game.action_size)
        return a


class HumanLinesPlayer:
    def __init__(self, game):
        self.game = game

    def play(self, board):
        # display(board)
        valid = self.game.getValidMoves(board, 1)
        n = self.game.n
        valid_dict = defaultdict(list)

        for i in range(0, self.game.action_size):
            if valid[i]:
                valid_dict[((i % n), (i // n) % n)].append(((i // n**2) % n, i // n**3))
        for (x_from, y_from), to_list in valid_dict.items():
            print(
                f"From: ({x_from}, {y_from}), To: {", ".join([f"({x_to}, {y_to})" for (x_to, y_to) in to_list])}"
            )
        while True:
            input_from = input("From: ")
            input_to = input("To: ")
            n = self.game.n
            try:
                sx, sy = tuple(int(i) for i in input_from.split(" "))
                tx, ty = tuple(int(i) for i in input_to.split(" "))
                if not (0 <= sx < n and 0 <= sy < n):
                    print("Invalid move.")
                    continue
                if not (0 <= tx < n and 0 <= ty < n):
                    print("Invalid move.")
                    continue

                move = sx + sy * n + tx * n**2 + ty * n**3
                if valid[move] != 1:
                    print("Invalid move.")
                    continue
                break
            except ValueError:
                "Invalid move."
            print("Invalid move")
        return move

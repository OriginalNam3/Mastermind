import random
from collections import Counter


class Mastermind:
    def __init__(self):
        self.c = [0, 1, 2, 3, 4, 5, 6, 7]
        self.rn = 4
        self.t = 0
        self.code = ''
        self.g = []
        self.state = True

    def gen_code(self):
        self.code = [random.choice(self.c) for _ in range(self.rn)]

    def check(self, guess):
        self.t += 1
        cc = sum((Counter(self.code) & Counter(guess)).values())
        c = sum([t == g for t, g in zip(self.code, guess)])
        cc -= c
        self.g.append([guess, [c, cc]])
        if c == self.rn or self.t >= 10: self.state = False
        return c, cc

    def get_guesses(self):
        return self.g

    def is_game_over(self):
        return not self.state

    def valid(self, c):
        for char in c:
            if char not in self.c:
                return False
        return True

    def reset(self):
        self.g = []
        self.t = 0
        self.state = True
        self.gen_code()

    def get_last_guess(self):
        return self.g[-1]

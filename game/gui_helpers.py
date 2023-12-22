import random

import pygame
from pygame.locals import *

class Board:
    size = (600, 400)

    def __init__(self, position, bowls=[], banks=[]):
        self.pos = position
        self.bowls = bowls
        self.banks = banks

    def render(self):
        board = pygame.Surface(self.size)
        for bowl in self.bowls:
            pygame.draw.circle(board, (0, 0, 255), bowl.pos, bowl.size)
            for piece in bowl.pieces:
                pygame.draw.circle(board, (0, 0, 20), piece.pos, piece.size)
        for bank in self.banks:
            pygame.draw.circle(board, (0, 0, 255), bank.pos, bank.size)
            for piece in bank.pieces:
                pygame.draw.circle(board, (0, 0, 20), piece.pos, piece.size)
        return board


class Bowl:
    size = 20

    def __init__(self, id, owner, starting_value, position):
        self.id = id
        self.owner = owner
        self.value = starting_value
        self.pos = position
        self.pieces = []
        for i in range(self.value):
            p = Piece()
            p.gen_pos(self.size, self.pos)
            self.pieces.append(p)


class Bank:
    size = 40

    def __init__(self, owner, position):
        self.owner = owner
        self.pos = position
        self.value = 0
        self.pieces = []


class Piece:
    size = 5

    def __init__(self, position=(0,0)):
        self.pos = position

    def gen_pos(self, parent_size, parent_position):
        x = random.randrange(parent_position[0] - 0.5*parent_size, parent_position[0] + 0.5*parent_size)
        y = random.randrange(parent_position[1] - 0.5*parent_size, parent_position[1] + 0.5*parent_size)
        self.pos = (x, y)

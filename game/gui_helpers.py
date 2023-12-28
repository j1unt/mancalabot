import math
import random

import pygame
from pygame.locals import *

class Board:
    BOARD_COLOR = (117, 98, 46)
    POSITION_COLOR_1 = (90, 94, 204)
    POSITION_COLOR_2 = (201, 83, 92)
    PIECE_COLOR = (39, 29, 107)
    FONT_COLOR = (0,0,0)

    def __init__(self, parent_size, font_name):
        # Set board size and position
        self.size = (0.8 * parent_size[0], 0.5 * parent_size[1])
        self.pos = (0.5 * parent_size[0] - 0.5 * self.size[0], 0.5 * parent_size[1] - 0.5 * self.size[1])
        self.font = pygame.font.SysFont(font_name, 20)

        # Create bowls, banks, and pieces
        # Banks: 20% of width each
        # Bowls: 10% of width each
        """
         0 1 2 3 4 5 6 7 8 9
        | | | | | | | | | | |
        --B--b-b-b-b-b-b--B--
        """
        self.bowls = []
        for i in range(12):
            x_offset = 0.25 + 0.1 * i if i < 6 else 0.25 + 0.1 * (11 - i)
            y_offset = 0.3 if i < 6 else 0.7
            b = Bowl(i,
                     1 if i < 6 else 2,
                       4,
                       0.04 * self.size[0],
                       (x_offset * self.size[0], y_offset * self.size[1]),
                       self.POSITION_COLOR_1 if i < 6 else self.POSITION_COLOR_2,
                       (self.font, self.FONT_COLOR)
                    )
            self.bowls.append(b)

        self.banks = [
            Bank(1, 0.09 * self.size[0], (0.9 * self.size[0], 0.5 * self.size[1]), self.POSITION_COLOR_1, (self.font, self.FONT_COLOR)), 
            Bank(2, 0.09 * self.size[0], (0.1 * self.size[0], 0.5 * self.size[1]), self.POSITION_COLOR_2, (self.font, self.FONT_COLOR))
            ]
    

    def render(self):
        board = pygame.Surface(self.size)
        board.fill(self.BOARD_COLOR)
        # Draw bowls
        for i, bowl in enumerate(self.bowls):
            pygame.draw.circle(board, bowl.color, bowl.pos, bowl.radius)
            label = bowl.label()
            board.blit(label[0], label[1])
            for piece in bowl.pieces:
                pygame.draw.circle(board, self.PIECE_COLOR, piece.pos, piece.radius)
        # Draw banks
        pygame.draw.circle(board, self.POSITION_COLOR_1, self.banks[0].pos, self.banks[0].radius)
        pygame.draw.circle(board, self.POSITION_COLOR_2, self.banks[1].pos, self.banks[1].radius)
        for bank in self.banks:
            label = bank.label()
            board.blit(label[0], label[1])
            for piece in bank.pieces:
                pygame.draw.circle(board, self.PIECE_COLOR, piece.pos, piece.radius)
        return board


class Bowl:

    def __init__(self, id, owner, starting_value, radius, position, color, font):
        self.id = id
        self.owner = owner
        self.value = starting_value
        self.radius = radius
        self.pos = position
        self.pieces = []
        self.color = color
        self.font = font[0]
        self.font_color = font[1]
        self.add(self.value)

    def add(self, num):
        for i in range(num):
            p = Piece()
            p.gen_pos(self.radius, self.pos, self.pieces)
            self.pieces.append(p)
            self.value = len(self.pieces)

    def remove_all(self):
        self.pieces = []
        self.value = 0

    def label(self):
        label = self.font.render(f'{self.value}', 1, self.font_color)
        label_pos = (self.pos[0] - 0.5 * label.get_width(), self.pos[1] - 1.5 * self.radius - 0.5 * label.get_height())
        return (label, label_pos)


class Bank:

    def __init__(self, owner, radius, position, color, font):
        self.owner = owner
        self.radius = radius
        self.pos = position
        self.value = 0
        self.pieces = []
        self.color = color
        self.font = font[0]
        self.font_color = font[1]

    def add(self, num):
        for i in range(num):
            p = Piece()
            p.gen_pos(self.radius, self.pos, self.pieces)
            self.pieces.append(p)
            self.value = len(self.pieces)

    def remove_all(self):
        self.pieces = []
        self.value = 0

    def label(self):
        label = self.font.render(f'{self.value}', 1, self.font_color)
        label_pos = (self.pos[0] - 0.5 * label.get_width(), self.pos[1] - 1.2 * self.radius - 0.5 * label.get_height())
        return (label, label_pos)


class Piece:
    radius = 5

    def __init__(self, position=(0,0)):
        self.pos = position

    def gen_pos(self, parent_radius, parent_position, other_pieces):
        """
        Generates a random position within the parent circle for the piece to be placed, collision free
        Infinite loops if there are no valid positions
        """
        x = None
        y = None
        # Check for collisions
        while True:
            r = (parent_radius - self.radius) * math.sqrt(random.random())
            theta = random.random() * 2 * math.pi
            x = parent_position[0] + r * math.cos(theta)
            y = parent_position[1] + r * math.sin(theta)
            collision = False
            for p in other_pieces:
                dist = math.hypot(x - p.pos[0], y - p.pos[1])
                if dist < 2 * self.radius:
                    collision = True
                    break
            if not collision:
                break
        self.pos = (x, y)

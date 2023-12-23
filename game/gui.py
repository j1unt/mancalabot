import math

import pygame
from pygame.locals import *

from mancala import MancalaGame
from gui_helpers import Board, Bowl, Bank

class GUI:
    def __init__(self, width, height, mode, starting_player):
        if height > width:
            raise Exception('Invalid window size')
        self.width = width
        self.height = height
        self.mode = mode
        self.player = starting_player

    def run(self):
        # Start Mancala oracle
        game = MancalaGame(gui=True)
        game.start_game()

        # Setup
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(f'Mancala ({self.mode} mode)')
        screen.fill((46, 42, 39)) # Background color

        # Create initial board state
        board = Board((self.width, self.height))

        # Draw initial board state
        screen.blit(board.render(), board.pos)
        pygame.display.flip()

        # Main game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    for bowl in [b for b in board.bowls if b.id in game.get_options()]:
                        dist_x = pos[0] - (bowl.pos[0] + 0.1*self.width)
                        dist_y = pos[1] - (bowl.pos[1] + 0.25*self.height)
                        dist = math.hypot(dist_x, dist_y)
                        if dist <= bowl.radius:
                            # Run a game step
                            update = game.step(bowl.id)
                            # Update gui board
                            for i, a in enumerate(update[0]):
                                if a > 0 and i < 12:
                                    board.bowls[i].add(a)
                                elif a > 0 and i >= 12:
                                    board.banks[12 - i].add(a)
                            for i, r in enumerate(update[1]):
                                if r >= 1 and i < 12:
                                    board.bowls[i].remove_all()
                                elif r > 1 and i >= 12:
                                    board.banks[i - 12].remove_all()
                    screen.blit(board.render(), board.pos)
                    pygame.display.flip()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                elif event.type == QUIT:
                    running = False

g = GUI(1200, 700, 'fun', 1)
g.run()
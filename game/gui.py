import pygame
from pygame.locals import *

from gui_helpers import Board, Bowl, Bank

class GUI:
    def __init__(self, h, w):
        self.height = h
        self.width = w

    def run(self):
        # Setup
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        screen.fill((255, 255, 255))

        # Create initial board state
        bowls = [Bowl(1, 1, 2, (100,100))]
        board = Board((100, 200), bowls, [])

        # Draw initial board state
        screen.blit(board.render(), board.pos)
        pygame.display.flip()

        # Main game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                elif event.type == QUIT:
                    running = False

g = GUI(800,800)
g.run()
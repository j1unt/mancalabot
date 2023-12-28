import math

import pygame
from pygame.locals import *

from mancala import MancalaGame
from gui_helpers import Board, Bowl, Bank

class GUI:
    BACKGROUND_COLOR = (46, 42, 39)

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
        font_list = pygame.font.get_fonts()
        font_name = 'monospace'
        for f in font_list:
            if 'bold' in f:
                font_name = f
        font = pygame.font.SysFont(font_name, 30)
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(f'Mancala ({self.mode} mode)')

        # Create initial board state
        board = Board((self.width, self.height), font_name)

        # Draw initial board state
        self.render_screen(screen, font, game.player, board)
        pygame.display.flip()

        # Main game loop
        running = True
        finished = False
        while running:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1 and not finished:
                    pos = pygame.mouse.get_pos()
                    for bowl in [b for b in board.bowls if b.id in game.get_options()]:
                        dist_x = pos[0] - (bowl.pos[0] + 0.1*self.width)
                        dist_y = pos[1] - (bowl.pos[1] + 0.25*self.height)
                        dist = math.hypot(dist_x, dist_y)
                        if dist <= bowl.radius:
                            win_label = None
                            # Run a game step
                            update = game.step(bowl.id)
                            if update[0]:
                                win_label = font.render(f'Player {update[1]} wins!', 1, (0,255,255))
                                finished = True
                            if update[2] and update[3]:
                                # Update gui board
                                for i, a in enumerate(update[2]):
                                    if a > 0 and i < 12:
                                        board.bowls[i].add(a)
                                    elif a > 0 and i >= 12:
                                        board.banks[12 - i].add(a)
                                for i, r in enumerate(update[3]):
                                    if r >= 1 and i < 12:
                                        board.bowls[i].remove_all()
                                    elif r > 1 and i >= 12:
                                        board.banks[i - 12].remove_all()
                            self.render_screen(screen, font, game.player, board, win_label)
                            pygame.display.flip()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                elif event.type == QUIT:
                    running = False

    def render_screen(self, screen, font, player, board, win_label=None):
        screen.fill(self.BACKGROUND_COLOR)

        mancala_label = font.render('Mancala', 1, (255,255,0))
        screen.blit(mancala_label, (0.5 * self.width - 0.5 * mancala_label.get_width(), 0.1 * self.height))

        player_label = font.render(f'Player {player}\'s turn', 1, (0,255,255))
        screen.blit(player_label, (0.5 * self.width - 0.5 * player_label.get_width(), 0.8 * self.height))

        if win_label:
            screen.blit(win_label, (0.5 * self.width - 0.5 * win_label.get_width(), 0.05 * self.height - 0.5 * win_label.get_height()))

        screen.blit(board.render(), board.pos)
        
        return screen
            

g = GUI(1200, 700, 'fun', 1)
g.run()
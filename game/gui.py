import math
import time

import pygame
from pygame.locals import *

from mancala import MancalaGame
from gui_helpers import Board, Bowl, Bank

"""
A class to run the mancala engine in a GUI game loop
"""

class GUI:
    BACKGROUND_COLOR = (46, 42, 39)

    def __init__(self, width, height, mode, starting_player, delay=0.5):
        if height > width:
            raise Exception('Invalid window size')
        self.width = width
        self.height = height
        self.mode = mode
        self.player = starting_player
        self.delay = delay # Sets time.sleep() amount for automated moves

    def run(self):
        # Start Mancala oracle
        self.game = MancalaGame(mode=self.mode, gui=True, )
        self.game.start_game()

        # Setup
        pygame.init()
        font_list = pygame.font.get_fonts()
        self.font_name = 'monospace'
        for f in font_list:
            if 'bold' in f:
                font_name = f
        self.font = pygame.font.SysFont(font_name, 30)
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(f'Mancala ({self.mode} mode)')

        # Create initial board state
        self.board = Board((self.width, self.height), font_name)

        # Draw initial board state
        self.render_screen()
        pygame.display.flip()

        # Main game loop
        running = True
        finished = False
        while running:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1 and not finished:
                    pos = pygame.mouse.get_pos()
                    for bowl in [b for b in self.board.bowls if b.id in self.game.get_options()]:
                        dist_x = pos[0] - (bowl.pos[0] + 0.1*self.width)
                        dist_y = pos[1] - (bowl.pos[1] + 0.25*self.height)
                        dist = math.hypot(dist_x, dist_y)
                        if dist <= bowl.radius:
                            finished = self.game_step(bowl)
                            pygame.display.flip()
                            # If not in default mode, we need to step again to override manual P2 move
                            if self.mode == 'random' and self.game.player == 2 and not finished:
                                while self.game.player == 2 and not finished:
                                    time.sleep(self.delay)
                                    finished = self.game_step()
                                    pygame.display.flip()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                elif event.type == QUIT:
                    running = False

    def game_step(self, choice=None):
        """
        Performs a game step and returns a boolean to show whether or not the game ended
        Game is manual for both players by default.
        """
        
        finish = False
        win_label = None
        # Run a game step
        update = None
        if choice:
            update = self.game.step(choice.id)
        else:
            update = self.game.step()
        if update[0]:
            win_label = self.font.render(f'Player {update[1]} wins!', 1, (0,255,255))
            finish = True
        if update[2] and update[3]:
            # Update gui board
            for i, a in enumerate(update[2]):
                if a > 0 and i < 12:
                    self.board.bowls[i].add(a)
                elif a > 0 and i >= 12:
                    self.board.banks[12 - i].add(a)
            for i, r in enumerate(update[3]):
                if r >= 1 and i < 12:
                    self.board.bowls[i].remove_all()
                elif r > 1 and i >= 12:
                    self.board.banks[i - 12].remove_all()
        self.render_screen(win_label)
        return finish

    def render_screen(self, win_label=None):
        """
        Renders a new state on the screen
        """

        self.screen.fill(self.BACKGROUND_COLOR)

        mancala_label = self.font.render('Mancala', 1, (255,255,0))
        self.screen.blit(mancala_label, (0.5 * self.width - 0.5 * mancala_label.get_width(), 0.1 * self.height))

        player_label = self.font.render(f'Player {self.game.player}\'s turn', 1, (0,255,255))
        self.screen.blit(player_label, (0.5 * self.width - 0.5 * player_label.get_width(), 0.8 * self.height))

        if win_label:
            self.screen.blit(win_label, (0.5 * self.width - 0.5 * win_label.get_width(), 0.05 * self.height - 0.5 * win_label.get_height()))

        self.screen.blit(self.board.render(), self.board.pos)
        
        return self.screen
            

g = GUI(1200, 700, 'random', 1, delay=1)
g.run()
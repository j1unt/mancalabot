from mancala import MancalaGame

"""
Training script to generate random data

Outputs a log of games to './mancala_data_raw.json'
"""

NUM_GAMES = 10
TRAINING_MODE = 'random_training'

game = MancalaGame(1, NUM_GAMES, TRAINING_MODE)

game.gen_data()
game.get_log()
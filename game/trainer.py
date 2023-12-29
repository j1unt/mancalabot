from mancala import MancalaGame

NUM_GAMES = 10
TRAINING_MODE = 'random_training'
MAX_MOVES = 100

game = MancalaGame(1, NUM_GAMES, TRAINING_MODE)

game.gen_data(MAX_MOVES)
game.get_log()
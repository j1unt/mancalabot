from mancala import MancalaGame

NUM_GAMES = 10
TRAINING_MODE = 'random_training'

game = MancalaGame(1, NUM_GAMES, TRAINING_MODE)

game.gen_data()
game.get_log()
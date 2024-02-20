import pandas as pd
import torch

from mancala_dataset import MancalaDataset
from mancala_bot import MancalaBot

"""
Main file to run the bot
"""

training_data = MancalaDataset('./random_training_data.csv', './random_training_move_ratings.csv')
bot = MancalaBot(training_data, 16, 5, 0.1)
bot.train()
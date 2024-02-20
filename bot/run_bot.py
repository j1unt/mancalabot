import pandas as pd
import matplotlib.pyplot as plt
import torch

from mancala_dataset import MancalaDataset
from mancala_bot import MancalaBot

"""
Main file to run the bot
"""

training_data = MancalaDataset('./random_training_data.csv', './random_training_move_ratings.csv')
bot = MancalaBot(training_data, 64, 1, 0.03)
loss_data = bot.train(record_data=True)

# Plot log
y = loss_data[0][0]
x = loss_data[0][1]

plt.title('Batch vs Loss')
plt.xlabel('Batch')
plt.ylabel('Loss')
plt.plot(x, y, color='purple')
plt.show()
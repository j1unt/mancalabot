import os

import torch
import pandas as pd
import numpy as np
from torch.utils.data import Dataset, DataLoader
from torch import nn, optim

from mancala_dataset import MancalaDataset
from pipeline import MancalaPipeline

device = ('cuda' if torch.cuda.is_available() else 'cpu')

class MancalaBotModel(nn.Module):
    """
    A model to play Mancala

    Features:
    train()
     - runs a training session with the given parameters
    save()
     - saves the bot's current state
    get_move(board, options)
     - returns a selection based on the given moves and board state

    Structure:
    input layer:
    board, bank 1, bank 2 values
    player
    move
    outputs:
    [0,1] where 1 is the best move, 0 the worst
    loss:
    Each move is rated with:
    Minmax, normalized to 0.4 with range of -0.2, 0.2
    Win: Min(1, 1 + minmax())
    Loss: Max(0,  0 + minmax())

    Training:
    The bot takes in a list of moves (and associated state) and move ratings, and updates based on the calculated loss
    Choosing a move:
    The bot rates each possible move, then returns the most highly rated one.
    """
    def __init__(self):
        super().__init__()
        
        self.input_size = 18
        self.hidden_neurons = 48
        self.output_size = 1

        self.sigmoid = torch.sigmoid

        self.hidden_layer = nn.Linear(self.input_size, self.hidden_neurons, dtype=torch.float64)
        self.activation = nn.ReLU()
        self.output_layer = nn.Linear(self.hidden_neurons, self.output_size, dtype=torch.float64)
        
    def forward(self, x):
        
        # Pass data to hidden layer
        x = self.hidden_layer(x)

        # Use activation function on input
        x = self.activation(x)

        # Pass data to output layer
        x = self.output_layer(x)

        # Convert output to [0,1]
        x = self.sigmoid(x)

        return x
        
    def save(self, file_name='mancala_bot_model_save'):
        folder_path = './model_saves'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        file_name = os.path.join(folder_path, file_name)
        torch.save(self.state_dict(), file_name)

class MancalaBot:
    """
    Defines the bot that uses the model
    Will support training as well as single move evaluation
    """
    def __init__(self, data, batch_size, epochs, lr):
        self.model = MancalaBotModel()
        self.dataloader = DataLoader(data, batch_size)
        self.epochs = epochs
        self.lr = lr
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.lr)
        self.loss_fn = nn.MSELoss()

    def train_step(self, input, target):
        output = self.model(input)
        loss = self.loss_fn(output, target)
        loss.backward()
        self.optimizer.step()
        self.optimizer.zero_grad()
        return loss

    def train(self, save=False, record_data=False):
        log = []
        for t in range(self.epochs):
            losses = []
            batches = []
            for batch, (X, y) in enumerate(self.dataloader):
                current_loss = self.train_step(X, y)
                print(f'Batch: {batch} | Loss: {current_loss.item()}')
                if record_data:
                    losses.append(current_loss.item())
                    batches.append(batch)
            log.append((losses, batches))
        if save:
            self.model.save()
        if record_data:
            return log

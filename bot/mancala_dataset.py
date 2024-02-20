import os
import csv
import torch
import pandas as pd
import numpy as np
from torch.utils.data import Dataset, DataLoader

class MancalaDataset(Dataset):
    """
    Creates a torch dataset from a csv file for the bot to use
    """
    def __init__(self, csv_file, ratings_file):
        self.data = pd.read_csv(csv_file, header=None)
        self.data.rename(columns={0: 'bowl1',
                             1: 'bowl2',
                             2: 'bowl3',
                             3: 'bowl4',
                             4: 'bowl5',
                             5: 'bowl6',
                             6: 'bowl7',
                             7: 'bowl8',
                             8: 'bowl9',
                             9: 'bowl10',
                             10: 'bowl11',
                             11: 'bowl12',
                             12: 'bank1',
                             13: 'bank2',
                             14: 'choice',
                             15: 'refresh',
                             16: 'capture',
                             17: 'points_scored'}, inplace=True)
        self.ratings=[]
        with open(ratings_file, newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                self.ratings.append(row[0])

    def __getitem__(self, idx):
        input_item = torch.tensor(pd.DataFrame.to_numpy(self.data.iloc[[idx]]).flatten()).to(torch.float64)
        label = torch.tensor([float(self.ratings[idx])]).to(torch.float64)
        return (input_item, label)

    def __len__(self):
        return len(self.data)

m = MancalaDataset('./random_training_data.csv', './random_training_move_ratings.csv')
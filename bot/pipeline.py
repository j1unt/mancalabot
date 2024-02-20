import csv
import json

"""
Transforms readable JSON training data into a CSV file for the dataset
Calculates move ratings for each move in options
Generates loss values based on winner and move rating
"""

class MancalaPipeline:

    def __init__(self, file_name):
        with open(file_name) as json_file:
            self.data = json.load(json_file)

    def convert(self):
        input_data = []
        move_ratings = []
        for i in range(self.data['length']):
            game = self.data[f'game{i}']
            if len(game['states']) != len(game['moves']):
                print('Error: States and moves are different lengths!')
            for j in range(len(game['states'])):

                # Create input data
                curr = game['states'][j]['board']
                curr.append(game['states'][j]['bank1'])
                curr.append(game['states'][j]['bank2'])
                curr.append(game['moves'][j]['choice'])
                curr.append(1 if game['moves'][j]['refresh'] else 0)
                curr.append(1 if game['moves'][j]['capture'] else 0)
                points_scored = game['moves'][j]['additions'][12] + game['moves'][j]['additions'][13]
                curr.append(points_scored)
                input_data.append(curr)

                # Generate move rating
                won = game['moves'][j]['player'] == game['winner']
                move_ratings.append(self.rate_move(curr[4], curr[5], points_scored, won))

        with open('random_training_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for row in input_data:
                writer.writerow(row)
            file.close()
        with open('random_training_move_ratings.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for rating in move_ratings:
                writer.writerow([rating])
            file.close()

    def rate_move(self, refresh, capture, points_scored, won):
        """
        Returns a move rating to be used as a label
        This will be the function the bot approximates
        It is heavily based on wins/losses to be generalized,
        and avoid convergence to a definable function
        """

        rating = -0.2
        rating += 0.1 * refresh + 0.1 * capture + max(0.2, 0.05 * points_scored)
        if won:
            rating = min(1, rating + 1)
        else:
            rating = max(0, rating + 0)
        return rating

m = MancalaPipeline('./mancala_data_raw.json')
m.convert()
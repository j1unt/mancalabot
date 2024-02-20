import json
import random

from mancala_helpers import Position, Board

"""
Class to simulate Mancala games

Records data on:
 - Board states
  - Current player
  - Bowls & Banks
   - index
   - type
   - value
   - owner
 - Moves
  - Current player
  - Index chosen
  - Refresh
  - Capture
  - Additions
  - Removals

Modes:
    - Main modes
    'default': Runs a manual game
    'random': Runs a manual game against random moves
    'bot': Runs a manual game against the bot
    'bot_vs_bot': Runs a bot vs bot game
    - Training modes
    'random_training': Generates a dataset of games from fully random moves
    'bot_vs_random_training': Generates a dataset of bot vs random moves
    'bot_vs_bot_training': Generates a dataset of bot vs bot games

GUI:
    True: Runs the game in the GUI
    False: Runs the game in the console

"""
class MancalaGame:

    def __init__(self, starting_player=1, num_games=1, mode='default', gui=False, tickrate=0):
        self.starting_player = starting_player
        self.num_games = num_games
        self.mode = mode
        self.gui = gui
        self.tickrate = tickrate
        self.storage = []
        self.board = None


    def gen_data(self):
        """
        Runs (self.num_games) games if a training mode is selected.
        Data is recorded in storage, get_log() must be called externally to save it.
        """

        if self.mode not in ['random_training', 'bot_vs_random_training', 'bot_vs_bot_training']:
            print('Training mode not selected: Cannot generate data!')
            return
        else:
            for g in range(self.num_games):
                self.start_game(starting_player=self.starting_player)
                while(True):
                    update = self.step()
                    if update[0] == True:
                        break
        print('Training complete!')


    def start_game(self, starting_player=1):
        """
        Starts a game in the selected mode.

        Board layout by indices of positions, clockwise:
                  Player 1's board
        |       | 0  1  2  3  4  5 |       |
        |bank 2 |                  |bank 1 |
        |       | 11 10 9  8  7  6 |       |
                  Player 2's board
        """

        self.states = []
        self.moves = []
        self.player = starting_player
        
        # Create board
        self.board = Board()
        for i in range(0,6):
            self.board.add(Position(i, 'bowl', 4, 1, None))
        for i in range(6,12):
            self.board.add(Position(i, 'bowl', 4, 2, None))
        for i, p in enumerate(self.board.positions[:11]):
            p.next = self.board[i + 1]
        self.board.add(Position(12, 'store', 0, 1, self.board[6]))
        self.board.add(Position(13, 'store', 0, 2, self.board[0]))
        self.board[5].next = self.board[12]
        self.board[11].next = self.board[13]


    def step(self, move=None):
        """
        Performs an iteration of mancala:
        Accepts an optional move parameter. Ignored if the mode should generate a move here.
        Raises an error if the supplied move is not an option.
        Records state.
        Executes the move.
        Checks for a win.
        Ends the game if needed.
        Returns returns win state and (winner if True, 0 if False or tie), and additions/removals.
        """

        # Log board state
        self.states.append(
            {
                'board': self.board.flatten(),
                'bank1': self.board.bank1().value,
                'bank2': self.board.bank2().value,
                'player': self.player,
                'options': self.get_options(),
            }
        )

        # If board is empty, end the game
        if self.board.sum() <= 0:
            winner = self.end_game()
            return (True, winner, None, None)

        # Make a move
        if move == None:
            move = self.make_move(self.player)
        else:
            move = self.make_move(self.player, move)
        self.moves.append(move)
        # Switch player, or don't switch if player got a refresh
        if move[2] == False:
            if self.player == 1:
                self.player = 2
            elif self.player == 2:
                self.player = 1

        # Check for a win
        # Note - It's possible a game can be over before this check passes.
        # Ending the game at the exact point it's impossible for a player to win requires a much more robust check
        # May implement it, but it doesn't seem worth extra computation or time
        num_remaining = self.board.sum()
        if self.board.bank1().value - self.board.bank2().value > num_remaining:
            winner = self.end_game()
            return (True, winner, move[3], move[4])
        elif self.board.bank2().value - self.board.bank1().value  > num_remaining:
            winner = self.end_game()
            return (True, winner, move[3], move[4])
        
        # If the next player has no options, end the game
        if not self.get_options():
            winnings = self.board.sum()
            additions = [0] * 14
            if self.player == 1:
                self.board[13].value = self.board[13].value + winnings
                additions[13] = winnings
            elif self.player == 2:
                self.board[12].value = self.board[12].value + winnings
                additions[12] = winnings
            removals = self.board.clear_bowls()
            winner = self.end_game()
            for i in range(14):
                additions[i] += move[3][i]
                removals[i] += move[4][i]
            return (True, winner, additions, removals)

        # Return win state, winning player, additions and removals
        return (False, None, move[3], move[4])


    def make_move(self, player=0, move=None):
        """
        Generates a decision based on game mode, then executes the move on the board
        Returns a tuple containing the move log
        """

        # Make choice
        choice = None
        if ((self.mode == 'default') or (self.mode == 'random' and player == 1)) and not self.gui:
            options = self.get_options()
            self.display_board_console(player, options)
            while(choice not in options):
                choice = int(input())
        elif ((self.mode == 'default') or (self.mode == 'random' and player == 1)) and self.gui and move != None:
            choice = move
        elif self.mode == 'random' and player == 2:
            choice = random.choice([i + 6 for i, b in enumerate(self.board.bowls2()) if b.value != 0])
        elif self.mode == 'random_training':
            if player == 1:
                choice = random.choice([i for i, b in enumerate(self.board.bowls1()) if b.value != 0])
            elif player == 2:
                choice = random.choice([i + 6 for i, b in enumerate(self.board.bowls2()) if b.value != 0])
        else:
            raise Exception('make_move: Invalid move or mode: ' + str(self.mode) + ' Player ' + str(player) + ' move: ' + str(move))

        # Execute move
        additions = [0] * 14
        removals = [0] * 14

        curr = self.board[choice]
        amount = curr.value
        curr.value = 0
        removals[curr.index] += 1
        curr = curr.next
        
        refresh = False
        capture = False
        final_position = None
        count = 0
        while count < amount:
            if curr.index == self.board.bank1().index and player != 1:
                curr = curr.next
            elif curr.index == self.board.bank2().index and player != 2:
                curr = curr.next
            else:
                final_position = curr
                curr.increment()
                additions[curr.index] += 1
                curr = curr.next
                count += 1
        
        # Check for capture or turn refresh on the final position
        # Refresh if player ended in their own store
        # Capture if player ended in their own empty bowl adjacent to a non-empty enemy bowl
        if final_position.owner == player and final_position.type == 'store':
            refresh = True
            if self.mode == 'default' and not self.gui:
                print('Refresh!')
        elif final_position.owner == player and final_position.value == 1 and final_position.type == 'bowl':
            amount_won = self.board[11 - final_position.index].value + 1
            if amount_won > 1:
                capture = True
                if self.mode == 'default' and not self.gui:
                    print(f'Captured {amount_won} pieces!')
                self.board[11 - final_position.index] = 0
                self.board[final_position.index] = 0
                removals[11 - final_position.index] += 1
                removals[final_position.index] += 1
                if player == 1:
                    self.board[self.board.bank1().index].value += amount_won
                    additions[self.board.bank1().index] += amount_won
                elif player == 2:
                    self.board[self.board.bank2().index].value += amount_won
                    additions[self.board.bank2().index] += amount_won

        return (choice, refresh, capture, additions, removals, player)
    

    def end_game(self):
        """
        Handles a game finish.
        """

        # Decide winner
        winner = 0
        if self.board.bank1().value > self.board.bank2().value:
            winner = 1
        elif self.board.bank2().value > self.board.bank1().value:
            winner = 2

        if self.mode == 'default' and not self.gui:
            print(f'Player {winner} won!')
        elif self.mode == 'random_training':
            print(f'Game {len(self.storage)} complete. Winner: Player {winner}')

        final_moves = []
        for i, move in enumerate(self.moves):
            final_moves.append({
                'index': i,
                'choice': move[0],
                'refresh': move[1],
                'capture': move[2],
                'additions': move[3],
                'removals': move[4],
                'player': move[5],
            })
        self.storage.append(
            {
                'id': len(self.storage),
                'mode': self.mode,
                'starting_player': self.starting_player,
                'winner': winner,
                'states': self.states,
                'moves': final_moves,
            }
        )

        return winner


    def get_options(self):
        """
        Returns the current player's valid options for moves
        """

        options = None
        if self.player == 1:
            options = [i for i, b in enumerate(self.board.bowls1()) if b.value != 0]
        elif self.player == 2:
            options = [i + 6 for i, b in enumerate(self.board.bowls2()) if b.value != 0]
        return options
    

    def get_log(self, filename='mancala_data_raw.json'):
        """
        Saves a JSON log of all the games
        """

        with open(filename, 'w') as file:
            res = {}
            for i, game in enumerate(self.storage):
                res[f'game{i}'] = game
            res['length'] = len(self.storage)
            json.dump(res, file)
            file.close()


    def display_board_console(self, player=None, options=None):
        """
        Displays the board state in console
        """

        print('Board: (clockwise)')
        print(f'Bank 2: {self.board.bank2().value}')
        print(f'^ 11: {self.board[11].value}  |  0: {self.board[0].value} P')
        print(f'| 10: {self.board[10].value}  |  1: {self.board[1].value} 1')
        print(f'|  9: {self.board[9].value}  |  2: {self.board[2].value} |')
        print(f'|  8: {self.board[8].value}  |  3: {self.board[3].value} |')
        print(f'P  7: {self.board[7].value}  |  4: {self.board[4].value} |')
        print(f'2  6: {self.board[6].value}  |  5: {self.board[5].value} V')
        print(f'Bank 1: {self.board.bank1().value}\n')
        print(f'Player {str(player)}, choose a bowl to move: ')
        print(str(options) + '\n')
        print('Choice: ')

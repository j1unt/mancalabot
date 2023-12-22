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


    def run_game(self, max_moves=100, starting_player=1):
        """
        Runs a game in the selected mode.

        Board layout by indices of positions, clockwise:
                  Player 1's board
        |       | 0  1  2  3  4  5 |       |
        |bank 2 |                  |bank 1 |
        |       | 11 10 9  8  7  6 |       |
                  Player 2's board
        """
        states = []
        moves = []
        player = starting_player
        
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

        # Main game loop
        while(self.board.sum() > 0):

            # Log board state
            states.append(
                {
                    'board': self.board.flatten(),
                    'bank1': self.board.bank1().value,
                    'bank2': self.board.bank2().value,
                    'player': player,
                }
            )

            # Make a move
            move = self.make_move(player)
            moves.append(move)
            # Don't switch if player got a refresh
            if move[2] == False:
                if player == 1:
                    player = 2
                elif player == 2:
                    player = 1

            # Check for a win
            num_remaining = self.board.sum()
            if self.board.bank1().value - self.board.bank2().value > num_remaining:
                self.end_game(states, moves, 1)
                return
            elif self.board.bank2().value - self.board.bank1().value  > num_remaining:
                self.end_game(states, moves, 2)
                return
        # If tied or broken
        self.end_game(states, moves, 0)


    def end_game(self, states=None, moves=None, winner=None):
        """
        Handles a game finish.
        """
        if self.mode == 'default' and not self.gui:
            print(f'Player {winner} won!')
        self.storage.append(
            {
                'id': len(self.storage),
                'mode': self.mode,
                'starting_player': self.starting_player,
                'states': states,
                'moves': moves,
                'winner': winner,
            }
        )


    def make_move(self, player=0):
        """
        Generates a decision based on game mode, then executes the move on the board
        Returns a tuple containing the move log
        """
        # Make choice
        choice = None
        if self.mode == 'default' and not self.gui:
            options = None
            if player == 1:
                options = [i for i, b in enumerate(self.board.bowls1()) if b.value != 0]
            elif player == 2:
                options = [i + 6 for i, b in enumerate(self.board.bowls2()) if b.value != 0]
            self.display_board_console(player, options)
            while(choice not in options):
                choice = int(input())
        elif self.mode == 'random':
            if player == 1:
                choice = random.choice([i for i, b in enumerate(self.board.bowls1()) if b.value != 0])
            elif player == 2:
                choice = random.choice([i + 6 for i, b in enumerate(self.board.bowls2()) if b.value != 0])
        else:
            raise('make_move: Invalid mode: ' + str(self.mode))

        # Execute move
        curr = self.board[choice]
        amount = curr.value
        curr.value = 0
        curr = curr.next
        
        refresh = False
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
                if self.mode == 'default' and not self.gui:
                    print(f'Captured {amount_won} pieces!')
                self.board[11 - final_position.index] = 0
                self.board[final_position.index] = 0
                if player == 1:
                    self.board[self.board.bank1().index].value += amount_won
                elif player == 2:
                    self.board[self.board.bank2().index].value += amount_won

        return (player, choice, refresh)
    

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

# Main code
game = MancalaGame()
game.run_game()
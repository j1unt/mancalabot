"""
Helper classes for the mancala engine
"""

# Defines each position a piece can be in on the board. Types are Banks and Bowls.
class Position:
    def __init__(self, index, type, value, owner, next):
        self.index = index
        self.type = type
        self.value = value
        self.owner = owner
        self.next = next

    def increment(self):
        self.value += 1
    
# Defines a container for the linked list of positions.
class Board:
    def __init__(self):
        self.positions = []

    def __setitem__(self, key, val):
        self.positions[key].value = val
    
    def __getitem__(self, key):
        return self.positions[key]
    
    def add(self, val):
        self.positions.append(val)
    
    # Sum excludes banks
    def sum(self):
        sum = 0
        for i in range(0,12):
            sum += self.positions[i].value
        return sum
    
    # Returns a list of bowl values
    def flatten(self):
        return [self.positions[i].value for i in range(0,12)]
    
    # Clears all bowls and returns an array representing the removals
    def clear_bowls(self):
        removals = [0] * 14
        for i, pos in enumerate(self.positions):
            if pos.value > 0 and i < 12:
                removals[pos.index] = pos.value
                pos.value = 0
        return removals
    
    # These correspond to player 1 and 2
    def bank1(self):
        return self.positions[12]
    
    def bank2(self):
        return self.positions[13]
    
    def bowls1(self):
        return self.positions[0:6]
    
    def bowls2(self):
        return self.positions[6:12]

import math
import numpy as np
class Metrics:
  
    def __init__(self):
        self.min_wins = 0
        self.max_wins = 0
        self.count = 0
        
    def update(self, score):
        if score > 0:
            self.max_wins += 1
        elif score < 0:
            self.min_wins += 1
        self.count += 1
       
    def get_p_win(self, player):
        try:
            if player == 'min':
                return self.min_wins / self.count
            elif player == 'max':
                return self.max_wins / self.count
            else:
                raise ValueError('player {} must be min or max'.format(player))
        except ZeroDivisionError:
            raise ValueError('must be updated at least once \
                              to get win probability')

    def get_expected_value(self, player):
        try:
            if player == 'min':
                return (self.min_wins - self.max_wins) / self.count
            elif player == 'max':
                return (self.max_wins -self.min_wins) / self.count
            else:
                raise ValueError('player {} must be min or max'.format(player))
        except ZeroDivisionError:
            raise ValueError('must be updated at least once \
                              to get expected value')

    def get_explore_term(self, parent, c=1.41):
        if parent.count:
            return c * (math.log(parent.count) / self.count) ** (1 / 2)
        else:
            return 0 
        
        
    def get_ucb(self, player, parent, c=1.41, default=6):
        if self.count:
            p_win = self.get_p_win(player)
            explore_term = self.get_explore_term(parent)
            return p_win + explore_term
        else:
            return default
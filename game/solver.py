from src.constants import *
from uuid import uuid4
from random import randint
from src.objects import  Player

# class POMDPPlayer(Player):
#     def __init__(self, name, player_num):
#         # Create a new player
#         # Initialize variables for things like learning rate and Q-table

#         super().__init__(name, player_num)

#         # Initialize variables
#         self.learning_rate = 0.1
#         self.discount_rate = 0.99
        
#         # Initialize Q-table
#         self.q_table = {}
            
#     def get_options(self):
#         #OVERWRITES PLAYERS METHOD
#         #get all possible actions 
		
#     def make_a_move(self):
#         #choose an action via q learning 
		
#     def make_bet(self):
#         #OVERWRITES PLAYERS METHOD
#         #calcualte a bet based on current bank
		
class Random(Player):
    def __init__(self, name, player_num):
        super().__init__(name, player_num)
    
    def make_bet(self, amount):
        self.bet = randint(5, self.money)
    
    def get_options(self):
        ret = [CMD.HIT, CMD.STAND]
        sums = set(self.sums())
        if len(self.cards) == 2 and self.money >= self.bet and (9 in sums or 10 in sums or 11 in sums):
            ret.append(CMD.DOUBLE)
        self.options = ret
        choice = randint(0, len(self.options)-1)
        return ord(self.options[choice].value)

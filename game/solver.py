from src.constants import *
from uuid import uuid4
from random import randint
from src.objects import Player, Card
from game import Game

class POMDPPlayer(Player):
    def __init__(self, name, player_num, game: Game):
        # Create a new player
        # Initialize variables for things like learning rate and Q-table

        super().__init__(name, player_num)

        # Initialize variables
        self.learning_rate = 0.1
        self.discount_rate = 0.99
        
        # Initialize Q-table
        self.q_table = {}

        self.seen = []
        self.numdecks = game.get_num_decks()
        self.numCards = self.numdecks * 52
        self.numSeen = 0
        self.allCards = []

        for deck in self.numdecks:
            for num in list(range(2,11)) + ['J','Q','K','A']:
                for suit in SUIT:
                    self.allCards.append(Card(suit, num))
		
    def make_a_move(self, options):
        #choose an action via q learning 
        action = None
        return action
    
    def update_seen(self):
        self.numSeen = self.numSeen + 1

        if self.numSeen == self.numCards:
            self.seen = []

    def get_options(self, game: Game):
        #OVERWRITES PLAYERS METHOD
        #get all possible actions 
        options = []

        #add cards on the table to seen 
        ontable = []
        numontable = 0

        for p in game.players:
            for card in p.cards:
                if card not in self.seen and card.facedown is False:
                    self.seen.append(card)
                    self.update_seen()
                    ontable.append(card)
                    numontable = numontable + 1
        
        for card in game.dealer.cards:
            if card not in self.seen and card.facedown is False:
                self.seen.append(card)
                self.update_seen()
                ontable.append(card)
                numontable = numontable + 1

        #possible cards to be dealt out next 
        possible = self.allCards - self.seen

        #CALLS MAKE A MOVE PASSING IN THE POSSIBLE ACTIONS AND RETURNS WHAT THAT RETURNS 
        return self.make_a_move(options)
		
    def make_bet(self):
        #OVERWRITES PLAYERS METHOD
        #calcualte a bet based on current bank
        self.bet = 5 #placeholder
		
class Random(Player):
    def __init__(self, name, player_num):
        super().__init__(name, player_num)
    
    def make_bet(self, amount):
        if self.money <= 500:
            self.bet = randint(5, self.money)
        else:
            self.bet = randint(5, 500)
    
    def get_options(self):
        ret = [CMD.HIT, CMD.STAND]
        sums = set(self.sums())
        if len(self.cards) == 2 and self.money >= self.bet and (9 in sums or 10 in sums or 11 in sums):
            ret.append(CMD.DOUBLE)
        self.options = ret
        choice = randint(0, len(self.options)-1)
        return ord(self.options[choice].value)

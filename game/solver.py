from src.constants import *
from random import randint
from src.objects import Player, Card, Dealer


class POMDPPlayer(Player):
    def __init__(self, name, player_num, numDecks):
        # Create a new player
        # Initialize variables for things like learning rate and Q-table

        super().__init__(name, player_num)
        self.number = player_num

        # Initialize variables
        self.learning_rate = 0.1
        self.discount_rate = 0.99
        
        # Initialize Q-table
        self.q_table = {}

        self.seen = []
        self.numdecks = numDecks
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

    def get_options(self, players: Player, dealer: Dealer):
        #OVERWRITES PLAYERS METHOD
        #get all possible actions 
        options = []

        #add cards on the table to seen 
        ontable = []
        numontable = 0

        for p in players:
            for card in p.cards:
                if card not in self.seen and card.facedown is False:
                    self.seen.append(card)
                    self.update_seen()
                    ontable.append(card)
                    numontable = numontable + 1
        
        for card in dealer.cards:
            if card not in self.seen and card.facedown is False:
                self.seen.append(card)
                self.update_seen()
                ontable.append(card)
                numontable = numontable + 1

        #possible cards to be dealt out next 
        possible = self.allCards - self.seen

        #CALLS MAKE A MOVE PASSING IN THE POSSIBLE ACTIONS AND RETURNS WHAT THAT RETURNS 
        return self.make_a_move(options)
		
    def make_bet(self, high, low):
        #OVERWRITES PLAYERS METHOD
        #calcualte a bet based on current bank

        if self.money >= high:
            self.bet = 1
        elif self.money < low:
            self.bet = 0
        else:
            prob = 0
            #set this to the probability of getting a winning hand 
            if prob >= 80:
                if self.money <= 500:
                    if self.money-250 < 5:
                        self.bet = randint(5, self.money)
                    else:
                        self.bet = randint(self.money-250, self.money)
                else:
                    self.bet = randint(250, 500)

            elif prob >= 60:
                if self.money <= 250:
                    if self.money-100 < 5:
                        self.bet = randint(5, self.money)
                    else:
                        self.bet = randint(self.money-100, self.money)
                else:
                    self.bet = randint(150, 250)

            elif prob >= 40:
                if self.money <= 150:
                    if self.money-100 < 5:
                        self.bet = randint(5, self.money)
                    else:
                        self.bet = randint(self.money-100, self.money)
                else:
                    self.bet = randint(50, 150)

            else:
                if self.money <= 50:
                    if self.money-45 < 5:
                        self.bet = randint(5, self.money)
                    else:
                        self.bet = randint(self.money-45, self.money)
                else:
                    self.bet = randint(5, 50)
		
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

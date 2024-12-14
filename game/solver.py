from src.constants import *
from random import randint
from src.objects import Player, Card, Dealer
from simulator import Simulator
from simulate import CardSet, BetState, ObservedState, BeliefState, DealerState

class POMDPPlayer(Player):
    def __init__(self, name, player_num, numDecks, high, low):
        # Create a new player
        # Initialize variables for things like learning rate and Q-table

        super().__init__(name, player_num)
        self.number = player_num

        # Initialize variables
        self.learning_rate = 0.1
        self.discount_rate = 0.99
        
        # Initialize Q-table
        self.q_table = {}

        self.seen = CardSet()
        self.numdecks = numDecks
        self.numCards = self.numdecks * 52
        self.numSeen = 0
        self.allCards = []
        self.simulator = Simulator(500,high,low)

        for deck in range(self.numdecks):
            for num in list(range(2,11)) + ['J','Q','K','A']:
                for suit in SUIT:
                    self.allCards.append(Card(suit, num))

        self.deckcards = CardSet(self.allCards)
		
    def make_a_move(self, options, possible, dealers, playerhas):
        #choose an action via q learning 
        action = self.simulator.Turn(playerhas, dealers, self.seen, self.numdecks, self.money, self.bet)
        return action
    
    def update_seen(self):
        self.numSeen = self.numSeen + 1

        if self.numSeen == self.numCards:
            self.seen = CardSet()

    def get_options(self, players: Player, dealer: Dealer):
        #OVERWRITES PLAYERS METHOD
        #get all possible actions 
        options = []

        #add cards on the table to seen 
        playerhas = CardSet()
        dealers = CardSet()
        numontable = 0

        for p in players:
            for card in p.cards:
                if card not in self.seen and card.facedown is False:
                    self.seen.add_card_obj(card)
                    self.update_seen()
                    playerhas.add_card_obj(card)
                    numontable = numontable + 1
        
        for card in dealer.cards:
            if card not in self.seen and card.facedown is False:
                self.seen.add_card_obj(card)
                self.update_seen()
                dealers.add_card_obj(card)
                numontable = numontable + 1

        #possible cards to be dealt out next 
        possible = CardSet(self.allCards)

        possible.subtract_set(self.seen)

        #CALLS MAKE A MOVE PASSING IN THE POSSIBLE ACTIONS AND RETURNS WHAT THAT RETURNS 
        return self.make_a_move(options, possible, dealers, playerhas)
		
    def make_bet(self, high, low):
        #OVERWRITES PLAYERS METHOD
        #calcualte a bet based on current bank

        state = BetState(self.money,self.numdecks, self.seen, 500, high, low, None, None, 1)

        if self.money >= high:
            self.bet = -1
        elif self.money < low:
            self.bet = -2
        else:
            bet = self.simulator.betting(state)
            #set this to which bet to take (from the action?)
            if bet == 'h':
                if self.money <= 500:
                    self.bet = int(self.money*.7)
                    self.money -= self.bet
                else:
                    self.bet = int(500*.7)
                    self.money -= self.bet

            elif bet == 'm':
                if self.money <= 500:
                    self.bet = int(self.money*.4)
                    self.money -= self.bet
                else:
                    self.bet = int(500*.4)
                    self.money -= self.bet

            elif bet == 'l':
                if self.money <= 500:
                    self.bet = int(self.money*.1)
                    self.money -= self.bet
                else:
                    self.bet = int(500*.1)
                    self.money -= self.bet

        return self.bet
		
class Random(Player):
    def __init__(self, name, player_num):
        super().__init__(name, player_num)
    
    def make_bet(self, amount):
        if self.money <= 500:
            self.bet = randint(5, self.money)
        else:
            self.bet = randint(5, 500)

        self.money -= self.bet

        return self.bet
    
    def get_options(self):
        ret = [CMD.HIT, CMD.STAND]
        sums = set(self.sums())
        if len(self.cards) == 2 and self.money >= self.bet and (9 in sums or 10 in sums or 11 in sums):
            ret.append(CMD.DOUBLE)
        self.options = ret
        choice = randint(0, len(self.options)-1)
        return ord(self.options[choice].value)

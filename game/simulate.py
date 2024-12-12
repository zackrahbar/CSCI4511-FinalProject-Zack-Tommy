from src.objects import Player, Card, Dealer
import sys
import copy
# Observed state object and simulator objects. 
# a pompd agent will pass all their obervations into a state then will run the simulator on it to perform 
# monecarlotree search so that agent can make the best decison
STANDARD_DECK = {
            'A' : 4,
            2 : 4,
            3 : 4,
            4 : 4,
            5 : 4,
            6 : 4,
            7 : 4,
            8 : 4,
            9 : 4,
            10: 16
        }

class CardSet:
    #easier way of converting list of cards into dictionarys of values
    #like a 52 card deck would be encoded like
    # A | 4 
    # 2 | 4 
    # 3 | 4 
    # 4 | 4 
    # 5 | 4 
    # 6 | 4 
    # 7 | 4 
    # 8 | 4 
    # 9 | 4 
    # 10| 16 bc K, Q, J and 10 are all valued at 10
    
    def __init__(self, game_cards: list[Card]= None, decks: int=None):
        '''
        Create a new CardSet
        No params will return an empty card set
        game_cards = an array of Card objects
        decks = int -> create a card set prefilled with decks number of 52 card decks 
        Game_cards and decks cannot both be set to not None. Default is both = None and return empty set'''
        if game_cards != None and decks != None:
            print("Incorrect parameters", file=sys.stderr)
            return False 
        self.cards = {
            'A' : 0,
            2 : 0,
            3 : 0,
            4 : 0,
            5 : 0,
            6 : 0,
            7 : 0,
            8 : 0,
            9 : 0,
            10 : 0
        } # dictionary of all possible cards
        if game_cards != None:
            #iterate over cards and update them into the list
            for card in game_cards:
                if card.num.isdigit():
                    num = int(card.num)
                    self.cards[num] += 1
                elif card.num == 'A':
                    self.cards['A'] += 1
                elif card.num == 'J' or card.num == 'Q' or card.num == 'K':
                    self.cards[10] += 1
                else:
                    print("card Error", file=sys.stderr)
        if decks != None:
            # set quanities to decks times number in standard deck
            for key in self.cards.keys():
                self.cards[key] = decks * STANDARD_DECK[key]
    def add_card_obj(self, card: Card):
        if card.num.isdigit():
            num = int(card.num)
            self.cards[num] += 1
        elif card.num == 'A':
            self.cards['A'] += 1
        elif card.num == 'J' or card.num == 'Q' or card.num == 'K':
            self.cards[10] += 1
        else:
            print("card Error", file=sys.stderr)
    def add_card_value(self, num):
        '''num should be an integer or a string 'A' for ace. k,q,j are all 10. '''
        if num.isdigit():
            num = int(num)
            self.cards[num] += 1
        elif num == 'A':
            self.cards['A'] += 1
        elif num == 'J' or num == 'Q' or num == 'K':
            self.cards[10] += 1
        else:
            print("card Error", file=sys.stderr)
    
    def count(self):
        '''Return the count of the cards in this deck'''
        total = 0
        for key in self.cards.keys():
            total += self.cards[key]
        return total
    
    def probability_of_num(self, num):
        '''return the probability of pulling this card. with value num. 
            num should be an integer or a string 'A' for ace. k,q,j are all 10. '''
        total_count = self.count()
        card_count = self.cards[num]
        return float(card_count)/float(total_count)
    def subtract_set(self, other_set):
        '''This will subtract from the original set the other set and return true on success
        useage: setA.subtract_set(setB) if set A has 5 aces and set B has 3 aces then set A will have 2 Aces after
        Set b is not changed
        if set B has more of a card then Set A has then false is returned and Set A is unchanged because this set operation is invalid. 
        (A card was probably double counted)'''
        new_set = {}
        for key in self.cards.keys():
            new_set[key] = self.cards[key] - other_set.cards[key]
            if new_set[key] < 0:
                return False
        self.cards = new_set
        return True
    



class ObservedState:
    def __init__(self, money: int, turn: int, decks: int, seen_cards: CardSet, player_cards: CardSet, dealer_cards: CardSet):
       '''
       Takes in current State
        money -> the players current balance
        turn -> int describing the current turn: 0 Player bets or stops, 1 player choice of hit stand etc, 3 is stop high, 4 is stop loss. 5 is other player hitting 
         an agent should never make an ObservedState with turn 3 or 4. 
        decks -> int. number of total decks used.
        seenCards -> CardSet of the seen cards since last reshulffle inlcuding cards on table but excluding dealer and player cards
        player_cards -> CardSet of cards currently in our hand
        dealer_cards -> CardSet of cards in dealers hand 
       '''
       self.money = money
       self.turn = turn
       self.decks = decks
       #set up empty sets for now becuase we haven't observed anything yet. 
       self.seen_cards = copy.deepcopy(seen_cards) # includes only cards from previous rounds and this rounds cards that are not the dealers or the players cards
       self.player_cards = copy.deepcopy(player_cards) # cards currently in our hand
       self.dealer_cards = copy.deepcopy(dealer_cards) # cards observed in dealers hand (so the face up one)
    
    def generate_successor_actions(self):
        if self.turn == 0:
            #Betting round so options are to bet in increments of 5 or stop-success or stop-failure
            #define actions as a triple (Agent, action) Agent 0 = dealer, 1 = this player, 2 = +other player.

        elif self.turn == 1:
            #player is deciding on hit stand, maybe double

        elif self.turn == 2:
            # dealer is deterministically choosing to hit or stand based off the dealer cards
        
        elif self.turn == 3:
            # no successor states this is a final success state

        elif self.turn == 4:
            # no successor states this is final failure state

        elif self.turn == 5:
            # state where we observe aditional cards come onto the table for other players hitting
            # we can make an assumptions about how many aditional cards would come out or we can model each of the other players transitions.
            # assumptions would be like assume that per player a max of 2 cards would be drawn per player.
             
    def generate_successor(self, action):
        '''generate successor state based off an action'''

    def observe_card_after_hit(self, card: Card):
        '''need to figure out how to handle this bc this would be a successor state. this would break the tree as well because successor states would no longer point to real successors'''
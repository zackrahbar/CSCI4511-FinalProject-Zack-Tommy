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
    


# state life cycles
# Action     : Player bets ->  Cards are delt -> beliefs applied ->  players are simulated   ->         Our choice                                 -> other remaining players ->    Dealer turn         -> Betting state 
# State type :    state    ->  ObservedState  ->  Belief states  -> policies and Transitions -> generate all possible states with transition probs -> policys and tranitions  ->  dealer policy applied -> goes to betting state with new utility
# the belief states in this case are beliefs of what possible card the dealer has. 
# the belief probablity of these states is based off proababilty of the value of the card

# Bet state -> choose bet
# cards are delt -> Observed state 
# beliefs are enumerated -> Belief states 
# other players simulated -> dealer state
# money is distributed -> bet state 

class BetState:
    def __init__(self, money: int, turn: int, decks: int, seen_cards: CardSet, max_bet: int):
        '''
        Takes in current State
        money -> the players current balance
        decks -> int. number of total decks used.
        seenCards -> CardSet of the seen cards since last reshulffle

        this state generates bet actions that when completed will generate possible observed states (because the cards are delt after bets)
        '''
        self.money = money
        self.turn = turn
        self.decks = decks
        #set up empty sets for now becuase we haven't observed anything yet. 
        self.seen_cards = copy.deepcopy(seen_cards) # includes only cards from previous rounds and this rounds cards that are not the dealers or the players cards
        self.child_states = []
        self.max_bet = max_bet

    def generate_actions(self):
        # generates betting actions 
        # returns [actions]
        # 5 actions : stop success, stop failure, bet low, bet med, bet high

        #take proportion of num and round down to lowest whole number divisable by 5 
        percent = lambda num, proportion: (num * proportion) - ((num * proportion)%5)

        if self.money * .4 > self.max_bet:
            # since 40% of our bead is higher than max bet we will say bet high = 90% of max bet, bet med is 40% of max and low is 10%
            bet_high = percent(self.max_bet,.40)
            bet_ = percent(self.max_bet,.40)
            #Not Done this yet

    def generate_next_states(self,action):
        '''
        genrate a list of possible next states and their transition probabilities. 
        [(Next_state, transition_probability),(Next_state, transition_probability),(Next_state, transition_probability),(Next_state, transition_probability)]
        transition probabilities are based off cards remaining in the deck
        '''


class ObservedState:
    def __init__(self, money: int, decks: int, seen_cards: CardSet, player_cards: CardSet, dealer_cards: CardSet):
       '''
       this is our observation of the table after the cards are delt. this sate is generated by the BetState
       this state generates 10 possible belief states. 
        money -> the players current balance
       
        decks -> int. number of total decks used.
        seenCards -> CardSet of the seen cards since last reshulffle inlcuding cards on table but excluding dealer and player cards
        player_cards -> CardSet of cards currently in our hand
        dealer_cards -> CardSet of cards in dealers hand 
       '''
       self.money = money
       self.decks = decks
       #set up empty sets for now becuase we haven't observed anything yet. 
       self.seen_cards = copy.deepcopy(seen_cards) # includes only cards from previous rounds and this rounds cards that are not the dealers or the players cards
       self.player_cards = copy.deepcopy(player_cards) # cards currently in our hand
       self.dealer_cards = copy.deepcopy(dealer_cards) # cards observed in dealers hand (so the face up one)
    
    
             
    def generate_belief_states(self, action):
        '''generate successor state based off an action'''



class BeliefState: 
    '''
        Generated by the Observation state. this state is a state where we believe the hidden dealers card to be someparticular value. 
        actions generated from this state are the POMDP players actions.  
        these actions could result staying in this state ( hit ) or transitioning to a dealer state ( stand or hit and bust) 

    '''
    def generate_actions(self):
        print()

    def generate_next_states():
        '''

        returns an array of future states [(Next_state, transition_probability),(Next_state, transition_probability),(Next_state, transition_probability),(Next_state, transition_probability)] 
        next state is either either another belief state or a dealer state (stand or hit->bust)
        transition proabability is the based off the remaining cards in the deck and the probability for that card. using cardset functions'''

class DealerState:
    '''
        generated by the belief state after the player is simulated to bust or the player stands.
        actions follow a deterministic policy but since we the cards recieved while performing that policy they are not deterministic we model 
        the dealer playing. 
        this state generates actions that lead to a second DealerState (if this need to hit again) or to a bet state where the round is completed and the player is given their winnings


    '''
    
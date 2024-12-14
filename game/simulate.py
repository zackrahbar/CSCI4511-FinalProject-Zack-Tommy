from src.objects import Player, Card, Dealer
import sys
import copy
from src.constants import *

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
        if isinstance(num,int):
            if self.cards[num] == 0: 
                return False
            self.cards[num] += 1
        elif card.num.isdigit():
            num = int(card.num)
            self.cards[num] += 1
        elif card.num == 'A':
            self.cards['A'] += 1
        elif card.num == 'J' or card.num == 'Q' or card.num == 'K':
            self.cards[10] += 1
        else:
            print("card Error", file=sys.stderr)
            return False
        return True
    def add_card_value(self, num):
        '''num should be an integer or a string 'A' for ace. k,q,j are all 10. '''
        if isinstance(num,int):
            if self.cards[num] == 0: 
                return False
            self.cards[num] += 1
        elif num.isdigit():
            num = int(num)
            self.cards[num] += 1
        elif num == 'A':
            self.cards['A'] += 1
        elif num == 'J' or num == 'Q' or num == 'K':
            self.cards[10] += 1
        else:
            print("card Error", file=sys.stderr)
            return False
        return True
    def remove_card_obj(self, card: Card):
        if isinstance(num,int):
            if self.cards[num] == 0: 
                return False
            self.cards[num] -= 1
        elif card.num.isdigit():
            num = int(card.num)
            if self.cards[num] == 0: 
                return False
            self.cards[num] -= 1
        elif card.num == 'A':
            if self.cards['A'] == 0: 
                return False
            self.cards['A'] -= 1
        elif card.num == 'J' or card.num == 'Q' or card.num == 'K':
            if self.cards[10] == 0: 
                return False
            self.cards[10] -= 1
        else:
            print("card Error", file=sys.stderr)
            return False
        return True
        
    def remove_card_value(self, num):
        '''num should be an integer or a string 'A' for ace. k,q,j are all 10. '''
        if isinstance(num,int):
            if self.cards[num] == 0: 
                return False
            self.cards[num] -= 1
        elif num.isdigit():
            num = int(num)
            if self.cards[num] == 0: 
                return False
            self.cards[num] -= 1
        elif num == 'A':
            if self.cards['A'] == 0: 
                return False
            self.cards['A'] -= 1
        elif num == 'J' or num == 'Q' or num == 'K':
            if self.cards[10] == 0: 
                return False
            self.cards[10] -= 1
        else:
            print("card Error", file=sys.stderr)
            return False
        return True

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
    
    def set_sum(self):
        '''
            If the sum is using an ace and is over 21 return the lower sum.
        '''
        sum = 0
        # add all regular cards
        for i in range(2,11):
            sum += i * self.cards[i]
        for k in range(self.cards['A']):
            if (sum + 11) > 21:
                sum + 1
        return sum
    
    def add_set(self, other_set):
        '''Adds the other set to this current set '''
        new_set = {}
        for key in self.cards.keys():
            new_set[key] = self.cards[key] + other_set.cards[key]
            if new_set[key] < 0:
                return False
        self.cards = new_set
        return True
    
    def is_equal(self, other_set):
        '''Returns true if the sets are the same '''
        
        for key in self.cards.keys():
            if self.cards[key] != other_set.cards[key]:
                return False
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
    def __init__(self, money: int, decks: int, seen_cards: CardSet, max_bet: int, stop_high: int, stop_low: int, parent, action_taken_here, transition_prob, value=0):
        '''
        Takes in current State
        money -> the players current balance
        decks -> int. number of total decks used.
        seenCards -> CardSet of the seen cards since last reshulffle

        this state generates bet actions that when completed will generate possible observed states (because the cards are delt after bets)
        '''
        self.money = money
        self.decks = decks
        
        self.seen_cards = copy.deepcopy(seen_cards) # includes only cards from previous rounds and this rounds cards that are not the dealers or the players cards
        self.child_states = []
        self.max_bet = max_bet
        self.stop_high = stop_high
        self.stop_low = stop_low
        self.child = []
        self.parent = parent
        self.childtotal = 0 
        self.weighted_value_high = value
        self.weighted_value_med = 0
        self.weighted_value_low = 0
        self.parent_tuple = (parent, action_taken_here, transition_prob)

    def set_weighted_value_total(self,value):
        self.weighted_value_total = value

    def set_child(self, child):
        self.child.extend(child)
        self.childtotal = self.childtotal + len(child)

    def generate_actions(self):
        # generates betting actions 
        # returns [actions]
        # 5 actions : stop success, stop failure, bet low, bet med, bet high

        #take proportion of num and round down to lowest whole number divisable by 5 
        # percent = lambda num, proportion: (num * proportion) - ((num * proportion)%5)

        # if self.money * .4 > self.max_bet:
        #     # since 40% of our bead is higher than max bet we will say bet high = 90% of max bet, bet med is 40% of max and low is 10%
        #     bet_high = percent(self.max_bet, .90)
        #     bet_med = percent(self.max_bet, .40)
        #     bet_low = percent(self.max_bet, .10)
        # elif self.money * .9 < self.max_bet:
        #     # since 40% and 90% of our money is less than max bet we will use our money to set proportions so we adject our bets to the money we have. 
        #     bet_high = percent(self.money, .90)
        #     bet_med = percent(self.money, .40)
        #     bet_low = percent(self.money, .10)
        # else: 
        #     bet_high = percent(self.max_bet, .90)
        #     bet_med = percent(self.max_bet, .40)
        #     bet_low = percent(self.max_bet, .10)
        # actions = [
        #            'betH '+ str(bet_high),
        #            'betM '+ str(bet_med),
        #            'betL '+ str(bet_low),
        #            ]
        actions = ['betH '+ str(100)]
        if self.money > self.stop_high:
            actions = ['Stop Success']
        if self.money < self.stop_low:
            actions = ['Stop Failure']

        return actions
        
    def generate_next_states(self,action: str):
        '''
        list[tuple[ObservedState,float]]
        genrate a list of possible next states and their transition probabilities. 
        [(Next_state, transition_probability),(Next_state, transition_probability),(Next_state, transition_probability),(Next_state, transition_probability)]
        transition probabilities are based off cards remaining in the deck
        
        returns either observed states or will return betState in the case of Stop Success or Stop Failure 
        
        '''
        if action == 'Stop Success':
            #error should have stopped here
            print('Tree recursion error generate next states in BetState, success', file= sys.stderr)
        if action == 'Stop Failure':
            #error should have stopped here
            print('Tree recursion error generate next states in BetState, failure', file= sys.stderr)
        [action, bet_amount] = action.split(' ', 1)
        if not bet_amount.isdigit(): 
            print('Error generate next states in BetState, invalid action', file= sys.stderr)

        new_money = self.money - int(bet_amount)
        
        # reaminaing deck

        remaining_deck = CardSet(decks=self.decks)
        
        remaining_deck.subtract_set(self.seen_cards)

        #create all possible combinations of 3 cards being delt. 1 to player then 1 to dealer then 1 to player. 
        new_states=[]

        for c1 in list(range(2,11)) + ['A']:
            #get probability 
            probability = 1 
            probability_c1 = remaining_deck.probability_of_num(c1)
            # take a card out of seen cards
            if remaining_deck.remove_card_value(c1) == False:
                # a card is not able to be taken so skip this combination
                new_states.append((None,0))
                continue 
            probability = probability * probability_c1
            player_cards = CardSet()
            dealer_cards = CardSet()
            player_cards.add_card_value(c1)
            for c2 in list(range(2,11)) + ['A']:
                #update prob
                probability_c2 = remaining_deck.probability_of_num(c2)
                # take a card out of seen cards and add to dealer cards
                if remaining_deck.remove_card_value(c2) == False:
                    # a card is not able to be taken so skip this combination
                    new_states.append((None,0))
                    continue 
                probability = probability * probability_c2
                dealer_cards.add_card_value(c2)
                for c3 in list(range(2,11)) + ['A']:
                    #update prob
                    probability_c3 = remaining_deck.probability_of_num(c3) # this is now the transition probability for this state from previous state given this action
                    # take a card out of seen cards and add to dealer cards
                    if remaining_deck.remove_card_value(c2) == False:
                    # a card is not able to be taken so skip this combination
                        new_states.append((None,0))
                        continue 
                    probability = probability * probability_c3
                    player_cards.add_card_value(c3)
                    new_state = ObservedState(new_money,self.decks,int(bet_amount),self.seen_cards,player_cards,dealer_cards, self,action,probability)
                    new_states.append((new_state, probability))
                    # reset seen cards and player cards. 
                    player_cards.remove_card_value(c3)
                    remaining_deck.add_card_value(c3)
                dealer_cards.remove_card_value(c2)
                remaining_deck.add_card_value(c2)
            player_cards.remove_card_value(c1)
            remaining_deck.add_card_value(c1)

        #return new states with thier transition probabilities
        self.child.extend(new_states)
        self.childtotal = self.childtotal + len(new_states)
        return new_states

class ObservedState:
    def __init__(self, money: int, decks: int, bet: int, seen_cards: CardSet, player_cards: CardSet, dealer_cards: CardSet, parent, action_taken_here, transition_prob):
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
        self.bet = bet
        self.seen_cards = copy.deepcopy(seen_cards) # includes only cards from previous rounds and this rounds cards that are not the dealers or the players cards
        self.player_cards = copy.deepcopy(player_cards) # cards currently in our hand
        self.dealer_cards = copy.deepcopy(dealer_cards) # cards observed in dealers hand (so the face up one)
        self.child = []
        self.parent = parent
        self.childtotal = 0 
        self.weighted_value_total = 0
        self.parent_tuple = (parent, action_taken_here, transition_prob)

    def set_weighted_value_total(self,value):
        self.weighted_value_total = value

    def set_child(self, child):
        self.child.extend(child)
        self.childtotal = self.childtotal + len(child)
    
             
    def generate_belief_states(self, num):
        '''give the dealer a card and then would say the belief probability is the 
        chance of that card being pulled from remaining unseen cards '''

        possible = CardSet(None, self.decks)
        possible.subtract_set(self.seen_cards)
        possible.subtract_set(self.player_cards)
        possible.subtract_set(self.dealer_cards)

        #num = card.num

        if num == 'J' or num == 'Q' or num == 'K':
            belief = possible.probability_of_num(10)
        else:
            belief = possible.probability_of_num(num)

        #self.seen_cards.add_card_obj(card)
        self.dealer_cards.add_card_value(num)
            
        state = BeliefState(self.money, self.decks, self.bet, self.seen_cards, self.player_cards, self.dealer_cards, self, None, belief)
        
        self.child.append((state,belief))
        self.childtotal = self.childtotal + 1
        return (state, belief)



class BeliefState: 
    '''
        Generated by the Observation state. this state is a state where we believe the hidden dealers card to be someparticular value. 
        actions generated from this state are the POMDP players actions.  
        these actions could result staying in this state ( hit ) or transitioning to a dealer state ( stand or hit and bust) 

    '''

    def __init__(self, money: int, decks: int, bet:int, seen_cards:CardSet, player_cards:CardSet, dealer_cards:CardSet, parent, action_taken_here, transition_prob):
        '''
            create new beleif state. this is a state where we have taken a belief based on the observed game state. (We assume we know what the dealers card is)
            from this state the player will choose actions of hit stand or double. 
        '''
        self.money = money
        self.decks = decks
        self.bet = bet
        self.seen_cards = copy.deepcopy(seen_cards)
        self.player_cards = copy.deepcopy(player_cards)
        self.dealer_cards = copy.deepcopy(dealer_cards)
        self.child = []
        self.parent = parent
        self.childtotal = 0 
        self.weighted_value_hit = 0
        self.weighted_value_stand = 0
        self.weighted_value_double = 0
        self.parent_tuple = (parent, action_taken_here, transition_prob)

    def set_weighted_value_total(self,value):
        self.weighted_value_total = value

    def set_child(self, child):
            self.child.extend(child)
            self.childtotal = self.childtotal + len(child)  

    def generate_next_states(self,action):
        '''
        possible actions: 'h' 's' 'd'
        returns an array of future states [(Next_state, transition_probability),(Next_state, transition_probability),(Next_state, transition_probability),(Next_state, transition_probability)] 
        next state is either either another belief state or a dealer state (stand or hit->bust)
        transition proabability is the based off the remaining cards in the deck and the probability for that card. using cardset functions'''
        # get remaining deck 
        remaining_deck = CardSet(decks=self.decks)
        
        remaining_deck.subtract_set(self.seen_cards)
        remaining_deck.subtract_set(self.player_cards)
        remaining_deck.subtract_set(self.dealer_cards)

        new_states = []
        if action == 'h':
            #hit
            for card in list(range(2,11)) + ['A']:
                #update prob
                probability = remaining_deck.probability_of_num(card) # this is now the transition probability for this state from previous state given this action
                # take a card out of seen cards and add to dealer cards
                if remaining_deck.remove_card_value(card) == False:
                # a card is not able to be taken so skip this combination
                    new_states.append((None,0))
                    continue 
                self.player_cards.add_card_value(card)
                #if sum is too high then make dealer state. if under 21 then make belief state
                if self.player_cards.set_sum() >= 21:
                    new_state = DealerState(self.money,self.decks,self.bet, self.seen_cards, self.player_cards, self.dealer_cards,self,'h',probability)
                else:
                    new_state = BeliefState(self.money,self.decks,self.bet,self.seen_cards,self.player_cards,self.dealer_cards,self,'h',probability)
                new_states.append((new_state, probability))
                # reset seen cards and player cards. 
                self.player_cards.remove_card_value(card)
                remaining_deck.add_card_value(card)
        elif action == 's':
            new_state = DealerState(self.money,self.decks,self.bet,self.seen_cards,self.player_cards,self.dealer_cards,self,'s',1)
            new_states.append((new_state, 1))
        
        return new_states


    def generate_next_states_OLD(self, action):

        '''

        returns an array of future states [(Next_state, transition_probability),(Next_state, transition_probability),(Next_state, transition_probability),(Next_state, transition_probability)] 
        next state is either either another belief state or a dealer state (stand or hit->bust)
        transition proabability is the based off the remaining cards in the deck and the probability for that card. using cardset functions'''


        values = ['A',2,3,4,5,6,7,8,9,10]

        # total = [0]
        # for card in self.player_cards:
        #     if card.num == 'A':
        #         temp = [11 + t for t in total]
        #         total = [1 + t for t in total]
        #         total.extend(temp)
        #     elif not card.num.isdigit():
        #         total = [10 + t for t in total]
        #     else:
        #         total = [int(card.num) + t for t in total]
        # total = [t for t in total if t <= 21]
        total = [self.player_cards.set_sum()]
        #to get sum of cardset use self.player_cards.set_sum() 

        #VERIFY THIS FIX WORKS
        if self.player_cards.cards['A'] == 1 and self.player_cards.count() == 2:
            total.insert(0,(self.player_cards.set_sum()-10))

        
        total.sort()
        if action == 'h':
            returning = []
            for value in values:
                if self.player_cards.cards[value] > 0:
                    #TODO modify this to include the probability of it being hit 
                    prob = self.player_cards.probability_of_num(value)
                    if len(total) == 1:
                        if value != 'A':
                            if value + total[0] >= 21:
                                self.player_cards.add_card_value(value)
                                self.seen_cards.add_card_value(value)
                                dealer = DealerState(self.money,self.decks,self.bet,self.seen_cards,self.player_cards,self.dealer_cards, self, 'h',prob)
                                self.child.append(dealer)
                                self.childtotal = self.childtotal + 1
                                return dealer
                            else:
                                self.player_cards.add_card_value(value)
                                self.seen_cards.add_card_value(value)
                                belief = BeliefState(self.money,self.decks,self.bet,self.seen_cards,self.player_cards,self.dealer_cards, self, 'h',prob)
                                returning.append(belief)
                        else:
                                low_ace = total[0] + 1
                                high_ace = total[0] + 11
                                
                                if low_ace <= 21 or high_ace <= 21:
                                    self.player_cards.add_card_value(value)
                                    self.seen_cards.add_card_value(value)
                                    belief = BeliefState(self.money,self.decks,self.bet,self.seen_cards,self.player_cards,self.dealer_cards, self, 'h',prob)
                                    returning.append(belief)
                                
                                if low_ace > 21 and high_ace > 21:
                                    self.player_cards.add_card_value(value)
                                    self.seen_cards.add_card_value(value)
                                    dealer = DealerState(self.money,self.decks,self.bet,self.seen_cards,self.player_cards,self.dealer_cards, self, 'h',prob)
                                    self.child.append(dealer)
                                    self.childtotal = self.childtotal + 1
                                    return dealer

                    if len(total) == 2:
                        for t in total:
                            if value != 'A':
                                if value + t >= 21:
                                    self.player_cards.add_card_value(value)
                                    self.seen_cards.add_card_value(value)
                                    dealer = DealerState(self.money,self.decks,self.bet,self.seen_cards,self.player_cards,self.dealer_cards, self, 'h',prob)
                                    self.child.append(dealer)
                                    self.childtotal = self.childtotal + 1
                                    return dealer
                                else:
                                    self.player_cards.add_card_value(value)
                                    self.seen_cards.add_card_value(value)
                                    belief = BeliefState(self.money,self.decks,self.bet,self.seen_cards,self.player_cards,self.dealer_cards, self, 'h',prob)
                                    returning.append(belief)
                            else:
                                low_ace = total[0] + 1
                                high_ace = total[0] + 11
                                
                                if low_ace <= 21 or high_ace <= 21:
                                    self.player_cards.add_card_value(value)
                                    self.seen_cards.add_card_value(value)
                                    belief = BeliefState(self.money,self.decks,self.bet,self.seen_cards,self.player_cards,self.dealer_cards, self, 'h',prob)
                                    returning.append(belief)
                                
                                if low_ace > 21 and high_ace > 21:
                                    self.player_cards.add_card_value(value)
                                    self.seen_cards.add_card_value(value)
                                    dealer = DealerState(self.money,self.decks,self.bet,self.seen_cards,self.player_cards,self.dealer_cards, self, 'h',prob)
                                    self.child.append(dealer)
                                    self.childtotal = self.childtotal + 1
                                    return dealer

            self.child.extend(returning)
            self.childtotal = self.childtotal + len(returning)
            return returning

        elif action == 's':
            prob = 1
            dealer = [DealerState(self.money,self.decks,self.bet,self.seen_cards,self.player_cards,self.dealer_cards, self, 's',prob)]
            self.child.append(dealer)
            self.childtotal = self.childtotal + 1
            return dealer

        elif action == 'd':
            #TODO IDK what to do here so I macd it same as stand  
            # double the bet and decrease the money and 

            prob = 1
            dealer = [DealerState(self.money,self.decks,self.bet,self.seen_cards,self.player_cards,self.dealer_cards, self, 'd',prob)]
            self.child.append(dealer)
            self.childtotal = self.childtotal + 1
            return dealer


    def generate_action(self):
        # total = [0]
        # for card in self.player_cards:
        #     if card.num == 'A':
        #         temp = [11 + t for t in total]
        #         total = [1 + t for t in total]
        #         total.extend(temp)
        #     elif not card.num.isdigit():
        #         total = [10 + t for t in total]
        #     else:
        #         total = [int(card.num) + t for t in total]
        # total = [t for t in total if t <= 21]

        available = ['s']
        # for t in total:
        #     if t < 20:
        #         available.append('h')
        #         break
        if self.player_cards.set_sum() < 21:
            available.append('h')


        #sums = set(total)
        # turn off double even though its like 95% implemented. 
        # if len(self.cards) == 2 and self.money >= self.bet and (9 in sums or 10 in sums or 11 in sums):
        #     available.append('d')

        return available
        
class DealerState:
    '''
        generated by the belief state after the player is simulated to bust or the player stands.
        actions follow a deterministic policy but since we the cards recieved while performing that policy they are not deterministic we model 
        the dealer playing. 
        this state generates actions that lead to a second DealerState (if this need to hit again) or to a bet state where the round is completed and the player is given their winnings


    '''

    def __init__(self, money: int, decks: int, bet:int, seen_cards:CardSet, player_cards:CardSet, dealer_cards:CardSet, parent, action_taken_here, transition_prob):
        '''
            create a new dealer state where a dealer will take an action. this state will generate new dealer states in the case where they have to hit again. 
            if the dealer stood on the soft 17 then will generate a bet state where the player's money is updated according to if they won.

            create new beleif state. this is a state where we have taken a belief based on the observed game state. (We assume we know what the dealers card is)
            from this state the player will choose actions of hit stand or double. 
        '''
        self.money = money
        self.decks = decks
        self.bet = bet
        self.seen_cards = copy.deepcopy(seen_cards)
        self.player_cards = copy.deepcopy(player_cards)
        self.dealer_cards = copy.deepcopy(dealer_cards)
        self.child = []
        self.parent = parent
        self.childtotal = 0 
        self.weighted_value_total = 0
        self.parent_tuple = (parent, action_taken_here, transition_prob)

    def set_weighted_value_total(self,value):
        self.weighted_value_total = value

    def set_child(self, child):
            self.child.extend(child)
            self.childtotal = self.childtotal + len(child)
    
    def generate_actions(self):
        '''
        this will generate the possible actions the dealer can take. since the dealer is deterministic in their policy there will only be one action returned
        ['Hit','Stand']
        '''

        total = self.player_cards.set_sum()

        
        if total < 17:
            return 'h'
        else:
            return 's'


    #static for evaluation
    @staticmethod
    def evaluate_payout(player_cards, dealer_cards, bet):
        player_sum = player_cards.set_sum()
        dealer_sum = dealer_cards.set_sum()
        payout = 0
        #check for bust first. 
        if player_sum > 21: 
            payout = 0
        #check if either has black jack
        elif player_sum == 21 and player_cards.count() == 2:
            #player has 21 with only 2 cards  Blackjack!
            #check dealer
            if dealer_sum == 21 and dealer_cards.count() == 2:
                #tie they both have BlackJack 
                #player get thier money back in this case
                payout = bet
            else:
                #player wins with blackjack so 2.5
                payout =  bet * 2.5
        #check for dealer blackjack
        elif dealer_sum == 21 and dealer_cards.count() == 2:
            payout = 0
        #check dealer bust
        elif dealer_sum > 21:
            #regular win 
            payout = bet * 2
        #check for regular win
        elif player_sum > dealer_sum: 
            payout = bet * 2 
        #tie
        elif player_sum == dealer_sum:
            payout = bet
        elif player_sum < dealer_sum:
            #loss. 
            payout = 0
        return payout
        
    def generate_state(self, action: str, max_bet: int, stop_high: int, stop_low: int):
        '''
            for each dealer action there is possible out comes for each of actions depending on what card they get either we return a dealer state or a bet state. 
            Parameters: max_bet, stop_high, stop_low are used when generating betting states

            returns [(state, probability), ... ]
            where utility is the money in the new state. 
        '''
        if action == 'Stand':
            #dealer stand so evaluate who won and create a new bet state with an updated money. clear the table by adding dealer and player cards to the seen cards set
            
            payout = DealerState.evaluate_payout(self.player_cards,self.dealer_cards,self.bet)
            # create new bet state
            new_seen_cards = copy.deepcopy(self.seen_cards)
            new_seen_cards.add_set(self.player_cards)
            new_seen_cards.add_set(self.dealer_cards)
            new_money = self.money + payout
            state = BetState(new_money,self.decks,new_seen_cards,max_bet,stop_high,stop_low, self, None, 1,value=payout)
            return [(state, 1)]
        
        if action == 'Hit':
            # generate a new dealerstate object 
            new_states = []

            remaining_deck = CardSet(decks=self.decks)
            remaining_deck.subtract_set(self.seen_cards)
            remaining_deck.subtract_set(self.player_cards)
            remaining_deck.subtract_set(self.dealer_cards)
            for card in list(range(2,11))+['A']:
                probability = 1 
                probability = remaining_deck.probability_of_num[card]
                # take a card out of seen cards
                if remaining_deck.remove_card_value[card] == False:
                    # a card is not able to be taken so skip this combination
                    new_states.append((None,0))
                    continue 
                self.dealer_cards.add_card_value[card]
                if self.dealer_cards.set_sum() <= 21:
                    new_state = DealerState(self.money,self.decks,self.bet,self.seen_cards,self.player_cards,self.dealer_cards, self, 'h', probability)
                else:
                    #if dealer busts return a bet state
                    payout = DealerState.evaluate_payout(self.player_cards,self.dealer_cards,self.bet)
                    new_seen_cards = copy.deepcopy(self.seen_cards)
                    #round is over so add these cards to the seen cards
                    new_seen_cards.add_set(self.player_cards)
                    new_seen_cards.add_set(self.dealer_cards)
                    new_money = self.money + payout
                    new_state = BetState(new_money,self.decks,new_seen_cards,max_bet,stop_high,stop_low, self, 'h', probability, payout)
                new_states.append((new_state, probability))
                remaining_deck.add_card_value[card]
                self.dealer_cards.remove_card_value[card]
            
            self.child.extend(new_states)
            self.childtotal = self.childtotal + len(new_states)
            return new_states
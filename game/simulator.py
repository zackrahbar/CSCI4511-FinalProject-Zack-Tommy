from simulate import CardSet, BetState, ObservedState, BeliefState, DealerState
from src.objects import Player, Card, Dealer
import sys
import copy
from src.constants import *
import math

class Simulator:
    def __init__(self, max_bet: int, stop_high: int, stop_low: int):
        self.max_bet = max_bet
        self.stop_high = stop_high
        self.stop_low = stop_low
    def betting(self, bet_state: BetState ):
        
        
        self.root_bet_state = bet_state
        bet_state_actions = bet_state.generate_actions()
        print("Bet state actions: ", bet_state_actions, file=sys.stderr)
        if len(bet_state_actions) == 1 and bet_state_actions[0] == 'Stop Success':
            #return succcess
            return -1 
        if len(bet_state_actions) == 1 and bet_state_actions[0] == 'Stop Failure':
            #return failure
            return -2
        

        # exploring down the tree. 
        # can add filtering here inbetween steps. by sorting the nodes. using .sort(reverse=True, key= lambda x: x[1]) sorts so highest probability is at front. 
        self.observed_state_tuples = Simulator.get_observed_states_from_bet_state(bet_state, 1.0)

        self.belief_state_tuples = Simulator.get_belief_states_from_observed_states(self.observed_state_tuples)

        self.dealer_state_tuples = Simulator.get_dealer_states_from_belief_states(self.belief_state_tuples)

        self.final_bet_states = self.get_bet_states_from_dealer_states(self.dealer_state_tuples)

        #todo call backprop on the bet states.  

        for bet_leaf in self.final_bet_states:
            self.backprop(bet_leaf)

        value = self.root_bet_state.weighted_value_high
        # high and low cut off med is inbetween
        
        LOW_CUTOFF = 95
        HIGH_CUTOFF = 105

        if value > HIGH_CUTOFF:
            action = 'h'
        elif value < LOW_CUTOFF:
            action = 'l'
        else:
            action = 'm'

        print('In betting value: ', value, ' returning action:', action, file = sys.stderr)
        return action

    def turn(self, player_cards: CardSet, dealer_cards: CardSet, seen_cards: CardSet, decks: int, money:int, bet: int ):
        '''
            player cards -> cards in player hand
            dealer_cards -> cards in dealer hand (one 1 card)
            seen_cards -> cards seen in prevous rounds 
            
        '''

        #check obervation states to see if any mactch 
        #find state 
        matching_state = None
        for obs_state_tuple in self.observed_state_tuples:
            (state, prob) = obs_state_tuple
            #check if the cards are the same
            if player_cards.is_equal(state.player_cards):
                if dealer_cards.is_equal(state.dealer_cards):
                    if seen_cards.is_equal(state.seen_cards):
                        matching_state = obs_state_tuple
                    else:
                        print("player and dealer mathch but seen don't, might be error")

        if matching_state == None:
            # it wasn't found so generate it
            matching_state = ObservedState(money, decks,bet,seen_cards,player_cards,dealer_cards,None,None,0)
        
        new_belief_states = Simulator.get_belief_states_from_observed_states([(matching_state,1)])

        new_dealer_state_tuples = Simulator.get_dealer_states_from_belief_states(new_belief_states)

        new_final_bet_states = self.get_bet_states_from_dealer_states(new_dealer_state_tuples)

        print('starting backprop len: ',len(new_final_bet_states), file=sys.stderr)
        for bet_leaf in new_final_bet_states:
            self.backprop(bet_leaf, depth= 'Observed State')
        
        print('ending backprop', file=sys.stderr)
        #get weighted sum accross all belief states then pick highest
        total_weighted_value_hit = 0
        total_weighted_value_stand = 0
        total_weighted_value_double = 0
        
        for belief_state_tuple in new_belief_states:
            (state, prob) = belief_state_tuple
            total_weighted_value_hit += (state.parent_tuple[2] * state.weighted_value_hit)
            total_weighted_value_stand += (state.parent_tuple[2] * state.weighted_value_stand)
            total_weighted_value_double += (state.parent_tuple[2] * state.weighted_value_double)

        highest = (total_weighted_value_hit, total_weighted_value_stand, total_weighted_value_double)
        #assert highest != 0, "Error highest should not be zero"
        #print('done weighted sum total_weighted_value_hit: ', total_weighted_value_hit,' total_weighted_value_stand:',total_weighted_value_stand,'total_weighted_value_double: ', total_weighted_value_double, file=sys.stderr)
        action = 's'

        if highest == total_weighted_value_hit:
            #hit is best
            action = 'h'
        if highest == total_weighted_value_stand:
            action = 's'
        if highest == total_weighted_value_double:
            action = 'd'
        
        print('In turn highest value: ', highest, ' returning action:', action, ' |values Hit: ', total_weighted_value_hit, ' stand: ', total_weighted_value_stand,' double: ', total_weighted_value_double, file = sys.stderr)
        return action
    @staticmethod
    def get_observed_states_from_bet_state(bet_state: BetState, percent_to_keep: float) -> list[tuple[ObservedState,float]]: 
        '''
        given a bet state generate the possible observed states
        percent_to_keep is the proportion of the total number of states that should be explored. 
        '''
        actions = bet_state.generate_actions()
        if len(actions) == 1:
            #stop success or failure 
            if actions[0] == 'Stop Success':
            #error should have stopped here
                return [(None,1)]
            if actions[0] == 'Stop Failure':
                return [(None,0)]
            
        states_to_return = []
        for action in actions:
            next_states = bet_state.generate_next_states(action)
            #sort the list and we will take a number of the highest probability instances
            next_states.sort(reverse=True, key= lambda x: x[1])
            num_to_check = math.floor(len(next_states) * percent_to_keep)
            states_to_return.extend(next_states[0:num_to_check])
        print('Done get_observed_states_from_bet_state len returing', len(states_to_return), file=sys.stderr)
        
        return states_to_return 
        
    
    @staticmethod 
    def get_belief_states_from_observed_states(observed_states: list[tuple[ObservedState,float]]) -> list[tuple[BeliefState,float]]:
        belief_states = []
        for state_tuple in observed_states:
            (state, belief) = state_tuple
            for num in list(range(2,11))+['A']:
                belief_states.append(state.generate_belief_states(num))
        print('Done get_belief_states_from_observed_states len returing', len(belief_states), file=sys.stderr)
        return belief_states
        

    @staticmethod
    def get_dealer_states_from_belief_states(belief_states: list[tuple[BeliefState,float]], depth:list[int]=[3,2,1],iterations:int = 2)-> list[tuple[DealerState]]:
        print('In get_dealer_states_from_belief_states---------------',file=sys.stderr)
        

        belief_states_to_process = belief_states
        dealer_states_to_return = []
        belief_states_v2 = []
        
        while(len(belief_states_to_process) > 0):
            
            belief_state_tuple = belief_states_to_process.pop()
            (belief_state, prob) = belief_state_tuple

            #the belief state we generate actions then for each action we generate next states
            actions = belief_state.generate_action()
            next_states = []
            for action in actions:
                next_states.extend(belief_state.generate_next_states(action))
            
            #now filter next_states into dealer states and belief states to process
            
            dealer_states_to_return.extend([(st,prob) for (st,prob) in next_states if isinstance(st,DealerState)])
            new_belief_states = [(st,prob) for (st,prob) in next_states if isinstance(st,BeliefState)]
            new_belief_states.sort(reverse=True, key= lambda x: x[1])
            belief_states_v2.extend(new_belief_states[0:depth[2-iterations]])

            if(len(belief_states_to_process) == 1 and iterations > 0 ):
                iterations -= 1
                print('adding belief states v2 to the queue len: ', len(belief_states_v2),file=sys.stderr)
                belief_states_to_process.extend(belief_states_v2)
                belief_states_v2 = []
            # for next_state_tuple in next_states:
                
            #     (next_state, prob) = next_state_tuple
            #     if next_state == None:
            #         continue
            #     # print("Filtering next state of type  ",type(next_state), file=sys.stderr)

            #     if isinstance(next_state, DealerState):
            #         dealer_states_to_return.append(next_state_tuple)
            #     elif isinstance(next_state, BeliefState):
            #         belief_states_v2.append(next_state_tuple)
            #         #pass
            #     else:
            #         #ERROR
            #         print("Next state type not found of type  ",type(next_state), file=sys.stderr)
        print('remaining belief states to process len', len(belief_states_v2), file=sys.stderr)
        print("returning get_dealer_states_from_belief_states len: ", len(dealer_states_to_return),file=sys.stderr)
        return dealer_states_to_return



        # while(len(belief_states_to_process) > 0):
        #     #print('\t while loop len : ',len(belief_states_to_process),file=sys.stderr )
        #     (state, belief_prob) = belief_states_to_process.pop()
        #     print('this state type: ', type(state), file=sys.stderr)
        #     if isinstance(state, DealerState):
        #         print('DealerState!!',file=sys.stderr)
        #         dealer_states_to_return.append((state, belief_prob))
        #         continue
        #     #state = belief_states_to_process.pop()
        #     actions = state.generate_action()
        #     #print('\t\t actions', actions,file=sys.stderr)

        #     for action in actions:
        #         new_states = state.generate_next_states(action)
        #         #print('\t\t len new_states', len(new_states),file=sys.stderr)

        #         if new_states != None:
        #             for state_tuple in new_states:

        #                 if state_tuple == None:
        #                     continue
        #                 (state, prob) = state_tuple
        #                 if state == None:
        #                     continue
        #                 if isinstance(state_tuple[0],DealerState):
        #                     dealer_states_to_return.append(state_tuple)
        #                 elif isinstance(state_tuple[0], BeliefState): 
        #                     #belief_states_to_process.append(state_tuple)
        #                     pass
        #                 else:
        #                     print('\t\t Unknown obj in tuple',type(state),file=sys.stderr)
        # print('Done get_dealer_states_from_belief_states len returing:', len(dealer_states_to_return), file=sys.stderr)
        # return dealer_states_to_return


                
    def get_bet_states_from_dealer_states(self, dealer_states: list[tuple[DealerState,float]]) -> list[BetState]:
        dealer_states_to_process = dealer_states
        bet_states = []
        #use the list as a queue for the dealer states that need to be processed multiple times. 
        while(len(dealer_states_to_process) > 0 ):
            (this_state, prob) = dealer_states_to_process.pop()
            if this_state == None:
                continue
            actions = this_state.generate_actions()
            for action in actions:
                next_states = this_state.generate_state(action, self.max_bet, self.stop_high, self.stop_low)
                for state_tuple in next_states:
                    (state, probability) = state_tuple
                    #if the state is another dealer state add it to the 
                    if state == None:
                        continue
                    elif isinstance(state,DealerState):
                        dealer_states_to_process.append(state_tuple)
                    else:
                        bet_states.append(state_tuple)
        print('Done get_bet_states_from_dealer_states len returning',len (bet_states), file=sys.stderr)
                        
        return bet_states
                        
                       


    # TODO for back prop function 
    # in the state classes add a parent tuple 
    # so (parent_state, action_from_parent, transition_probability_given action)
    # add to the constructor so nodes know where they came from. 
    # add a children_count
    # add a weighted_value_total for each action which is a weighted average for this node of the children. 
    # so each child will update this with their own value times their tansition probablity.
    

    def backprop(self, bet_state:BetState, depth= 'Bet Root'):
        '''
        depth = 'Bet Root'
        depth = 'Observed State' will stop propigating at observed state for decison tree.  
        '''
        #go from bet state to dealer state
        print('backprob bet state value', bet_state.weighted_value_high, file=sys.stderr)
        prev_state = bet_state
        next_state = prev_state.parent 
        prev_value = bet_state.weighted_value_high
        while (isinstance(next_state, DealerState)):
            #dealer State
            next_state.weighted_value_total = next_state.weighted_value_total + (prev_value * prev_state.parent_tuple[2])
            #iterate forward
            prev_value = next_state.weighted_value_total
            prev_state = next_state
            next_state = next_state.parent
            
        #next_state is now a belief state and prev_state is a dealer State
        while(isinstance(next_state,BeliefState)):
            #next state is belief state
            action = prev_state.parent_tuple[1]
            #get prev_state's value
            value = 0
            if isinstance(prev_state,DealerState):
                value = prev_state.weighted_value_total
            else:
                value = max(prev_state.weighted_value_hit, prev_state.weighted_value_stand, prev_state.weighted_value_double)
            if action == 'h':
                next_state.weighted_value_hit += (prev_state.parent_tuple[2] * value)
            elif action == 's':
                next_state.weighted_value_stand += (prev_state.parent_tuple[2] * value)
            elif action == 'd':
                next_state.weighted_value_stand += (prev_state.parent_tuple[2] * value)
            else:
                print("error in backprob 2nd while", file=sys.stderr)
                return False
            #iterate forward
            prev_state = next_state            
            next_state = next_state.parent

        assert isinstance(next_state,ObservedState), "Error not observed state"
        
        #update the observed state from the belief state
        next_state.weighted_value_total += prev_state.weighted_value_total * prev_state.parent_tuple[2]

        #stop early if only observed 
        if depth != 'Bet Root':
            return


        prev_state = next_state
        next_state = next_state.parent

        assert isinstance(next_state,BetState), "Error not bet State"
        [action, bet] = prev_state.parent_tuple[1].split(' ', 1)
        
        if(action == 'betH'): 
            #high bet 
            next_state.weighted_value_high += prev_state.weighted_value_total*prev_state.parent_tuple[2]
        elif action == 'betM':
            next_state.weighted_value_med += prev_state.weighted_value_total*prev_state.parent_tuple[2]
        elif action == 'betL':
            next_state.weighted_value_low += prev_state.weighted_value_total*prev_state.parent_tuple[2]
        else: 
            print("error in backprob action not found", file=sys.stderr)
            return False
        


        # starting = state

        # while not isinstance(starting.parent, BetState):
        #     #update weigheted value of parent
        #     starting.parent.weighted_value_total = starting.parent.weighted_value_total + (starting.weighted_value_total * starting.parent_tuple[2])

        #     #update child counter of parent
        #     starting.parent.childtotal = starting.parent.childtotal + 1

        #     starting = starting.parent


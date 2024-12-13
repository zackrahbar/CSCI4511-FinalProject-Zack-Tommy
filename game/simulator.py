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
            return 1 
        if len(bet_state_actions) == 1 and bet_state_actions[0] == 'Stop Failure':
            #return failure
            return 0
        

        # exploring down the tree. 
        # can add filtering here inbetween steps. by sorting the nodes. using .sort(reverse=True, key= lambda x: x[1]) sorts so highest probability is at front. 
        observed_state_tuples = Simulator.get_observed_states_from_bet_state(bet_state, 1.0)

        belief_state_tuples = Simulator.get_belief_states_from_observed_states(observed_state_tuples)

        dealer_state_tuples = Simulator.get_dealer_states_from_belief_states(belief_state_tuples)

        final_bet_states = self.get_bet_states_from_dealer_states(dealer_state_tuples)

        #todo call backprop on the bet states. 



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

        return states_to_return 
        
    
    @staticmethod 
    def get_belief_states_from_observed_states(observed_states: list[tuple[ObservedState,float]]) -> list[tuple[BeliefState,float]]:
        belief_states = []
        for state_tuple in observed_states:
            (state, belief) = state_tuple
            for num in list(range(2,11)+['A']):
                belief_states.append(state.generate_belief_states(num))
        return belief_states
        

    @staticmethod
    def get_dealer_states_from_belief_states(belief_states: list[tuple[BeliefState,float]])-> list[tuple[DealerState]]:
        belief_states_to_process = belief_states
        dealer_states_to_return = []
        while(len(belief_states_to_process) > 0):
            (state, belief_prob) = belief_states_to_process.pop()
            actions = state.generate_action()
            for action in actions:
                new_states = state.generate_next_states(action)
                for state_tuple in new_states:
                    if state_tuple[0] == None:
                        continue
                    if state_tuple[0].isinstance(DealerState):
                        dealer_states_to_return.append(state_tuple)
                    else: 
                        belief_states_to_process.append(state_tuple)
        return dealer_states_to_return


                
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
                    elif state.isinstance(DealerState):
                        dealer_states_to_process.append(state_tuple)
                    else:
                        bet_states.append(state_tuple)
        return bet_states
                        
                       


    # TODO for back prop function 
    # in the state classes add a parent tuple 
    # so (parent_state, action_from_parent, transition_probability_given action)
    # add to the constructor so nodes know where they came from. 
    # add a children_count
    # add a weighted_value_total for each action which is a weighted average for this node of the children. 
    # so each child will update this with their own value times their tansition probablity.
    

    def turn(self):
        '''
        '''
from simulate import CardSet, BetState, ObservedState, BeliefState, DealerState
from src.objects import Player, Card, Dealer
import sys
import copy
from src.constants import *

class Simulator:
    def __init__(self):
        ''' idk '''
    def betting(self, bet_state: BetState, max_bet: int, stop_high: int, stop_low: int ):
        
        
        self.root_bet_state = bet_state
        bet_state_actions = bet_state.generate_actions()
        print("Bet state actions: ", bet_state_actions, file=sys.stderr)
        if len(bet_state_actions) == 1 and bet_state_actions[0] == 'Stop Success':
            #return succcess
            return 1 
        if len(bet_state_actions) == 1 and bet_state_actions[0] == 'Stop Failure':
            #return failure
            return 0
        possible_observed_states = []
        for action in bet_state_actions:
            possible_observed_states.extend(bet_state.generate_next_states(action))
        belief_states = []
        # now for each of the possible observed states we will generate 10 belief states
        for (observed_state, probability) in possible_observed_states:
            for num in list(range(2,11)+['A']):
                belief_states.append(observed_state.generate_belief_states(num))
            
        # explore the belief states
        for belief_state in belief_states:
            (state, probability) = belief_state
            actions_bs = state.generate_action()
            for act in actions_bs:
                act




    @staticmethod            
    def get_bet_states_from_dealer(dealer_states: list[tuple[DealerState,float]], max_bet: int, stop_high: int, stop_low: int ) -> list[BetState]:
        dealer_states_to_process = dealer_states
        while(len(dealer_states_to_process) > 0 ):
            (this_state, prob) = dealer_states_to_process.pop()
            actions = this_state.generate_actions()
            for action in actions:
                next_states = this_state.generate_state(action, max_bet, stop_high, stop_low)
                for state in next_states 
    def turn(self):
        '''
        '''
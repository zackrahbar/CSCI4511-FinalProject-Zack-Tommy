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
    def get_observed_states_from_bet_state(bet_state: BetState) -> list[tuple[ObservedState,float]]: 
        actions = bet_state.generate_actions()
        if len(actions) == 1:
            #stop success or failure 
            if actions == 'Stop Success':
            #error should have stopped here
                pass
            if action == 'Stop Failure':
                pass
            #todo finish this 
        pass
        
    
    @staticmethod 
    def get_belief_states_from_observed_states(observed_states: list[tuple[ObservedState,float]]) -> list[tuple[BeliefState,float]]:
        pass

    @staticmethod
    def get_dealer_states_from_belief_states(belief_states: list[tuple[BeliefState,float]])-> list[tuple[DealerState]]:
        
        
        
        pass


    @staticmethod            
    def get_bet_states_from_dealer_states(dealer_states: list[tuple[DealerState,float]], max_bet: int, stop_high: int, stop_low: int ) -> list[BetState]:
        dealer_states_to_process = dealer_states
        bet_states = []
        #use the list as a queue for the dealer states that need to be processed multiple times. 
        while(len(dealer_states_to_process) > 0 ):
            (this_state, prob) = dealer_states_to_process.pop()
            if this_state == None:
                continue
            actions = this_state.generate_actions()
            for action in actions:
                next_states = this_state.generate_state(action, max_bet, stop_high, stop_low)
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
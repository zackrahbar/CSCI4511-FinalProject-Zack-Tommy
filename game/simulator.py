from simulate import CardSet, BetState, ObservedState, BeliefState, DealerState
from src.objects import Player, Card, Dealer
import sys
import copy
from src.constants import *

class Simulator:
    def __init__(self):

    def betting(self):

    def backprop(self, state):

        starting = state

        while not isinstance(starting.parent, BetState):
            #update weigheted value of parent
            starting.parent.weighted_value_total = starting.parent.weighted_value_total + (starting.weighted_value_total * starting.parent_tuple[2])

            #update child counter of parent
            starting.parent.childtotal = starting.parent.childtotal + 1

            starting = starting.parent


    def turn(self):
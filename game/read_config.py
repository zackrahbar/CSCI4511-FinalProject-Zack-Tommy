
import yaml
import sys
from src.constants import SUIT
from src.objects import Card
#config class opens a config file and then stores it in memory and addess accessor functions for 

# variables expected in config metadata 
METADATA_CONTAINS_VARS = ['players',
                              'computer_players',
                              'deck_mode',
                              'num_decks',
                              'deck_seed']
# varaiabled expected in a computer player
PLAYER_COMP_CONTAINS_VARS = [
    'mode',
    'start_money',
    'stop_loss_high',
    'stop_loss_low'
]
PLAYER_USER_CONTAINS_VARS = [
    'mode',
    'start_money'
]

MAX_CFG_PLAYERS = 4
MAX_CFG_NUM_DECKS = 10

class Config:

    

    def __init__(self, path: str):
        #check if file exists
        self.players = []
        self.total_players = 0
        self.computer_players = 0 
        self.deck_mode = 'random'
        self.num_decks = 8
        self.deck_seed = 'seed'
        self.cards = []
        try: 
            with open(path, "r") as file:
                yaml_data = yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Error: The file '{path}' does not exist. Please check the file path.", file=sys.stderr)
            sys.exit(1)
        except yaml.YAMLError as e: 
            print(f"Error: Failed to parse the YAML file. Details: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"An unexpected error occurred: {e}", file=sys.stderr)
            sys.exit(1)

        # convert into varaibles 
        try:
            metadata = yaml_data['metadata']
            for key in METADATA_CONTAINS_VARS:
                if key not in metadata:
                    print("Error key : ", key, 'does not exist in metadata', file=sys.stderr)
                    sys.exit(1)
            self.total_players = int(metadata['players'])
            if self.total_players > MAX_CFG_PLAYERS or self.total_players < 1:
                print("Error: num players is invalid: ", self.total_players, 'Must be 1 or greater and less than ',MAX_CFG_PLAYERS, file=sys.stderr)
                sys.exit(1)
            
            self.computer_players = int(metadata['computer_players'])
            if(self.computer_players < 0) or (self.computer_players > self.total_players):
                print("Error: num computer_players is invalid: ", self.total_players, 'Must be 0 or greater and less than players specified', file=sys.stderr)
                sys.exit(1)
            self.deck_mode = metadata['deck_mode']
            
            if(self.deck_mode != 'ordered' and self.deck_mode != 'uniform_random' and self.deck_mode != 'random'):
                print("Error: invalid deck mode: ", self.deck_mode, file=sys.stderr)
                sys.exit(1)
            self.num_decks = int(metadata['num_decks'])
            if(self.num_decks < 1 or self.num_decks > MAX_CFG_NUM_DECKS):
                print("Error: invalid num decks", file=sys.stderr)
                sys.exit(1)
            
            self.deck_seed = metadata['deck_seed']

            self.players = []
            # now check for player configs
            computer_cnt = 0
            for i in range(1,self.total_players+1):
                key = 'player' + str(i)
                player = yaml_data[key]
                print("this player: ", key , file=sys.stderr)
                print(player, file=sys.stderr)
                if 'mode' not in player:
                    print("Error key : ", 'mode', 'does not exist in metadata', file=sys.stderr)
                    sys.exit(1)
                if player['mode'] == 'computer':
                    for key in PLAYER_COMP_CONTAINS_VARS:
                        if key not in player:
                            print("Error key : ", key, 'does not exist in player ', i,'.', file=sys.stderr)
                            sys.exit(1)
                elif player['mode'] == 'user':
                    for key in PLAYER_USER_CONTAINS_VARS:
                        if key not in player:
                            print("Error key : ", key, 'does not exist in player ', i,'.', file=sys.stderr)
                            sys.exit(1)
                    
                elif player['mode'] == 'random':
                    for key in PLAYER_USER_CONTAINS_VARS:
                        if key not in player:
                            print("Error key : ", key, 'does not exist in player ', i,'.', file=sys.stderr)
                            sys.exit(1)
                    
                else:
                    print("Error in key : ", 'mode is incorrect in player', i,'.', file=sys.stderr)
                    sys.exit(1)
                self.players.append(player)

            print("Players", file=sys.stderr)
            print(self.players, file=sys.stderr)

            #now parse deck if required 
            self.cards = []
            if self.deck_mode == 'ordered':
                if 'deck' not in yaml_data:
                    print("Error: deck is not specified when deck mode is ordered", file=sys.stderr)
                    sys.exit(1)
                yaml_card_list = yaml_data['deck']
                #build deck obejcts 
                for card_str in yaml_card_list: 
                    print("card_str", file=sys.stderr)
                    
                    [suit,num] = card_str.split('',1)
                    this_suit
                    if suit == 'D': 
                        this_suit = SUIT.D
                    elif suit == 'S':
                        this_suit = SUIT.S
                    elif suit == 'H':
                        this_suit = SUIT.H
                    elif suit == 'C':
                        this_suit = SUIT.C
                    else: 
                        print("Card Suit invalid ", suit, file=sys.stderr)
                        sys.exit(1)
                    card = Card(this_suit,num)
                    self.cards.append(card)

            

        except yaml.YAMLError as e: 
            print(f"Error: Failed to parse the YAML file. Details: {e}", file=sys.stderr)
            sys.exit(1)

        
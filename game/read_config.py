
import yaml
import sys
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

        try: 
            with open(path, "r") as file:
                yaml_data = yaml.load(file)
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
            if(self.deck_mode != 'ordered' or self.deck_mode != 'uniform_random' or self.deck_mode != 'random'):
                print("Error: invalid deck mode", file=sys.stderr)
                sys.exit(1)
            self.num_decks = int(metadata['num_decks'])
            if(self.num_decks < 1 or self.num_decks > MAX_CFG_NUM_DECKS):
                print("Error: invalid num decks", file=sys.stderr)
                sys.exit(1)
            
            self.deck_seed = metadata['deck_seed']

            self.players = []
            # now check for player configs
            computer_cnt = 0
            for i in range(0,self.total_players):
                key = 'player' + str(self.total_players)
                player = yaml_data[key]
                if 'mode' not in player:
                    print("Error key : ", 'mode', 'does not exist in metadata', file=sys.stderr)
                    sys.exit(1)
                if player['mode'] == 'computer':
                    for key in PLAYER_COMP_CONTAINS_VARS:
                        if key not in metadata:
                            print("Error key : ", key, 'does not exist in player ', i,'.', file=sys.stderr)
                            sys.exit(1)
                elif player['mode'] == 'user':
                    for key in PLAYER_USER_CONTAINS_VARS:
                        if key not in metadata:
                            print("Error key : ", key, 'does not exist in player ', i,'.', file=sys.stderr)
                            sys.exit(1)
                else:
                    print("Error in key : ", 'mode is incorrect in player', i,'.', file=sys.stderr)
                    sys.exit(1)
                self.players.append(player)



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
                    #TODO finish this my spliting strings then creating card objects and then adding to the list


        except yaml.YAMLError as e: 
            print(f"Error: Failed to parse the YAML file. Details: {e}", file=sys.stderr)
            sys.exit(1)

        
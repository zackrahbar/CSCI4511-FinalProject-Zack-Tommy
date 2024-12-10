
import yaml
#config class opens a config file and then stores it in memory and addess accessor functions for 
class Config:

    def __init__(self, path: str):
        #check if file exists
        self.players = []

        try: 
            with open(path, "r") as file:
                yaml_data = yaml.load(file)





        except FileNotFoundError:
            print(f"Error: The file '{path}' does not exist. Please check the file path.")
        except yaml.YAMLError as e: 
            
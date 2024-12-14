# CSCI4511-FinalProject-Zack-Tommy

Project Report:

Software and Hardware Requirements:
 A laptop with python installed.

How to run:
  cd into the game folder
  python game.py -f configs/___.YAML 2> err.log
  replace the ____ with your desired file, for example 1user1rand.yaml creates a game with one random player and one human player
  We have created 4 config files that are best to showcase our work:
    1: 1user1POMDP.YAML creates 1 human player and 1 POMDP player
    2: POMDPAgent.YAML creates just a POMDP player
    3: 1user1rand.YAML creates 1 human player and 1 random player
    4: POMDPAgent.YAML creates just a random player
  Using one of the files with a human player will allow you to slow the pace of the game deliberately by not inputting commands right away in order to see the moves the random or POMDP players are making.

  if you run this command in the terminal it may return an error, this is because in order to work, your terminal must be strecthed to cover your whole screen, only then can the interface work and the simulation run


Data Soruces:
 We found the implemented game of blackjack int he terminal usign python from this repository: https://github.com/Justinyu1618/terminal_blackjack
 This repository included the playable game of plackjack with the logic for the dealer, the cards, and the game flow. The game was designed to be played by a human entering commands in the terminal. The README.md file in the folder game is the readme from this file and contains an explanation of the logic used and how to play the game.

Motivation:
 We were motivated to pursue this project because of blackjack. While we both knew of the game, neither fo us had an intimate knowledge of it and were excited to not only solve the game but to learn something new while doing so. We also found the triviality of thsi problem interesting. There are so many variations on number of decks, number of opponents, and type of opponents, and modifying each of these values could make the problem much easier or much more complicated. Findign a solution that worked for an easier variation and the problem and a harder variation of the problem excited us and provided motivation to pursue this project. 

Explanation of acomplishments:
 solver.py:
  We created this file. This file contains the classes for two new types of players for this game, a random player and a POMDP player. These classes both extend Player from objects.py but with redefined methods to take in the appropriate inputs and output commands instead of them beign entered in the terminal.
 game.py:
  This file existed already. We modified it to work with our new player types. This required editing the method calls for each player type since they required inputs. We removed a loop of human feedback to ask if the game should continue after each round and let the POMDP player make that decision. We modified this file to read in information from a config file to determine the numebr of decks for a round, the number of players, the types of players, their starting money, and their stoploss and their goal. This replaced logic in the original game that either had these values hardcoded or relied on user input. 
configs (folder):
 We created these files. This folder contains a variety of configuration files that are used to create versions of teh game for our testing purposes. These files define the numebr of decks for a round, the number of players, the types of players, their starting money, and their stoploss and their goal.
read_config.py:
 We created this file. This file pareses the .YAML configuration file and passes that data into game.py when called. 
simulate.py:
 We created this file. This file contains the definiton of 5 classes: CardSet, BetState, ObservedState, BeliefState, and DealerState. CardSet was a class we cdesigned to make our calculations easier. This class contains a set of cards, and a variety of mehtods such as calculatign the total value of cards in a CardSet, subtract a cardset from another, and the brobability of a crad being the next card dealt from a cardset. The four state classes represent the four types of states we have defined for our problem. Each one contains a get actions method that returns the possible action(s) that can be taken from this state. They also contain a get states method that given an action returns the possible state(s) that can occur from the current state and the action specified. Each of these four state classes contain a parent and child variable (which can be any type of the four states) to form the tree of states throughout our game.
simulator.py:
 We created this file. This is where we perform our Monte Carlo search and calculate bets and actiosn for the POMDP player to take.   

Measurement of success:
 We measure our success by analysing the win percentage of the random player and the POMDP player. Simply if the POMDP player can win a higher percentage games than the random player we have designed a player that is taking more intentional actions and truly playing blackjack using Monte Carlo Tree Search rather than taking actions and makign bets randomly. 
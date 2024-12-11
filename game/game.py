from uuid import uuid4
from src.display_util import DisplayTable
from src.constants import *
from src.objects import Card, Player, Dealer
from random import randint
import curses
import sys
from read_config import Config 
from solver import Random, POMDPPlayer

class Game:
	def __init__(self, stdscr, cfg):
		self.config = cfg
		self.players = []
		if cfg != None:
			self.num_decks = cfg.num_decks
		else:
			self.num_decks = NUM_DECKS
		self.dealer = Dealer(self.num_decks)
		self.display = DisplayTable(stdscr)
		self.screen = stdscr
	
	def get_num_decks(self):
		return self.num_decks

	def sleep(self, time):
		self.screen.timeout(time)
		self.screen.getch()
		self.screen.timeout(-1)

	def run(self):
		while(True):
			if self.start():
				keep_playing = True
				while(keep_playing):
					self.sleep(1000)
					self.gameplay()
					self.reset()
					if not self.players:
						break
					keep_playing = self.end()
			self.end_game()

	def start(self):
		curses.echo()
		if curses.LINES < MIN_HEIGHT:
			self.print(f"HEIGHT TOO SMALL ({curses.LINES})")
			self.sleep(2000)
			return False
		self.display.set_dealer(self.dealer)
		max_players = min(int(curses.COLS / MIN_PLAYER_WIDTH), MAX_PLAYERS)
		self.display.max_players = max_players
		self.display.set_state("starting")
		self.display.refresh()
		if int(curses.COLS / MIN_PLAYER_WIDTH) < MAX_PLAYERS:
			self.print("*Screen too small**")
		p_count = 0
		key = None
		if self.config != None:
			for cfg_player in self.config.players:
				p_count += 1
				if cfg_player['mode'] == 'random': 
					new_player = Random(f"Player {p_count}", f"P{p_count}")
				elif cfg_player['mode'] == 'user':
					new_player = Player(f"Player {p_count}", f"P{p_count}")
					#TODO add POMDP
				elif cfg_player['mode'] == 'POMDP':
					new_player = POMDPPlayer(f"Player {p_count}", f"P{p_count}", self.get_num_decks())
				self.players.append(new_player)
				self.display.add_player(new_player)
		else:
			while(p_count != max_players and key != ord('s')):
				key = self.screen.getch()
				if key == ord('n'):
					p_count += 1
					new_player = Player(f"Player {p_count}", f"P{p_count}")
					self.players.append(new_player)
					self.display.add_player(new_player)
		return True
		
	def gameplay(self):
		self.display.set_state("betting")
		self._betting()
		self.display.set_state("dealing")
		self._dealing()
		self.display.set_state("turn")
		self._turn()
		self.display.set_state("scoring")
		self._scoring()
		self.sleep(1000)
		self.check_losers()	

	def _betting(self):
		for player in self.players:
			if isinstance(player, Random):
				self.display.set_turn(player)
				bet = player.make_bet(0)
				self.display.set_state("betting")
			elif isinstance(player,Player):
				self.display.set_turn(player)
				bet = ""
				while(not bet.isdigit() or int(bet) > player.money or int(bet) < BET_MIN or int(bet) > BET_MAX):
					bet = self.screen.getstr()
					self.display.set_state("betting_error")
				self.display.set_state("betting")
				player.make_bet(bet)
			elif isinstance(player,POMDPPlayer):
				self.display.set_turn(player)
				bet = player.make_bet(self)
				if bet == 0:
					player.lose()
				if bet == 1:
					player.lose()
				self.display.set_state("betting")
		self.display.set_turn(None)
	
	def _dealing(self):
		for i in range(2):
			for p in self.players:
				p.add_card(self.dealer.deal())
				self.display.refresh()
				self.sleep(300)
			self.dealer.add_card(self.dealer.deal(facedown = i == 1))
			self.display.refresh()

	def _turn(self):
		for i in range(len(self.players)):
			player = self.players[i]
			if isinstance(player, Random):
				cmd = player.get_options()
				self.display.set_turn(player)
				while(True):
					if cmd == ord('h'):
						player.add_card(self.dealer.deal())
						cmd = player.get_options()
					elif cmd == ord(CMD.STAND.value):
						break
					elif cmd == ord(CMD.DOUBLE.value) and CMD.DOUBLE in set(player.options):
						player.money -= player.bet
						player.bet *= 2
						player.add_card(self.dealer.deal())
						if player.bust():
							self.dealer.add_money(player.lose())
						break
					self.display.refresh()
					self.sleep(300)
					if player.bust():
						self.dealer.add_money(player.lose())
						break
			elif isinstance(player,Player):
				player.get_options()
				self.display.set_turn(player)
				while(True):
					cmd = self.screen.getch()
					while(cmd not in list(map(lambda x:ord(x.value), CMD))):
						cmd = self.screen.getch()
					if cmd == ord('h'):
						player.add_card(self.dealer.deal())
					elif cmd == ord(CMD.STAND.value):
						break
					elif cmd == ord(CMD.DOUBLE.value) and CMD.DOUBLE in set(player.options):
						player.money -= player.bet
						player.bet *= 2
						player.add_card(self.dealer.deal())
						if player.bust():
							self.dealer.add_money(player.lose())
						break
					self.display.refresh()
					self.sleep(300)
					if player.bust():
						self.dealer.add_money(player.lose())
						break
		self.display.set_turn(None)
		self.dealer.reveal()
		while(not self.dealer_bust() and max(self.dealer.sums()) < 17):
			self.dealer.add_card(self.dealer.deal())
			self.print("Dealing....", 1000)

	def _scoring(self):
		if(not self.dealer.bust() and any([p.cards for p in self.players])):
			dealer_sum = max(self.dealer.sums())
			for p in self.players:
				if p.cards:
					self.display.set_turn(p)
					self.print(f"{p.name} vs Dealer", 1000)
					if max(p.sums()) > dealer_sum: 
						self.print(f"{p.name} Wins!")
						self.dealer.money -= p.bet
						p.win()
					elif max(p.sums()) < dealer_sum:
						self.print("Dealer Wins!")
						self.dealer.add_money(p.lose())
					else:
						self.print("Standoff!")
						p.standoff()
					self.sleep(1000)

	def end(self):
		self.display.set_state("end")
		while(True):
			cmd = self.screen.getch()
			if cmd == ord('y'):
				return True 
			elif cmd == ord('n'):
				return False

	def end_game(self):
		for i in range(5,0,-1):
			self.print(f" Game Over! (restarting in {i})",1000)
		self.display.restart()


	def print(self, msg, delay=0):
		self.display.print(msg)
		self.sleep(delay)

	def reset(self):
		for p in self.players:
			p.reset()
		self.dealer.reset()
		self.display.set_turn(None)
	
	def check_losers(self):
		to_remove = set()
		for p in self.players:
			if p.money <= 0:
				self.print(f"{p.name} has lost!", 1000)
				to_remove.add(p)
				self.display.remove_player(p)
		for p in to_remove:
			self.players.remove(p)

		
	def dealer_bust(self):
		if self.dealer.bust():
			self.print("Dealer BUST!", 1000)
			for p in self.players:
				if p.cards: 
					self.dealer.money -= p.bet
					p.win()
			self.display.refresh()
			return True
		return False

def open_test_config_file(path: str):
	print("", file=sys.stderr)

def main(stdscr):


	## add in testing support
	args = sys.argv[1:]
	if len(args) == 2:
		if args[0] == '-f':
			path = args[1]
			cfg = Config(path)
		print("Invalid args")
	else: 
		cfg = None
	#TODO add config to the game state so that we can access it when setting up the game

	init_colors()
	game = Game(stdscr,cfg)
	game.run()

if __name__ == '__main__':
	stdscr = curses.initscr()
	curses.wrapper(main)	


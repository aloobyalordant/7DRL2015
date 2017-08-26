import libtcodpy as libtcod

class PowerUp:

	def __init__(self, name = "Example bonus", tech_description = "Does specific thing under specific circumstance", verbose_description= "A vague and mysterious item, said to confer great fortune on those who can satisfy its capricious whims.", updates_on_player_attack_choice = False, affects_strength_at_attack_choice = False):
		self.name = name
		self.tech_description = tech_description  		# short description of what item does
		self.verbose_description= verbose_description  		# a wordier description that someone in the game world might give
		self.updates_on_player_attack_choice = updates_on_player_attack_choice
		self.affects_strength_at_attack_choice = affects_strength_at_attack_choice


class WallHugger(PowerUp):

	def __init__(self):
		PowerUp.__init__(self, name = "Wall Hugger", tech_description = "+1 strength when up against a wall", verbose_description = "Whether as cover or as a dead end, a wall at your back will grant you strength", updates_on_player_attack_choice = True, affects_strength_at_attack_choice = True)
		self.activated = False

	def update_on_player_attack_choice(self, player, objectsArray, map):
		# global player, objectsArray, map    #I feel I should be able to do this instead of passing them to method, but... no?
		against_wall = False
		try:
			if map[player.x-1][player.y-1].blocked and map[player.x-1][player.y].blocked and map[player.x-1][player.y+1].blocked:
				against_wall = True
		except IndexError:		#todo: check that this is the right thing to catch...
			print ''
		try:
			if map[player.x+1][player.y-1].blocked and map[player.x+1][player.y].blocked and map[player.x+1][player.y+1].blocked:
				against_wall = True
		except IndexError:		#todo: check that this is the right thing to catch...
			print ''
		try:
			if map[player.x-1][player.y-1].blocked and map[player.x][player.y-1].blocked and map[player.x+1][player.y-1].blocked:
				against_wall = True
		except IndexError:		#todo: check that this is the right thing to catch...
			print ''
		try:
			if map[player.x-1][player.y+1].blocked and map[player.x][player.y+1].blocked and map[player.x+1][player.y+1].blocked:
				against_wall = True
		except IndexError:		#todo: check that this is the right thing to catch...
			print ''
		if against_wall:
			self.activated = True
		else:
			self.activated = False


	def affect_strength_at_attack_choice(self):
		if self.activated:
			print "+1 strength from " + str(self.name)
			return 1
		else:
			return 0

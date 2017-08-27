import libtcodpy as libtcod

class PowerUp:

	def __init__(self, name = "Example bonus", tech_description = "Does specific thing under specific circumstance", verbose_description= "A vague and mysterious item, said to confer great fortune on those who can satisfy its capricious whims."):
#, updates_on_player_attack_choice = False, affects_strength_at_attack_choice = False):
		self.name = name
		self.tech_description = tech_description  		# short description of what item does
		self.verbose_description= verbose_description  		# a wordier description that someone in the game world might give
		# self.updates_on_player_attack_choice = updates_on_player_attack_choice
		# self.affects_strength_at_attack_choice = affects_strength_at_attack_choice
		self.activated = False		# generally this is a thing that determines whether to grant a bonus. Won't always be applicable

class WallHugger(PowerUp):

	def __init__(self):
		PowerUp.__init__(self, name = "Wall Hugger", tech_description = "+1 strength when up against a wall", verbose_description = "Whether as cover or as a dead end, a wall at your back will grant you strength.")
#, updates_on_player_attack_choice = True, affects_strength_at_attack_choice = True)

	# Activates if player has 3 wall segments on one side
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
			self.activated = False			# probably a good safety tip is to always reset activated status
			print "+1 strength from " + str(self.name)
			return 1
		else:
			return 0




class Mindfulness(PowerUp):

	def __init__(self):
		PowerUp.__init__(self, name = "Mindfulness", tech_description = "+1 energy recharge when standing still", verbose_description = "Stop and take a moment to focus on yourself and your surroundings, and you will find yourself energised and better prepared for the challenges ahead.")

	#standing still is enough to activate this ability
	def update_on_standing_still(self, player, objectsArray, map):
		self.activated = True
	
	def affect_rate_of_energy_recharge(self):
		if self.activated:
			self.activated = False			# probably a good safety tip is to always reset activated status
			print "+1 energy from " + str(self.name)
			return 1
		else:
			return 0


class NeptunesBlessing(PowerUp):

	def __init__(self):
		PowerUp.__init__(self, name = "Neptune's Blessing", tech_description = "+1 strength when next to or in water", verbose_description = "A coral amulet that grants increased strength when near water.")

	#TODO: 
	# Activates if there is water on the player's square or hoirzontally/vertically adjacent
	def update_on_player_attack_choice(self, player, objectsArray, map):

		# global player, objectsArray, map    #I feel I should be able to do this instead of passing them to method, but... no?
		near_water = False

		# test for water at player's location
		for ob in objectsArray[player.x][player.y]:
			if ob.name == 'water':
				near_water = True

		# test for water left of player
		if player.x > 0:
			for ob in objectsArray[player.x-1][player.y]:
				if ob.name == 'water':
					near_water = True


		# test for water right of player
		if player.x < len(objectsArray)-1:
			for ob in objectsArray[player.x+1][player.y]:
				if ob.name == 'water':
					near_water = True


		# test for water immediately north of player
		if player.y > 0:
			for ob in objectsArray[player.x][player.y-1]:
				if ob.name == 'water':
					near_water = True


		# test for water immediately south of player
		if player.y < len(objectsArray[player.x])-1:
			for ob in objectsArray[player.x][player.y+1]:
				if ob.name == 'water':
					near_water = True

		if near_water:
			self.activated = True
		else:
			self.activated = False


	def affect_strength_at_attack_choice(self):
		if self.activated:
			self.activated = False			# probably a good safety tip is to always reset activated status
			print "+1 strength from " + str(self.name)
			return 1
		else:
			return 0


class Amphibious(PowerUp):

	def __init__(self):
		PowerUp.__init__(self, name = "Amphibious", tech_description = "able to attack in water", verbose_description = "Fight in water as easily as on land.")


	def update_on_testing_can_attack(self, error_message):
		print 'messg ' + error_message
		if error_message == 'in water':
			self.activated = True

	def allows_attack(self):
		if self.activated:
			self.activated = False			# probably a good safety tip is to always reset activated status
			print "attack allowed due to " + str(self.name)
			return True
		else:
			return False
		

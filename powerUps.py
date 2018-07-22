import tdl as libtcod
#import libtcodpy as libtcod
import random
from random import randint


class PowerUp:

	def __init__(self, name = "Example bonus", tech_description = "Does specific thing under specific circumstance", verbose_description= "A vague and mysterious item, said to confer great fortune on those who can satisfy its capricious whims.", code = '???', cost = 3, status =  'dormant', tags = []):
#, updates_on_player_attack_choice = False, affects_strength_at_attack_choice = False):
		self.name = name
		self.tech_description = tech_description  		# short description of what item does
		self.verbose_description= verbose_description  		# a wordier description that someone in the game world might give
		self.code = code 					# 3 character code to represent this upgrade in GUI ?
		self.cost = cost 					# default cost for this upgrade (currency to be determined)
		# self.updates_on_player_attack_choice = updates_on_player_attack_choice
		# self.affects_strength_at_attack_choice = affects_strength_at_attack_choice
		self.activated = False		# generally this is a thing that determines whether to grant a bonus. Won't always be applicable
		self.status = status		# 'dormant' - not doing anything; 'enabled' = in a situation to potentially do a thing; 'active' - doing a thing
		self.tags = tags		# including... aggressive for things that increase attack strength, reflexive for things that affect the player inc energy stuff and healing, and supportive for things that don't fit in either category???

class WallHugger(PowerUp):

	def __init__(self):
		PowerUp.__init__(self, name = "Wall Hugger", tech_description = "+1 strength when up against a wall", verbose_description = "Whether as cover or as a dead end, a wall at your back will grant you strength.", code='W.H', tags = ['aggressive'])
#, updates_on_player_attack_choice = True, affects_strength_at_attack_choice = True)

	# Activates if player has 3 wall segments on one side
	def update_on_player_attack_choice(self, player, objectsArray, map, player_weapon):
		# global player, objectsArray, map    #I feel I should be able to do this instead of passing them to method, but... no?
		against_wall = False
		try:
			if map[player.x-1][player.y-1].blocked and map[player.x-1][player.y].blocked and map[player.x-1][player.y+1].blocked:
				against_wall = True
		except IndexError:		#todo: check that this is the right thing to catch...
			print('')
		try:
			if map[player.x+1][player.y-1].blocked and map[player.x+1][player.y].blocked and map[player.x+1][player.y+1].blocked:
				against_wall = True
		except IndexError:		#todo: check that this is the right thing to catch...
			print('')
		try:
			if map[player.x-1][player.y-1].blocked and map[player.x][player.y-1].blocked and map[player.x+1][player.y-1].blocked:
				against_wall = True
		except IndexError:		#todo: check that this is the right thing to catch...
			print('')
		try:
			if map[player.x-1][player.y+1].blocked and map[player.x][player.y+1].blocked and map[player.x+1][player.y+1].blocked:
				against_wall = True
		except IndexError:		#todo: check that this is the right thing to catch...
			print('')
		if against_wall:
			self.activated = True
		else:
			self.activated = False


	def affect_strength_at_attack_choice(self):
		if self.activated:
			self.activated = False			# probably a good safety tip is to always reset activated status
			print("+1 strength from " + str(self.name))
			self.status = 'active'
			return 1
		else:
			return 0




class Mindfulness(PowerUp):

	def __init__(self):
		PowerUp.__init__(self, name = "Mindfulness", tech_description = "+1 energy recharge when standing still", verbose_description = "Stop and take a moment to focus on yourself and your surroundings, and you will find yourself energised and better prepared for the challenges ahead.", code='Mnd', tags = ['reflexive'])

	#standing still is enough to activate this ability
	def update_on_standing_still(self, player, objectsArray, map):
		self.activated = True
	
	def affect_rate_of_energy_recharge(self):
		if self.activated:
			self.activated = False			# probably a good safety tip is to always reset activated status
			print("+1 energy from " + str(self.name))
			self.status = 'active'
			return 1
		else:
			return 0


class NeptunesBlessing(PowerUp):

	def __init__(self):
		PowerUp.__init__(self, name = "Neptune's Blessing", tech_description = "+1 strength when next to or in water", verbose_description = "A coral amulet that grants increased strength when near water.", code='N.B', tags = ['aggressive'])

	#TODO: 
	# Activates if there is water on the player's square or hoirzontally/vertically adjacent
	def update_on_player_attack_choice(self, player, objectsArray, map, player_weapon):

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
			print("+1 strength from " + str(self.name))
			self.status = 'active'
			return 1
		else:
			return 0


class Amphibious(PowerUp):

	def __init__(self):
		PowerUp.__init__(self, name = "Amphibious", tech_description = "able to attack in water", verbose_description = "Fight in water as easily as on land.", code='Amp', tags = ['supportive'])


	def update_on_testing_can_attack(self, error_message):
		print('messg ' + error_message)
		if error_message == 'in water':
			self.activated = True

	def allows_attack(self):
		if self.activated:
			self.activated = False			# probably a good safety tip is to always reset activated status
			print("attack allowed due to " + str(self.name))
			self.status = 'active'
			return True
		else:
			return False
		
class PersonalSpace(PowerUp):

	def __init__(self):
		PowerUp.__init__(self, name = "Personal Space", tech_description = "+1 strength when more than 2 spaces from any walls or doors", verbose_description = "Nothing better than an open battlefield to grant you strength.", code='P.S', tags = ['aggressive'])
#, updates_on_player_attack_choice = True, affects_strength_at_attack_choice = True)

	# Activates if player has no walls or doors on any adjacent space (including diagonally)
	# Update: now has to be 2 spaces in any direction (was OP before)
	# TODO actuzlly do this (currently it's just the wallhugger code)
	def update_on_player_attack_choice(self, player, objectsArray, map, player_weapon):
		# global player, objectsArray, map    #I feel I should be able to do this instead of passing them to method, but... no?
		lots_of_space = True

		try:
			for dx in range (-2,2+1):			#ergh
				for dy in range(-2,2+1):
					if map[player.x+dx][player.y+dy].blocked:
						lots_of_space = False
					for object in objectsArray[player.x+dx][player.y+dy]:
						if object.blocks and object.door is not None:
							lots_of_space = False
		except IndexError:
			print('')


	#	try: 
	#		if map[player.x-1][player.y].blocked:
	#			lots_of_space = False
	#		for object in objectsArray[player.x-1][player.y]:
	#			if object.blocks and object.door is not None:
	#				lots_of_space = False
	#	except IndexError:
	#		print('')
	#
	#	try: 
	#		if map[player.x+1][player.y].blocked:
	#			lots_of_space = False
	#		for object in objectsArray[player.x+1][player.y]:
	#			if object.blocks and object.door is not None:
	#				lots_of_space = False
	#	except IndexError:
	#		print('')
#
#		try: 
#			if map[player.x][player.y-1].blocked:
#				lots_of_space = False
#			for object in objectsArray[player.x][player.y-1]:
#				if object.blocks and object.door is not None:
#					lots_of_space = False
#		except IndexError:
#			print('')
#
#		try: 
#			if map[player.x][player.y+1].blocked:
#				lots_of_space = False
#			for object in objectsArray[player.x][player.y+1]:
#				if object.blocks and object.door is not None:
#					lots_of_space = False
#		except IndexError:
#			print('')
#
#
#		try: 
#			if map[player.x-1][player.y+1].blocked:
#				lots_of_space = False
#			for object in objectsArray[player.x-1][player.y+1]:
#				if object.blocks and object.door is not None:
#					lots_of_space = False
#		except IndexError:
#			print('')
#
#		try: 
#			if map[player.x+1][player.y-1].blocked:
#				lots_of_space = False
#			for object in objectsArray[player.x+1][player.y-1]:
#				if object.blocks and object.door is not None:
#					lots_of_space = False
#		except IndexError:
#			print('')
#
#		try: 
#			if map[player.x+1][player.y+1].blocked:
#				lots_of_space = False
#			for object in objectsArray[player.x+1][player.y+1]:
#				if object.blocks and object.door is not None:
#					lots_of_space = False
#		except IndexError:
#			print('')
#
#		try: 
#			if map[player.x-1][player.y-1].blocked:
#				lots_of_space = False
#			for object in objectsArray[player.x-1][player.y-1]:
#				if object.blocks and object.door is not None:
#					lots_of_space = False
#		except IndexError:
#			print('')


		if lots_of_space:
			self.activated = True
		else:
			self.activated = False


	def affect_strength_at_attack_choice(self):
		if self.activated:
			self.activated = False			# probably a good safety tip is to always reset activated status
			print("+1 strength from " + str(self.name))
			self.status = 'active'
			return 1
		else:
			return 0


#todo Perfectionist: +1 strength when all your attacks hit

class Perfectionist(PowerUp):


	def __init__(self):
		PowerUp.__init__(self, name = "Perfectionist", tech_description = "+1 strength when all attacks hit", verbose_description = "Power is nothing without control. Additional strength for attacks with 100%% accuracy.", code='Pef', tags = ['aggressive'])

	def update_based_on_player_accuracy(self, all_player_attacks_on_target):
		if all_player_attacks_on_target:
			self.activated = True
		else:
			self.activated = False
		

	# give +1 damage to this attack object
	def affect_strength_of_individual_attack(self, player, attack_object):
		if self.activated == True:
			if attack_object.attack.attacker == player:
				#self.activated = False	 # Not reseting activated, because it has to affect multiple attakcs. Be careful!
				print("+1 strength from " + str(self.name))
				self.status = 'active'
				attack_object.attack.damage += 1

class Leapfrog(PowerUp):
	
	def __init__(self):
		PowerUp.__init__(self, name = "Leapfrog", tech_description = "-1 energy cost for jumping", verbose_description = "Leap through the air with ease!", code='L.F', tags = ['reflexive'])
		self.consumed = False

	def upgrade_player_stats_once(self,player):
		if self.consumed == False:
			print('boh')
			self.status = 'active'
			player.fighter.jump_recharge_time = max(player.fighter.jump_recharge_time - 1, 0) #to a minimum 0? Or should it be 1?
			self.consumed = True


#TODO
# Pick up objects from further away... probably the code for this actually has to be in the main file.
class FarReaching(PowerUp):
	
	def __init__(self):
		#PowerUp.__init__(self, name = "Far Reaching", tech_description = "+1 radius for picking up objects", verbose_description = "Mark hasn't implemented this one yet.", code='F.R')
		PowerUp.__init__(self, name = "Far Reaching", tech_description = "+1 radius for picking up objects", verbose_description = "Experience the joy of picking up nearby objects without having to be literally on top of them.", code='F.R', cost = 2, tags = ['supportive'])

	# most of the work for this one is done in the main game file, ah well.
	def increase_pickup_radius(self):
		self.status = 'active'
		return 1
#


class ScrapingTheBarrel(PowerUp):

	def __init__(self):
		PowerUp.__init__(self, name = "Scraping the Barrel", tech_description = "+1 strength when weapon is on 10 durability or less", verbose_description = "Get extra power from a weapon that's close to breaking.", code='StB', tags = ['aggressive'])

	# Activates if player weapon is on 10 or less durability
	def update_on_player_attack_choice(self, player, objectsArray, map, player_weapon):

		if player_weapon.durability <= 10:
			self.activated = True
		else:
			self.activated = False


	def affect_strength_at_attack_choice(self):
		if self.activated:
			self.activated = False			# probably a good safety tip is to always reset activated status
			print("+1 strength from " + str(self.name))
			self.status = 'active'
			return 1
		else:
			return 0


# TODO: might need to change this if I get round to having variable durability on weapons?
class NewWeaponSmell(PowerUp):

	def __init__(self):
		PowerUp.__init__(self, name = "New Weapon Smell", tech_description = "+1 strength when weapon is on 50 durability or more", verbose_description = "As the wise know, shiny new things are always the best.", code='NWS', tags = ['aggressive'])

	# Activates if player weapon is on 10 or less durability
	def update_on_player_attack_choice(self, player, objectsArray, map, player_weapon):

		if player_weapon.durability >= 50:
			self.activated = True
		else:
			self.activated = False


	def affect_strength_at_attack_choice(self):
		if self.activated:
			self.activated = False			# probably a good safety tip is to always reset activated status
			print("+1 strength from " + str(self.name))
			self.status = 'active'
			return 1
		else:
			return 0

# TODO: might need to change this if I get round to having variable durability on weapons?
class Rejuvenation(PowerUp):

	def __init__(self):
		PowerUp.__init__(self, name = "Rejuvenation", tech_description = "1-off full heal and energy recharge", verbose_description = "I shall heal all your wounds!", code='[+]', tags = ['reflexive'])
		self.consumed = False


	def upgrade_player_stats_once(self,player):
		if self.consumed == False:
			self.status = 'active'
			player.fighter.wounds = 0
			player.fighter.fully_heal()
			self.consumed = True


#Gives the player +1 strength, but only for this level
class InstantaneousStrength(PowerUp):

	def __init__(self):
		PowerUp.__init__(self, name = "Instantaneous Strength", tech_description = "+1 strength for this floor", verbose_description = "For the remainder of this floor, I shall enhance your damage in combat!", code='I.S', cost = 2, tags = ['aggressive'])
		self.activated = True
		self.level_number = None
	# Activates if player weapon is on 10 or less durability
	def update_based_on_level(self, dungeon_level):

		if self.activated:
			if self.level_number is None:
				self.level_number = dungeon_level
				self.tech_description = "+1 strength on floor " + str(self.level_number)
			elif dungeon_level != self.level_number:  #deactivate after leaving the level
				self.activated = False
	

	def affect_strength_at_attack_choice(self):
		if self.activated:
			print("+1 strength from " + str(self.name))
			self.status = 'active'
			return 1
		else:
			return 0


class DareDevil(PowerUp):

	def __init__(self):
		PowerUp.__init__(self, name = "Daredevil", tech_description = "+1 strength when on 1 max health", verbose_description = "A blessing of strength on those one false move from the afterlife", code='D.D', tags = ['aggressive'])

	# Activates if player weapon is on 10 or less durability
	def update_on_player_attack_choice(self, player, objectsArray, map, player_weapon):

		if  player.fighter.max_hp - player.fighter.wounds <= 1:
			self.activated = True
		else:
			self.activated = False


	def affect_strength_at_attack_choice(self):
		if self.activated:
			self.activated = False			# probably a good safety tip is to always reset activated status
			print("+1 strength from " + str(self.name))
			self.status = 'active'
			return 1
		else:
			return 0


# +10 durability to new weapons
class Fortification(PowerUp):
	def __init__(self):
		PowerUp.__init__(self, name = "Fortification", tech_description = "+10 durability to weapons", verbose_description = "Your weapons will last longer", code='Frt', tags = ['supportive'])
		self.first_boost_done = False



	def upgrade_player_weapon_once(self,player, weapon):
		if self.first_boost_done == False:
			weapon.durability += 10
			self.status = 'active'
			self.first_boost_done = True

	def affect_weapon_on_creation(self, player, weapon):
		weapon.durability += 10
		self.status = 'active'

def Get_Random_Upgrade():
	# create list of possible upgrades
	upgrade_list = []
	upgrade_list.append(WallHugger())
	upgrade_list.append(Mindfulness())
	upgrade_list.append(NeptunesBlessing())
	upgrade_list.append(Amphibious())
	upgrade_list.append(PersonalSpace())
	upgrade_list.append(Perfectionist())
	upgrade_list.append(Leapfrog())
	upgrade_list.append(FarReaching())
	upgrade_list.append(ScrapingTheBarrel())
	upgrade_list.append(NewWeaponSmell())
	upgrade_list.append(Rejuvenation())
	upgrade_list.append(InstantaneousStrength())
	upgrade_list.append(DareDevil())
	upgrade_list.append(Fortification())


	# split into three lists - aggressive, reflexive, supportive
	aggressive_list = []
	reflexive_list = []
	supportive_list = []
	for upgrade in upgrade_list:
		if 'aggressive' in upgrade.tags:
			aggressive_list.append(upgrade)
		if 'reflexive' in upgrade.tags:
			reflexive_list.append(upgrade)
		if 'supportive' in upgrade.tags:
			supportive_list.append(upgrade)

	# roll a D3 to decide what category of thing to return - this hopefully leads to a more balanced variety of upgrades?
	upgrade_shortlist = []
	type_choice = randint(0,2)
	if type_choice == 0:
		upgrade_shortlist = aggressive_list
	elif type_choice == 1:
		upgrade_shortlist = reflexive_list
	if type_choice == 2:
		upgrade_shortlist = supportive_list
	



	# return a random upgrade from list
	choice = randint( 0, len(upgrade_shortlist)-1)
	return upgrade_shortlist[choice]
	#return upgrade_list[len(upgrade_list)-1]		#temp just return the sweet new thing
	#return PersonalSpace()					#return this particular thing, for testing purposes

# return a particular upgrade, for testing purposes
def Get_Test_Upgrade():

	#return WallHugger()		#working!
#	return Mindfulness()		# working!
	#return NeptunesBlessing()	# working!
#	return Amphibious()		# working!
#	return PersonalSpace()		#BROKEN
#	return Perfectionist()		# NOT IMPLEMENTED
#	return Leapfrog()		#working but doesn't report back!
#	return FarReaching()		#working!
#	return ScrapingTheBarrel()	#working! and I finally reinstated durability decreasing by 2 on a clash
#	return NewWeaponSmell()		# working!
#	return Rejuvenation()		# Uncertain! (but should  presumably work since it has similar timing to fortification)
#	return InstantaneousStrength()	# workss!
#	return DareDevil()		# works!
#	return Fortification()		# works!


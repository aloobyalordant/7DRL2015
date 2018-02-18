import tdl as libtcod
#import libtcodpy as libtcod
import random
from random import randint

MAP_WIDTH = 80
MAP_HEIGHT = 30

ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 10
MAX_ROOM_MONSTERS = 5
MAX_MONSTERS = 30		# maxmum monsters per level? who knows

DEFAULT_ENEMY_SPAWN_RATE = 200	#this is how often enemies spawn. lower number = more enemies!

# The thing that tells you what the levels should look like and what kinds of enemies there are.
# We'll just be giving you the names of enemies, what those enemies look like is covered elsewhere.

class Level_Settings:

	def __init__(self):
		self.bigArray = []
		
		# Level 0 is just strawmen! stationary strawmen, flailing strawmen, strawmen on wheels!
		# and, suddenly for some reason, ninjas
		enemy_probs = []
		#enemy_probs.append(('strawman', 50))
		enemy_probs.append(('swordsman', 50))
		# enemy_probs.append(('flailing strawman', 25))
		#enemy_probs.append(('stupid swordsman', 25))
		enemy_probs.append(('rook', 25))
		#enemy_probs.append(('strawman on wheels', 1))
		lev0 = Level_Setting(
			max_map_width = 60,
			max_map_height = 30,
			max_rooms = 5,
			level_type = 'classic',
			max_room_monsters = 3,
			enemy_spawn_rate = DEFAULT_ENEMY_SPAWN_RATE/2,
			enemy_probabilities = enemy_probs,
			#keys_required = len(self.bigArray),
			keys_required = 3,		# special for the tutorial
			initial_alarm_level = 0
			)

		self.bigArray.append(lev0)



#		# Level Samurai has all samurai, all the time.
#		enemy_probs = []
#		enemy_probs.append(('samurai', 50))
#		levsamurai = Level_Setting(
#			level_type = 'modern',
#			max_room_monsters = 1,
#			enemy_probabilities = enemy_probs,
#			enemy_spawn_rate = 20)
#		
#		self.bigArray.append(levsamurai)

		
	#	enemy_probs = []
	#	levtest = Level_Setting(
	#		max_map_width = 60,
	#		max_map_height = 30,
	#		max_rooms = 3,
	#		level_type = 'classic',
	#		max_room_monsters = 0,
	#		enemy_probabilities = enemy_probs)
#
	#	for i in range (0, 10):
	#		self.bigArray.append(levtest)


		# randomly decide that out of Bomen, Rooks and Rogues, one of them will appear in level 1, and the other 2 will appear in level 2
		#num =  randint( 0, 1)
		#if num == 0:
		##	enemyprobs1 = [('swordsman', 50), ('rogue', 30)]
		##	enemyprobs2 =  [('swordsman', 50), ('boman', 50), ('rook', 50)]
		##elif num == 0:
		#	enemyprobs1 = [('swordsman', 50), ('boman', 50)]
		#	enemyprobs2 =  [('swordsman', 50),  ('rook', 50),  ('rogue', 30)]
		#else:
		#	enemyprobs1 = [('swordsman', 50), ('rook', 50)]
		#	enemyprobs2 =  [('swordsman', 50),  ('rogue', 30), ('boman', 50)]

		# temp changing the random bit because i want to test rooks
		#enemyprobs1 = [('swordsman', 50), ('rook', 50)]
		#enemyprobs2 =  [('swordsman', 50), ('boman', 50), ('rook', 50), ('rogue', 30)]

	#	enemyprobs1 = [('albatross', 10), ('bustard', 10), ('crane', 10), ('dove', 10), ('eagle', 10), ('falcon', 10)]
	#	enemyprobs2 =  [('swordsman', 50), ('boman', 50), ('rook', 50), ('rogue', 30)]



		# Let's try having a set of the new 'basic' enemies, and then select three of them at random for each level
		enemies_probs_set = [ ('bustard', 10), ('crane', 10), ('dove', 10), ('eagle', 10), ('falcon', 10)]
		enemyprobs1 = []
		for i in range (0,2):
			j = randint( 0, len(enemies_probs_set)-1)
			enemy_choice = enemies_probs_set[j]
			enemyprobs1.append(enemy_choice)
			enemies_probs_set.remove(enemy_choice)
		enemyprobs1.append(('albatross', 10))
		enemyprobs1.append(('eagle', 10))
		enemies_probs_set = [('bustard', 10), ('crane', 10), ('dove', 10), ('eagle', 10), ('falcon', 10)]
		enemyprobs2 = []
		for i in range (0,2):
			j = randint( 0, len(enemies_probs_set)-1)
			enemy_choice = enemies_probs_set[j]
			enemyprobs2.append(enemy_choice)
			enemies_probs_set.remove(enemy_choice)
		enemyprobs2.append(('albatross', 10))
		enemyprobs1.append(('eagle', 10))


		# A level with small rooms and few enemies
		#enemy_probs = []
		#enemy_probs.append(('swordsman', 50))	
		#enemy_probs.append(('rogue', 50))
		enemy_probs = enemyprobs1
		levsr = Level_Setting(
			max_rooms = 12,
			room_max_size = 7,
			room_min_size = 4,	
			max_map_height = 20,
			max_map_width = 40,
			max_room_monsters = 1,
			level_type = 'classic',
			enemy_probabilities = enemy_probs,
			number_sec_drones = len(self.bigArray),
			keys_required = len(self.bigArray),
			initial_alarm_level = 0
			)
		self.bigArray.append(levsr)
		
		# Level 2 has swordsmen, which are your basic mooks? And bomen.
		#enemy_probs = []
		#enemy_probs.append(('swordsman', 50))
		#enemy_probs.append(('boman', 50))
		#enemy_probs.append(('rook', 50))
		enemy_probs = enemyprobs2	
		enemy_probs.append(('ninja', 5))
		lev1 = Level_Setting(
			max_rooms = 8,
			room_max_size = 12,	#20,
			room_min_size = 4,	#15,
			max_room_monsters = 1,
			level_type = 'modern',
			enemy_probabilities = enemy_probs,
			number_sec_drones = len(self.bigArray),
			keys_required = len(self.bigArray),
			initial_alarm_level = len(self.bigArray)
			)
		
		self.bigArray.append(lev1)


#		# Levelsurprisesamura has swordsmen, which are your basic mooks? And bomen.
#		enemy_probs = []
#		enemy_probs.append(('samurai', 20))
#		enemy_probs.append(('swordsman', 50))
#	#	enemy_probs.append(('rook', 50))
#	#	enemy_probs.append(('flailing strawman', 50))
#	#	enemy_probs.append(('ninja', 5))
#		surprisesamurai = Level_Setting(
#			max_rooms = 8,
#			room_max_size = 12,
#			room_min_size = 4,
#			max_room_monsters = 1,
#			enemy_spawn_rate = 140,
#			level_type = 'modern',
#			enemy_probabilities = enemy_probs)
#		
#		self.bigArray.append(surprisesamurai)




		# Level 3 has swordsmen,  bomen, and axe maniacs.
		enemy_probs = []
		enemy_probs.append(('swordsman', 50))
		enemy_probs.append(('boman', 50))
		enemy_probs.append(('axe maniac', 30))
		enemy_probs.append(('ninja', 5))
		lev3 = Level_Setting(
			level_type = 'modern',
			max_room_monsters = 1,
			enemy_probabilities = enemy_probs,
			#enemy_spawn_rate = 20
			number_sec_drones = len(self.bigArray),
			keys_required = len(self.bigArray),
			initial_alarm_level = len(self.bigArray),
			color_scheme = 'coldTest',
			effects = ['cold']	
			)
		
		self.bigArray.append(lev3)



#		# CURRENTLY COMMENTED OUT BECAUSE WIERD LEVEL NAVIGATION BUG
#		# Level arena has swordsmen,  bomen, and (occasionally) axe maniacs. And a scary samurai as the boss! In a big arena level because why not
#		enemy_probs = []
#		enemy_probs.append(('swordsman', 50))
#		enemy_probs.append(('rook', 30))
#		enemy_probs.append(('boman', 30))
#		enemy_probs.append(('axe maniac', 1))
#		enemy_probs.append(('ninja', 4))
#	#	enemy_probs.append(('samurai', 1))
#		levarena = Level_Setting(
#			level_type = 'arena',
#			max_map_width = 60,
#			max_map_height = 30,
#			max_room_monsters = 1,
#			boss = 'hammer sister',
#			boss = 'samurai',
#			enemy_probabilities = enemy_probs,
#			#enemy_spawn_rate = 20
#			number_sec_drones = len(self.bigArray),
#			keys_required = len(self.bigArray),
#			initial_alarm_level = len(self.bigArray)
#			)
#		
#		self.bigArray.append(levarena)


		# Level 4 seems to have  it all.  # except now we replaced swrodsmen with Tridentors
		enemy_probs = []
		# enemy_probs.append(('swordsman', 30))
		enemy_probs.append(('tridentor', 30))
		enemy_probs.append(('boman', 10))
		enemy_probs.append(('axe maniac', 10))
		enemy_probs.append(('ninja', 10))
		enemy_probs.append(('rook', 10))
		enemy_probs.append(('nunchuck fanatic', 10))
		lev4 = Level_Setting(
			level_type = 'modern',
			room_max_size = 20,
			room_min_size = 10,
			max_rooms = 8,
			max_room_monsters = 5,
			enemy_probabilities = enemy_probs,
			number_sec_drones = len(self.bigArray),
			keys_required = len(self.bigArray),
			initial_alarm_level = len(self.bigArray)
			)
		
		self.bigArray.append(lev4)



		# Last level has the wizard! And some other dudes for flavour, I guess.
		enemy_probs = []
		enemy_probs.append(('swordsman', 10))
		enemy_probs.append(('ninja', 10))
		last_lev = Level_Setting(
			room_max_size = 20,
			room_min_size = 15,
			max_rooms = 10,
			max_room_monsters = 10,
			boss = 'wizard',
			final_level = True,
			enemy_probabilities = enemy_probs)
		
		self.bigArray.append(last_lev)


		self.bigArray.append(lev3)



		# randomly add some effects to levels! Todo: maybe make effects more likely to carry between levels.
		i = 2
		while i < len(self.bigArray):
#		for i in range (0, len(self.bigArray)-1):
			temp_lev_set = self.bigArray[i]
			# 1 in 4 chance of being wterlogged, for level 2 onwards
			testnum =  randint( 0, 3)
			print('doing ' + str(testnum))
			if testnum == 0:
				effects_copy = list(self.bigArray[i].effects)
				effects_copy.append('waterlogged')
				self.bigArray[i].effects = effects_copy
				print ('adding water' + str(self.bigArray[i].enemy_probabilities))
			else:
				print ('not watering' + str(self.bigArray[i].enemy_probabilities))
			print(str(self.bigArray[i].effects))



			# 1 in 5 chance of having large rooms, another 1 in of having small rooms for level 2 onwards
			testnum =  randint( 0, 4)
			print('doing ' + str(testnum))
			if testnum == 0:
				effects_copy = list(self.bigArray[i].effects)
				effects_copy.append('large rooms')
				self.bigArray[i].effects = effects_copy
			elif testnum == 1:
				effects_copy = list(self.bigArray[i].effects)
				effects_copy.append('small rooms')
				self.bigArray[i].effects = effects_copy




			i += 1

#		for j in range (0, 5):
#			print('hi' + str(j) + str(self.bigArray[j].effects))
#
#		temp_lev = self.get_setting(2)
#		other_lev = self.get_setting(3)
#		print('ha' + str(temp_lev.effects) + " vs " +  str(other_lev.effects))
#		temp_lev.effects = ['waterlogged']
#		print('ha' + str(temp_lev.effects) + " vs " +  str(other_lev.effects))
#
#
#		for j in range (0, 5):
#			print('ho' + str(j) + str(self.bigArray[j].effects))


		#alter level settings based on effects, maybe?
		for lev_set in self.bigArray:
			if 'waterlogged' in lev_set.effects:
				# take out swordsmen and add tridentors if level is waterlogged
				swordsman_found = False
				for (name, prob) in lev_set.enemy_probabilities:
					if name == 'swordsman':
						swordsman_found = True
						lev_set.enemy_probabilities.remove((name,prob))
						lev_set.enemy_probabilities.append(('tridentor', prob))
				if not swordsman_found:
					 # if we didn't find any swordsmen to replace, add a few tridentors anyway
					lev_set.enemy_probabilities.append(('tridentor', 30))

			if 'large rooms' in lev_set.effects:
				lev_set.room_max_size = 20
				lev_set.room_min_size = 15
			elif 'small rooms' in lev_set.effects:
				lev_set.room_max_size = 7
				lev_set.room_min_size = 4

	def get_setting(self, level_num):
		return self.bigArray[level_num]			
		



class Level_Setting:

	def __init__(self, max_map_width = MAP_WIDTH, max_map_height = MAP_HEIGHT, max_rooms = MAX_ROOMS, room_max_size = ROOM_MAX_SIZE, room_min_size = ROOM_MIN_SIZE, max_room_monsters = MAX_ROOM_MONSTERS,  enemy_probabilities = None, enemy_spawn_rate = DEFAULT_ENEMY_SPAWN_RATE, boss=None, final_level = False, level_type = 'classic', max_monsters = MAX_MONSTERS, number_sec_drones = 1, keys_required = 0, initial_alarm_level = 1, color_scheme = 'lobbyTest', effects = []):
		self.max_map_width = max_map_width
		self.max_map_height = max_map_height
		self.room_max_size = room_max_size
		self.room_min_size = room_min_size
		self.max_rooms = max_rooms
		self.max_room_monsters = max_room_monsters
		if enemy_probabilities is not None:
			self.enemy_probabilities = enemy_probabilities
		else:
			 self.enemy_probabilities = []
		self.enemy_spawn_rate = enemy_spawn_rate
		self.boss = boss
		self.final_level = final_level
		self.level_type = level_type
		self.max_monsters = max_monsters

		total_prob = 0
		for (name, prob) in enemy_probabilities:
			total_prob += prob
		self.total_enemy_prob = total_prob
		self.number_sec_drones = number_sec_drones
		self.keys_required = keys_required
		self.initial_alarm_level = initial_alarm_level
		self.color_scheme = color_scheme
		self.effects = effects
	
		

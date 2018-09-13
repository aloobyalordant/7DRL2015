import tdl as libtcod
#import libtcodpy as libtcod
import random
from random import randint

MAP_WIDTH = 60
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
		enemy_probs.append(('greenhorn', 50))
		# enemy_probs.append(('flailing strawman', 25))
		#enemy_probs.append(('stupid swordsman', 25))
		enemy_probs.append(('bustard', 25))
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
			security_timer = 8,		# special for the tutorial
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
		#enemies_probs_set = [ ('bustard', 10), ('crane', 10), ('dove', 10),  ('falcon', 10)]
#		enemyprobs1 = []
#		#for i in range (0,2):
#		#	j = randint( 0, len(enemies_probs_set)-1)
#		#	enemy_choice = enemies_probs_set[j]
#		#	enemyprobs1.append(enemy_choice)
#		#	enemies_probs_set.remove(enemy_choice)
#		#enemyprobs1.append(('albatross', 10))
#		enemyprobs1.append(('greenhorn', 10))
#		enemyprobs1.append(('crane', 10))
#		#enemyprobs1.append(('bustard', 10))
#		#enemyprobs1.append(('eagle', 10))
#		enemies_probs_set = [('crane', 5),  ('dove', 10),  ('falcon', 10), ('bustard', 10)]
#		third_enemy_choice = randint( 0, len(enemies_probs_set)-1)
#		third_enemy = enemies_probs_set[third_enemy_choice]
#		enemyprobs2 = []
#		#enemyprobs2.append(('albatross', 10))
#		enemyprobs1.append(('greenhorn', 10))
#		#enemyprobs2.append(('bustard', 10))
#		enemyprobs2.append(third_enemy)
#
#		enemies_probs_set.remove(third_enemy)
#		enemies_probs_set.append(('eagle', 5))
#
#		enemyprobs3 = []
#		#enemyprobs3.append(('albatross', 10))
#		enemyprobs1.append(('greenhorn', 10))
#		if randint(0,3) == 0:
#			enemyprobs3.append(('bustard', 10))
#		else:
#			enemyprobs3.append(third_enemy)
#
#		fourth_enemy_choice = randint( 0, len(enemies_probs_set)-1)
#		fourth_enemy = enemies_probs_set[fourth_enemy_choice]
#		enemyprobs3.append(fourth_enemy)

		



		# Ok so. Let's try and clean up that enemy probabilities 
		
		# Initially: It could be a greenhorn and crane, it could be a greenhorn and a bustard!
		enemyprobs1 = []
		enemybench = []		# enemies not currently being used, but that we might soon
	#	if randint(0,1) == 0:	TEMP COMMENTED OUT RANDOMIZATION TO MAKE TESTING EASIER
		if 0 == 0:
			#enemyprobs1 = [('greenhorn', 20), ('crane',10), ('gunslinger',10)]   #[('bustard', 10), ('crane', 10), ('dove', 10),  ('falcon', 10)]
			enemyprobs1 = [('greenhorn-cautious', 20), ('crane',10), ('hammerer',10)] 
			enemybench = [('bustard',10), ('dove', 10),  ('falcon', 10)]
		else:
			enemyprobs1 = [('greenhorn', 20), ('bustard',10)] 
			enemybench = [('crane', 10), ('dove', 10),  ('falcon', 10)]

		# For level 2: Take one enemy out (probably not the greenhorn?), and add one new one from the bench
		# Actually... let's not do that. let's keep all the enemies from level &, and just add one more
		enemyprobs2 = list(enemyprobs1)
		#if randint(0,2) == 0:
		#	enemy_to_drop = enemyprobs2[0]
		#else:
		#	enemy_to_drop = enemyprobs2[0]
		enemy_to_add = enemybench[randint(0, len(enemybench) - 1)]
		#enemyprobs2.remove(enemy_to_drop)
		enemyprobs2.append(enemy_to_add)
		enemybench.remove(enemy_to_add)

		

		# Now add the eagle to the bench! And drop a random enemy, and add a new one from the bench
		enemybench.append(('eagle',5))
		enemyprobs3 = list(enemyprobs2)
		enemy_to_drop = enemyprobs3[randint(0, len(enemyprobs3) - 1)]
		enemy_to_add = enemybench[randint(0, len(enemybench) - 1)]
		enemyprobs3.remove(enemy_to_drop)
		enemyprobs3.append(enemy_to_add)
		enemybench.remove(enemy_to_add)




		#for i in range (0,2):
		#	j = randint( 0, len(enemies_probs_set)-1)
		#	enemy_choice = enemies_probs_set[j]
		#	enemyprobs2.append(enemy_choice)
		#	enemies_probs_set.remove(enemy_choice)
		#enemyprobs2.append(('albatross', 10))
		#enemyprobs1.append(('eagle', 10))


		# A level with small rooms and few enemies
		#enemy_probs = []
		#enemy_probs.append(('swordsman', 50))	
		#enemy_probs.append(('rogue', 50))

		
		enemy_probs = enemyprobs1
		levsr = Level_Setting(
			max_rooms = 12,
			room_max_size = 12,
			room_min_size = 5,	
			max_map_height = 25,
			max_map_width = 50,
			min_room_monsters = 0,
			max_room_monsters = 3,
			level_type = 'classic',
			enemy_probabilities = enemy_probs,
			number_sec_drones = randint(1,3) + randint(1,3),	#2d3 drones? let's see #len(self.bigArray),
			keys_required =  2, #len(self.bigArray),
			number_keys = 3,
			number_shrines = 4,
			guard_probability = (1,35),			# 1 in 35 chance of a given space having a guard on
			initial_alarm_level = 0,
			door_probability = (7,8),
			security_timer = 7
			)
		self.bigArray.append(levsr)
		
		# Level 2 has swordsmen, which are your basic mooks? And bomen.
		#enemy_probs = []
		#enemy_probs.append(('swordsman', 50))
		#enemy_probs.append(('boman', 50))
		#enemy_probs.append(('rook', 50))
		temp_keys_req = len(self.bigArray) + 1
		temp_keys_here = 2*temp_keys_req
		temp_number_sec_drones = 3*temp_keys_req
		temp_number_shrines = 5

		enemy_probs = enemyprobs2	
		#enemy_probs.append(('ninja', 5))
		lev1 = Level_Setting(
			max_rooms = 8,
			room_max_size = 12,	#20,
			room_min_size = 4,	#15,
			min_room_monsters = 0,
			max_room_monsters = 4,
			level_type = 'modern',
			enemy_probabilities = enemy_probs,
			number_sec_drones  = temp_number_sec_drones, # len(self.bigArray),
			number_keys = temp_keys_here,
			keys_required = temp_keys_req, #len(self.bigArray),
			number_shrines = temp_number_shrines,
			initial_alarm_level = len(self.bigArray),
			door_probability = (5,8),
			security_timer = 6
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



		# New level 3 
		temp_keys_req = len(self.bigArray) + 1
		temp_keys_here = 2*temp_keys_req
		temp_number_sec_drones = 3*temp_keys_req
		temp_number_shrines = 5

		enemy_probs = enemyprobs3	
		#enemy_probs.append(('ninja', 5))
		lev2 = Level_Setting(
			max_rooms = 8,
			room_max_size = 12,	#20,
			room_min_size = 4,	#15,
			level_type = 'modern',
			enemy_probabilities = enemy_probs,
			number_sec_drones  = temp_number_sec_drones, # len(self.bigArray),
			number_keys = temp_keys_here,
			keys_required = temp_keys_req, #len(self.bigArray),
			number_shrines = temp_number_shrines,
			initial_alarm_level = len(self.bigArray),
			security_timer = 5
			)
		
		self.bigArray.append(lev2)


		# Level 3 has swordsmen,  bomen, and axe maniacs.
		enemy_probs = []
		enemy_probs.append(('swordsman', 50))
		enemy_probs.append(('boman', 50))
		enemy_probs.append(('axe maniac', 30))
		enemy_probs.append(('ninja', 5))
		temp_keys_req = len(self.bigArray) + 1
		temp_keys_here = 2*temp_keys_req
		temp_number_sec_drones = 3*temp_keys_req
		temp_number_shrines = 5
		lev3 = Level_Setting(
			level_type = 'modern',
			enemy_probabilities = enemy_probs,
			#enemy_spawn_rate = 20
			number_sec_drones  = temp_number_sec_drones, # len(self.bigArray),
			number_keys = temp_keys_here,
			keys_required = temp_keys_req, #len(self.bigArray),
			number_shrines = temp_number_shrines,
			initial_alarm_level = len(self.bigArray),
			color_scheme = 'coldTest'#,
			#effects = ['cold']	
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
		enemy_probs.append(('bustard', 10))
		enemy_probs.append(('nunchuck fanatic', 10))
		temp_keys_req = len(self.bigArray) + 1
		temp_keys_here = 2*temp_keys_req
		temp_number_sec_drones = 3*temp_keys_req
		temp_number_shrines = 5
		lev4 = Level_Setting(
			level_type = 'modern',
			room_max_size = 20,
			room_min_size = 10,
			max_rooms = 8,
			enemy_probabilities = enemy_probs,
			number_sec_drones  = temp_number_sec_drones, # len(self.bigArray),
			number_keys = temp_keys_here,
			keys_required = temp_keys_req, #len(self.bigArray),
			number_shrines = temp_number_shrines,
			initial_alarm_level = len(self.bigArray)
			)
		
		self.bigArray.append(lev4)



		# Last level has the wizard! And some other dudes for flavour, I guess.
		enemy_probs = []
		enemy_probs.append(('swordsman', 10))
		enemy_probs.append(('ninja', 10))
		last_lev = Level_Setting(
			level_type = 'modern',
			room_max_size = 20,
			room_min_size = 15,
			max_rooms = 10,
			boss = 'wizard',
			final_level = True,
			number_sec_drones = len(self.bigArray),
			number_keys = 0,
			keys_required = 0, #len(self.bigArray),
			number_shrines = 5,
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
				#lev_set.room_max_size = 20
				#lev_set.room_min_size = 15
				lev_set.room_size_second_dice = (10,10)
			elif 'small rooms' in lev_set.effects:
				#lev_set.room_max_size = 7
				#lev_set.room_min_size = 4
				lev_set.room_size_first_dice = (2,2)

	def get_setting(self, level_num):
		return self.bigArray[level_num]			
		



class Level_Setting:

	def __init__(self, max_map_width = MAP_WIDTH, max_map_height = MAP_HEIGHT, max_rooms = MAX_ROOMS, room_max_size = ROOM_MAX_SIZE, room_min_size = ROOM_MIN_SIZE, max_room_monsters = None,  min_room_monsters = 1, enemy_probabilities = None, enemy_spawn_rate = DEFAULT_ENEMY_SPAWN_RATE, boss=None, final_level = False, level_type = 'classic', max_monsters = MAX_MONSTERS, number_sec_drones = 1, number_keys = 0, keys_required = 0, number_shrines = 1, guard_probability = (1,25), initial_alarm_level = 1, color_scheme = 'lobbyTest', effects = [], door_probability = (1,8), security_timer = 4, room_size_first_dice = (3,7), room_size_second_dice = (3,7), start_ele_direction = None, start_ele_spawn = None):
		self.max_map_width = max_map_width
		self.max_map_height = max_map_height
		self.room_max_size = room_max_size
		self.room_min_size = room_min_size
		self.max_rooms = max_rooms
		self.max_room_monsters = max_room_monsters
		self.min_room_monsters = min_room_monsters
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
		self.number_keys = number_keys
		self.keys_required = keys_required
		self.number_shrines = number_shrines
		self.guard_probability = guard_probability
		self.initial_alarm_level = initial_alarm_level
		self.color_scheme = color_scheme
		self.effects = effects
		self.door_probability = door_probability # prob of (a,b) means individual rooms have an a in b chance of having doors
		self.security_timer = security_timer 	# how long security drones take before  they spot you
		self.room_size_first_dice = room_size_first_dice   # dice (a,b) takes random values between a and b inclusive;
		self.room_size_second_dice = room_size_second_dice # room height or width is determined by rolling two dice and adding together
		self.start_ele_direction = start_ele_direction
		self.start_ele_spawn = start_ele_spawn
		

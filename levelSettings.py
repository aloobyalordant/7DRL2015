import libtcodpy as libtcod

MAP_WIDTH = 80
MAP_HEIGHT = 30

ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 10
MAX_ROOM_MONSTERS = 5
MAX_MONSTERS = 30		# maxmum monsters per level? who knows

DEFAULT_ENEMY_SPAWN_RATE = 20	#this is how often enemies spawn. lower number = more enemies!

# The thing that tells you what the levels should look like and what kinds of enemies there are.
# We'll just be giving you the names of enemies, what those enemies look like is covered elsewhere.

class Level_Settings:

	def __init__(self):
		self.bigArray = []
		
		# Level 0 is just strawmen! stationary strawmen, flailing strawmen, strawmen on wheels!
		# and, suddenly for some reason, ninjas
		enemy_probs = []
		enemy_probs.append(('strawman', 50))
		enemy_probs.append(('flailing strawman', 25))
		enemy_probs.append(('strawman on wheels', 25))
		lev0 = Level_Setting(
			max_map_width = 60,
			max_map_height = 30,
			max_rooms = 5,
			level_type = 'classic',
			max_room_monsters = 3,
			enemy_probabilities = enemy_probs)

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

		# A level with small rooms and few enemies
		enemy_probs = []
		enemy_probs.append(('swordsman', 50))
		enemy_probs.append(('rook', 50))
	#	enemy_probs.append(('nunchuck fanatic', 50))
	#	enemy_probs.append(('ninja', 5))
		levsr = Level_Setting(
			max_rooms = 12,
			room_max_size = 7,
			room_min_size = 4,	
			max_map_height = 20,
			max_map_width = 40,
			max_room_monsters = 1,
			#enemy_spawn_rate = 100,
			level_type = 'classic',
			enemy_probabilities = enemy_probs)
		self.bigArray.append(levsr)
		
		# Level 2 has swordsmen, which are your basic mooks? And bomen.
		enemy_probs = []
		enemy_probs.append(('swordsman', 50))
		enemy_probs.append(('boman', 50))
		enemy_probs.append(('rook', 50))
	#	enemy_probs.append(('flailing strawman', 50))
		enemy_probs.append(('ninja', 5))
		lev1 = Level_Setting(
			max_rooms = 8,
			room_max_size = 20,
			room_min_size = 15,
			max_room_monsters = 1,
			#enemy_spawn_rate = 30,
			level_type = 'modern',
			enemy_probabilities = enemy_probs)
		
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
			enemy_probabilities = enemy_probs
			#enemy_spawn_rate = 20
			)
		
		self.bigArray.append(lev3)




		# Level arena has swordsmen,  bomen, and (occasionally) axe maniacs. And a scary samurai as the boss! In a big arena level because why not
		enemy_probs = []
		enemy_probs.append(('swordsman', 50))
		enemy_probs.append(('rook', 30))
		enemy_probs.append(('boman', 30))
		enemy_probs.append(('axe maniac', 1))
		enemy_probs.append(('ninja', 4))
	#	enemy_probs.append(('samurai', 1))
		levarena = Level_Setting(
			level_type = 'arena',
			max_map_width = 60,
			max_map_height = 30,
			max_room_monsters = 1,
#			boss = 'hammer sister',
			boss = 'samurai',
			enemy_probabilities = enemy_probs
			#enemy_spawn_rate = 20
			)
		
#TODO		self.bigArray.append(levarena)


		# Level 4 seems to have  it all.
		enemy_probs = []
		enemy_probs.append(('swordsman', 30))
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
			enemy_probabilities = enemy_probs)
		
#TODO		self.bigArray.append(lev4)



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

	def get_setting(self, level_num):
		return self.bigArray[level_num]			
		



class Level_Setting:

	def __init__(self, max_map_width = MAP_WIDTH, max_map_height = MAP_HEIGHT, max_rooms = MAX_ROOMS, room_max_size = ROOM_MAX_SIZE, room_min_size = ROOM_MIN_SIZE, max_room_monsters = MAX_ROOM_MONSTERS,  enemy_probabilities = None, enemy_spawn_rate = DEFAULT_ENEMY_SPAWN_RATE, boss=None, final_level = False, level_type = 'classic', max_monsters = MAX_MONSTERS):
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
	
		

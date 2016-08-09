import libtcodpy as libtcod
from objectClass import Object

#Controls
ControlMode = 'Crypsis' 	# 'Wheatley'   'Glados'
if ControlMode == 'Glados':
	ATTCKUPLEFT	 = 'q'
	ATTCKUP		 = 'w'
	ATTCKUPRIGHT	 = 'e'
	ATTCKRIGHT	 = 'd'
	ATTCKDOWNRIGHT	 = 'c'
	ATTCKDOWN	 = 'x'
	ATTCKDOWNLEFT	 = 'z'
	ATTCKLEFT	 = 'a'

	ATTCKDOWNALT	 = 's'
elif ControlMode == 'Crypsis':
	ATTCKUPLEFT	 = 'a'
	ATTCKUP		 = 'z'
	ATTCKUPRIGHT	 = 'e'
	ATTCKRIGHT	 = 'd'
	ATTCKDOWNRIGHT	 = 'c'
	ATTCKDOWN	 = 'x'
	ATTCKDOWNLEFT	 = 'w'
	ATTCKLEFT	 = 'q'

	ATTCKDOWNALT	 = 's'

ELEVATOR_DOOR_CLOSURE_PERIOD = 5

class Object_Datum:

	def __init__(self, x, y, name, info = None, more_info = None):
		self.x = x
		self.y = y
		self.name = name
		self.info = info	# e.g. the name of the god if this is a shrine, etc.
		self.more_info = more_info

class Object_Name:

	def __init__(self, name, info = None, more_info = None):
		self.name = name
		self.info = info	# e.g. the name of the god if this is a shrine, etc.
		self.more_info = more_info


class Level_Data:

	def __init__(self, map, player_start_x, player_start_y,  object_data = [],  nearest_points_array = [[]], center_points = [], spawn_points = [], elevators = []):
		self.map = map
		self.object_data = object_data
		self.player_start_x = player_start_x
		self.player_start_y = player_start_y
		self.nearest_points_array = nearest_points_array
		self.center_points = center_points
		self.spawn_points = spawn_points
		self.elevators = elevators

class Tile:
	#a tile of the map and its properties
	def __init__(self, blocked, block_sight = None):
		self.blocked = blocked

	#by default, if a tile is blocked, it also blocks sight
		if block_sight is None: block_sight = blocked
		self.block_sight = block_sight

		self.explored = False

class Rect:
	#a rectangle on the map. used to characterize a room.
	def __init__(self, x, y, w, h):
		self.x1 = x
		self.y1 = y
		self.x2 = x + w-1
		self.y2 = y + h-1

	def center(self):
		center_x = (self.x1 + self.x2) / 2
		center_y = (self.y1 + self.y2) / 2
		return (center_x, center_y)
 
	def intersect(self, other):
		#returns true if this rectangle intersects with another one
		return (self.x1 <= other.x2 and self.x2 >= other.x1 and
		self.y1 <= other.y2 and self.y2 >= other.y1)


	def touching(self, other):
		#like intersecting, excpt that rectangles with tiles adjacent to each other also count
		return (self.x1 <= other.x2+1 and self.x2+1 >= other.x1 and
		self.y1 <= other.y2+1 and self.y2+1 >= other.y1)

	def contained_in(self, other):
		# is this rectangle contained inside another one?
		return (self.x1 >= other.x1 and self.x2<= other.x2 and self.y1 >= other.y1 and self.y2 <= other.y2)


	def strictly_contained_in(self, other):
		# is this rectangle contained inside another one? And not the same rectangle, it's actually smaller?
		return (self.contained_in(other) and (self.x1 != other.x1 or self.y1 != other.y1 or self.x2 != other.x2 or self.y2 != other.y2))




class Level_Segment:
	def __init__(self, seg_map = [[]], seg_data = []):
		self.seg_map = seg_map
		self.seg_data = seg_data

class Elevator:

	def __init__(self, door_points, spawn_points, player_authorised = False):
		self.door_points = door_points
		self.spawn_points = spawn_points
		self.player_authorised = player_authorised
		self.time_unoccupied = 5
		self.doors_open = False
		self.doors_opening = False
		self.doors_closing = False
		self.ready_to_go_up = False
		self.doors = []
		for (x,y) in self.door_points:
			door = Object(x, y, '+', 'elevator door', libtcod.red, blocks=True, door = Elevator_Door(x,y,horizontal = False), always_visible=True) 
			self.doors.append(door)
			#print "doooooooR"
			#map[od.x][od.y].block_sight = True
			#objects.append(door)

	def update(self, elevator_occupied, player_in_elevator = False, player_near_elevator = False, player_in_doorway = False):
		if elevator_occupied:
			self.time_unoccupied = 0
		else:
			self.time_unoccupied = self.time_unoccupied+1


		if player_in_doorway:
			self.set_doors_open(True)
		else:
			if  self.player_authorised and player_near_elevator:
				self.set_doors_open(True)
			elif self.time_unoccupied >= ELEVATOR_DOOR_CLOSURE_PERIOD:
				self.set_doors_open(False)
			else:
				self.set_doors_open(True)

		if player_in_elevator and self.player_authorised:
			self.set_doors_open(False)
			self.ready_to_go_up = True

		#print "elevatorupdate" + str(self.time_unoccupied)

	def set_player_authorisation(self, player_authorised):
		self.player_authorised = player_authorised

	
	#admin for setting doors open/closed, mainly to do with tracking if doors are in the process of opening or closing
	def set_doors_open(self, set_open):
		self.doors_opening = False
		self.doors_closing = False
		if set_open == True:
			if self.doors_open == False:
				self.doors_opening = True
			self.doors_open = True
		else:
			if self.doors_open == True:
				self.doors_closing = True
			self.doors_open = False

class Elevator_Door:
	def __init__(self, x,y, horizontal):
		self.x=x
		self.y=y
		self.horizontal = horizontal

class Level_Generator:

	def make_level(self, dungeon_level, level_settings):


		lev_set = level_settings
		#lev_set = game_level_settings.get_setting(dungeon_level)

		room_range = lev_set.max_rooms
		map_width = lev_set.max_map_width
		map_height = lev_set.max_map_height
		room_min_size = lev_set.room_min_size
		room_max_size = lev_set.room_max_size
		max_map_height = lev_set.max_map_height
		max_map_width = lev_set.max_map_width
		
		#fill map with "blocked" tiles
		map = [[ Tile(True)
			for y in range(max_map_height) ]
				for x in range(max_map_width) ]
	
		nearest_points_array  = [[ None
			for y in range(max_map_height) ]
				for x in range(max_map_width) ]		
	
		rooms = []
		num_rooms = 0
	
		spawn_points = []
		center_points = []
		object_data = []
		elevators = []
 
	
		if dungeon_level == 0:
			new_room = Rect(10,10,5,5)
			self.create_room(new_room, map, center_points, nearest_points_array)

			(new_x, new_y) = new_room.center()
			#this is the first room, where the player starts at
			player_start_x = new_x
			player_start_y = new_y

			#object_data.append(Object_Datum(new_x,new_y,'stairs'))


			self.create_half_corridor(new_room, 5, 12, map, center_points, nearest_points_array, object_data)


			object_data.append(Object_Datum(19,12,'message', 'Lesson 1. The true warrior can strike enemies from many directions. Up, left, even diagonally.'))
			old_room = new_room
			new_room = Rect(20,10,8,5)
			self.create_room(new_room, map, center_points, nearest_points_array)
			(new_x, new_y) = new_room.center()
			(prev_x, prev_y) = old_room.center()
			self.append_segment(map, self.create_segment('Tut-Attack'), 20, 10, object_data)
			self.create_h_tunnel(prev_x, new_x, prev_y, map, nearest_points_array, center_points, narrow = True)
			#self.create_v_tunnel(new_y, prev_y, new_x, map, nearest_points_array, center_points, narrow = True)



			object_data.append(Object_Datum(32,12,'message', 'Lesson 2. The secret of all combat is this: Hit your enemy without your enemy hitting you!'))
			old_room = new_room
			new_room = Rect(33,10,7,5)
			self.create_room(new_room, map, center_points, nearest_points_array)
			(new_x, new_y) = new_room.center()
			(prev_x, prev_y) = old_room.center()
			self.append_segment(map, self.create_segment('Tut-Avoid-Attacks'), 33, 10, object_data)
			self.create_h_tunnel(prev_x, new_x, prev_y, map, nearest_points_array, center_points, narrow = True)
			#self.create_v_tunnel(new_y, prev_y, new_x, map, nearest_points_array, center_points)



			object_data.append(Object_Datum(49,12,'message', 'Lesson 3. Do not strike at where your enemy is! Strike at where your enemy is going to be!'))
			old_room = new_room
			new_room = Rect(50,10,7,5)
			self.create_room(new_room, map, center_points, nearest_points_array)
			(new_x, new_y) = new_room.center()
			(prev_x, prev_y) = old_room.center()
			self.append_segment(map, self.create_segment('Tut-Moving-Enemies'), 50, 10, object_data)
			self.create_h_tunnel(prev_x, new_x, prev_y, map, nearest_points_array, center_points, narrow = True)


			self.create_half_corridor(new_room, 53, 5, map, center_points, nearest_points_array, object_data)


			object_data.append(Object_Datum(53,19,'message', 'Lesson 4. A warrior is not their weapon. A warrior knows when it is time to trade their weapon for another.'))
			old_room = new_room
			new_room = Rect(50,20,7,5)
			self.create_room(new_room, map, center_points, nearest_points_array)
			(new_x, new_y) = new_room.center()
			(prev_x, prev_y) = old_room.center()
			object_data.append(Object_Datum(new_x, new_y,'weapon', 'sai'))
			#self.append_segment(map, self.create_segment('Tut-Moving-Enemies'), 50, 10, object_data)
			#self.create_h_tunnel(prev_x, new_x, prev_y, map, nearest_points_array, center_points, narrow = True)
			self.create_v_tunnel(new_y, prev_y, new_x, map, nearest_points_array, center_points, narrow = True)


			self.create_half_corridor(new_room, 53, 27, map, center_points, nearest_points_array, object_data)


			self.create_half_corridor(new_room, 58, 20, map, center_points, nearest_points_array, object_data)

			object_data.append(Object_Datum(41,22,'message', 'Lesson 6. Be not afraid to run into the place your enemy has just struck.'))
			old_room = new_room
			new_room = Rect(33,20,7,5)
			self.create_room(new_room, map, center_points, nearest_points_array)
			(new_x, new_y) = new_room.center()
			(prev_x, prev_y) = old_room.center()
			self.append_segment(map, self.create_segment('Tut-Gauntlet'), 33, 20, object_data)
			self.create_h_tunnel(prev_x, new_x, prev_y, map, nearest_points_array, center_points, narrow = True)
			#self.create_v_tunnel(new_y, prev_y, new_x, map, nearest_points_array, center_points)

			object_data.append(Object_Datum(26,22,'message', 'In this next room lies a foe. If you can defeat them, your training will be complete.'))
			old_room = new_room
			new_room = Rect(15,18,12,5)
			self.create_room(new_room, map, center_points, nearest_points_array)
			(new_x, new_y) = new_room.center()
			(prev_x, prev_y) = old_room.center()
			self.append_segment(map, self.create_segment('Tut-Test'), 15, 18, object_data)
			self.create_h_tunnel(prev_x, new_x, prev_y, map, nearest_points_array, center_points, narrow = True)

		#	old_room = new_room
		#	new_room = Rect(20,20,7,5)
		#	self.create_room(new_room, map, center_points, nearest_points_array)
		#	(new_x, new_y) = new_room.center()
		#	(prev_x, prev_y) = old_room.center()
		#	#self.append_segment(map, self.create_segment('Tut-Gauntlet'), 33, 10, object_data)
		#	self.create_h_tunnel(prev_x, new_x, prev_y, map, nearest_points_array, center_points, narrow = True)
		#	#self.create_v_tunnel(new_y, prev_y, new_x, map, nearest_points_array, center_points)


			#object_data.append(Object_Datum(new_x,new_y,'stairs'))

			#finally... add some elevators??
			#print 'adding elevators...'
			elev1 = Rect(5, 10, 5, 4)
			elev2 = Rect(10, 20, 5, 4)
			rooms.append(elev1)
			rooms.append(elev2)

			self.create_elevator(elev1, map, spawn_points, center_points, nearest_points_array, object_data,  elevators, 'Small-Elevator-Right')	
			self.create_elevator(elev2, map, spawn_points, center_points, nearest_points_array, object_data,  elevators, 'Small-Elevator-Right')

		elif lev_set.level_type == 'arena':


			room_min_size = lev_set.room_min_size
			room_max_size = lev_set.room_max_size		
			max_map_height = lev_set.max_map_height
			max_map_width = lev_set.max_map_width

			#let's.... *start* by making some elevators
			#print 'adding elevators...'
			elev1 = Rect(1, 7, 5, 4)
			elev2 = Rect(max_map_width-6, 7, 5, 4)
			elev3 = Rect(max_map_width-6, max_map_height -11, 5, 4)
			elev4 = Rect(1, max_map_height - 11, 5, 4)
			rooms.append(elev1)
			rooms.append(elev2)
			rooms.append(elev3)
			rooms.append(elev4)
			self.create_elevator(elev1, map, spawn_points, center_points, nearest_points_array, object_data,  elevators, 'Small-Elevator-Right')
			self.create_elevator(elev2, map, spawn_points, center_points, nearest_points_array, object_data,  elevators, 'Small-Elevator-Left')
			self.create_elevator(elev3, map, spawn_points, center_points, nearest_points_array, object_data,  elevators, 'Small-Elevator-Left')
			self.create_elevator(elev4, map, spawn_points, center_points, nearest_points_array, object_data,  elevators, 'Small-Elevator-Right')
	
			for r in range((max_map_width-11-7-1)/8):
				elevtop = Rect((8*r)+9,1,4,5)
				rooms.append(elevtop)
				self.create_elevator(elevtop, map, spawn_points, center_points, nearest_points_array, object_data,  elevators, 'Small-Elevator-Down')
				elevbot = Rect((8*r)+9, max_map_height -6,4,5)
				rooms.append(elevbot)
				self.create_elevator(elevbot, map, spawn_points, center_points, nearest_points_array, object_data,  elevators, 'Small-Elevator-Up')

			


			# now... make the limits of our other rooms be such that there come close to but don't overlap the elevators..
			horiz_lower_bound = 6
			horiz_upper_bound = max_map_width-5
			vert_lower_bound = 6
			vert_upper_bound = max_map_height-5


			new_room = Rect(horiz_lower_bound, vert_lower_bound, horiz_upper_bound - horiz_lower_bound, vert_upper_bound- vert_lower_bound)
			self.create_room(new_room, map, center_points, nearest_points_array)
			rooms.append(new_room)
			self.place_objects(new_room, lev_set, map, object_data, dungeon_level)	
	
			#place some random blocks around
			for i in range((horiz_upper_bound - horiz_lower_bound)*(vert_upper_bound- vert_lower_bound)/30):
			#for i in range(50):
				#choose random spot to place a block
				x = libtcod.random_get_int(0, new_room.x1+1, new_room.x2-1)
				y = libtcod.random_get_int(0, new_room.y1+1, new_room.y2-1)
		
				#only place it if the tile is not already blocked
				if not self.is_occupied(x, y, map, object_data):				
					map[x][y].blocked = True
					map[x][y].block_sight = True
	
	

			choice = libtcod.random_get_int(0, 0, len(spawn_points)-1)
			(player_start_x, player_start_y) = spawn_points[choice] 	#rooms[len(rooms)-1].center()
			(new_x, new_y) = rooms[len(rooms)-1].center()
			#object_data.append(Object_Datum(new_x,new_y, 'stairs'))
			object_data.append(Object_Datum(new_x,new_y, 'security system'))


			if lev_set.boss is not None:
				#boss_monster = create_monster(new_x,new_y,lev_set.boss)
				#objects.append(boss_monster)
				object_data.append(Object_Datum(new_x,new_y, 'boss', lev_set.boss))		


#		elif dungeon_level >= 1 and dungeon_level <= 10:
		#elif 1 == 0:		#temporarily cutting this out... let's see what happens		
		
		#THIS BIT IS WHERE MOST LEVELS GET THEIR DATA FROM
		# GOODNESS KNOWS WHAT THE OTHER CASES ARE FOR
		elif lev_set.level_type == 'modern' or lev_set.level_type == 'classic':

			self.fill_a_rectangle(map, lev_set, dungeon_level, object_data, rooms, nearest_points_array, center_points, spawn_points, elevators)

#			new_room = Rect(20,20,5,5)
#			self.create_room(new_room, map, center_points, nearest_points_array)
#			rooms.append(new_room)
#			self.place_objects(new_room, lev_set, map, object_data, dungeon_level)
#			self.recursively_generate(map, lev_set, dungeon_level, object_data, rooms, room_range, new_room, nearest_points_array, center_points)

			#bit of a hack for now - the player can spawn anywhere enemies can spawn...
			choice = libtcod.random_get_int(0, 0, len(spawn_points)-1)
			(player_start_x, player_start_y) = spawn_points[choice] 	#rooms[len(rooms)-1].center()
			(new_x, new_y) = rooms[4].center()

			#if lev_set.final_level is not True:
			#	object_data.append(Object_Datum(new_x,new_y, 'security system'))


			if lev_set.boss is not None:
				#boss_monster = create_monster(new_x,new_y,lev_set.boss)
				#objects.append(boss_monster)
				object_data.append(Object_Datum(new_x,new_y, 'boss', lev_set.boss))

			self.add_security_systems(map, lev_set, dungeon_level, object_data, rooms, elevators, lev_set.number_sec_systems)
	


		#elif lev_set.level_type == 'modern':
		#elif lev_set.level_type == 'classic':
		elif 1 == 0:
			# okay, maybe let's get some larger rooms going that can overlap?
	
			# so for now, this is the code for classic mode, with the code for checking room overlaps removed
			for r in range(room_range):
				#random width and height
				w = libtcod.random_get_int(0, room_min_size, room_max_size)
				h = libtcod.random_get_int(0, room_min_size, room_max_size)
				#random position without going out of the boundaries of the map
				x = libtcod.random_get_int(0, 0, map_width - w - 1)
				y = libtcod.random_get_int(0, 0, map_height - h - 1)
		
				#"Rect" class makes rectangles easier to work with
				new_room = Rect(x, y, w, h)
		 
	
		
				if True:
					#this means there are no intersections, so this room is valid
		
					#"paint" it to the map's tiles
					self.create_room(new_room, map, center_points, nearest_points_array)
					#add some contents to this room, such as monsters
					self.place_objects(new_room, lev_set, map, object_data, dungeon_level)
		
					#center coordinates of new room, will be useful later
					(new_x, new_y) = new_room.center()
					if num_rooms == 0:
						#this is the first room, where the player starts at
						player_start_x = new_x
						player_start_y = new_y
					else:
						#all rooms after the first:
						#connect it to the previous room with a tunnel
		
						#center coordinates of previous room
						(prev_x, prev_y) = rooms[num_rooms-1].center()
		
						#draw a coin (random number that is either 0 or 1)
						if libtcod.random_get_int(0, 0, 1) == 1:
							#first move horizontally, then vertically
							self.create_h_tunnel(prev_x, new_x, prev_y, map, nearest_points_array, center_points)
							self.create_v_tunnel(new_y, prev_y, new_x, map, nearest_points_array, center_points)
						else:
							#first move vertically, then horizontally
							self.create_v_tunnel(prev_y, new_y, prev_x, map, nearest_points_array, center_points)
							self.create_h_tunnel(new_x, prev_x, new_y, map, nearest_points_array, center_points)
		
					#finally, append the new room to the list
					rooms.append(new_room)
					num_rooms += 1
	
			#create_segment()

			
			#create stairs at the center of the last room
			#stairs = Object(new_x, new_y, '<', 'stairs', libtcod.white, always_visible=True)
			#objects.append(stairs)
			#stairs.send_to_back()  #so it's drawn below the monsters
			
			#object_data.append(Object_Datum(new_x,new_y,'stairs'))
			if lev_set.final_level is not True:
				object_data.append(Object_Datum(new_x,new_y, 'security system'))

		
			if lev_set.boss is not None:
				#boss_monster = create_monster(new_x,new_y,lev_set.boss)
				#objects.append(boss_monster)
				object_data.append(Object_Datum(new_x,new_y, 'boss', lev_set.boss))
	
	
			# now, append some elevators?
			num_norm_rooms = num_rooms
			elev1 = Rect(5, 5, 4, 4)
			elev2 = Rect(max_map_width-5, 5, 4, 4)
			elev3 = Rect(max_map_width-5, max_map_height -5, 4, 4)
			elev4 = Rect(5, max_map_height - 5, 4, 4)
			self.create_elevator(elev1, map, spawn_points, center_points, nearest_points_array, elevators, object_data)
			self.create_elevator(elev2, map, spawn_points, center_points, nearest_points_array, elevators, object_data)
			self.create_elevator(elev3, map, spawn_points, center_points, nearest_points_array, elevators, object_data)
			self.create_elevator(elev4, map, spawn_points, center_points, nearest_points_array, elevators, object_data)
			(new_x, new_y) = elev1.center()
			num = libtcod.random_get_int(0, 0, num_norm_rooms-1)
			(prev_x, prev_y) = rooms[num].center()
				#draw a coin (random number that is either 0 or 1)
			if libtcod.random_get_int(0, 0, 1) == 1:
				#first move horizontally, then vertically
				self.create_h_tunnel(prev_x, new_x, prev_y, map, nearest_points_array, center_points)
				self.create_v_tunnel(new_y, prev_y, new_x, map, nearest_points_array, center_points)
			else:
				#first move vertically, then horizontally
				self.create_v_tunnel(prev_y, new_y, prev_x, map, nearest_points_array, center_points)
				self.create_h_tunnel(new_x, prev_x, new_y, map, nearest_points_array, center_points)
			(new_x, new_y) = elev2.center()
			num = libtcod.random_get_int(0, 0, num_norm_rooms-1)
			(prev_x, prev_y) = rooms[num].center()
				#draw a coin (random number that is either 0 or 1)
			if libtcod.random_get_int(0, 0, 1) == 1:
				#first move horizontally, then vertically
				self.create_h_tunnel(prev_x, new_x, prev_y, map, nearest_points_array, center_points)
				self.create_v_tunnel(new_y, prev_y, new_x, map, nearest_points_array, center_points)
			else:
				#first move vertically, then horizontally
				self.create_v_tunnel(prev_y, new_y, prev_x, map, nearest_points_array, center_points)
				self.create_h_tunnel(new_x, prev_x, new_y, map, nearest_points_array, center_points)
			(new_x, new_y) = elev3.center()
			num = libtcod.random_get_int(0, 0, num_norm_rooms-1)
			(prev_x, prev_y) = rooms[num].center()
				#draw a coin (random number that is either 0 or 1)
			if libtcod.random_get_int(0, 0, 1) == 1:
				#first move horizontally, then vertically
				self.create_h_tunnel(prev_x, new_x, prev_y, map, nearest_points_array, center_points)
				self.create_v_tunnel(prev_y, new_y, new_x, map, nearest_points_array, center_points)
			else:
				#first move vertically, then horizontally
				self.create_v_tunnel(prev_y, new_y, prev_x, map, nearest_points_array, center_points)
				self.create_h_tunnel(new_x, prev_x, new_y, map, nearest_points_array, center_points)
			(new_x, new_y) = elev4.center()
			num = libtcod.random_get_int(0, 0, num_norm_rooms-1)
			(prev_x, prev_y) = rooms[num].center()
				#draw a coin (random number that is either 0 or 1)
			if libtcod.random_get_int(0, 0, 1) == 1:
				#first move horizontally, then vertically
				self.create_h_tunnel(prev_x, new_x, prev_y, map, nearest_points_array, center_points)
				self.create_v_tunnel(new_y, prev_y, new_x, map, nearest_points_array, center_points)
			else:
				#first move vertically, then horizontally
				self.create_v_tunnel(prev_y, new_y, prev_x, map, nearest_points_array, center_points)
				self.create_h_tunnel(new_x, prev_x, new_y, map, nearest_points_array, center_points)
				# ok that was a bunch of code to append some elevators! Let's see how it goes
	
	
	
		else:		# 'classic' mode
	
			for r in range(room_range):
				#random width and height
				w = libtcod.random_get_int(0, room_min_size, room_max_size)
				h = libtcod.random_get_int(0, room_min_size, room_max_size)
				#random position without going out of the boundaries of the map
				x = libtcod.random_get_int(0, 0, map_width - w - 1)
				y = libtcod.random_get_int(0, 0, map_height - h - 1)
		
				#"Rect" class makes rectangles easier to work with
				new_room = Rect(x, y, w, h)
		 
				#run through the other rooms and see if they intersect with this one
				failed = False
				for other_room in rooms:
					if new_room.intersect(other_room):
						failed = True
						break
		
				if not failed:
					#this means there are no intersections, so this room is valid
		
					#"paint" it to the map's tiles
					self.create_room(new_room, map, center_points, nearest_points_array)
					#add some contents to this room, such as monsters
					self.place_objects(new_room, lev_set, map, object_data, dungeon_level)
		
					#center coordinates of new room, will be useful later
					(new_x, new_y) = new_room.center()
					if num_rooms == 0:
						#this is the first room, where the player starts at
						player_start_x = new_x
						player_start_y = new_y
					else:
						#all rooms after the first:
						#connect it to the previous room with a tunnel
		
						#center coordinates of previous room
						(prev_x, prev_y) = rooms[num_rooms-1].center()
		
						#draw a coin (random number that is either 0 or 1)
						if libtcod.random_get_int(0, 0, 1) == 1:
							#first move horizontally, then vertically
							self.create_h_tunnel(prev_x, new_x, prev_y, map, nearest_points_array, center_points)
							self.create_v_tunnel(new_y, prev_y, new_x, map, nearest_points_array, center_points)
						else:
							#first move vertically, then horizontally
							self.create_v_tunnel(prev_y, new_y, prev_x, map, nearest_points_array, center_points)
							self.create_h_tunnel(new_x, prev_x, new_y, map, nearest_points_array, center_points)
		
					#finally, append the new room to the list
					rooms.append(new_room)
					num_rooms += 1
		
			#create stairs at the center of the last room
			#stairs = Object(new_x, new_y, '<', 'stairs', libtcod.white, always_visible=True)
			#objects.append(stairs)
			#stairs.send_to_back()  #so it's drawn below the monsters
			#object_data.append(Object_Datum(new_x,new_y, 'stairs'))
			
			if lev_set.boss is not None:
				#boss_monster = create_monster(new_x,new_y,lev_set.boss)
				#objects.append(boss_monster)
				object_data.append(Object_Datum(new_x,new_y, 'boss', lev_set.boss))




		#self.append_segment(map, self.create_segment(), player_start_x, player_start_y, object_data)


		return Level_Data(map, player_start_x, player_start_y, object_data, nearest_points_array, center_points, spawn_points, elevators)

			
	#	process_nearest_center_points()
	
	#	calculate_nav_data()	


	def create_room(self,room, map, center_points, nearest_points_array):
		#global map, spawn_points, center_points, nearest_points_array


		(new_x, new_y) = room.center()
		center_points.append((new_x,new_y))

		#go through the tiles in the rectangle and make them passable
		for x in range(room.x1, room.x2+1):
			for y in range(room.y1, room.y2+1):
				map[x][y].blocked = False
				map[x][y].block_sight = False
				nearest_points_array[x][y] = (new_x, new_y)



	def add_security_systems(self, map, lev_set, dungeon_level, object_data, rooms, elevators, number_sec_systems):
		# create an initial shortlist of rooms where one could place security system
		# for now, theshortlist is just anything that's not an elevator. This should probabl change later.
		initial_shortlist = []
		for room in rooms:
			if room in elevators:
				print "room in elevators..."
			else:
				initial_shortlist.append(room)
		current_shortlist = initial_shortlist

		for i in range(0, number_sec_systems):		
			# choose a room at random, stick a security system in, strike it off the shortlist
			num = libtcod.random_get_int(0, 0, len(current_shortlist)-1)
			selected_room = current_shortlist[num]
			self.add_security_system(map, lev_set, dungeon_level, object_data, rooms, elevators, selected_room)
			current_shortlist.remove(selected_room)
			# have we run out of rooms? then refresh the list, allow doubling up to happen.
			if len(current_shortlist) == 0:
				current_shortlist = initial_shortlist


	def add_security_system(self, map, lev_set, dungeon_level, object_data, rooms, elevators, security_room):
		(sec_x,sec_y) = security_room.center()
		object_data.append(Object_Datum(sec_x,sec_y,'security system'))
		self.decorate_room(security_room, lev_set, map, object_data, dungeon_level,symbol = '.')
	


	def place_objects(self, room, lev_set, map, object_data, dungeon_level):
		#global game_level_settings, dungeon_level, god_healer
	
		#lev_set = game_level_settings.get_setting(dungeon_level)

		max_room_monsters = lev_set.max_room_monsters

		#choose random number of monsters
		num_monsters = libtcod.random_get_int(0, 0, max_room_monsters)
		

		for i in range(num_monsters):
		#for i in range(50):
			#choose random spot for this monster
			x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
			y = libtcod.random_get_int(0, room.y1+1, room.y2-1)
	
			#only place it if the tile is not blocked
			if not self.is_occupied(x, y, map, object_data):
	
				total_enemy_prob = lev_set.total_enemy_prob
				enemy_probabilities = lev_set.enemy_probabilities

				
	
				enemy_name = 'none'
				num = libtcod.random_get_int(0,0, total_enemy_prob)
				for (name, prob) in enemy_probabilities:
					#print '(' + name + ',' + str(prob) + ')'
					if num <= prob:
						enemy_name = name
						break
					else:
						num -= prob
	
				#monster = create_monster(x,y,name)
				#objects.append(monster)
				object_data.append(Object_Datum(x,y,'monster', name))
	
		# on first level, in in 2 chance of a weapon appearing in a room I guess
		if dungeon_level == 0:
			num = libtcod.random_get_int(0, 0, 2)
			if num == 0:
				x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
				y = libtcod.random_get_int(0, room.y1+1, room.y2-1)
				#new_weapon = Object(x,y, 's', 'sword', default_weapon_color, blocks = False, weapon = True)
				#drop_weapon(new_weapon)
				#objects.append(new_weapon)
				#new_weapon.send_to_back()
				object_data.append(Object_Datum(x,y,'weapon', 'sword'))
			elif num == 1:
				x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
				y = libtcod.random_get_int(0, room.y1+1, room.y2-1)
				#new_weapon = Object(x,y, 'f', 'sai', default_weapon_color, blocks = False, weapon = True)
				#drop_weapon(new_weapon)
				#objects.append(new_weapon)
				#new_weapon.send_to_back()
				object_data.append(Object_Datum(x,y,'weapon', 'sai'))
	
		# on higher levels, maybe there are shrines? Maybe??
		else:
			num = libtcod.random_get_int(0,0,6)
			if num == 0:
				(shrine_x, shrine_y) = room.center()
				#new_shrine = Object(shrine_x, shrine_y, '&', 'shrine to ' + god_healer.name, default_altar_color, blocks=False, shrine= Shrine(god_healer), always_visible=True) 		
				#objects.append(new_shrine)
				#new_shrine.send_to_back()
				object_data.append(Object_Datum(shrine_x,shrine_y, 'shrine', 'healer'))
				self.decorate_room(room, lev_set, map, object_data, dungeon_level,symbol = '+')
		# or maybe security systems?
		#	elif num == 1:
		#		if lev_set.final_level is not True:	#don't have sec systems on final levels?
		#			(sec_x,sec_y) = room.center()
		#			object_data.append(Object_Datum(sec_x,sec_y,'security system'))
		#			self.decorate_room(room, lev_set, map, object_data, dungeon_level,symbol = '.')


	# Create pretty decorations on the border of the room! Let's see if it looks any good.
	def decorate_room(self, room, lev_set, map, object_data, dungeon_level,symbol = '~'):
		# corners
		object_data.append(Object_Datum(room.x1,room.y1, 'decoration', symbol))
		object_data.append(Object_Datum(room.x1,room.y2, 'decoration', symbol))
		object_data.append(Object_Datum(room.x2,room.y1, 'decoration', symbol))
		object_data.append(Object_Datum(room.x2,room.y2, 'decoration', symbol))
		#top and bottom
		for x in range(room.x1+1, room.x2):
			object_data.append(Object_Datum(x,room.y1, 'decoration', symbol))
			object_data.append(Object_Datum(x,room.y2, 'decoration', symbol))
		for y in range(room.y1+1, room.y2):
			object_data.append(Object_Datum(room.x1,y, 'decoration', symbol))
			object_data.append(Object_Datum(room.x2,y, 'decoration', symbol))


	def is_occupied(self, x, y, map, object_data):
		#first test the map tile
		if map[x][y].blocked:
			return True

		#now check for any blocking objects
		for object_datum in object_data:
			if object_datum.x == x and object_datum.y == y:		#slight change to previous - no check that object 'blocks'.
				return True
		return False


	def create_corridor(self, room1, room2, map, center_points,  nearest_points_array, object_data, doors_on = False, doors_off = False, width = 3):


		#door stuff
		if doors_on == True:
			do_doors = True
		elif doors_off == True:
			do_doors = False
		else:
			if libtcod.random_get_int(0, 0, 1) == 1:
				do_doors = True
			else:
				do_doors = False



		half_width = (width-1)/2
		# okay let's think about this. First... are they horizontally aligned?
		if max(room1.x1, room2.x1)+half_width < min(room1.x2, room2.x2 - half_width):
			#horitontally aligned!
			jx = libtcod.random_get_int(0, max(room1.x1, room2.x1)+half_width, min(room1.x2, room2.x2)-half_width-1)
			jy = (max(room1.y1, room2.y1) + min(room1.y2, room2.y2))/2
		#	print 'horiz align (' + str(jx) + ', ' + str(jy) + ')'
			self.create_half_corridor(room1, jx, jy, map, center_points,  nearest_points_array, object_data, do_doors)
			self.create_half_corridor(room2, jx, jy, map, center_points,  nearest_points_array, object_data, do_doors)
		elif max(room1.y1, room2.y1)+half_width < min(room1.y2, room2.y2) - half_width:
			#vertically aligned!
			jy = libtcod.random_get_int(0, max(room1.y1, room2.y1)+half_width, min(room1.y2, room2.y2)-half_width-1)
			jx = (max(room1.x1, room2.x1) + min(room1.x2, room2.x2))/2
		#	print 'vert align (' + str(jx) + ', ' + str(jy) + ')'
			self.create_half_corridor(room1, jx, jy, map, center_points,  nearest_points_array, object_data, do_doors)
			self.create_half_corridor(room2, jx, jy, map, center_points,  nearest_points_array, object_data, do_doors)
		else:
			# neither! we're gonna have to go round some corners.	
			if libtcod.random_get_int(0, 0, 1) == 1:
				# go vertical and then horizontal
				jx = libtcod.random_get_int(0, room1.x1, room1.x2)
				jy = libtcod.random_get_int(0, room2.y1, room2.y2)
			else: 
				# go horizontal and then vertical
				jx = libtcod.random_get_int(0, room2.x1, room2.x2)
				jy = libtcod.random_get_int(0, room1.y1, room1.y2)
		#	print 'neith align (' + str(jx) + ', ' + str(jy) + ')'
			self.create_half_corridor(room1, jx, jy, map, center_points,  nearest_points_array, object_data, do_doors)
			self.create_half_corridor(room2, jx, jy, map, center_points,  nearest_points_array, object_data, do_doors)


	def create_half_corridor(self, room1, jx, jy, map, center_points,  nearest_points_array, object_data, do_doors = False,  width = 3,):
		if nearest_points_array[jx][jy] is None:
			center_points.append((jx,jy))
		half_width = (width-1)/2
	
		#door stuff
		#if doors_on == True:
		#	do_doors = True
		#elif doors_off == True:
		#	do_doors = False
		#else:
		#	if libtcod.random_get_int(0, 0, 1) == 1:
		#		do_doors = True
		#	else:
		#		do_doors = False


		map[jx][jy].blocked = False
		map[jx][jy].block_sight = False
			

		if jx in range(room1.x1, room1.x2+1):
		#	print 'horiz?'
			(other_x, min_y) = room1.center()
			max_y = min_y
			end_y = max_y
			# vertical times!
			if jy < room1.y1:
				#going up times!
		#		print 'hup'
				min_y = jy
				max_y = room1.y1-1
				end_y = max_y

			elif jy > room1.y2:
				# going down times!
		#		print 'hop'
				min_y = room1.y2
				max_y = jy
				end_y = min_y
		#	else:
		#		print 'woops'
			for y in range(min_y, max_y+1):
		#		print 'yo ' + str(y)
				for x in range(jx - half_width, jx + half_width+1):
		#			print 'yooo (' + str(x) + ', ' + str(y) + ')'
					map[x][y].blocked = False
					map[x][y].block_sight = False
					if nearest_points_array[x][y] is None:
						nearest_points_array[x][y] = (jx, jy)
			if do_doors == True:
				for x in range(jx - half_width, jx + half_width+1):
					if x != jx:
						map[x][end_y].blocked = True
						map[x][end_y].block_sight = True
				object_data.append(Object_Datum(jx, end_y, 'door', 'horizontal'))

		elif jy in range(room1.y1, room1.y2+1):
		#	print 'vert?'
			#horizontal times!
			(min_x, other_y) = room1.center()
			max_x = min_x
			end_x = max_x
			if jx < room1.x1:
				#going left times!
				min_x = jx
				max_x = room1.x1-1
				end_x = max_x
			elif jx > room1.x2:
				# going right times!
				min_x = room1.x2
				max_x = jx
				end_x = min_x
		#	else:
		#		print 'wups'
			for x in range(min_x, max_x+1):
				for y in range(jy - half_width, jy + half_width+1):
					map[x][y].blocked = False
					map[x][y].block_sight = False
					if nearest_points_array[x][y] is None:
						nearest_points_array[x][y] = (jx, jy)
			if do_doors == True:
				for y in range(jy - half_width, jy + half_width+1):
					if y != jy:
						map[end_x][y].blocked = True
						map[end_x][y].block_sight = True
				object_data.append(Object_Datum(end_x, jy, 'door', 'vertical'))

		#else: 
		#	print 'nope'

	def create_h_tunnel(self, x1, x2, y, map, nearest_points_array, center_points, narrow = False):
		#global map, nearest_points_array, center_points
		if nearest_points_array[x2][y] is None:
			center_points.append((x2,y))
		for x in range(min(x1, x2), max(x1, x2) + 1):
			map[x][y].blocked = False
			map[x][y].block_sight = False
			if narrow == False:
				map[x][y-1].blocked = False
				map[x][y-1].block_sight = False
				map[x][y+1].blocked = False
				map[x][y+1].block_sight = False
			if nearest_points_array[x][y] is None:
				nearest_points_array[x][y] = (x2, y)
			if nearest_points_array[x][y-1] is None:
				nearest_points_array[x][y-1] = (x2, y)
			if nearest_points_array[x][y+1] is None:
				nearest_points_array[x][y+1] = (x2, y)
	
	def create_v_tunnel(self, y1, y2, x, map, nearest_points_array, center_points, narrow = False):
		#global map, nearest_points_array, center_points
		if nearest_points_array[x][y2] is None:
			center_points.append((x,y2))
		#vertical tunnel
		for y in range(min(y1, y2), max(y1, y2) + 1):
			map[x][y].blocked = False
			map[x][y].block_sight = False
			if narrow == False:
				map[x-1][y].blocked = False
				map[x-1][y].block_sight = False
				map[x+1][y].blocked = False
				map[x+1][y].block_sight = False
			if nearest_points_array[x][y] is None:
				nearest_points_array[x][y] =  (x,y2)
			if nearest_points_array[x-1][y] is None:
				nearest_points_array[x-1][y] =  (x,y2)
			if nearest_points_array[x+1][y] is None:
				nearest_points_array[x+1][y] =  (x,y2)
	


	def create_elevator(self, elevator, map, spawn_points, center_points, nearest_points_array, object_data, elevators, elevator_type = 'Small-Elevator-Right'):
		# like creating a room, but with a spawn point!
		#global map, spawn_points, center_points, nearest_points_array

		(new_x, new_y) = elevator.center()
		center_points.append((new_x,new_y))
		#spawn_points.append((new_x,new_y))
	
		#go through the tiles in the rectangle and make them passable


		for x in range(elevator.x1, elevator.x2+1):
			for y in range(elevator.y1, elevator.y2+1):
				map[x][y].blocked = False
				map[x][y].block_sight = False
				nearest_points_array[x][y] = (new_x, new_y)

		door_points = []
		#spawn_points = []	
		local_spawn_points = []
		if elevator_type == 'Small-Elevator-Left':
			seg_map =      [[0,0,1,1,1],
					[0,0,3,4,4],
					[0,0,3,4,4],
					[0,0,1,1,1]]
		elif elevator_type == 'Small-Elevator-Right':
			seg_map =      [[1,1,1,0,0],
					[4,4,3,0,0],
					[4,4,3,0,0],
					[1,1,1,0,0]]
		elif elevator_type == 'Small-Elevator-Down':
			seg_map =      [[1,4,4,1],
					[1,4,4,1],
					[1,3,3,1],
					[0,0,0,0],
					[0,0,0,0]]
		elif elevator_type == 'Small-Elevator-Up':
			seg_map =      [[0,0,0,0],
					[0,0,0,0],
					[1,3,3,1],
					[1,4,4,1],
					[1,4,4,1]]
		for y in range(0, len(seg_map)):
			for x in range(0, len(seg_map[0])):
				if (seg_map[y][x] == 3):
					door_point = (elevator.x1 + x, elevator.y1 + y)
					door_points.append(door_point)
				elif (seg_map[y][x] == 4):
					spawn_point = (elevator.x1+x, elevator.y1+y)
					local_spawn_points.append(spawn_point)
					spawn_points.append(spawn_point)
				elif (seg_map[y][x] == 1):	
					map[elevator.x1 + x][elevator.y1 + y].blocked = True
					map[elevator.x1 + x][elevator.y1 + y].block_sight = True

		new_elevator = Elevator(door_points, local_spawn_points)
		#print "elevatooooooooR"
		elevators.append(new_elevator)

			

	#	elevator_segment = self.create_segment(code=elevator_type)
	#	self.append_segment(map, elevator_segment, elevator.x1, elevator.y1, object_data)
#	def append_segment(self, map, segment, x_offset, y_offset, object_data):
#	def create_segment(self, code = None):




	def append_segment(self, map, segment, x_offset, y_offset, object_data):
		map_segment = segment.seg_map
		for y in range (0, len(map_segment)):
			for x in range (0, len(map_segment[y])):
				if map_segment[y][x] == 0:
					map[x + x_offset][y + y_offset].blocked = False
					map[x + x_offset][y + y_offset].block_sight = False
				elif map_segment[y][x] == 1:
					map[x + x_offset][y + y_offset].blocked = True
					map[x + x_offset][y + y_offset].block_sight = True
		for od in segment.seg_data:
			object_data.append(Object_Datum(od.x + x_offset, od.y + y_offset, od.name, od.info, od.more_info))



			
	def create_segment(self, code = None):
		seg_data = []
		seg_map = [[]]

		if code == 'Tut-Attack':
			A = Object_Name('monster', 'strawman')
			#B = Object_Name('strawman', 'sai', 'w')
			#M = Object_Name('message', 'Good lord it\'s some sort of message on the floor!!!')
			seg_map =      [[0,0,0,0,0,0,0,0],
					[0,0,0,A,0,0,A,0],
					[0,A,0,0,0,0,0,0],
					[0,0,0,0,A,0,A,0],
					[0,0,0,0,0,0,0,0]]


		elif code == 'Tut-Avoid-Attacks':
			A = Object_Name('strawman', 'sai', ATTCKUP)
			B = Object_Name('strawman', 'sai', ATTCKLEFT)
			seg_map =      [[0,0,0,0,0,B,0],
					[0,0,0,0,0,0,0],
					[0,0,A,0,B,0,B],
					[0,0,0,0,0,0,0],
					[0,0,0,0,0,A,0]]


		elif code == 'Tut-Moving-Enemies':
			A = Object_Name('monster', 'strawman on wheels')
			seg_map =      [[0,0,0,0,0,0,0],
					[0,A,0,0,0,0,0],
					[0,0,0,0,0,0,0],
					[0,0,0,0,0,A,0],
					[0,0,0,0,0,0,0]]


		elif code == 'Tut-Gauntlet':
			A = Object_Name('strawman', 'spear', ATTCKDOWNALT)
			B = Object_Name('strawman', 'spear', ATTCKUP)
			C = Object_Name('door', 'horizontal')
			D = Object_Name('door', 'vertical')
			seg_map =      [[1,A,1,A,1,A,1],
					[1,0,1,0,1,0,1],
					[0,0,0,0,0,0,0],
					[1,0,1,0,1,0,1],
					[1,B,1,B,1,B,1]]


		elif code == 'Tut-Test':
			R = Object_Name('monster','rook')
			D = Object_Name('door', 'vertical')
			seg_map =      [[0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1],
					[0,0,0,0,0,0,1,0,0,0,1,1,1,1,1,1],
					[0,0,1,1,0,0,1,1,0,0,1,0,0,0,0,0],
					[0,0,1,0,0,0,0,1,1,0,1,0,0,0,0,0],
					[0,R,0,0,0,0,0,0,0,0,D,0,0,0,0,0],
					[0,1,1,0,0,0,0,1,0,0,1,0,0,0,0,0],
					[0,0,1,1,0,0,1,1,0,0,1,0,0,0,0,0],
					[0,0,0,1,0,0,0,0,0,0,1,1,1,1,1,1],
					[0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1]]



		elif code == 'Whole-Tutorial':
			A = Object_Name('monster', 'strawman')
			B = Object_Name('strawman', 'sai', ATTCKUP)
			C = Object_Name('strawman', 'sai', ATTCKLEFT)
			seg_map =      [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
					[1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,1,1,0,0,0,0,0,B,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
					[1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,A,0,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
					[1,0,0,0,0,0,0,0,0,0,0,0,0,0,A,0,0,0,A,0,0,0,0,B,0,C,0,C,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,],
					[1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,A,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
					[1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,A,0,0,1,1,1,0,0,0,0,0,B,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
					[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
					[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
					[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
					[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
					[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,],
					[0,0,0,A,0,0,A,0],
					[0,A,0,0,0,0,0,0],
					[0,0,0,0,A,0,A,0],
					[0,0,0,0,0,0,0,0]]

		elif code == 'Small-Elevator-Right':
			D = Object_Name('stairs')
			seg_map =      [[1,1,1,0,0],
					[0,0,D,0,0],
					[0,0,D,0,0],
					[1,1,1,0,0]]

		elif code == 'Small-Elevator-Left':
			D = Object_Name('stairs')
			seg_map =      [[0,0,1,1,1],
					[0,0,D,0,0],
					[0,0,D,0,0],
					[0,0,1,1,1]]

		else:
			H = Object_Name('shrine', 'healer')	
			seg_map =      [[0,0,0,0,0],
					[0,0,0,0,0],
					[0,1,1,1,0],
					[0,H,0,1,0],
					[0,0,0,0,0]]
		#seg_data.append(Object_Datum(2,3, 'shrine', 'healer'))

		# now take the object names from the maps, and turn them into object data
		for y in range (0, len(seg_map)):
			for x in range (0, len(seg_map[y])):
				obname = seg_map[y][x]
				if not (obname >= 0 and obname <= 9):
					# so it's not a number, it's an object name
					seg_data.append(Object_Datum(x,y, obname.name, obname.info, obname.more_info))
					seg_map[y][x] = 0

				#if seg_map[y][x] == 0:
				#	map[x + x_offset][y + y_offset].blocked = False
				#	map[x + x_offset][y + y_offset].block_sight = False
				#elif map_segment[y][x] == 1:
				#	map[x + x_offset][y + y_offset].blocked = True
				#	map[x + x_offset][y + y_offset].block_sight = True

		
		return Level_Segment(seg_map, seg_data)




	#	segment_map =  [[1,1,1,1,1,1,1],
	#			[0,0,0,1,0,0,0],
	#			[0,0,0,0,0,0,0],
	#			[0,0,1,1,1,0,0],
	#			[0,0,0,0,0,0,0],
	#			[0,0,0,1,0,0,0],
	#			[1,1,1,1,1,1,1]


	def recursively_generate(self, map, lev_set, dungeon_level, object_data, rooms, room_range, current_room, nearest_points_array, center_points):
		

		# exit condition - too many rooms already?
		if len(rooms) < room_range:

			x = current_room.x1
			y = current_room.y1
			w = current_room.x2-x
			h = current_room.y2-y

			room_min_size = lev_set.room_min_size
			room_max_size = lev_set.room_max_size

			poss_rooms = []
			
			# create a list of potential rooms we might make branching off of this one.
			#poss_rooms.append(Rect(x, y - h - 2,w,h))
			#poss_rooms.append(Rect(x, y + h + 2,w,h))
			#poss_rooms.append(Rect(x-w-2, y, w,h))
			#poss_rooms.append(Rect(x+w+2,y,w,h))

			# trying to do variable room size
			new_w =  libtcod.random_get_int(0, room_min_size, room_max_size)
			new_h = libtcod.random_get_int(0, room_min_size, room_max_size)

			poss_rooms.append(Rect(x, y - new_h - 1,w,new_h))
			poss_rooms.append(Rect(x, y + h + 1,w,new_h))
			poss_rooms.append(Rect(x-new_w-1, y, new_w,h))
			poss_rooms.append(Rect(x+w+1,y,new_w,h))

			# okay let's try doing something with variable rooms sizes... 


			room_shortlist = []
			# find out which of your potential rooms can actually fit in the current design.
			for pr in poss_rooms:
				space_taken = False
				if pr.x1 <= 0 or pr.x2 >= len(map)-1 or pr.y1 <= 0 or pr.y2 >= len(map[0])-1:
					space_taken = True
				for other_room in rooms:
					if pr.intersect(other_room):
						space_taken = True
				if space_taken == False:
					room_shortlist.append(pr)

			# pick new room at random
			if len(room_shortlist) > 0:		# only pick a room if rooms exist!

				created_rooms = []

				#decide how many rooms to do.
				number_rooms = libtcod.random_get_int(0, 1, len(room_shortlist))

				for i in range(1, number_rooms+1):
					#print str(number_rooms) + ' - ' + str(i)
					choice = libtcod.random_get_int(0, 0, len(room_shortlist)-1)

					new_room = room_shortlist[choice]
	
					self.create_room(new_room, map, center_points, nearest_points_array)
					rooms.append(new_room)
					self.place_objects(new_room, lev_set, map, object_data, dungeon_level)
	

					self.create_corridor(current_room, new_room, map, center_points,  nearest_points_array, object_data)
			#MONKEYHORSE
			#		(prev_x, prev_y) = current_room.center()
			#		(new_x, new_y) = new_room.center()
			#		if new_room.x1 == x:
			#			#move vertically
			#			self.create_v_tunnel(new_y, prev_y, new_x, map, nearest_points_array, center_points, narrow = True)
			#		else:
			#			# horizontally
			#			self.create_h_tunnel(new_x, prev_x, new_y, map, nearest_points_array, center_points, narrow = True)
					
					created_rooms.append(new_room)
				
					room_shortlist.remove(new_room)

				# recurse on the new rooms!
				for j in range(0, len(created_rooms)):
					self.recursively_generate(map, lev_set, dungeon_level, object_data, rooms, room_range, created_rooms[j], nearest_points_array, center_points)




			# construct a list of possible places to put the next room

				# if the room already overlaps with another, don't use it...

		# if there are no options availablem return. otherwise...

		# pick one of the options at random

		# create the room

		# add a connecting corridor

		# recursively build out from the new room...

		# or for a more even design, maybe build a bunch of new ones and then build out from each of them?
		


	# method of creating rooms that is basically "try and pack rooms into a particular rectangular area until there's no room
	def fill_a_rectangle(self, map, lev_set, dungeon_level, object_data, rooms, nearest_points_array, center_points, spawn_points, elevators):




		room_min_size = lev_set.room_min_size
		room_max_size = lev_set.room_max_size		
		max_map_height = lev_set.max_map_height
		max_map_width = lev_set.max_map_width

		#let's.... *start* by making some elevators
		#print 'adding elevators...'
		elev1 = Rect(1, 2, 5, 4)
		elev2 = Rect(max_map_width-6, 2, 5, 4)
		elev3 = Rect(max_map_width-6, max_map_height -6, 5, 4)
		elev4 = Rect(1, max_map_height - 6, 5, 4)
		rooms.append(elev1)
		rooms.append(elev2)
		rooms.append(elev3)
		rooms.append(elev4)

		self.create_elevator(elev1, map, spawn_points, center_points, nearest_points_array, object_data,  elevators, 'Small-Elevator-Right')
		self.create_elevator(elev2, map, spawn_points, center_points, nearest_points_array, object_data,  elevators, 'Small-Elevator-Left')
		self.create_elevator(elev3, map, spawn_points, center_points, nearest_points_array, object_data,  elevators, 'Small-Elevator-Left')
		self.create_elevator(elev4, map, spawn_points, center_points, nearest_points_array, object_data,  elevators, 'Small-Elevator-Right')


		# now... make the limits of our other rooms be such that there come close to but don't overlap the elevators..
		horiz_lower_bound = 6
		horiz_upper_bound = max_map_width-5
		vert_lower_bound = 1
		vert_upper_bound = max_map_height
		


		# initialize a list of maximal potential rooms - all the rooms of maximum size that could exist.
		maximal_potential_rooms = []
		for i in range (horiz_lower_bound, horiz_upper_bound - room_max_size):
			for j in range(vert_lower_bound, vert_upper_bound - room_max_size):
				maximal_potential_rooms.append(Rect(i,j, room_max_size, room_max_size))
		
		# each time we make a new room from here on, it has a chance of getting doors. 
		# this array keeps tracks of which rooms should have doors.
		doorhavers = []
		for i in range(len(rooms)):
			doorhavers.append(False)

#		for r in range(0,2):
		while len(maximal_potential_rooms) > 0:

		


			# pick a random room from the maximal potential rooms list
			choice = libtcod.random_get_int(0, 0, len(maximal_potential_rooms)-1)
			temp_new_room = maximal_potential_rooms[choice]
			# for variety, vary the room size a little 
			# I am cheating and just randomly trimming the edges.
			# only trim if the room isn't too small already though
			if temp_new_room.x2-temp_new_room.x1 < 4:
				trim_left = 0
				trim_right = 0
			else:
				trim_left = libtcod.random_get_int(0, 0, 1)
				trim_right = libtcod.random_get_int(0, 0, 1)
			if temp_new_room.y2-temp_new_room.y1 < 4:
				trim_top = 0
				trim_bottom = 0
			else :
				trim_top = libtcod.random_get_int(0, 0, 1)
				trim_bottom = libtcod.random_get_int(0, 0, 1)
			new_room = Rect(temp_new_room.x1+trim_left, temp_new_room.y1+trim_top, temp_new_room.x2-temp_new_room.x1+1-trim_left-trim_right, temp_new_room.y2-temp_new_room.y1+1-trim_top-trim_bottom)
			#TODO: if room is close to the border, move it along.
			#Put this new room into the map
			self.create_room(new_room, map, center_points, nearest_points_array)
			rooms.append(new_room)
			self.place_objects(new_room, lev_set, map, object_data, dungeon_level)
		
			# decide whether or not this room has doors. FOR NOW JUST A 1/8 CHANCE OF HAVING DOORS
			if libtcod.random_get_int(0, 0, 7) == 1:
				doorhavers.append(True)
			else:
				doorhavers.append(False)



			#Now update the maximal room list to remove rooms that clash with the new room amd replace them with their remainders
			new_maximal_potential_rooms = []
			long_list = []
			for old_room in maximal_potential_rooms:
				# if old_room hasn't been affected by new_room, just pass it on to the next list of potential rooms
				if not old_room.touching(new_room):
					long_list.append(old_room)

				else:
					# ok now here's where things get complicated
					#If there is space within old_room to fit a new smaller room to any of the left, right, top or bottom of new_room, add those smaller rooms to the list.
					squeezed_to_left = False
					if old_room.x1 < new_room.x1:
						squeezed_to_left = True
						left_x1 = old_room.x1
						left_x2 = new_room.x1-2  #don't want rooms to touch, after all
						if left_x2<left_x1:		# sanity check - don't want negative sized rooms
							squeezed_to_left = False

					if squeezed_to_left:
						left_room = Rect(old_room.x1, old_room.y1, left_x2-old_room.x1+1, old_room.y2-old_room.y1+1) 	
						long_list.append(left_room)

					squeezed_up = False
					if old_room.y1 < new_room.y1:
						squeezed_up = True
						up_y1 = old_room.y1
						up_y2 = new_room.y1-2  #don't want rooms to touch, after all
						if up_y2<up_y1:		# sanity check - don't want negative sized rooms
							squeezed_up = False

					if squeezed_up:
						up_room = Rect(old_room.x1, old_room.y1, old_room.x2-old_room.x1+1, up_y2-old_room.y1+1) 	
						long_list.append(up_room)


					squeezed_to_right = False
					if old_room.x2 > new_room.x2:
						squeezed_to_right = True
						right_x1 = new_room.x2 + 2 #don't want rooms to touch after all
						right_x2 = old_room.x2
						if right_x2<right_x1:		#sanity check - don't want negative sized rooms
							squeezed_to_right = False
			
					if squeezed_to_right:
						right_room = Rect(right_x1, old_room.y1, right_x2-right_x1+1, old_room.y2-old_room.y1+1)
						long_list.append(right_room)

					squeezed_down = False
					if old_room.y2 > new_room.y2:
						squeezed_down = True
						down_y1 = new_room.y2 + 2 #don't want rooms to touch after all
						down_y2 = old_room.y2
						if down_y2<down_y1:		#sanity check - don't want negative sized rooms
							squeezed_down = False
			
					if squeezed_down:
						down_room = Rect(old_room.x1, down_y1, old_room.x2-old_room.x1+1, down_y2-down_y1+1)
						long_list.append(down_room)

			# go through long list and add them to the new maximal potential rooms list.
			# if anything in the long list is already covered by something in the new list (i.e. fits inside it), don't add it
			new_maximal_potential_rooms = []

			# only pass rooms on if they aren't strictly contained in any other room in the list.
			long_len = len(long_list)
			for i in range(0, long_len):
				conflict = False
				if long_list[i].x2 < long_list[i].x1 + 1 or long_list[i].y2 < long_list[i].y1 + 1:
					conflict = True
				for j in range(0, long_len):
					if long_list[i].contained_in(long_list[j]) and (j<i or  long_list[i].strictly_contained_in(long_list[j]) ):
						conflict = True
				if conflict == False:
					new_maximal_potential_rooms.append(long_list[i])

			# do final update of the maximal potential rooms list.
			maximal_potential_rooms = new_maximal_potential_rooms

		# Ok all the room creation has been done! But what's this? There are no doors or corridors! You can't actually get from one room to another! So ok let's fix that.
		# This should include joining up the elevators to things. Let's see...

		# The process below will mostly join everything up. But once in a blue moon you get a tiny room that's isolated from the rest.
		# So to get round this, we're going to do some connectivity checking.
		connectivity = []	#2d matrix saying which rooms are connected to each other. Initally, rooms only connected to themselves.
		for i in range(0, len(rooms)):
			temprow = []
			connectivity.append(temprow)
			for j in range(0, len(rooms)):
				if i==j:
					connectivity[i].append(1)
				else:
					connectivity[i].append(0)


		# For now we are doing this in a very naive way. go through every pair of rooms and join them up if they are in line and close.
		for i in range(0, len(rooms)):
			for j in range(0, len(rooms)):
				if i <= j:	# just to make sure we cover each pair only once
					break
				else:
					# are they adjacent?
					adjacent = False
					dist = 4 #the max distance we can have between two rooms for them to count as 'adjacent'.
							# basically dist+1 should be just enough to squeeze a tiny room in between?
					#is room i to the left of room j?
					if rooms[j].x1 > rooms[i].x2 and rooms[j].x1 - rooms[i].x2 <= dist and rooms[i].y2 > rooms[j].y1 and rooms[j].y2 > rooms[i].y1:
						adjacent = True
					#	print 'left adjacency! (' + str(rooms[i].x1) + ',' + str(rooms[i].y1) + ',' + str(rooms[i].x2) + ',' + str(rooms[i].y2) + ') - (' + str(rooms[j].x1) + ',' + str(rooms[j].y1) + ',' + str(rooms[j].x2) + ',' + str(rooms[j].y2) + ')' 

			
						#create a corridor
						corridor_y = libtcod.random_get_int(0, max(rooms[i].y1,rooms[j].y1), min(rooms[i].y2, rooms[j].y2))
						for x in range(rooms[i].x2, rooms[j].x1):
							map[x][corridor_y].blocked = False
							map[x][corridor_y].block_sight = False
							if nearest_points_array[x][corridor_y] is None:
								nearest_points_array[x][corridor_y] = rooms[j].center()
	
						# Add some doors! Maybe. Not if one of the rooms is an elevator.
						roomidoors = doorhavers[i]
						roomjdoors = doorhavers[j]
						if i < len(elevators) or j < len(elevators):
							roomidoors = False
							roomjdoors = False
						# if both rooms are due to have doors, just pick one of them
						if roomidoors and roomjdoors:
							if libtcod.random_get_int(0, 0, 1) == 1:
								roomidoors = False
							else:
								roomjdoors = False
						
						if roomidoors:
							map[rooms[i].x2+1][corridor_y].block_sight = True
							object_data.append(Object_Datum(rooms[i].x2+1, corridor_y, 'door', 'horizontal'))
						if roomjdoors:
							map[rooms[j].x1-1][corridor_y].block_sight = True
							object_data.append(Object_Datum(rooms[j].x1-1, corridor_y, 'door', 'horizontal'))
						




					#is room i to the right of room j?
					if rooms[i].x1 > rooms[j].x2 and rooms[i].x1 - rooms[j].x2 <= dist and rooms[i].y2 > rooms[j].y1 and rooms[j].y2 > rooms[i].y1:
						adjacent = True
			#			print 'right adjacency!'

						#create a corridor
						corridor_y = libtcod.random_get_int(0, max(rooms[i].y1,rooms[j].y1), min(rooms[i].y2, rooms[j].y2))
						for x in range(rooms[j].x2, rooms[i].x1):
							map[x][corridor_y].blocked = False
							map[x][corridor_y].block_sight = False
							if nearest_points_array[x][corridor_y] is None:
								nearest_points_array[x][corridor_y] = rooms[j].center()

						# Add some doors! Maybe. Not if one of the rooms is an elevator.
						roomidoors = doorhavers[i]
						roomjdoors = doorhavers[j]
						if i < len(elevators) or j < len(elevators):
							roomidoors = False
							roomjdoors = False
						# if both rooms are due to have doors, just pick one of them
						if roomidoors and roomjdoors:
							if libtcod.random_get_int(0, 0, 1) == 1:
								roomidoors = False
							else:
								roomjdoors = False
						if roomjdoors:
							map[rooms[j].x2+1][corridor_y].block_sight = True
							object_data.append(Object_Datum(rooms[j].x2+1, corridor_y, 'door', 'horizontal'))
						if roomidoors:
							map[rooms[i].x1-1][corridor_y].block_sight = True
							object_data.append(Object_Datum(rooms[i].x1-1, corridor_y, 'door', 'horizontal'))
						


					#is room i just above room j?
					if rooms[j].y1 > rooms[i].y2 and rooms[j].y1 - rooms[i].y2 <= dist and rooms[i].x2 > rooms[j].x1 and rooms[j].x2 > rooms[i].x1:
						adjacent = True
			#			print 'above adjacency!'

						#create a corridor
						corridor_x = libtcod.random_get_int(0, max(rooms[i].x1,rooms[j].x1), min(rooms[i].x2, rooms[j].x2))
						for y in range(rooms[i].y2, rooms[j].y1):
							map[corridor_x][y].blocked = False
							map[corridor_x][y].block_sight = False
							if nearest_points_array[corridor_x][y] is None:
								nearest_points_array[corridor_x][y] = rooms[j].center()

						# Add some doors! Maybe. Not if one of the rooms is an elevator.
						roomidoors = doorhavers[i]
						roomjdoors = doorhavers[j]
						if i < len(elevators) or j < len(elevators):
							roomidoors = False
							roomjdoors = False
						# if both rooms are due to have doors, just pick one of them
						if roomidoors and roomjdoors:
							if libtcod.random_get_int(0, 0, 1) == 1:
								roomidoors = False
							else:
								roomjdoors = False
						if roomidoors:
							map[corridor_x][rooms[i].y2+1].block_sight = True
							object_data.append(Object_Datum(corridor_x, rooms[i].y2+1, 'door', 'vertical'))
						if roomjdoors:
							map[corridor_x][rooms[j].y1-1].block_sight = True
							object_data.append(Object_Datum(corridor_x, rooms[j].y1-1, 'door', 'vertical'))


					#is room i just below room j?
					if rooms[i].y1 > rooms[j].y2 and rooms[i].y1 - rooms[j].y2 <= dist and rooms[i].x2 > rooms[j].x1 and rooms[j].x2 > rooms[i].x1:
						adjacent = True
			#			print 'below adjacency!'

						#create a corridor
						corridor_x = libtcod.random_get_int(0, max(rooms[i].x1,rooms[j].x1), min(rooms[i].x2, rooms[j].x2))
						for y in range(rooms[j].y2, rooms[i].y1):
							map[corridor_x][y].blocked = False
							map[corridor_x][y].block_sight = False
							if nearest_points_array[corridor_x][y] is None:
								nearest_points_array[corridor_x][y] = rooms[j].center()

						# Add some doors! Maybe. Not if one of the rooms is an elevator.
						roomidoors = doorhavers[i]
						roomjdoors = doorhavers[j]
						if i < len(elevators) or j < len(elevators):
							roomidoors = False
							roomjdoors = False
						# if both rooms are due to have doors, just pick one of them
						if roomidoors and roomjdoors:
							if libtcod.random_get_int(0, 0, 1) == 1:
								roomidoors = False
							else:
								roomjdoors = False
						if roomjdoors:
							map[corridor_x][rooms[j].y2+1].block_sight = True
							object_data.append(Object_Datum(corridor_x, rooms[j].y2+1, 'door', 'vertical'))
						if roomidoors:
							map[corridor_x][rooms[i].y1-1].block_sight = True
							object_data.append(Object_Datum(corridor_x, rooms[i].y1-1, 'door', 'vertical'))


				if adjacent: #update the connectivity list
					#print str(i) + " and " + str(j) + " joined" + str(connectivity[i]) + " woop " + str(connectivity[j])
					for h in range(0, len(rooms)):
						for k in range(0, len(rooms)):
							if (connectivity[i][h] == 1 or connectivity[h][i]) == 1 and (connectivity[j][k] == 1 or connectivity[k][j] == 1):
								connectivity[h][k] = 1
								connectivity[k][h] = 1
						#basically, things connected to i and things connected to j are now connected to each other
						
		#Ok our rooms have been created and joined up.
		# Is there anything that missed being joined up? If something isn't connected to the first room, we need to do something
		#print connectivity
		for i in range(0, len(rooms)):
			if connectivity[i][4] == 0: #room is not connected to room 4. Why room 4? Because that's the first non-elevator room... 
				# we fix the connectivity by super expanding the room. This should intersect with something...
				#print 'help (' + str(rooms[i].x1) + ',' + str(rooms[i].y1) + ')-(' + str(rooms[i].x2) + ',' + str(rooms[i].y2) + ')'
				for x in range(rooms[i].x1-4, rooms[i].x2 + 5):
					for y in range(rooms[i].y1 - 4, rooms[i].y2+5):
						if x > 0  and x < lev_set.max_map_width - 1 and y > 0 and y < lev_set.max_map_height - 1:
							map[x][y].blocked = False
							map[x][y].block_sight = False
							if nearest_points_array[x][y] is None:
								nearest_points_array[x][y] = rooms[i].center()




		# now, append some elevators? Just slap bang in the middle of everything....



				#	if adjacent:
				#		self.create_corridor(rooms[i], rooms[j], map, center_points,  nearest_points_array, object_data, doors_on = False, doors_off = True, width = 1)				

		# Step 2: Join things that are adjacent. Maybe a bit selectively but to begin with let's just join everything.



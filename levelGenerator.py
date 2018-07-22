import tdl as libtcod
#import libtcodpy as libtcod
from objectClass import Object
from random import randint

import math


# COLORS. LET'S TRY AND PUT ALL THE COLORS HERE

# Environment colors (walls +floors, altars, visible or not)
color_dark_wall = (100,100,100)		#(0, 0, 100)
color_light_wall = (130, 110, 50)
color_dark_ground = (150,150,150)		#(50, 50, 150)
color_light_ground = (200, 180, 50)
color_fog_of_war = (0,0,0)			#libtcod.black
default_altar_color = color_light_wall
default_message_color = color_light_wall
default_decoration_color = (250,230,50)		#(165,145,50)
water_background_color = (100,100,250)
water_foreground_color = (25,25,250)
blood_background_color = (200,0,0)
blood_foreground_color = (150,0,0)

# collectiable e.g. weapons and plants and keys
default_flower_color = 	(50,150,0)
default_weapon_color = (50,50,50) #libtcod.grey


# enemies, including player
PLAYER_COLOR = (255, 255, 255)
#color_sneaky_enemy
#color_shortrange_enemy
#color_midrange_enemy
#color_longrange_enemy
#color_big_boss

color_swordsman = (0,0,191)		#libtcod.dark_blue
color_boman = 	(0,128,0)		#libtcod.darker_green
color_rook = 	(0,0,128)		#libtcod.darker_blue
color_axe_maniac = (128,0,0)		#libtcod.darker_red
color_tridentor = (0,0, 255)		#libtcod.blue
color_ninja = 	(0,0,0)		#libtcod.black
color_wizard = (95, 0, 128)			#libtcod.darker_purple

# text colors
default_background_color = (0,0,0)
default_text_color = (255,255,255)
color_energy = (0,255,255)
color_faded_energy = (0,0,255)
color_warning = (255,127,0)
color_big_alert = (255,0,0)


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

	def __init__(self, map, background_map, player_start_x, player_start_y,  object_data = [],  nearest_points_array = [[]], center_points = [], spawn_points = [], elevators = [], room_adjacencies = []):
		self.map = map
		self.background_map = background_map
		self.object_data = object_data
		self.player_start_x = player_start_x
		self.player_start_y = player_start_y
		self.nearest_points_array = nearest_points_array
		self.center_points = center_points
		self.spawn_points = spawn_points
		self.elevators = elevators
		self.room_adjacencies = room_adjacencies

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
		self.width = w
		self.height = h

	def center(self):
		center_x = int((self.x1 + self.x2) / 2)
		center_y = int((self.y1 + self.y2) / 2)
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

	def __init__(self, door_points, spawn_points, player_authorised = False, direction = None):
		self.door_points = door_points
		self.spawn_points = spawn_points
		self.player_authorised = player_authorised
		self.time_unoccupied = 5
		self.doors_open = False
		self.doors_opening = False
		self.doors_closing = False
		self.ready_to_go_up = False
		self.direction = direction 	#direction the elevator is facing. 'up',  'down', 'left', 'right'
		self.doors = []
		for (x,y) in self.door_points:
			door = Object(x, y, '+', 'elevator door', color_axe_maniac, blocks=True, door = Elevator_Door(x,y,horizontal = False), always_visible=True) 
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


		#map to allow variation in background tiles
		background_map = [[ 0
			for y in range(max_map_height) ]
				for x in range(max_map_width) ]
	
		rooms = []
		num_rooms = 0
	
		spawn_points = []
		center_points = []
		object_data = []
		elevators = []
		room_adjacencies = []
 
	
		if dungeon_level == 0:
			#self.original_tutorial(object_data, map, center_points, nearest_points_array, rooms, num_rooms, spawn_points, elevators, room_adjacencies)
			#player_start_x = 12
			#player_start_y = 12

			max_map_height = 100
			max_map_width = 100
			map_width = 100
			map_height = 100
			#fill map with "blocked" tiles
			map = [[ Tile(True)
				for y in range(max_map_height) ]
					for x in range(max_map_width) ]
	
			nearest_points_array  = [[ None
				for y in range(max_map_height) ]
					for x in range(max_map_width) ]		


			#map to allow variation in background tiles
			background_map = [[ 0
				for y in range(max_map_height) ]
					for x in range(max_map_width) ]
			

			# return first level, either the tutorial or test room, depending
			self.first_level(object_data, map, background_map, center_points, nearest_points_array, rooms, num_rooms, spawn_points, elevators, room_adjacencies)
			# self.test_room(object_data, map, background_map, center_points, nearest_points_array, rooms, num_rooms, spawn_points, elevators, room_adjacencies)
			#self.new_tutorial(object_data, map, background_map, center_points, nearest_points_array, rooms, num_rooms, spawn_points, elevators, room_adjacencies)
			player_start_x = 11
			player_start_y = 61
			#max_map_width = lev_set.max_map_width + 1

		elif lev_set.level_type == 'arena':


			room_min_size = lev_set.room_min_size
			room_max_size = lev_set.room_max_size		
			max_map_height = lev_set.max_map_height
			max_map_width = lev_set.max_map_width

			start_ele_direction = lev_set.start_ele_direction
			start_ele_spawn = lev_set.start_ele_spawn


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
			self.create_elevator(elev1, map, spawn_points, center_points, nearest_points_array, object_data,  elevators, 'Small-Elevator-Right', background_map)
			self.create_elevator(elev2, map, spawn_points, center_points, nearest_points_array, object_data,  elevators, 'Small-Elevator-Left', background_map)
			self.create_elevator(elev3, map, spawn_points, center_points, nearest_points_array, object_data,  elevators, 'Small-Elevator-Left', background_map)
			self.create_elevator(elev4, map, spawn_points, center_points, nearest_points_array, object_data,  elevators, 'Small-Elevator-Right', background_map)
	
			for r in range((max_map_width-11-7-1)/8):
				elevtop = Rect((8*r)+9,1,4,5)
				rooms.append(elevtop)
				self.create_elevator(elevtop, map, spawn_points, center_points, nearest_points_array, object_data,  elevators, 'Small-Elevator-Down', background_map)
				elevbot = Rect((8*r)+9, max_map_height -6,4,5)
				rooms.append(elevbot)
				self.create_elevator(elevbot, map, spawn_points, center_points, nearest_points_array, object_data,  elevators, 'Small-Elevator-Up', background_map)

			


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
				if new_room.x1 < new_room.x2 - 1 and new_room.y1 < new_room.y2 - 1:
					x = randint(new_room.x1+1, new_room.x2-1)
					y = randint(new_room.y1+1, new_room.y2-1)
		
					#only place it if the tile is not already blocked
					if not self.is_occupied(x, y, map, object_data):				
						map[x][y].blocked = True
						map[x][y].block_sight = True
	

			# generate set of potential starting points for player - ideally, in an elevator facing the same direction as the one they entered, with the player in the same relative position within th elevator.
			starting_points = []
			for ele in elevators:
				if (ele.direction == start_ele_direction and start_ele_spawn is not None):
					if start_ele_spawn < len(ele.spawn_points):
						starting_points.append[ele.spawn_points[start_ele_spawn]]
			# if there are no ideal start points, just use the set of all enemy spawn points
			if len(starting_points) <= 0:
				starting_points = spawn_points

			choice = randint(0, len(starting_points)-1)
			(player_start_x, player_start_y) = starting_points[choice] 	#rooms[len(rooms)-1].center()
			(new_x, new_y) = rooms[len(rooms)-1].center()
			#object_data.append(Object_Datum(new_x,new_y, 'stairs'))
			object_data.append(Object_Datum(new_x,new_y, 'security drone'))


			if lev_set.boss is not None:
				#boss_monster = create_monster(new_x,new_y,lev_set.boss)
				#objects.append(boss_monster)
				object_data.append(Object_Datum(new_x,new_y, 'boss', lev_set.boss))		


#		elif dungeon_level >= 1 and dungeon_level <= 10:
		#elif 1 == 0:		#temporarily cutting this out... let's see what happens		
		
		#THIS BIT IS WHERE MOST LEVELS GET THEIR DATA FROM
		# GOODNESS KNOWS WHAT THE OTHER CASES ARE FOR
		elif lev_set.level_type == 'modern' or lev_set.level_type == 'classic':

			self.fill_a_rectangle(map, background_map, lev_set, dungeon_level, object_data, rooms, nearest_points_array, center_points, spawn_points, elevators, room_adjacencies)
			
			#print("super duper length " + str(len(room_adjacencies)) + "but also " + str(len(elevators)))

#			new_room = Rect(20,20,5,5)
#			self.create_room(new_room, map, center_points, nearest_points_array)
#			rooms.append(new_room)
#			self.place_objects(new_room, lev_set, map, object_data, dungeon_level)
#			self.recursively_generate(map, lev_set, dungeon_level, object_data, rooms, room_range, new_room, nearest_points_array, center_points)



			start_ele_direction = lev_set.start_ele_direction
			start_ele_spawn = lev_set.start_ele_spawn

			# generate set of potential starting points for player - ideally, in an elevator facing the same direction as the one they entered, with the player in the same relative position within th elevator.
			starting_points = []
			for ele in elevators:
				if (ele.direction == start_ele_direction and start_ele_spawn is not None):
					if start_ele_spawn < len(ele.spawn_points):
						starting_points.append(ele.spawn_points[start_ele_spawn])
			# if there are no ideal start points, just use the set of all enemy spawn points
			if len(starting_points) <= 0:
				starting_points = spawn_points

			choice = randint(0, len(starting_points)-1)
			(player_start_x, player_start_y) = starting_points[choice] 	#rooms[len(rooms)-1].center()
			(new_x, new_y) = rooms[4].center()

			#if lev_set.final_level is not True:
			#	object_data.append(Object_Datum(new_x,new_y, 'security drone'))


			if lev_set.boss is not None:
				#boss_monster = create_monster(new_x,new_y,lev_set.boss)
				#objects.append(boss_monster)
				object_data.append(Object_Datum(new_x,new_y, 'boss', lev_set.boss))


			# Add security drones to rooms, as per the level settings
			self.add_drones_and_keys(map, lev_set, dungeon_level, object_data, rooms, elevators)
	

		#	# Add shrines to rooms, as per level settings
			self.add_shrines(map, lev_set, dungeon_level, object_data, rooms, elevators)
	
		#	# Add enemies to rooms
			self.add_guards(map, lev_set, dungeon_level, object_data, rooms, elevators)

		#	# Add other objects to rooms,
			self.add_objects(map, lev_set, dungeon_level, object_data, rooms, elevators)
			
			
		#	self.place_objects(new_room, lev_set, map, object_data, dungeon_level)


		# TIME TO COMMENT OUT A BUNCH OF CODE
#		#elif lev_set.level_type == 'modern':
#		#elif lev_set.level_type == 'classic':
#		elif 1 == 0:
#			# okay, maybe let's get some larger rooms going that can overlap?
#	
#			# so for now, this is the code for classic mode, with the code for checking room overlaps removed
#			for r in range(room_range):
#				#random width and height
#				w = randint(room_min_size, room_max_size)
#				h = randint(room_min_size, room_max_size)
#				#random position without going out of the boundaries of the map
#				x = randint(0, map_width - w - 1)
#				y = randint(0, map_height - h - 1)
#		
#				#"Rect" class makes rectangles easier to work with
#				new_room = Rect(x, y, w, h)
#		 
#	
#		
#				if True:
#					#this means there are no intersections, so this room is valid
#		
#					#"paint" it to the map's tiles
#					self.create_room(new_room, map, center_points, nearest_points_array)
#					#add some contents to this room, such as monsters
#					self.place_objects(new_room, lev_set, map, object_data, dungeon_level)
#		
#					#center coordinates of new room, will be useful later
#					(new_x, new_y) = new_room.center()
#					if num_rooms == 0:
#						#this is the first room, where the player starts at
#						player_start_x = new_x
#						player_start_y = new_y
#					else:
#						#all rooms after the first:
#						#connect it to the previous room with a tunnel
#		
#						#center coordinates of previous room
#						(prev_x, prev_y) = rooms[num_rooms-1].center()
#		
#						#draw a coin (random number that is either 0 or 1)
#						if randint(0, 1) == 1:
#							#first move horizontally, then vertically
#							self.create_h_tunnel(prev_x, new_x, prev_y, map, nearest_points_array, center_points)
#							self.create_v_tunnel(new_y, prev_y, new_x, map, nearest_points_array, center_points)
#						else:
#							#first move vertically, then horizontally
#							self.create_v_tunnel(prev_y, new_y, prev_x, map, nearest_points_array, center_points)
#							self.create_h_tunnel(new_x, prev_x, new_y, map, nearest_points_array, center_points)
#		
#					#finally, append the new room to the list
#					rooms.append(new_room)
#					num_rooms += 1
#	
#			#create_segment()
#
#			
#			#create stairs at the center of the last room
#			#stairs = Object(new_x, new_y, '<', 'stairs', libtcod.white, always_visible=True)
#			#objects.append(stairs)
#			#stairs.send_to_back()  #so it's drawn below the monsters
#			
#			#object_data.append(Object_Datum(new_x,new_y,'stairs'))
#			if lev_set.final_level is not True:
#				object_data.append(Object_Datum(new_x,new_y, 'security drone'))
#
#		
#			if lev_set.boss is not None:
#				#boss_monster = create_monster(new_x,new_y,lev_set.boss)
#				#objects.append(boss_monster)
#				object_data.append(Object_Datum(new_x,new_y, 'boss', lev_set.boss))
#	
#	
#			# now, append some elevators?
#			num_norm_rooms = num_rooms
#			elev1 = Rect(5, 5, 4, 4)
#			elev2 = Rect(max_map_width-5, 5, 4, 4)
#			elev3 = Rect(max_map_width-5, max_map_height -5, 4, 4)
#			elev4 = Rect(5, max_map_height - 5, 4, 4)
#			self.create_elevator(elev1, map, spawn_points, center_points, nearest_points_array, elevators, object_data, background_map)
#			self.create_elevator(elev2, map, spawn_points, center_points, nearest_points_array, elevators, object_data, background_map)
#			self.create_elevator(elev3, map, spawn_points, center_points, nearest_points_array, elevators, object_data, background_map)
#			self.create_elevator(elev4, map, spawn_points, center_points, nearest_points_array, elevators, object_data, background_map)
#			(new_x, new_y) = elev1.center()
#			num = randint(0, num_norm_rooms-1)
#			(prev_x, prev_y) = rooms[num].center()
#				#draw a coin (random number that is either 0 or 1)
#			if randint(0, 1) == 1:
#				#first move horizontally, then vertically
#				self.create_h_tunnel(prev_x, new_x, prev_y, map, nearest_points_array, center_points)
#				self.create_v_tunnel(new_y, prev_y, new_x, map, nearest_points_array, center_points)
#			else:
#				#first move vertically, then horizontally
#				self.create_v_tunnel(prev_y, new_y, prev_x, map, nearest_points_array, center_points)
#				self.create_h_tunnel(new_x, prev_x, new_y, map, nearest_points_array, center_points)
#			(new_x, new_y) = elev2.center()
#			num = randint(0, num_norm_rooms-1)
#			(prev_x, prev_y) = rooms[num].center()
#				#draw a coin (random number that is either 0 or 1)
#			if randint(0, 1) == 1:
#				#first move horizontally, then vertically
#				self.create_h_tunnel(prev_x, new_x, prev_y, map, nearest_points_array, center_points)
#				self.create_v_tunnel(new_y, prev_y, new_x, map, nearest_points_array, center_points)
#			else:
#				#first move vertically, then horizontally
#				self.create_v_tunnel(prev_y, new_y, prev_x, map, nearest_points_array, center_points)
#				self.create_h_tunnel(new_x, prev_x, new_y, map, nearest_points_array, center_points)
#			(new_x, new_y) = elev3.center()
#			num = randint(0, num_norm_rooms-1)
#			(prev_x, prev_y) = rooms[num].center()
#				#draw a coin (random number that is either 0 or 1)
#			if randint(0, 1) == 1:
#				#first move horizontally, then vertically
#				self.create_h_tunnel(prev_x, new_x, prev_y, map, nearest_points_array, center_points)
#				self.create_v_tunnel(prev_y, new_y, new_x, map, nearest_points_array, center_points)
#			else:
#				#first move vertically, then horizontally
#				self.create_v_tunnel(prev_y, new_y, prev_x, map, nearest_points_array, center_points)
#				self.create_h_tunnel(new_x, prev_x, new_y, map, nearest_points_array, center_points)
#			(new_x, new_y) = elev4.center()
#			num = randint(0, num_norm_rooms-1)
#			(prev_x, prev_y) = rooms[num].center()
#				#draw a coin (random number that is either 0 or 1)
#			if randint(0, 1) == 1:
#				#first move horizontally, then vertically
#				self.create_h_tunnel(prev_x, new_x, prev_y, map, nearest_points_array, center_points)
#				self.create_v_tunnel(new_y, prev_y, new_x, map, nearest_points_array, center_points)
#			else:
#				#first move vertically, then horizontally
#				self.create_v_tunnel(prev_y, new_y, prev_x, map, nearest_points_array, center_points)
#				self.create_h_tunnel(new_x, prev_x, new_y, map, nearest_points_array, center_points)
#				# ok that was a bunch of code to append some elevators! Let's see how it goes
#	
	# WOOO! That was one bunch of level generation code that Iwasn't using. Here's another!
	
#		else:		# 'classic' mode
#	
#			for r in range(room_range):
#				#random width and height
#				w = randint(room_min_size, room_max_size)
#				h = randint(room_min_size, room_max_size)
#				#random position without going out of the boundaries of the map
#				x = randint(0, map_width - w - 1)
#				y = randint(0, map_height - h - 1)
#		
#				#"Rect" class makes rectangles easier to work with
#				new_room = Rect(x, y, w, h)
#		 
#				#run through the other rooms and see if they intersect with this one
#				failed = False
#				for other_room in rooms:
#					if new_room.intersect(other_room):
#						failed = True
#						break
#		
#				if not failed:
#					#this means there are no intersections, so this room is valid
#		
#					#"paint" it to the map's tiles
#					self.create_room(new_room, map, center_points, nearest_points_array)
#					#add some contents to this room, such as monsters
#					self.place_objects(new_room, lev_set, map, object_data, dungeon_level)
#		
#					#center coordinates of new room, will be useful later
#					(new_x, new_y) = new_room.center()
#					if num_rooms == 0:
#						#this is the first room, where the player starts at
#						player_start_x = new_x
#						player_start_y = new_y
#					else:
#						#all rooms after the first:
#						#connect it to the previous room with a tunnel
#		
#						#center coordinates of previous room
#						(prev_x, prev_y) = rooms[num_rooms-1].center()
#		
#						#draw a coin (random number that is either 0 or 1)
#						if randint(0, 1) == 1:
#							#first move horizontally, then vertically
#							self.create_h_tunnel(prev_x, new_x, prev_y, map, nearest_points_array, center_points)
#							self.create_v_tunnel(new_y, prev_y, new_x, map, nearest_points_array, center_points)
#						else:
#							#first move vertically, then horizontally
#							self.create_v_tunnel(prev_y, new_y, prev_x, map, nearest_points_array, center_points)
#							self.create_h_tunnel(new_x, prev_x, new_y, map, nearest_points_array, center_points)
#		
#					#finally, append the new room to the list
#					rooms.append(new_room)
#					num_rooms += 1
#		
#			#create stairs at the center of the last room
#			#stairs = Object(new_x, new_y, '<', 'stairs', libtcod.white, always_visible=True)
#			#objects.append(stairs)
#			#stairs.send_to_back()  #so it's drawn below the monsters
#			#object_data.append(Object_Datum(new_x,new_y, 'stairs'))
#			
#			if lev_set.boss is not None:
#				#boss_monster = create_monster(new_x,new_y,lev_set.boss)
#				#objects.append(boss_monster)
#				object_data.append(Object_Datum(new_x,new_y, 'boss', lev_set.boss))
#
	# Hooray for commenting out things!


		# Here is a thing in a terrible place: delete water that is next to security drones
		# don't do it in waterlogged levels though?  and hopefully the tridentors will help you take them out if needs be?
		if dungeon_level > 0 and 'waterlogged' not in lev_set.effects:
			water_removal_list = []
			for od1 in object_data:
				for od2 in object_data:
					if od2.x >= od1.x-1 and od2.x <= od1.x + 1 and od2.y >= od1.y-1 and od2.y <= od1.y+1 and od2.name == 'water' and od1.name == 'security drone':
						water_removal_list.append(od2)
			for od in water_removal_list:
				print("REMOVING WATER")	
				try:	
					object_data.remove(od)
				
				except ValueError:
					print('')

		return Level_Data(map, background_map, player_start_x, player_start_y, object_data, nearest_points_array, center_points, spawn_points, elevators, room_adjacencies)

			
	#	process_nearest_center_points()
	
	#	calculate_nav_data()	


	def create_room(self,room, map, center_points, nearest_points_array, background_map = None):
		#global map, spawn_points, center_points, nearest_points_array


		(new_x, new_y) = room.center()
		center_points.append((new_x,new_y))

		#go through the tiles in the rectangle and make them passable
		for x in range(room.x1, room.x2+1):
			for y in range(room.y1, room.y2+1):
				map[x][y].blocked = False
				map[x][y].block_sight = False
				nearest_points_array[x][y] = (new_x, new_y)

		if background_map is not None :		# put a nice carpet in the middle if it's a big room
			if (room.x2 - room.x1 >4  and room.y2 - room.y1 >3) or  (room.x2 - room.x1 >3  and room.y2 - room.y1 >4):
				for x in range(room.x1, room.x2+1):
					for y in range(room.y1, room.y2+1):
						background_map[x][y] = 2
				for x in range(room.x1, room.x2+1):
					background_map[x][room.y1] = 0
					background_map[x][room.y2] = 0
				for y in range(room.y1, room.y2+1):
					background_map[room.x1][y] = 0
					background_map[room.x2][y] = 0



	def add_drones_and_keys(self, map, lev_set, dungeon_level, object_data, rooms, elevators):
		# create an initial shortlist of rooms where one could place security drone
		# for now, theshortlist is just anything that's not an elevator. This should probabl change later.
		number_sec_drones = lev_set.number_sec_drones
		number_keys = lev_set.number_keys

		initial_shortlist = []
		for room in rooms:
			# Add room to shortlist if it doesn't intersect an elevator
			# This is a bit of a hacky workaround but whatever.
			room_near_elevator = False
			for ele in elevators:
				for (x,y) in ele.spawn_points:
					#check this spawn point is not near the room.
					near_room = True
					if x < room.x1-1 or x > room.x2 + 1 or y < room.y1 - 1 or y > room.y2 + 1:
						near_room = False
					if near_room:
						room_near_elevator = True
			if room_near_elevator == False:
				initial_shortlist.append(room)
		current_shortlist = initial_shortlist
		
		number_affected_rooms = max(number_sec_drones, number_keys)

		for i in range(0, number_affected_rooms):		
			# choose a room at random, stick a security drone in, (update) DO NOTstrike it off the shortlist
			num = randint(0, len(current_shortlist)-1)
			selected_room = current_shortlist[num]


			#Decide whether we're adding a drone or a key or a drone that guards a key or a drone that drops a key.
			if i < min(number_sec_drones, number_keys):	# add drone and key
				# do a coin toss to decide if the drone guards a key or drops it
				drops_key = True
				guards_key = False
				if randint(0,1) == 0:
					drops_key = False
					guards_key = True
				# add the drone (and its key)
				self.add_security_drone(map, lev_set, dungeon_level, object_data, selected_room, drops_key, guards_key)
			elif i < number_sec_drones:	# add drone
				self.add_security_drone(map, lev_set, dungeon_level, object_data, selected_room, drops_key = False, guards_key = False)
			elif i < number_keys:		# add a key on its own
				self.add_key(map, lev_set, dungeon_level, object_data, selected_room)

			# Make it be a thing that drops keys!
			#self.add_security_drone(map, lev_set, dungeon_level, object_data, selected_room, drops_key = True, guards_key = False)
			#current_shortlist.remove(selected_room)
			# have we run out of rooms? then refresh the list, allow doubling up to happen.
			#if len(current_shortlist) == 0:
			#	current_shortlist = initial_shortlist


	# add a security systemhere. possibly holding a key, possibly guarding a key in the same room
	def add_security_drone(self, map, lev_set, dungeon_level, object_data, security_room, drops_key, guards_key):
		# new thing: place security drone randomly rather than in center of room

		sec_x = randint(security_room.x1, security_room.x2)
		sec_y = randint(security_room.y1, security_room.y2)
		#(sec_x,sec_y) = security_room.center()
		if drops_key:
			object_data.append(Object_Datum(sec_x,sec_y,'security drone', 'drops-key'))
		else: 
			object_data.append(Object_Datum(sec_x,sec_y,'security drone'))
			# Here is a terrible hack - clear water from around the security drone.

		if guards_key:
			key_x= randint(security_room.x1,security_room.x2) 
			key_y= randint(security_room.y1,security_room.y2) 
			object_data.append(Object_Datum(key_x,key_y,'key'))
			


		# commenting this out, because now that sec drones can activate if they see you for too long, it's kind of 
		# fun to stumble upon them by accident. Hopefully.
		#self.decorate_room(security_room, lev_set, map, object_data, dungeon_level,symbol = '.')


	# add an unguarded key to a room
	def add_key(self, map, lev_set, dungeon_level, object_data, key_room):

		key_x= randint(key_room.x1,key_room.x2) 
		key_y= randint(key_room.y1,key_room.y2) 
		object_data.append(Object_Datum(key_x,key_y,'key'))
	

	def add_shrines(self, map, lev_set, dungeon_level, object_data, rooms, elevators):
		# create an initial shortlist of rooms where one could place shrine
		# for now, theshortlist is just anything that's not an elevator. This should probabl change later.
		number_shrines = lev_set.number_shrines

		initial_shortlist = []
		for room in rooms:
			# Add room to shortlist if it doesn't intersect an elevator
			# This is a bit of a hacky workaround but whatever.
			room_near_elevator = False
			for ele in elevators:
				for (x,y) in ele.spawn_points:
					#check this spawn point is not near the room.
					near_room = True
					if x < room.x1-1 or x > room.x2 + 1 or y < room.y1 - 1 or y > room.y2 + 1:
						near_room = False
					if near_room:
						room_near_elevator = True
			if room_near_elevator == False:
				initial_shortlist.append(room)
		current_shortlist = initial_shortlist
		
		number_affected_rooms = number_shrines

		for i in range(0, number_affected_rooms):		
			# choose a room at random, stick a shrine in, DO strike it off the shortlist
			num = randint(0, len(current_shortlist)-1)
			selected_room = current_shortlist[num]
			self.add_shrine(map, lev_set, dungeon_level, object_data, selected_room)
			current_shortlist.remove(selected_room)
			# have we run out of rooms? then break, because I don't want to double up shrines. That'd be wierd.
			if len(current_shortlist) == 0:
				break
				#current_shortlist = initial_shortlist


	# Add a shrine to a room
	def add_shrine(self, map, lev_set, dungeon_level, object_data, shrine_room):
		(shrine_x, shrine_y) = shrine_room.center()
		object_data.append(Object_Datum(shrine_x,shrine_y, 'shrine', 'healer'))
		self.decorate_room(shrine_room, lev_set, map, object_data, dungeon_level,symbol = '+')
		# commented out for now: plant grass around the shrine
		#self.plant_grass_in_room(shrine_room, lev_set, map, object_data, shrine_x, shrine_y)
		# TODO hey I bet in future we're going to want to control what upgrades the shrines have, and what sort of distribution of upgrade types you can get


	def plant_grass_in_room(self, shrine_room, lev_set, map, object_data, shrine_x, shrine_y):
		growth_rounds = 10
		spread_prob_num= 1	# prob 1 in 2
		spread_prob_denom= 2	# prob 1 in 2
		#grass goes through 7 stages:
		# 0: no grass here
		# 1: seed planted here
		# 2: growing
		# 3: dispersing
		# 4: dispersing
		# 5: no longer dispersing
		# 6: dying (but new seeds can be planted)
		
		grass_array = [[ 0
			for y in range(shrine_room.height) ]
				for x in range(shrine_room.width) ]
		# put flowering grass at shrine center
		grass_array[shrine_x - shrine_room.x1][shrine_y - shrine_room.y1] = 3

		for round in range(growth_rounds):
			# cells in stage 0 or 6 can be seeded by adjacent cells in stage 3 or 4
			for y in range(shrine_room.height):
				for x in range(shrine_room.width):
					if grass_array[x][y] == 0 or grass_array[x][y] == 6:
						if x > 0:
							if grass_array[x-1][y] in range(3,5) and randint(1,spread_prob_denom)<= spread_prob_num:
								grass_array[x][y] = 1
						if y > 0:
							if grass_array[x][y-1] in range(3,5) and randint(1,spread_prob_denom)<= spread_prob_num:
								grass_array[x][y] = 1
						if x < shrine_room.width-1:
							if grass_array[x+1][y] in range(3,5) and randint(1,spread_prob_denom)<= spread_prob_num:
								grass_array[x][y] = 1
						if y < shrine_room.height-1:
							if grass_array[x][y+1] in range(3,5) and randint(1,spread_prob_denom)<= spread_prob_num:
								grass_array[x][y] = 1

			# now age all the grass (and kill the grass in stage 6):
			for y in range(shrine_room.height):
				for x in range(shrine_room.width):
					if  grass_array[x][y] > 0:
						 grass_array[x][y] =  grass_array[x][y] + 1
					if grass_array[x][y] > 6:
						 grass_array[x][y] = 0

		# ok now that that's all done, add grass in the places where the array says there is grass
		for y in range(shrine_room.height):
			for x in range(shrine_room.width):
				if  grass_array[x][y] > 0 and  grass_array[x][y] < 5:
					object_data.append(Object_Datum(shrine_room.x1 + x,shrine_room.y1 + y, 'grass'))




	# place some intial enemies on guard duty to rooms
	def add_guards(self, map, lev_set, dungeon_level, object_data, rooms, elevators):
		#place guards (potentially) in any room not overlapping an elevator

		initial_shortlist = []
		for room in rooms:
			# Add room to shortlist if it doesn't intersect an elevator
			# This is a bit of a hacky workaround but whatever.
			room_near_elevator = False
			for ele in elevators:
				for (x,y) in ele.spawn_points:
					#check this spawn point is not near the room.
					near_room = True
					if x < room.x1-1 or x > room.x2 + 1 or y < room.y1 - 1 or y > room.y2 + 1:
						near_room = False
					if near_room:
						room_near_elevator = True
			if room_near_elevator == False:
				self.add_guards_to_room(room, lev_set, map, object_data, dungeon_level)


	def add_guards_to_room(self, room, lev_set, map, object_data, dungeon_level):

		#each square has prob (guard_denominator/guard_numerator) of having a guard on it
		(guard_denominator, guard_numerator) = lev_set.guard_probability	
		
		# theseprobs handle the distribution of different enemy types within this level
		total_enemy_prob = lev_set.total_enemy_prob
		enemy_probabilities = lev_set.enemy_probabilities



		# Making this enemy distribution stuff a bit more complicated to allow for applying min and max's.
		# Start with an initial distribution of enemies based just on probabilities.
		# Also keep track of other spaces we could add guards.
		placement_list = []
		free_space_list = []		
		room_guard_count = 0
		for x in range(room.x1, room.x2+1):
			for y in range(room.y1, room.y2+1):
				#only place it if the tile is not blocked
				if not self.is_occupied(x, y, map, object_data):

					# now roll the dice to decide if an enemy spawns here
					if randint(1,guard_numerator) <= guard_denominator:	
						# Mark this as a place we intend to add a guard
						placement_list.append((x,y))
						room_guard_count += 1
					else:
						# Mark this as a free place where we could add eneies, if we need more
						free_space_list.append((x,y))

		# Update placement_list by removing items at random if we have too many guards:
		if lev_set.max_room_monsters is not None: 
			while lev_set.max_room_monsters < room_guard_count:
				# take out random guard locations
				place_deletion_choice = randint(0, len(placement_list) - 1)
				place_to_delete = placement_list[place_deletion_choice]
				placement_list.remove(place_to_delete)
				room_guard_count -= 1


		# Upfate placement list by adding more spaces from the free space list if we don't have enough guards		
		if lev_set.min_room_monsters is not None: 
			while lev_set.min_room_monsters > room_guard_count and len(free_space_list) > 0:
				# add random guard locations
				place_addition_choice = randint(0, len(free_space_list) - 1)
				place_to_add = free_space_list[place_addition_choice]
				placement_list.append(place_to_add)
				free_space_list.remove(place_to_add)
				room_guard_count += 1

		

		# Add an enemy to each of the specified places
		for (x,y) in placement_list:
			enemy_name = 'none'
			num = randint(0, total_enemy_prob)
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


	# add misc other objects (water + fruit, currently) to rooms
	def add_objects(self, map, lev_set, dungeon_level, object_data, rooms, elevators):
		#place guards (potentially) in any room not overlapping an elevator

		initial_shortlist = []
		for room in rooms:
			# Add room to shortlist if it doesn't intersect an elevator
			# This is a bit of a hacky workaround but whatever.
			room_near_elevator = False
			for ele in elevators:
				for (x,y) in ele.spawn_points:
					#check this spawn point is not near the room.
					near_room = True
					if x < room.x1-1 or x > room.x2 + 1 or y < room.y1 - 1 or y > room.y2 + 1:
						near_room = False
					if near_room:
						room_near_elevator = True
			if room_near_elevator == False:
				self.add_objects_to_room(room, lev_set, map, object_data, dungeon_level)

	# add misc other objects (water + fruit, currently) to a room
	def add_objects_to_room(self, room, lev_set, map, object_data, dungeon_level):

		#I swear there's some uncommented code further down

		#global game_level_settings, dungeon_level, god_healer
	
		#lev_set = game_level_settings.get_setting(dungeon_level)

		#max_room_monsters = lev_set.max_room_monsters

		#choose random number of monsters
		#num_monsters = randint(0, max_room_monsters)
		

		#print('x1 ' + str(room.x1) + ', x2 ' + str(room.x2) + ',y1 ' +  str(room.y1) + ',y2 ' + str(room.y2) + ',)')

	#	for i in range(num_monsters):
	#	#for i in range(50):
	#		#choose random spot for this monster
	#		x = randint(room.x1, room.x2)
	#		y = randint(room.y1, room.y2)
	#		# x = randint(room.x1+1, room.x2-1)
	#		# y = randint(room.y1+1, room.y2-1)
	#
	#		#only place it if the tile is not blocked
	#		if not self.is_occupied(x, y, map, object_data):
	#
	#			total_enemy_prob = lev_set.total_enemy_prob
	#			enemy_probabilities = lev_set.enemy_probabilities
#
#	#			
	#
	#			enemy_name = 'none'
	#			num = randint(0, total_enemy_prob)
	#			for (name, prob) in enemy_probabilities:
	#				#print '(' + name + ',' + str(prob) + ')'
	#				if num <= prob:
	#					enemy_name = name
	#					break
	#				else:
	#					num -= prob
	#
	#			#monster = create_monster(x,y,name)
	#			#objects.append(monster)
	#			object_data.append(Object_Datum(x,y,'monster', name))
	#
	#	# on first level, in in 2 chance of a weapon appearing in a room I guess
	#	if dungeon_level == 0:
	#		num = randint(0, 2)
	#		if num == 0:
	#			x = randint(room.x1, room.x2)
	#			y = randint(room.y1, room.y2)
	#		#	x = randint(room.x1+1, room.x2-1)
	#		#	y = randint(room.y1+1, room.y2-1)
	#			#new_weapon = Object(x,y, 's', 'sword', default_weapon_color, blocks = False, weapon = True)
	#			#drop_weapon(new_weapon)
	#			#objects.append(new_weapon)
	#			#new_weapon.send_to_back()
	#			object_data.append(Object_Datum(x,y,'weapon', 'sword'))
	#		elif num == 1:
	#			x = randint(room.x1, room.x2)
	#			y = randint(room.y1, room.y2)
	#		#	x = randint(room.x1+1, room.x2-1)
	#		#	y = randint(room.y1+1, room.y2-1)
	#			#new_weapon = Object(x,y, 'f', 'sai', default_weapon_color, blocks = False, weapon = True)
	#			#drop_weapon(new_weapon)
	#			#objects.append(new_weapon)
	#			#new_weapon.send_to_back()
	#			object_data.append(Object_Datum(x,y,'weapon', 'sai'))
	#
	#	# on higher levels, maybe there are shrines? Maybe??
	#	else:
	#		num = randint(0,6)
	#		if num == 0:
	#			(shrine_x, shrine_y) = room.center()
	#			#new_shrine = Object(shrine_x, shrine_y, '&', 'shrine to ' + god_healer.name, default_altar_color, blocks=Fa"lse, shrine= Shrine(god_healer), always_visible=True) 		
	#			#objects.append(new_shrine)
	#			#new_shrine.send_to_back()
	#			object_data.append(Object_Datum(shrine_x,shrine_y, 'shrine', 'healer'))
	#			self.decorate_room(room, lev_set, map, object_data, dungeon_level,symbol = '+')
	##	# or maybe security drones?
	#		elif num == 1:
	#			if lev_set.final_level is not True:	#don't have sec drones on final levels?
	#				keyval = randint(0,4)  #maybe drop a key
	#				if keyval == 0:
	#					self.add_security_drone(map, lev_set, dungeon_level, object_data, room, True)
	#				else:
	#					self.add_security_drone(map, lev_set, dungeon_level, object_data, room, False)
	#			
	#				#chance of key dropping nearby?
	#				keyval = randint(0,2)  #maybe drop a key
	#				if keyval == 0:
	#					(sec_x,sec_y) = room.center()
	#					xval= randint(room.x1,room.x2) 
	#					yval= randint(room.y1,room.y2) 
	#					object_data.append(Object_Datum(xval,yval,'key'))
	#					#TODO Make the code actually drop the key in a random place in the room.
	#
	#				#else:
	#				#	(sec_x,sec_y) = room.center()
	#				#	xval= randint(room.x1,room.x2) 
	#				#	yval= randint(room.y1,room.y2) 
	#				#	object_data.append(Object_Datum(xval,yval,'water'))


			# Maybe let's put some water in the room? 

			# If level is waterlogged, add lots of water
			if 'waterlogged' in lev_set.effects:
				num = randint(0,4)
				if num == 0:
					#Put a big puddle somewhere random in the  room!
					rad = randint(1,max(math.fabs(room.x2 - room.x1),math.fabs(room.y2 - room.y1)))
					cent_x = randint (room.x1, room.x2+1)
					cent_y = randint (room.y1, room.y2+1)
					
					for x in range(room.x1, room.x2+1):
						for y in range(room.y1, room.y2+1):
							if math.fabs(x - cent_x) +math.fabs(y-cent_y) <= rad:
							#if math.sqrt((x-cent_x) ** 2 + (y - cent_y) ** 2) <= rad:
								object_data.append(Object_Datum(x,y, 'water'))
	
					## flood the whole room! 
				elif num == 1:
					for x in range(room.x1, room.x2+1):
						for y in range(room.y1, room.y2+1):
							object_data.append(Object_Datum(x,y, 'water'))
							object_data.append(Object_Datum(x,y, 'water'))
				elif num == 2:
					#flood half the room?
					for x in range(room.x1, room.x2+1):
						for y in range(room.y1, room.y2+1):
							cointoss = randint(0, 1)
							if cointoss == 0:
								object_data.append(Object_Datum(x,y, 'water'))



			# If level is not waterlogged, add some water
			else:
				num = randint(0,6)
				if num == 0:
					#Put a medium puddle in the  room!
					rad = randint(1,3)
					(cent_x, cent_y) = room.center()
					
					for x in range(room.x1, room.x2+1):
						for y in range(room.y1, room.y2+1):
							if math.fabs(x - cent_x) +math.fabs(y-cent_y) <= rad:
							#if math.sqrt((x-cent_x) ** 2 + (y - cent_y) ** 2) <= rad:
								object_data.append(Object_Datum(x,y, 'water'))
	
					## flood the whole room! 
					#for x in range(room.x1, room.x2+1):
					#	for y in range(room.y1, room.y2+1):
					#		object_data.append(Object_Datum(x,y, 'water'))
					#		object_data.append(Object_Datum(x,y, 'water'))
				elif num == 1:
					#flood half the room?
					for x in range(room.x1, room.x2+1):
						for y in range(room.y1, room.y2+1):
							cointoss = randint(0, 1)
							if cointoss == 0:
								object_data.append(Object_Datum(x,y, 'water'))
	
			# Let's also plant plants! In every room, for now.
			if room.x1 < room.x2 -1 and room.y1 < room.y2 - 1:
				x = randint(room.x1+1, room.x2-1)
				y = randint(room.y1+1, room.y2-1)
				object_data.append(Object_Datum(x,y,'plant', 'tulip'))



			#And let's also add some honest to god trees in the corners! Maybe
			# Only add trees in big rooms
			if room.x2 - room.x1 > 2 and room.y2 - room.y1 > 2:
				room_corners = [(room.x1,room.y1),(room.x1,room.y2),(room.x2,room.y1),(room.x2,room.y2)]
				for (x,y) in room_corners:
					if not self.is_occupied(x,y,map, object_data):
						# see if we are in an actual corner, i.e. exactly one vertical neighbor blocked, exactly one horizontal neighbor blocked
						try:
							if ((map[x-1][y].blocked and not  map[x+1][y].blocked)or(not map[x-1][y].blocked and map[x+1][y].blocked)) and ((map[x][y-1].blocked and not  map[x][y+1].blocked)or(not map[x][y-1].blocked and map[x][y+1].blocked)) :
								# Finally, toss a coin to see if we should actually put a tree here.
								if randint(0,1) == 1:
									object_data.append(Object_Datum(x,y, 'tree'))
	
						except IndexError:		#todo: check that this is the right thing to catch...
							print('')		


			# Aaaaaaaand some faeries? this probbably shouldn't go here	
			rando_choice = randint(0,10)
			if rando_choice == 0:
				faerie_x= randint(room.x1,room.x2) 
				faerie_y= randint(room.y1,room.y2) 
				if not self.is_occupied(faerie_x,faerie_y,map, object_data):
					object_data.append(Object_Datum(faerie_x,faerie_y,'monster', 'faerie'))		
				
			elif rando_choice <= 5:  # rando_choice == 1:
				firepit_x= randint(room.x1,room.x2) 
				firepit_y= randint(room.y1,room.y2) 
				if not self.is_occupied(firepit_x,firepit_y,map, object_data):
					object_data.append(Object_Datum(firepit_x,firepit_y,'firepit'))	
			else:  # rando_choice == 1:
				fire_x= randint(room.x1,room.x2) 
				fire_y= randint(room.y1,room.y2) 
				if not self.is_occupied(fire_x,fire_y,map, object_data):
					object_data.append(Object_Datum(fire_x,fire_y,'fire'))	






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
			if randint(0, 1) == 1:
				do_doors = True
			else:
				do_doors = False



		half_width = int((width-1)/2)
		# okay let's think about this. First... are they horizontally aligned?
		if max(room1.x1, room2.x1)+half_width < min(room1.x2, room2.x2 - half_width):
			#horitontally aligned!
			jx = randint(max(room1.x1, room2.x1)+half_width, min(room1.x2, room2.x2)-half_width-1)
			jy = int((max(room1.y1, room2.y1) + min(room1.y2, room2.y2))/2)
		#	print 'horiz align (' + str(jx) + ', ' + str(jy) + ')'
			self.create_half_corridor(room1, jx, jy, map, center_points,  nearest_points_array, object_data, do_doors)
			self.create_half_corridor(room2, jx, jy, map, center_points,  nearest_points_array, object_data, do_doors)
		elif max(room1.y1, room2.y1)+half_width < min(room1.y2, room2.y2) - half_width:
			#vertically aligned!
			jy = randint(max(room1.y1, room2.y1)+half_width, min(room1.y2, room2.y2)-half_width-1)
			jx = int((max(room1.x1, room2.x1) + min(room1.x2, room2.x2))/2)
		#	print 'vert align (' + str(jx) + ', ' + str(jy) + ')'
			self.create_half_corridor(room1, jx, jy, map, center_points,  nearest_points_array, object_data, do_doors)
			self.create_half_corridor(room2, jx, jy, map, center_points,  nearest_points_array, object_data, do_doors)
		else:
			# neither! we're gonna have to go round some corners.	
			if randint(0, 1) == 1:
				# go vertical and then horizontal
				jx = randint(room1.x1, room1.x2)
				jy = randint(room2.y1, room2.y2)
			else: 
				# go horizontal and then vertical
				jx = randint(room2.x1, room2.x2)
				jy = randint(room1.y1, room1.y2)
		#	print 'neith align (' + str(jx) + ', ' + str(jy) + ')'
			self.create_half_corridor(room1, jx, jy, map, center_points,  nearest_points_array, object_data, do_doors)
			self.create_half_corridor(room2, jx, jy, map, center_points,  nearest_points_array, object_data, do_doors)


	def create_half_corridor(self, room1, jx, jy, map, center_points,  nearest_points_array, object_data, do_doors = False,  width = 3,):
		if nearest_points_array[jx][jy] is None:
			center_points.append((jx,jy))
		half_width = int((width-1)/2)
	
		#door stuff
		#if doors_on == True:
		#	do_doors = True
		#elif doors_off == True:
		#	do_doors = False
		#else:
		#	if randint(0, 1) == 1:
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
	


	def create_elevator(self, elevator, map, spawn_points, center_points, nearest_points_array, object_data, elevators, elevator_type = 'Small-Elevator-Right', background_map = None, easy_elevator = False):
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
		direction = None
		if elevator_type == 'Small-Elevator-Left':
			seg_map =      [[5,5,1,1,1],
					[5,0,3,4,4],
					[5,0,3,4,4],
					[5,5,1,1,1]]
			ele_direction = 'left'
		elif elevator_type == 'Small-Elevator-Right':
			seg_map =      [[1,1,1,5,5],
					[4,4,3,0,5],
					[4,4,3,0,5],
					[1,1,1,5,5]]
			ele_direction= 'right'
		elif elevator_type == 'Small-Elevator-Down':
			seg_map =      [[1,4,4,1],
					[1,4,4,1],
					[1,3,3,1],
					[0,5,5,0],
					[0,5,5,0]]
			ele_direction = 'down'
		elif elevator_type == 'Small-Elevator-Up':
			seg_map =      [[0,5,5,0],
					[0,5,5,0],
					[1,3,3,1],
					[1,4,4,1],
					[1,4,4,1]]
			ele_direction = 'up'
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
				elif (seg_map[y][x] == 5):  # and background_map is not None):
					#background_map[elevator.x1 + x][elevator.y1 + y] = 2
					object_data.append(Object_Datum(elevator.x1 + x,elevator.y1 + y, 'decoration', '\''))

		new_elevator = Elevator(door_points, local_spawn_points, player_authorised = easy_elevator, direction = ele_direction)
		#print "elevatooooooooR"
		elevators.append(new_elevator)

			

	#	elevator_segment = self.create_segment(code=elevator_type)
	#	self.append_segment(map, elevator_segment, elevator.x1, elevator.y1, object_data)
#	def append_segment(self, map, segment, x_offset, y_offset, object_data):
#	def create_segment(self, code = None):




	def append_segment(self, map, background_map, segment, x_offset, y_offset, object_data):
		map_segment = segment.seg_map
		for y in range (0, len(map_segment)):
			for x in range (0, len(map_segment[y])):
				if map_segment[y][x] == 0:
					map[x + x_offset][y + y_offset].blocked = False
					map[x + x_offset][y + y_offset].block_sight = False
				elif map_segment[y][x] == 1:
					map[x + x_offset][y + y_offset].blocked = True
					map[x + x_offset][y + y_offset].block_sight = True
				else: 		#for now, other options are treated as empty space
					map[x + x_offset][y + y_offset].blocked = False
					map[x + x_offset][y + y_offset].block_sight = False
				if map_segment[y][x] == 1:
					background_map[x + x_offset][y + y_offset] = 0  # default to 'default color' for walls, just in case
				else:
					background_map[x + x_offset][y + y_offset] = map_segment[y][x]
		for od in segment.seg_data:
			object_data.append(Object_Datum(od.x + x_offset, od.y + y_offset, od.name, od.info, od.more_info))



			
	def create_segment(self, seg_map = [[]], code = None):
		seg_data = []

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
					[0,0,0,0,0,0,0],
					[1,0,1,0,1,0,1],
					[1,B,1,B,1,B,1]]


		elif code == 'Tut-Test':
			R = Object_Name('monster','rook')
			S = Object_Name('monster','security drone')
			D = Object_Name('door', 'vertical')
			seg_map =      [[0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1],
					[0,0,0,0,0,0,1,0,0,0,1,1,1,1,1,1],
					[0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0],
					[0,0,0,0,0,S,0,0,0,0,D,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
					[0,0,1,0,0,0,0,1,0,0,1,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1],
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

		elif code == 'Ominous-Statues':
			A = Object_Name('monster', 'strawman')
			#B = Object_Name('strawman', 'sai', 'w')
			#M = Object_Name('message', 'Good lord it\'s some sort of message on the floor!!!')
			seg_map =      [[0,0,0,0,0,0,0,0,0,0,0,0],
					[0,A,0,0,A,0,0,A,0,0,A,0],
					[0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0],
					[0,A,0,0,A,0,0,A,0,0,A,0],
					[0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0],
					[0,A,0,0,A,0,0,A,0,0,A,0],
					[0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0]]


		elif seg_map == [[]]:
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
				obname_is_number = False
				try:
					z = int(str(obname))
					obname_is_number = True
				except ValueError:
					obname_is_number = False
				if not obname_is_number:
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
			new_w =  randint(room_min_size, room_max_size)
			new_h = randint(room_min_size, room_max_size)

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
				number_rooms = randint(1, len(room_shortlist))

				for i in range(1, number_rooms+1):
					#print str(number_rooms) + ' - ' + str(i)
					choice = randint(0, len(room_shortlist)-1)

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
	def fill_a_rectangle(self, map, background_map,  lev_set, dungeon_level, object_data, rooms, nearest_points_array, center_points, spawn_points, elevators, adjacency):




#		room_min_size = lev_set.room_min_size
#		room_max_size = lev_set.room_max_size		
		max_map_height = lev_set.max_map_height
		max_map_width = lev_set.max_map_width

		# Update: room max / min sizes are based on dice from level settings??

		(a,b) = lev_set.room_size_first_dice
		(c,d) = lev_set.room_size_second_dice
		room_min_size = a + c
		room_max_size = b + d	


		max_dist_between_rooms = 6



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

		self.create_elevator(elev1, map, spawn_points, center_points, nearest_points_array, object_data,  elevators, 'Small-Elevator-Right', background_map)
		self.create_elevator(elev2, map, spawn_points, center_points, nearest_points_array, object_data,  elevators, 'Small-Elevator-Left', background_map)
		self.create_elevator(elev3, map, spawn_points, center_points, nearest_points_array, object_data,  elevators, 'Small-Elevator-Left', background_map)
		self.create_elevator(elev4, map, spawn_points, center_points, nearest_points_array, object_data,  elevators, 'Small-Elevator-Right', background_map)


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
			choice = randint(0, len(maximal_potential_rooms)-1)
			temp_new_room = maximal_potential_rooms[choice]

			# Ok this is scary, but for the first time in a long time I'm going to change something about the level generation.
			# Previously: always take a maximum room, with each side possibly "trimmed".

			# Now: choose room size according to a distribution, then fit it in somewhere in this "maximal" box.
			#preferred_room_height = randint(4, room_max_size)	# todo: actually make this a 2 dice kind of distribution
			#preferred_room_width = randint(4, room_max_size)	# todo: actually make this a 2 dice kind of distribution
	

			(a,b) = lev_set.room_size_first_dice
			(c,d) = lev_set.room_size_second_dice
			preferred_room_height = randint(a, b) + randint(c,d)	
			preferred_room_width =  randint(a, b) + randint(c,d)	



			# If room height or width is larger than the currently allowed size, shrink them.
			if preferred_room_width > temp_new_room.x2-temp_new_room.x1:
				preferred_room_width = temp_new_room.x2-temp_new_room.x1
			if preferred_room_height > temp_new_room.y2-temp_new_room.y1:
				preferred_room_height = temp_new_room.y2-temp_new_room.y1
			# Now position the room at a random position that fits within this box  (i.e. choose starting x and starting y independently at random from the options that will fit))
			# preferred_room_x1 = randint(temp_new_room.x1, temp_new_room.x2 - preferred_room_width)
			# preferred_room_y1 = randint(temp_new_room.y1, temp_new_room.y2 - preferred_room_height)

			# Update: make the room be in one corner of the possibility box.  (hopefully this will mitigate narrow rooms?)

			preferred_room_x1 = temp_new_room.x1
			if randint(0,1) == 0:
				preferred_room_x1 = temp_new_room.x2 - preferred_room_width
			preferred_room_y1 = temp_new_room.y1
			if randint(0,1) == 0:
				preferred_room_y1 = temp_new_room.y2 - preferred_room_height

			new_room = Rect(preferred_room_x1, preferred_room_y1,  preferred_room_width, preferred_room_height)

			# Former "maximal with trimmed sides" code below:
#
#			# for variety, vary the room size a little 
#			# I am cheating and just randomly trimming the edges.
#			# only trim if the room isn't too small already though
#			if temp_new_room.x2-temp_new_room.x1 < 4:
#				trim_left = 0
#				trim_right = 0
#			else:
#				trim_left = randint(0, 1)
#				trim_right = randint(0, 1)
#			if temp_new_room.y2-temp_new_room.y1 < 4:
#				trim_top = 0
#				trim_bottom = 0
#			else :
#				trim_top = randint(0, 1)
#				trim_bottom = randint(0, 1)
#			new_room = Rect(temp_new_room.x1+trim_left, temp_new_room.y1+trim_top, temp_new_room.x2-temp_new_room.x1+1-trim_left-trim_right, temp_new_room.y2-temp_new_room.y1+1-trim_top-trim_bottom)
			#TODO: if room is close to the border, move it along.








			#Put this new room into the map
			self.create_room(new_room, map, center_points, nearest_points_array, background_map = background_map)
			rooms.append(new_room)
			#self.place_objects(new_room, lev_set, map, object_data, dungeon_level)
		
			# decide whether or not this room has doors.
			# Door probability is based on level settings.
			# Don't require doors if it's a narrow room (hopefully this leads to more "windy corridors" ?
			if new_room.width > 3 and new_room.height > 3:
				(doorNumerator, doorDenominator) = lev_set.door_probability
				if randint(1, doorDenominator) <= doorNumerator:
					doorhavers.append(True)
				else:
					doorhavers.append(False)
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


			# here's an extra thing - only pass rooms if they're bigger than a certain size?
			long_list = new_maximal_potential_rooms
			new_maximal_potential_rooms = []
			long_len = len(long_list)
			for i in range(0, long_len):
				if long_list[i].width >= 3 and  long_list[i].height >= 3: # TODO: make minimum room size be a settable thing
					new_maximal_potential_rooms.append(long_list[i])				


			# do final update of the maximal potential rooms list.
			maximal_potential_rooms = new_maximal_potential_rooms

		# Ok all the room creation has been done! But what's this? There are no doors or corridors! You can't actually get from one room to another! So ok let's fix that.
		# This should include joining up the elevators to things. Let's see...

		# The process below will mostly join everything up. But once in a blue moon you get a tiny room that's isolated from the rest.
		# So to get round this, we're going to do some connectivity checking.
		# And also list adjacencies while we're at it, because that will become useful later!
		connectivity = []	#2d matrix saying which rooms are connected to each other. Initally, rooms only connected to themselves.
		#adjacency = []		#array of sets listing the nieghbors of each room. Initially, nothing has any neighbors.
		for i in range(0, len(rooms)):
			temprow = []
			connectivity.append(temprow)
			tempSet = set()
			adjacency.append(tempSet)
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
					dist = max_dist_between_rooms #the max distance we can have between two rooms for them to count as 'adjacent'.
							# basically dist+1 should be just enough to squeeze a tiny room in between?
						 # TODO tie this measure to minimum room size
					#is room i to the left of room j?
					if rooms[j].x1 > rooms[i].x2 and rooms[j].x1 - rooms[i].x2 <= dist and rooms[i].y2 > rooms[j].y1 and rooms[j].y2 > rooms[i].y1:
						adjacent = True
					#	print 'left adjacency! (' + str(rooms[i].x1) + ',' + str(rooms[i].y1) + ',' + str(rooms[i].x2) + ',' + str(rooms[i].y2) + ') - (' + str(rooms[j].x1) + ',' + str(rooms[j].y1) + ',' + str(rooms[j].x2) + ',' + str(rooms[j].y2) + ')' 

			
						#create a corridor
						corridor_y = randint(max(rooms[i].y1,rooms[j].y1), min(rooms[i].y2, rooms[j].y2))
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
							if randint(0, 1) == 1:
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
						corridor_y = randint(max(rooms[i].y1,rooms[j].y1), min(rooms[i].y2, rooms[j].y2))
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
							if randint(0, 1) == 1:
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
						corridor_x = randint(max(rooms[i].x1,rooms[j].x1), min(rooms[i].x2, rooms[j].x2))
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
							if randint(0, 1) == 1:
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
						corridor_x = randint(max(rooms[i].x1,rooms[j].x1), min(rooms[i].x2, rooms[j].x2))
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
							if randint(0, 1) == 1:
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
					adjacency[i].add(j)
					adjacency[j].add(i)
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
				print("WARNING: SPAWN ROOM DISCONNECTED; EXCAVATING")

				excavate_dist = max_dist_between_rooms + 2
				excavate_points = []
				# WAIT I KNOW SOME OF THESE ARE NEGATIVE RANGES
				for x in range(rooms[i].x1+1, rooms[i].x2 -1 + 1):
					for y in range(rooms[i].y1-excavate_dist, rooms[i].y1-1 + 1):
						excavate_points.append((x,y))
					for y in range(rooms[i].y2+1,rooms[i].y2+excavate_dist +1):
						excavate_points.append((x,y))
				for y in range(rooms[i].y1 + 1, rooms[i].y2 -1 + 1):
					for x in range(rooms[i].x1-excavate_dist, rooms[i].x1-1 + 1):
						excavate_points.append((x,y))
					for x in range(rooms[i].x2+1,rooms[i].x2+excavate_dist +1):
						excavate_points.append((x,y))


				for (x,y) in excavate_points:
					if x > 0  and x < lev_set.max_map_width - 1 and y > 0 and y < lev_set.max_map_height - 1:
						map[x][y].blocked = False
						map[x][y].block_sight = False
						if nearest_points_array[x][y] is None:
							nearest_points_array[x][y] = rooms[i].center()

			else:
				print("ALL GOOD AT " + str(i))

		#print( "super length " + str(len(adjacency)))

		# now, append some elevators? Just slap bang in the middle of everything....



				#	if adjacent:
				#		self.create_corridor(rooms[i], rooms[j], map, center_points,  nearest_points_array, object_data, doors_on = False, doors_off = True, width = 1)				

		# Step 2: Join things that are adjacent. Maybe a bit selectively but to begin with let's just join everything.


	def original_tutorial(self, object_data, map, center_points, nearest_points_array, rooms, num_rooms, spawn_points, elevators, room_adjacencies):
	
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



		object_data.append(Object_Datum(44,12,'message', 'Lesson 3. Do not strike at where your enemy is! Strike at where your enemy is going to be!'))
		old_room = new_room
		new_room = Rect(50,10,7,5)
		self.create_room(new_room, map, center_points, nearest_points_array)
		(new_x, new_y) = new_room.center()
		(prev_x, prev_y) = old_room.center()
		self.append_segment(map, self.create_segment('Tut-Moving-Enemies'), 50, 10, object_data)
		self.create_h_tunnel(prev_x, new_x, prev_y, map, nearest_points_array, center_points, narrow = True)


		self.create_half_corridor(new_room, 53, 5, map, center_points, nearest_points_array, object_data)


		object_data.append(Object_Datum(53,19,'message', 'Lesson 4. A warrior is not their weapon. A warrior knows when it is time to trade their weapon for another.')) #. PS BEWARE THERE IS AN ENEMY LYING IN WAIT IN THIS ROOM'))
		#object_data.append(Object_Datum(58,19,'monster', 'swordsman'))
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

		object_data.append(Object_Datum(28,22,'message', 'The sentry in this next room holds a key. You must defeat it to move forward! But beware, it will summon aid.'))
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

		self.create_elevator(elev1, map, spawn_points, center_points, nearest_points_array, object_data,  elevators, 'Small-Elevator-Right', background_map)	
		self.create_elevator(elev2, map, spawn_points, center_points, nearest_points_array, object_data,  elevators, 'Small-Elevator-Right', background_map)




	def new_tutorial(self, object_data, map, background_map, center_points, nearest_points_array, rooms, num_rooms, spawn_points, elevators, room_adjacencies):


		# I think stuff is gonna get moved around a bunch, so here are some values you can adjust to move the whole thing
		ryofst = 5
		rxofst = 0
	
	#	new_room = Rect(10 + rxofst,10 + ryofst,5,5)
	#	self.create_room(new_room, map, center_points, nearest_points_array)

	#	(new_x, new_y) = new_room.center()
		#this is the first room, where the player starts at
	#	player_start_x = new_x
	#	player_start_y = new_y


	#	object_data.append(Object_Datum(19 +rxofst,12 + ryofst,'message', 'Lesson 1. The true warrior can strike enemies from many directions. Up, left, even diagonally.'))
	#	old_room = new_room
	#	new_room = Rect(20 + rxofst,10 + ryofst,8,5)
	#	self.create_room(new_room, map, center_points, nearest_points_array)
	#	(new_x, new_y) = new_room.center()
	#	(prev_x, prev_y) = old_room.center()
	#	self.append_segment(map, self.create_segment('Tut-Attack'), 20 + rxofst, 10 + ryofst, object_data)
	#	self.create_h_tunnel(prev_x, new_x, prev_y, map, nearest_points_array, center_points, narrow = True)
	#	#self.create_v_tunnel(new_y, prev_y, new_x, map, nearest_points_array, center_points, narrow = True)


		tut_rm_width = 8
		tut_rm_height = 8

		#new_room = Rect(tut_rm_width,tut_rm_height,7*tut_rm_width,8*tut_rm_height)
		#self.create_room(new_room, map, center_points, nearest_points_array)


		# Room 1. Welcome
		# makea new room and thereby update nearest_points_array hopefully
		new_room = Rect(tut_rm_width,7*tut_rm_height,tut_rm_width,tut_rm_height)
		self.create_room(new_room, map, center_points, nearest_points_array)
		C = Object_Name('easydoor', 'horizontal')	# a door that doesn't stick!
		D = Object_Name('message', "Welcome to the training area! Please walk through the door above to begin your training. (press #MOVEUP#)")
		E = Object_Name('monster', 'greenhorn')
		seg_map =      [[0,0,0,0,0,0,0,1],
				[1,1,1,0,1,1,1,1],
				[1,1,1,C,1,1,1,1],
				[1,0,0,0,0,0,1,1],
				[0,0,0,0,0,0,1,1],
				[0,0,0,D,0,0,1,1],
				[1,0,0,0,0,0,1,1],
				[1,0,0,0,0,0,1,1]]
		#seg_map = self.rotateSegment(seg_map)

		#old_room = new_room
#		new_room = Rect(tut_rm_width,7*tut_rm_height,tut_rm_width,tut_rm_height)
#		(new_x, new_y) = new_room.center()
#		(prev_x, prev_y) = old_room.center()
		self.append_segment(map, background_map, self.create_segment(seg_map), tut_rm_width,7*tut_rm_height, object_data)


		# Room 2. Pick up sword
	#	A = Object_Name('monster', 'strawman')
	#	B = Object_Name('weapon', 'sword')
	#	E = Object_Name('message', "Move to the weapon ahead of you and press #PICKUP# to pick it up.")	
	#	seg_map =      [[1,0,A,0,A,0,1,1],
	#			[1,1,0,0,0,1,1,1],
	#			[1,1,0,0,0,1,0,1],
	#			[1,1,0,B,0,1,0,1],
	#			[1,1,0,0,0,1,0,1],
	#			[1,1,0,E,0,1,0,1],
	#			[1,1,0,0,0,1,0,1],
	#			[1,1,1,0,1,1,1,1]]
	#	self.append_segment(map, background_map, self.create_segment(seg_map), tut_rm_width,6*tut_rm_height, object_data)


		# Room 2+3. Attack enemies
		# makea new room and thereby update nearest_points_array hopefully
		new_room = Rect( tut_rm_width,6*tut_rm_height+1,tut_rm_width,tut_rm_height-1)
		self.create_room(new_room, map, center_points, nearest_points_array)
		A = Object_Name('monster', 'strawman')	
		F = Object_Name('message', "Move next to an enemy and attack them! (#ATTCKUPLEFT#, #ATTCKUP#, #ATTCKUPRIGHT#, #ATTCKRIGHT#, #ATTCKDOWNRIGHT#, #ATTCKDOWN#, #ATTCKDOWNLEFT#, #ATTCKLEFT#)")
		B = Object_Name('weapon', 'shiv')
		E = Object_Name('message', "Move to the weapon ahead of you and press #PICKUP# to pick it up.")	
		seg_map =      [[0,0,0,0,0,0,0,1],
				[0,0,A,0,A,0,0,1],
				[0,0,0,0,0,0,0,1],
				[0,A,0,F,0,A,0,1],
				[0,0,0,B,0,0,0,1],
				[0,A,0,E,0,A,0,1],
				[0,0,0,0,0,0,0,1],
				[0,0,A,0,A,0,0,1]]
		self.append_segment(map, background_map, self.create_segment(seg_map), tut_rm_width,6*tut_rm_height, object_data)


		# Room 4. Note about energy
		# makea new room and thereby update nearest_points_array hopefully
		new_room = Rect( tut_rm_width,5*tut_rm_height+1,tut_rm_width,tut_rm_height-1)
		self.create_room(new_room, map, center_points, nearest_points_array)
		A = Object_Name('monster', 'strawman')	
		F = Object_Name('message', "Attacking uses up energy! If you are low on energy, walk around or stand still (#STANDSTILL#) to recharge.")
		seg_map =      [[1,1,1,1,1,1,1,1],
				[1,1,1,1,1,1,1,1],
				[1,1,1,1,1,1,1,1],
				[1,1,1,1,1,1,1,1],
				[1,0,0,0,1,1,1,1],
				[A,0,F,0,1,1,1,1],
				[1,0,0,0,1,1,1,1],
				[1,1,0,1,1,1,1,1]]
		seg_map = self.rotateSegment(seg_map)
		seg_map = self.rotateSegment(seg_map)
		seg_map = self.rotateSegment(seg_map)
		self.append_segment(map, background_map, self.create_segment(seg_map), tut_rm_width,5*tut_rm_height, object_data)


		# Room 5. Don't get hit.
		# makea new room and thereby update nearest_points_array hopefully
		new_room = Rect(2*tut_rm_width,5*tut_rm_height+1,tut_rm_width,tut_rm_height-1)
		self.create_room(new_room, map, center_points, nearest_points_array)
		B = Object_Name('strawman', 'sai', 'ATTCKLEFT')
		C = Object_Name('strawman', 'sai', 'ATTCKRIGHT')
		D = Object_Name('strawman', 'sai', 'ATTCKDOWNLEFT')
		F = Object_Name('message', "The secret of all combat is this: Hit your enemy without your enemy hitting you!")
		seg_map =      [[0,0,0,0,0,0,0,1],
				[0,0,0,0,0,0,D,1],
				[0,0,0,B,0,0,0,1],
				[0,0,0,0,0,0,0,1],
				[0,0,0,0,C,0,0,1],
				[F,0,0,0,0,0,0,1],
				[0,0,0,B,0,0,0,0],
				[0,0,0,0,0,0,0,1]]
		self.append_segment(map, background_map, self.create_segment(seg_map), 2*tut_rm_width,5*tut_rm_height, object_data)


		# Room 6. Move diagonally
		# makea new room and thereby update nearest_points_array hopefully
		new_room = Rect(3*tut_rm_width,5*tut_rm_height,tut_rm_width,tut_rm_height)
		self.create_room(new_room, map, center_points, nearest_points_array)
		B = Object_Name('strawman', 'sai', 'ATTCKLEFT')
		C = Object_Name('strawman', 'sai', 'ATTCKUP')
		F = Object_Name('message', "Don't forget you can move (and attack) diagonally.")
		seg_map =      [[1,1,1,1,1,1,0,0],
				[1,1,1,1,1,0,0,1],
				[1,1,1,1,0,0,1,1],
				[1,1,1,0,0,1,1,1],
				[1,1,0,0,1,1,1,1],
				[1,0,0,1,1,0,1,1],
				[F,0,1,1,1,1,1,1],
				[1,1,1,1,1,1,1,1]]
		self.append_segment(map, background_map, self.create_segment(seg_map), 3*tut_rm_width,5*tut_rm_height, object_data)


		# Room 7. Moving enemies
		# makea new room and thereby update nearest_points_array hopefully
		new_room = Rect(3*tut_rm_width,3*tut_rm_height,tut_rm_width,2*tut_rm_height)
		self.create_room(new_room, map, center_points, nearest_points_array)
		A = Object_Name('monster', 'strawman on wheels')
		F = Object_Name('message', "Do not strike at where your enemy is! Strike at where your enemy is going to be!")
		seg_map =      [[1,1,1,1,1,1,1,1],
				[0,0,0,0,0,0,0,0],
				[1,0,0,0,0,0,0,0],
				[1,0,0,0,0,0,0,0],
				[1,0,0,0,0,0,0,0],
				[1,0,0,0,0,0,0,0],
				[1,0,0,0,0,0,0,0],
				[1,0,0,0,0,0,0,0],
				[1,1,1,1,1,1,1,1],
				[1,0,0,0,0,0,0,0],
				[0,0,0,0,0,A,0,0],
				[1,0,A,0,0,0,0,0],
				[1,0,0,0,0,0,0,A],
				[1,0,0,A,0,0,0,0],
				[1,0,0,0,0,0,0,0],
				[1,0,0,0,0,0,F,0]]
		self.append_segment(map, background_map, self.create_segment(seg_map), 3*tut_rm_width,3*tut_rm_height, object_data)


		# Room 8. THE GAUNTLET
		# makea new room and thereby update nearest_points_array hopefully
		new_room = Rect(tut_rm_width,3*tut_rm_height,2*tut_rm_width,2*tut_rm_height-1)
		self.create_room(new_room, map, center_points, nearest_points_array)
		F = Object_Name('message', "Be not afraid to run into the place your enemy has just struck.")
		B = Object_Name('strawman', 'spear', 'ATTCKLEFT')
		C = Object_Name('strawman', 'spear', 'ATTCKUP')
		D = Object_Name('strawman', 'spear', 'ATTCKDOWN')
		E = Object_Name('strawman', 'spear', 'ATTCKRIGHT')
		seg_map =      [[1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1],
				[E,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0],
				[1,1,0,1,1,1,1,1,1,1,1,1,0,F,0,1],
				[E,0,0,1,1,1,1,1,1,1,1,1,0,0,0,1],
				[1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1],
				[E,0,0,1,1,D,1,1,1,1,1,1,1,0,0,B],
				[1,1,0,1,1,0,1,1,1,1,1,1,1,0,1,1],
				[1,1,0,0,0,0,1,1,1,1,1,E,0,0,1,1],
				[1,1,1,0,1,0,0,B,1,1,1,1,1,1,1,1],
				[1,1,1,C,1,0,1,1,1,1,1,1,0,0,0,1],
				[1,1,1,1,1,0,1,1,1,1,1,1,0,F,0,0],
				[1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1],
				[1,1,1,1,1,1,0,1,0,1,0,1,1,1,1,1],
				[1,1,1,1,1,1,C,1,C,1,C,1,1,1,1,1],
				[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
		self.append_segment(map, background_map, self.create_segment(seg_map), tut_rm_width,3*tut_rm_height, object_data)


		# Room 9 + 10. Fruit and jumping
		# makea new room and thereby update nearest_points_array hopefully
		new_room = Rect(tut_rm_width,tut_rm_height,2*tut_rm_width,2*tut_rm_height)
		self.create_room(new_room, map, center_points, nearest_points_array)
		A = Object_Name('strawman')
		F = Object_Name('message', "Taken wounds in battle? We recommend: fresh fruit.")
		G = Object_Name('message', "Sometimes the best thing to do is not to fight but to Jump (#JUMP#).")
		H = Object_Name('message', "Water is fine to swim in. You just can't attack while doing so.")
		W = Object_Name('water')
		B = Object_Name('plant')
		S = Object_Name('weapon', 'shiv')
		seg_map =      [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
				[1,0,0,0,0,0,0,0,0,0,0,0,0,W,W,0],
				[1,0,0,0,0,0,0,0,0,0,0,0,0,W,W,0],
				[1,0,0,0,0,0,0,0,0,0,0,0,W,W,A,0],
				[1,0,0,0,0,0,0,0,0,0,0,0,W,0,0,0],
				[1,0,0,0,0,0,0,0,0,0,0,W,W,A,0,0],
				[1,0,0,0,0,0,0,1,0,0,0,W,W,0,H,0],
				[1,A,A,A,A,A,A,1,0,0,0,0,W,A,0,0],
				[1,0,0,G,0,0,0,1,0,0,0,0,W,W,A,W],
				[1,0,0,0,B,0,0,1,0,0,0,0,0,W,W,W],
				[1,0,B,0,0,0,0,1,0,0,0,0,0,W,W,0],
				[1,0,0,0,0,B,0,1,0,0,0,0,0,0,0,0],
				[1,0,0,F,0,0,0,1,0,0,0,S,0,0,0,0],
				[1,0,0,0,B,0,0,1,0,0,0,0,0,0,0,0],
				[1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
				[1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1]]
		self.append_segment(map, background_map, self.create_segment(seg_map), tut_rm_width,tut_rm_height, object_data)



		# Room 11. Warning: swordsman
		# makea new room and thereby update nearest_points_array hopefully
		new_room = Rect(3*tut_rm_width,2*tut_rm_height,tut_rm_width,tut_rm_height)
		self.create_room(new_room, map, center_points, nearest_points_array)
		C = Object_Name('door', 'vertical')
		F = Object_Name('message', "Be warned! Ahead lies your first true foe.")
		G = Object_Name('message', "Remember your lessons. Avoid their attacks. Let them walk into yours. And good luck.")
		S = Object_Name('weapon', 'shiv')
		seg_map =      [[1,1,1,1,1,1,1,1],
				[1,1,1,1,1,1,1,1],
				[1,1,1,1,1,1,1,1],
				[1,1,1,1,1,1,1,1],
				[1,0,0,0,0,0,0,1],
				[0,0,F,0,0,G,0,C],
				[1,0,0,0,0,0,0,1],
				[1,1,1,1,1,1,1,1]]
		self.append_segment(map, background_map, self.create_segment(seg_map), 3*tut_rm_width,2*tut_rm_height, object_data)


	
		# Room 12. Swordsman battle
		# makea new room and thereby update nearest_points_array hopefully
		new_room = Rect(4*tut_rm_width, 2*tut_rm_height,2*tut_rm_width,2*tut_rm_height)
		self.create_room(new_room, map, center_points, nearest_points_array)
		C = Object_Name('monster', 'greenhorn')
		W = Object_Name('water')
		F = Object_Name('message', "Observe your next enemy's patterns closely! It is the key to defeating them.")
		S = Object_Name('weapon', 'shiv')
		seg_map =      [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
				[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[1,0,0,0,0,0,0,0,0,0,0,0,W,0,0,0],
				[1,0,0,0,0,0,0,0,0,0,0,W,W,W,0,0],
				[0,0,0,0,0,0,0,0,0,0,W,W,W,0,0,0],
				[1,0,0,0,0,0,0,0,0,0,0,W,W,W,0,0],
				[1,0,0,0,0,0,0,0,0,0,S,0,W,W,0,0],
				[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[1,0,0,0,0,0,0,0,0,0,0,0,C,0,0,0],
				[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[1,0,0,0,0,0,0,0,F,0,0,0,0,0,0,0],
				[1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1]]
		self.append_segment(map, background_map, self.create_segment(seg_map), 4*tut_rm_width, 2*tut_rm_height, object_data)

		# Room 13. Rook battle
		# makea new room and thereby update nearest_points_array hopefully
		new_room = Rect(4*tut_rm_width, 4*tut_rm_height,2*tut_rm_width,tut_rm_height)
		self.create_room(new_room, map, center_points, nearest_points_array)
		R = Object_Name('monster', 'rook')
		W = Object_Name('water')
		C = Object_Name('easydoor', 'horizontal')	# a door that doesn't stick!
		F = Object_Name('message', "This enemy has extended reach! But they cannot move or attack diagonally.")
		G = Object_Name('message', "They will try to get in line with you so they can attack. Stay out of the range of their weapon!")
		H = Object_Name('message', "Backing away from them will let you control how they approach you. Strike as they get in range!")
		I = Object_Name('message', "Weapons are heavy, and your enemy can only attack intermitently. The moment after they have attacked is an exellent time to strike!")
		seg_map =      [[1,1,1,1,1,1,1,1,C,1,1,1,1,1,1,1],
				[1,0,0,0,0,0,0,0,F,0,0,0,0,0,0,0],
				[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[1,0,0,G,0,0,0,0,0,0,0,0,R,I,0,0],
				[1,0,0,0,0,0,0,0,H,0,0,0,0,0,0,0],
				[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[1,1,1,1,1,1,1,1,C,1,1,1,1,1,1,1]]
		self.append_segment(map, background_map, self.create_segment(seg_map), 4*tut_rm_width, 4*tut_rm_height, object_data)


		# Room 14. Rook battle
		# makea new room and thereby update nearest_points_array hopefully
		new_room = Rect(4*tut_rm_width, 5*tut_rm_height,2*tut_rm_width,tut_rm_height)
		self.create_room(new_room, map, center_points, nearest_points_array)
		R = Object_Name('monster', 'bustard')
		C = Object_Name('monster', 'greenhorn')
		W = Object_Name('water')
		F = Object_Name('message', "But of course, we can't always take our enemies on one at a time. Sometimes, we get taken by surprise.")
		seg_map =      [[1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1],
				[1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0],
				[1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0],
				[1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0],
				[1,0,R,0,0,1,0,0,0,0,0,1,C,0,0,0],
				[1,0,0,0,0,0,0,0,F,0,0,0,0,0,0,0],
				[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1]]
		self.append_segment(map, background_map, self.create_segment(seg_map), 4*tut_rm_width, 5*tut_rm_height, object_data)


		# Room 15. Sneaking on security
		# makea new room and thereby update nearest_points_array hopefully
		new_room = Rect(4*tut_rm_width, 6*tut_rm_height,2*tut_rm_width,2*tut_rm_height)
		self.create_room(new_room, map, center_points, nearest_points_array)
		C = Object_Name('security drone', 'drops-key')
		W = Object_Name('water')
		F = Object_Name('message', "Security drones! Given enough time to observe you, they will sound an alarm. Try to sneak up on them before they do that.")
		G = Object_Name('message', "Sometimes though,you can't help but get spotted. The security drone will defend itself, but defeat it and the alarms will get a bit quieter.")
		B = Object_Name('plant')
		D = Object_Name('easydoor', 'horizontal')	# a door that doesn't stick!
		seg_map =      [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
				[1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
				[1,0,0,0,0,0,0,1,0,0,0,F,0,0,0,0],
				[1,0,0,0,0,0,0,1,0,0,1,0,1,1,1,1],
				[1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
				[D,0,G,0,0,0,0,1,0,0,1,0,0,0,0,1],
				[1,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1],
				[1,0,0,0,B,0,0,1,0,0,1,0,0,0,0,1],
				[1,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1],
				[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
				[1,0,0,0,0,0,0,B,0,0,1,C,0,0,0,1],
				[1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
				[1,0,S,0,0,0,0,1,1,1,1,1,1,1,1,1],
				[1,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0],
				[1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
				[1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1]]
		self.append_segment(map, background_map, self.create_segment(seg_map), 4*tut_rm_width, 6*tut_rm_height, object_data)



		# Room 16. Wailing on security
		# makea new room and thereby update nearest_points_array hopefully
		new_room = Rect(2*tut_rm_width, 6*tut_rm_height,2*tut_rm_width,2*tut_rm_height)
		self.create_room(new_room, map, center_points, nearest_points_array)
		C = Object_Name('security drone', 'drops-key')
		W = Object_Name('water')
		F = Object_Name('message', "The favour you get from defeating security drones can be exchanged at shrines for powerful abilities.")
		G = Object_Name('message', "Defeating security drones (even active ones) will give you rewards and sometimes keys.")
		H = Object_Name('message', "When you have aquired enough keys, you will be able to use the elevators to leave the level.")
		B = Object_Name('plant')
		X = Object_Name('shrine', 'rejuvenation')
		Y = Object_Name('shrine', 'instantaneous-strength')
		seg_map =      [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
				[1,0,0,0,0,W,0,0,W,0,0,0,0,0,0,W],
				[1,0,X,0,W,W,0,0,W,W,S,Y,0,C,W,W],
				[1,0,W,W,W,0,0,0,0,W,0,0,0,W,W,0],
				[1,W,W,W,0,B,0,F,0,W,W,W,W,W,0,0],
				[1,W,0,0,0,0,0,0,0,0,W,W,W,0,0,0],
				[1,0,0,0,0,0,0,0,0,0,0,W,W,0,G,0],
				[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[1,0,0,0,0,0,0,B,0,0,0,0,0,B,0,0],
				[1,0,0,0,C,0,0,0,0,0,0,0,0,0,0,0],
				[1,0,0,0,0,0,0,0,0,0,0,B,0,0,0,0],
				[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[1,0,0,0,0,0,B,0,0,0,0,0,0,0,C,0],
				[1,0,0,0,H,H,0,0,0,0,0,0,H,H,0,0],
				[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
		self.append_segment(map, background_map, self.create_segment(seg_map), 2*tut_rm_width, 6*tut_rm_height, object_data)


#		A = Object_Name('monster', 'strawman')
#		B = Object_Name('weapon', 'sword')
#		C = Object_Name('easydoor', 'horizontal')	# a door that doesn't stick!
##		B = Object_Name('shrine', 'healer')	
#		#B = Object_Name('strawman', 'sai', 'w')
#		#M = Object_Name('message', 'Good lord it\'s some sort of message on the floor!!!')
#		D = Object_Name('message', "Welcome to the training area! Please walk through the door above to begin your training. (press #MOVEUP#)")
#		E = Object_Name('message', "Move to the weapon ahead of you and press #PICKUP# to pick it up.")		
#		F = Object_Name('message', "Move next to an enemy and press SEVERAL LETTERS to attack.")
#		seg_map =      [[0,0,0,0,0,0,0,0,0],
#				[0,A,0,0,F,0,0,A,0],
#				[0,0,A,0,0,0,A,0,0],
#				[0,A,0,0,B,0,0,A,0],
#				[0,0,0,0,0,0,0,0,0],
#				[0,0,0,0,E,0,0,0,0],
#				[0,0,0,0,0,0,0,0,0],
#				[0,0,0,0,0,0,0,0,0],
#				[0,0,0,0,0,0,0,0,0],
#				[1,1,1,1,0,1,1,1,1],
#				[1,1,1,1,0,1,1,1,1],
#				[1,1,1,1,C,1,1,1,1],
#				[1,0,0,0,0,0,0,0,1],
#				[0,0,0,0,0,0,0,0,0],
#				[0,0,0,0,0,0,0,0,0],
#				[0,0,0,0,D,0,0,0,0],
#				[0,0,0,0,0,0,0,0,0],
#				[1,0,0,0,0,0,0,0,1],
#				[1,1,1,1,1,1,1,1,1]]
#		#seg_map = self.rotateSegment(seg_map)
#
#		#old_room = new_room
#		new_room = Rect(10 + rxofst,0 + ryofst,8,16)
#		self.create_room(new_room, map, center_points, nearest_points_array)
#		(new_x, new_y) = new_room.center()
##		(prev_x, prev_y) = old_room.center()
#		self.append_segment(map, background_map, self.create_segment(seg_map), 10 + rxofst, 0 + ryofst, object_data)
##		self.create_h_tunnel(prev_x, new_x, prev_y, map, nearest_points_array, center_points, narrow = True)
#		#object_data.append(Object_Datum(new_x, new_y,'weapon', 'sai'))
#		#self.create_v_tunnel(new_y, prev_y, new_x, map, nearest_points_array, center_points, narrow = True)
#
#
#		A = Object_Name('strawman')
#		B = Object_Name('strawman', 'sai', 'ATTCKLEFT')
#		C = Object_Name('strawman', 'sai', 'ATTCKUP')
##		B = Object_Name('shrine', 'healer')	
#		#B = Object_Name('strawman', 'sai', 'w')
#		#M = Object_Name('message', 'Good lord it\'s some sort of message on the floor!!!')
#		D = Object_Name('message', "'Lesson 2. The secret of all combat is this: Hit your enemy without your enemy hitting you!'")
#		E = Object_Name('message', "Move to the weapon ahead of you and press #PICKUP# to pick it up.")		
#		F = Object_Name('message', "Move next to an enemy and press SEVERAL LETTERS to attack.")
#		seg_map =      [[1,1,1,1,1,1,1,1,1,1,1],
#				[1,1,1,0,0,0,0,0,0,0,1],
#				[A,0,0,0,0,0,0,0,0,0,1],
#				[1,1,1,0,0,0,C,0,0,0,1],
#				[1,1,1,0,0,0,0,0,0,0,1],
#				[1,1,1,0,0,0,0,C,0,0,1],
#				[1,1,1,D,0,0,0,0,0,0,1],
#				[1,1,1,0,0,0,0,0,B,0,0],
#				[1,1,1,0,0,0,0,0,0,0,1],
#				[1,1,1,1,1,1,1,1,1,1,1]]
#
#		#old_room = new_room
#		new_room = Rect(19 + rxofst,0 + ryofst,8,10)
#		self.create_room(new_room, map, center_points, nearest_points_array)
#		(new_x, new_y) = new_room.center()
##		(prev_x, prev_y) = old_room.center()
#		self.append_segment(map, background_map, self.create_segment(seg_map), 19 + rxofst, 0 + ryofst, object_data)
##		self.create_h_tunnel(prev_x, new_x, prev_y, map, nearest_points_array, center_points, narrow = True)
#		#object_data.append(Object_Datum(new_x, new_y,'weapon', 'sai'))
#		#self.create_v_tunnel(new_y, prev_y, new_x, map, nearest_points_array, center_points, narrow = True)
#
#		rxofst = rxofst + 11
#
#		A = Object_Name('monster', 'strawman on wheels')
##		B = Object_Name('shrine', 'healer')	
#		#B = Object_Name('strawman', 'sai', 'w')
#		#M = Object_Name('message', 'Good lord it\'s some sort of message on the floor!!!')
#		D = Object_Name('message', "Lesson 3. Do not strike at where your enemy is! Strike at where your enemy is going to be!")
#		seg_map =      [[1,1,1,1,1,1,1,1,1,1,1],
#				[1,1,1,0,0,0,0,0,0,0,1],
#				[1,0,0,0,0,0,0,0,0,0,0],
#				[1,0,0,0,A,0,0,0,0,A,1],
#				[1,0,0,0,0,0,0,0,0,0,1],
#				[1,0,0,0,0,A,0,A,0,0,1],
#				[1,1,1,A,0,0,0,0,0,0,1],
#				[0,D,0,0,0,0,0,0,0,0,1],
#				[1,1,1,0,0,0,0,0,0,0,1],
#				[1,1,1,1,1,1,1,1,1,1,1]]
#
#		#old_room = new_room
#		new_room = Rect(19 + rxofst,0 + ryofst,8,10)
#		self.create_room(new_room, map, center_points, nearest_points_array)
#		(new_x, new_y) = new_room.center()
##		(prev_x, prev_y) = old_room.center()
#		self.append_segment(map, background_map, self.create_segment(seg_map), 19 + rxofst, 0 + ryofst, object_data)
##		self.create_h_tunnel(prev_x, new_x, prev_y, map, nearest_points_array, center_points, narrow = True)
#		#object_data.append(Object_Datum(new_x, new_y,'weapon', 'sai'))
#		#self.create_v_tunnel(new_y, prev_y, new_x, map, nearest_points_array, center_points, narrow = True)
#
#
#	
#
#		# "The Gauntlet"
#		A = Object_Name('strawman')
#		B = Object_Name('strawman', 'spear', 'ATTCKLEFT')
#		C = Object_Name('strawman', 'spear', 'ATTCKUP')
#		D = Object_Name('strawman', 'spear', 'ATTCKDOWN')
#		E = Object_Name('strawman', 'spear', 'ATTCKRIGHT')
##		B = Object_Name('shrine', 'healer')	
#		#B = Object_Name('strawman', 'sai', 'w')
#		#M = Object_Name('message', 'Good lord it\'s some sort of message on the floor!!!')	
#		F = Object_Name('message', "Lesson 3. Be not afraid to run into the place your enemy has just struck.")
#		seg_map =      [[1,1,1,1,D,1,D,1,D,1,1,1,1],
#				[1,1,1,1,0,1,0,1,0,1,1,1,1],
#				[0,F,0,0,0,0,0,0,0,0,0,B,0],
#				[1,1,1,1,1,1,1,1,1,0,1,1,1],
#				[1,1,1,1,1,1,1,1,1,0,0,B,1],
#				[1,1,1,1,1,0,0,0,0,0,1,1,1],
#				[1,1,1,1,1,0,1,0,1,0,1,1,1],
#				[1,1,1,1,1,0,1,C,1,C,1,1,1],
#				[1,1,1,1,1,0,1,1,1,1,1,1,1]]
#
#		#old_room = new_room
#		new_room = Rect(28 + rxofst,0 + ryofst,8,9)
#		self.create_room(new_room, map, center_points, nearest_points_array)
#		(new_x, new_y) = new_room.center()
##		(prev_x, prev_y) = old_room.center()
#		self.append_segment(map, background_map, self.create_segment(seg_map), 28 + rxofst, 0 + ryofst, object_data)
##		self.create_h_tunnel(prev_x, new_x, prev_y, map, nearest_points_array, center_points, narrow = True)
#		#object_data.append(Object_Datum(new_x, new_y,'weapon', 'sai'))
#		#self.create_v_tunnel(new_y, prev_y, new_x, map, nearest_points_array, center_points, narrow = True)
#
#
#
#		# JUMPING ROOM!
#		A = Object_Name('strawman')
#		W = Object_Name('water')
#		B = Object_Name('plant')
#		D = Object_Name('message', "Lesson 4. JUMP! (Press SPACEY BAR)")
#		E = Object_Name('message', "Jumping and attacking use up ENERGY. Getting hit on extra energy is super bad. Try to avoid it.")
#		F = Object_Name('message', "The rest is up to you. Good luck!")
##		B = Object_Name('shrine', 'healer')	
#		#B = Object_Name('strawman', 'sai', 'w')
#		#M = Object_Name('message', 'Good lord it\'s some sort of message on the floor!!!')	
#		seg_map =      [[1,1,1,B,1,1,1,1,1,1,1,1,1,1,1,1,1],
#				[1,1,1,0,0,0,0,0,W,0,0,0,W,0,0,0,0],
#				[1,1,1,0,0,B,0,0,W,0,0,0,W,0,0,0,F],
#				[1,1,1,0,0,0,0,0,W,0,0,0,A,0,0,0,0],
#				[1,1,1,0,0,0,0,D,W,0,0,0,A,0,E,0,1],
#				[1,1,1,0,0,0,0,0,W,0,0,0,A,0,0,0,1],
#				[1,1,1,0,0,0,0,0,W,0,0,0,W,0,0,0,1],
#				[1,1,1,0,0,0,0,0,W,0,0,0,W,0,0,0,1],
#				[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
#
#		#old_room = new_room
#		new_room = Rect(30 + rxofst,9 + ryofst,17,9)
#		self.create_room(new_room, map, center_points, nearest_points_array)
#		(new_x, new_y) = new_room.center()
##		(prev_x, prev_y) = old_room.center()
#		self.append_segment(map, background_map, self.create_segment(seg_map), 30 + rxofst, 9 + ryofst, object_data)
##		self.create_h_tunnel(prev_x, new_x, prev_y, map, nearest_points_array, center_points, narrow = True)
#		#object_data.append(Object_Datum(new_x, new_y,'weapon', 'sai'))
#		#self.create_v_tunnel(new_y, prev_y, new_x, map, nearest_points_array, center_points, narrow = True)
#
#
#
#
#		#finally... add some elevators??
		#print 'adding elevators...'
		elev1 = Rect(tut_rm_width-3,7*tut_rm_height+4, 5, 4)
		elev2 = Rect(2*tut_rm_width+3, 8*tut_rm_height-2, 4, 5)
		elev3 = Rect(3*tut_rm_width+3, 8*tut_rm_height-2, 4, 5)
		rooms.append(elev1)
		#rooms.append(elev2)

		# the elevator next to the start area just always allows the player in
		self.create_elevator(elev1, map, spawn_points, center_points, nearest_points_array, object_data,  elevators, 'Small-Elevator-Right', background_map, easy_elevator = True)	
		self.create_elevator(elev2, map, spawn_points, center_points, nearest_points_array, object_data,  elevators, 'Small-Elevator-Up', background_map)
		self.create_elevator(elev3, map, spawn_points, center_points, nearest_points_array, object_data,  elevators, 'Small-Elevator-Up', background_map)
		# . Move
		# .   Moving diagonally
		# . Pick up weapon 
		# . attack enemies
		# . avoid enemy attacks
		# .   Hit moving enemies by hitting where they will be! I forgot that one
		# . can go where enemies have just hit
		# . Jump
		# . beware about energy
		# . pick up keys
		# . fight one enemy
		# . fight a rook
		# . fight two enemies
		# .  o k so security drones:
		#		 - increase the alarm when they see you
		# 		 - decrease the alarm when they get killed
		#		 - higher alarm means more enemies are coming for you
		#		 - sometimes but not always have keys!
		#	hum hum hum how do I communicate all that.

		# . you need keys to get out of the level
		# "This sentry will sound an alarm if it sees you for too long! And it is hard to kill. But killing it will reduce the alarm. And sometimes it has keys.


	def rotateSegment(self, seg_map):
		segHeight = len(seg_map)
		segWidth = len(seg_map[0])
	
		new_map = [[ 0
			for y in range(segHeight) ]
				for x in range(segWidth) ]
		for y in range (0, segHeight):
			for x in range (0, segWidth):
				new_map[x][y] = seg_map[segHeight-1-y][x]
		return new_map




	def test_room(self, object_data, map, background_map, center_points, nearest_points_array, rooms, num_rooms, spawn_points, elevators, room_adjacencies):


		tut_rm_width = 8
		tut_rm_height = 8

		new_room = Rect(tut_rm_width,7*tut_rm_height,tut_rm_width,tut_rm_height)
		self.create_room(new_room, map, center_points, nearest_points_array)
		C = Object_Name('door')	# a door that may stick!
		#D = Object_Name('message', "Welcome to the training area! Please walk through the door above to begin your training. (press #MOVEUP#)")
		D = Object_Name('weapon', 'sword')
		E = Object_Name('monster', 'crane')
		F = Object_Name('fire')
		#G = Object_Name('firepit')
		G = Object_Name('shrine')
		H = Object_Name('plant')
		seg_map =      [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
				[1,1,1,0,0,0,0,0,H,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
				[1,1,1,C,0,0,0,0,0,0,0,0,C,0,0,0,C,0,0,0,0,0,1],
				[1,0,0,0,0,0,0,0,0,C,0,0,0,0,0,0,0,0,0,0,0,1,1],
				[0,0,0,0,0,G,0,C,0,0,0,G,0,G,0,G,0,0,G,0,C,1,1],
				[0,0,0,D,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
				[1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,1,1],
				[1,0,0,0,0,0,0,0,0,C,H,C,0,0,0,C,H,C,0,0,0,1,1]]
		#seg_map = self.rotateSegment(seg_map)

		#old_room = new_room
#		new_room = Rect(tut_rm_width,7*tut_rm_height,tut_rm_width,tut_rm_height)
#		(new_x, new_y) = new_room.center()
#		(prev_x, prev_y) = old_room.center()
		self.append_segment(map, background_map, self.create_segment(seg_map), tut_rm_width,7*tut_rm_height, object_data)


	def first_level(self, object_data, map, background_map, center_points, nearest_points_array, rooms, num_rooms, spawn_points, elevators, room_adjacencies):

		test_mode = False

		if test_mode:
			 self.test_room(object_data, map, background_map, center_points, nearest_points_array, rooms, num_rooms, spawn_points, elevators, room_adjacencies)
		else:
			 self.new_tutorial(object_data, map, background_map, center_points, nearest_points_array, rooms, num_rooms, spawn_points, elevators, room_adjacencies)


	


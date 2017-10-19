#PROBABLY NOT IN USE AT THE MOMENT BECAUSE I CAN'T GET THE HANG OF IMPORTING CODE :(

import tdl as libtcod
#import libtcodpy as libtcod


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

#from objectClass import Object
class Elevator:

	def __init__(self, door_points, spawn_points):
		self.door_points = door_points
		self.spawn_points = spawn_points
		self.doors = []
		for (x,y) in self.door_points:
			door = Object(x, y, '+', 'elevator door', libtcod.red, blocks=True, door = Door(horizontal = False), always_visible=True) 
			self.doors.append(door)
			print "doooooooR"
			#map[od.x][od.y].block_sight = True
			#objects.append(door)


class Door:
	def __init__(self, horizontal):
		self.horizontal = horizontal

	def take_damage(self, damage):
		#destroy the door!
		#if damage > 0:
		#	self.hp -= damage
		#	#check for death. if there's a death function, call it
		#	if self.hp <= 0:
		#		function = self.death_function
		#		if function is not None:
		#			function(self.owner)

		
		message('The door crashes down!', libtcod.orange)

		door = self.owner
		door.blocks = False
		door.door = None
		door.send_to_back()
		garbage_list.append(door)
		
		#update the map to say that this square isn't blocked, and update the nav data
		map[door.x][door.y].blocked = False
		map[door.x][door.y].block_sight = False
		
		nav_data_changed = True
		initialize_fov()		# this is ok, right? update the field of view stuff



class Object:
	#this is a generic object: the player, a monster, an item, the stairs...
	#it's always represented by a character on screen.
	def __init__(self, x, y, char, name, color, blocks=False, always_visible=False, fighter=None, decider=None, attack=None, weapon = False, shrine = None, floor_message = None, door = None, currently_invisible = False):
		self.x = x
		self.y = y
		self.char = char
		self.name = "STUPID" + name
		self.blocks = blocks
		self.color = color
		self.always_visible = always_visible
		self.fighter = fighter
		if self.fighter:  #let the fighter component know who owns it
			self.fighter.owner = self
		self.decider = decider
		if self.decider:  #let the decider component know who owns it
			self.decider.owner = self
		self.attack = attack
		if self.attack:
			self.attack.owner = self
		self.weapon = weapon
		self.shrine = shrine
		if self.shrine:
			self.shrine.owner = self
		self.floor_message = floor_message
		if self.floor_message:
			self.floor_message.owner = self
		self.door = door
		if self.door:
			self.door.owner = self
		self.currently_invisible = currently_invisible	# I am introducing this as a hack to make elevator doors go away.
								# Instead of actually going away, they'll be made invisible, not blocking
								# and not blocking light (different from being invisible).
								# Video games!
		
	def move(self, dx, dy):
		if not is_blocked(self.x + dx, self.y + dy):
			#move by the given amount
		        self.x += dx
		        self.y += dy


	def draw(self):
		print "y"
		#only show if it's visible to the player; or it's set to "always visible" and on an explored tile
		# also don't draw it if it's set to 'currently invisible'

		#if True:	# temporary hack to test enemy naviation
		if (libtcod.map_is_in_fov(fov_map, self.x, self.y) or (self.always_visible and map[self.x][self.y].explored)) and not self.currently_invisible:
			#set the color and then draw the character that represents this object at its position
			libtcod.console_set_default_foreground(con, self.color)
			libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)

	def clear(self):
		#erase the character that represents this object
		libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)

		#erase the character that represents this object
	#	if libtcod.map_is_in_fov(fov_map, self.x, self.y):
	#		libtcod.console_put_char_ex(con, self.x, self.y, '.', libtcod.white, libtcod.dark_blue)


	def move_towards(self, target_x, target_y):
		#vector from this object to the target, and distance
		dx = target_x - self.x
		dy = target_y - self.y
		distance = math.sqrt(dx ** 2 + dy ** 2)

		#normalize it to length 1 (preserving direction), then round it and
		#convert to integer so the movement is restricted to the map grid
		if distance != 0:
			dx = int(round(dx / distance))
			dy = int(round(dy / distance))
		self.move(dx, dy)


	def distance_to(self, other):
		#return the distance to another object
		dx = other.x - self.x
		dy = other.y - self.y
		return math.sqrt(dx ** 2 + dy ** 2)

	def send_to_back(self):
		#make this object be drawn first, so all others appear above it if they're in the same tile.
		global objects
		objects.remove(self)
		objects.insert(0, self)


	def send_to_front(self):
		#make this object be drawn last, so all others appear below it if they're in the same tile.
		global objects
		objects.remove(self)
		objects.append(self)

	def stun(self):
		if self.decider:
			if self.decider.ai:
				self.decider.ai.stun()



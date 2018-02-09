import tdl as libtcod
#from libtcod.map import Map
#import libtcodpy as libtcod
import time
import math
import textwrap
import random
#import shelve 	# for saving and loading			# TODO possibly cut; doesn't seem to play nice with cxfreeze
from random import randint
from weapons import Weapon_Unarmed, Weapon_Sword, Weapon_Staff, Weapon_Spear, Weapon_Dagger, Weapon_Strawhands, Weapon_Sai, Weapon_Sai_Alt, Weapon_Nunchuck, Weapon_Axe, Weapon_Katana, Weapon_Hammer, Weapon_Wierd_Sword, Weapon_Wierd_Staff, Weapon_Trident, Weapon_Ring_Of_Power
from levelSettings import Level_Settings
from levelGenerator import Level_Generator
from gods import God, God_Healer, God_Destroyer, God_Deliverer
from powerUps import PowerUp, WallHugger, Mindfulness, NeptunesBlessing, Amphibious, Perfectionist, Get_Random_Upgrade, Get_Test_Upgrade
from saveDataHandler import SaveDataHandler #, SaveDatum
from controlHandler import ControlHandler
from colorHandler import ColorHandler

SCREEN_WIDTH = 70
SCREEN_HEIGHT = 39

LIMIT_FPS = 20

#Controls
ControlMode = 'Crypsis' 	# 'Wheatley'   'Glados'


#if ControlMode == 'Glados':
#	ATTCKUPLEFT	 = 'q'
#	ATTCKUP		 = 'w'
#	ATTCKUPRIGHT	 = 'e'
#	ATTCKRIGHT	 = 'd'
#	ATTCKDOWNRIGHT	 = 'c'
#	ATTCKDOWN	 = 'x'
#	ATTCKDOWNLEFT	 = 'z'
#	ATTCKLEFT	 = 'a'
#
#	ATTCKDOWNALT	 = 's'
#elif ControlMode == 'Crypsis':
#	ATTCKUPLEFT	 = 'a'
#	ATTCKUP		 = 'z'
#	ATTCKUPRIGHT	 = 'e'
#	ATTCKRIGHT	 = 'd'
#	ATTCKDOWNRIGHT	 = 'c'
#	ATTCKDOWN	 = 'x'
#	ATTCKDOWNLEFT	 = 'w'
#	ATTCKLEFT	 = 'q'
#
#	ATTCKDOWNALT	 = 's'

#MOVEUPLEFT
#MOVEUP
#MOVEUPRIGHT
#MOVERIGHT
#MOVEDOWNRIGHT
#MOVEDOWN
#MOVEDOWNLEFT
#MOVELEFT

#MEDITATE
#PICKUP

#JUMP = 'r'


# Some lazy coding. this part of the code originally used variable names (e.g. ATTCKUP = 'z') for attack commands.
# Other parts now use string. We're just mapping one to the other so I don't have to rewrite a bunch
ATTCKUPLEFT	 = "ATTCKUPLEFT"
ATTCKUP		 = "ATTCKUP"
ATTCKUPRIGHT	 = "ATTCKUPRIGHT"
ATTCKRIGHT	 = "ATTCKRIGHT"
ATTCKDOWNRIGHT	 = "ATTCKDOWNRIGHT"
ATTCKDOWN	 = "ATTCKDOWN"
ATTCKDOWNLEFT	 = "ATTCKDOWNLEFT"
ATTCKLEFT	 = "ATTCKLEFT"
ATTCKDOWNALT	 = "ATTCKDOWNALT"


# and now here are some  3-character forms of these string names, to make AI code more readable.
# it's gonna use QWERTY-specific terms (like oQo for ATTCKUPLEFT), just because that makes 
# editing in these terms easier. sorry about that. when it comes to writing AI movement/ attack patterns,
# you would probably benefit from looking at a QWERTY keyboard.
oQo = ATTCKUPLEFT
oWo = ATTCKUP
oEo = ATTCKUPRIGHT
oDo = ATTCKRIGHT
oCo = ATTCKDOWNRIGHT
oXo = ATTCKDOWN
oZo = ATTCKDOWNLEFT
oAo =ATTCKLEFT



MAP_WIDTH = 80
MAP_HEIGHT = 43

ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 10
MAX_ROOM_MONSTERS = 5

WEAPON_FAILURE_WARNING_PERIOD = 10

ELEVATOR_DOOR_CLOSURE_PERIOD = 5
ELEVATOR_DISTANCE_CHECK = 4

CHANCE_OF_ENEMY_DROP = 30

STARTING_ENERGY  = 10

DEFAULT_JUMP_RECHARGE_TIME = 4		#40
DEFAULT_BLOOM_TIME = 37

STARTING_CURRENCY = 2


#color_dark_wall = libtcod.Color(0, 0, 100)
#color_dark_ground = libtcod.Color(50, 50, 150)
#color_dark_wall = (100, 100, 100)
#color_dark_ground = (150, 150, 150)

# FOV algorithm stuff
FOV_ALGO = 'BASIC' #0  #default FOV algorithm
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 50 #20

max_nav_data_loops = 1

# COLORS. LET'S TRY AND PUT ALL THE COLORS HERE
val_player = 255
val_seen_floor = 160
val_unseen_floor = 140
val_unseen_wall = 90
val_seen_wall = 100
val_enemies = 50
val_fog_of_war = 0

v_p = val_player
vsf = val_seen_floor
vuf = val_unseen_floor
vuw = val_unseen_wall
vsw = val_seen_wall
v_e = val_enemies
vfw = val_fog_of_war

# Environment colors (walls +floors, altars, visible or not)
color_dark_wall = 	(vuw,vuw,vuw)	#	(100,100,100)		#(0, 0, 100)
color_light_wall = 	(vsw,vsw,vsw)	#	(130, 110, 50)
color_dark_ground = 	(vuf,vuf,vuf)	#	(150,150,150)		#(50, 50, 150)
color_light_ground = 	(vsf,vsf,vsf)	#	(200, 180, 50)
color_fog_of_war = 	(vfw,vfw,vfw)	#	(0,0,0)			#libtcod.black
default_altar_color = color_light_wall
default_message_color = color_light_wall
default_decoration_color = 	(vuw,vuw,vuw)	#	(250,230,50)		#(165,145,50)
water_background_color = 	(vuf,vuf,vuf)	#	(100,100,250)
water_foreground_color = 	(vsw,vsw,vsw)	#	(25,25,250)
blood_background_color = 	(vuf,vuf,vuf)	#	(200,0,0)
blood_foreground_color = 	(vsw,vsw,vsw)	#	(150,0,0)

# collectiable e.g. weapons and plants and keys
default_flower_color = 	(vsw,vsw,vsw)	#(50,150,0)
default_weapon_color = (vsw,vsw,vsw)	#(50,50,50) #libtcod.grey


# enemies, including player
PLAYER_COLOR = (v_p,v_p,v_p)	#(255, 255, 255)
#color_sneaky_enemy
#color_shortrange_enemy
#color_midrange_enemy
#color_longrange_enemy
#color_big_boss

color_swordsman = 	(v_e,v_e,v_e)	#	(0,0,191)		#libtcod.dark_blue
color_boman = 		(v_e,v_e,v_e)	#	(0,128,0)		#libtcod.darker_green
color_rook = 		(v_e,v_e,v_e)	#	(0,0,128)		#libtcod.darker_blue
color_axe_maniac =	(v_e,v_e,v_e)	#	 (128,0,0)		#libtcod.darker_red
color_tridentor = 	(v_e,v_e,v_e)	#	(0,0, 255)		#libtcod.blue
color_ninja = 		(v_e,v_e,v_e)	#	(0,0,0)		#libtcod.black
color_wizard = 		(v_e,v_e,v_e)	#	(95, 0, 128)			#libtcod.darker_purple
color_alarmer_idle =	(vsw,vsw,vsw)
color_alarmer_suspicious = (v_p,v_p,v_p)
color_alarmer_alarmed = (v_e,v_e,v_e)

# text colors
default_background_color = 	(vfw,vfw,vfw)	#(0,0,0)
default_text_color = 		(vsf,vsf,vsf)	#(255,255,255)
color_energy = 			(v_p,v_p,v_p)	#(0,255,255)
color_faded_energy = 		(vsf,vsf,vsf)	#	(0,0,255)
color_warning = 		(v_p,v_p,v_p)	#	(255,127,0)
color_big_alert = 		(v_p,v_p,v_p)	#(255,0,0)

Color_Message_In_World=(v_p,v_p,v_p)		# e.g. messages on floor, deities or elevators talking to you
Color_Menu_Choice=(v_p,v_p,v_p)			# when the player has to input an option from mutliple choices
Color_Not_Allowed=(v_p,v_p,v_p)			# when a player action is invalid or prevented
Color_Dangerous_Combat=(v_p,v_p,v_p)		# when bad things happen in combat, like dying or getting hit
Color_Interesting_Combat=(v_p,v_p,v_p)		# notable combat stuff like enemies dying
Color_Boring_Combat=(v_p,v_p,v_p)		# Run of the mill combat stuff. you hit an enemy. yawn
Color_Interesting_In_World=(v_p,v_p,v_p)	# Events of note happening in the world. Like alarms going off
Color_Boring_In_World=(v_p,v_p,v_p)		# everyday occurences like doors opening
Color_Stat_Info=(v_p,v_p,v_p)			# info about not-in-the-world stuff like gaining energy
Color_Personal_Action=(v_p,v_p,v_p)		# Things the player does that aren't combat "you pick up the sword" etc


#sizes and coordinates relevant for the GUI and action screen
BAR_WIDTH = 20
PANEL_HEIGHT = 9
#MESSAGE_PANEL_HEIGHT = 4
MESSAGE_PANEL_HEIGHT = 30
MESSAGE_PANEL_WIDTH = 25
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT
ACTION_SCREEN_WIDTH = SCREEN_WIDTH - MESSAGE_PANEL_WIDTH
ACTION_SCREEN_HEIGHT = SCREEN_HEIGHT - PANEL_HEIGHT
ACTION_SCREEN_X = MESSAGE_PANEL_WIDTH
ACTION_SCREEN_Y = 0

CAMERA_FOCUS_WIDTH = 8
CAMERA_FOCUS_HEIGHT = 8

MSG_X = BAR_WIDTH + 2
#MSG_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
#MSG_WIDTH = SCREEN_WIDTH-2
#MSG_HEIGHT = MESSAGE_PANEL_HEIGHT
MSG_WIDTH = MESSAGE_PANEL_WIDTH-2
MSG_HEIGHT = MESSAGE_PANEL_HEIGHT-1



# Some bullshit  to  do  with translating libtcod console stuff into tdl stuff
# Console_Translator = libtconsoletranslatrix()


libtcod_BKGND_NONE= None #formerly written in the code as libtcod.BKGND_NONE, but we never actually need to use it. Sorry for all the cruft.
				# too lazy to go through and get rid of it all. Also I want to preserve it just in case
libtcod_BKGND_SET = None

libtcod_LEFT = 'Left'	#formerly libtcod_LEFT  . Formerly a flag for aligning text stuff I think; can't figure out how to do it in tdl
libtcod_RIGHT = 'Right'
libtcod_CENTER = 'Center'




# this is some nonsense to translate old libtcod console commands into tdl-friendly stuff so I won't have to tediously reformat lines
#class libtconsoletranslatrix:
#
#	def __init__(self):
#		self.default_bg_color = deafult_background_color
#		self.default_fg_color = default_text_color
#
#	def console_set_default_foreground()

def translated_console_set_default_foreground(console, color):
	console.set_colors(fg = color)

def translated_console_set_default_background(console, color):
	console.set_colors(bg = color)

def translated_console_clear(console):
	console.clear()


def translated_console_flush():
	libtcod.flush()

def translated_console_print_ex(console, x, y, libtcod_bkcgnd_type, libtcod_alignment, string):
	console.draw_str(int(x), int(y), string)		#maybe? ignore the other stuff and hope colors are already set ok?

def translated_console_print_ex_center(console, x, y, libtcod_bkcgnd_type, libtcod_alignment, string):
	console.draw_str(int(x) - int(len(string)/2), int(y), string)		
	#console.draw_str(int(x), int(y), string)		

def translated_console_set_char_background(console, x, y, color, libtcod_bkcgnd_type):
        console.draw_char(x, y, None,  fg=None, bg=color,)

def translated_console_is_window_closed():
	return libtcod.event.is_window_closed()  # I THINK??

def translated_console_set_fullscreen(fullscreen_val):
	return
	#libtcod.set_fullscreen(fullscreen_val)

def translated_console_is_fullscreen():
	return libtcod.get_fullscreen()

class Object:
	#this is a generic object: the player, a monster, an item, the stairs...
	#it's always represented by a character on screen.
	def __init__(self, x, y, char, name, color, blocks=False, always_visible=False, fighter=None, decider=None, attack=None, weapon = False, shrine = None, floor_message = None, door = None, currently_invisible = False, alarmer = None, plant = None, drops_key = False):  #raising_alarm = False):
		self.x = x
		self.y = y
		self.char = char
		self.name = name
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
		self.plant = plant
		if self.plant:
			self.plant.owner = self
		self.currently_invisible = currently_invisible	# I am introducing this as a hack 
								#to make elevator doors go away. Instead of actually going away, 									#they'll be made invisible, not blocking and not blocking light
								# (different from being invisible). Video games!
		#self.raising_alarm = raising_alarm
		self.alarmer = alarmer
		self.drops_key = drops_key

	def move(self, dx, dy):	
		global objectsArray
									#TODO will need to update objectarry
		if not is_blocked(self.x + dx, self.y + dy, generally_ignore_doors = False):
			#move by the given amount
			old_x = self.x
			old_y = self.y
			new_x = self.x + dx
			new_y = self.y + dy
			self.x = new_x
			self.y = new_y
			# print('HI! iM AT (' + str(old_x) + ',' + str(old_y) + ') and want to go to (' + str(new_x) + ',' + str(new_y) + ')')
			# Update objectsArray so that self is in the right list
			objectsArray[new_x][new_y].append(self)
			objectsArray[old_x][old_y].remove(self)
			


	def draw(self):
		global camera

		#x_offset = camera.x-SCREEN_WIDTH/2
		x_offset = int(camera.x-(SCREEN_WIDTH + MESSAGE_PANEL_WIDTH)/2)
		#y_offset = camera.y-SCREEN_HEIGHT/2
		y_offset = int(camera.y-(SCREEN_HEIGHT-PANEL_HEIGHT)/2)
		#only show if it's visible to the player; or it's set to "always visible" and on an explored tile
		# also don't draw it if it's set to 'currently invisible'

		#if True:	# temporary hack to test enemy naviation
		if (fov_map.fov[self.x, self.y] or (self.always_visible and map[self.x][self.y].explored)) and not self.currently_invisible:

			#set the color and then draw the character that represents this object at its position
		#	libtcod.console_set_default_foreground(con, self.color)
		#	libtcod.console_put_char(con, self.x - x_offset, self.y - y_offset, self.char, libtcod_BKGND_NONE)
		#	libtcod.console_put_char(con, self.x - x_offset, self.y - y_offset, self.char, libtcod_BKGND_NONE)
			con.draw_char(self.x - x_offset, self.y - y_offset, self.char, bg=None, fg = self.color)

	def clear(self):
		global camera

		x_offset = int(camera.x-(SCREEN_WIDTH + MESSAGE_PANEL_WIDTH)/2)
		#y_offset = camera.y-SCREEN_HEIGHT/2
		y_offset = int(camera.y-(SCREEN_HEIGHT-PANEL_HEIGHT)/2)
		#erase the character that represents this object
		#libtcod.console_put_char(con, self.x-x_offset, self.y - y_offset, ' ', libtcod_BKGND_NONE)
		con.draw_char(self.x - x_offset, self.y - y_offset, ' ', bg=None, fg = self.color)

		#erase the character that represents this object
	#	if libtcod.map_is_in_fov(fov_map, self.x, self.y):
	#		libtcod.console_put_char_ex(con, self.x, self.y, '.', libtcod.white, libtcod.dark_blue)


	def move_towards(self, target_x, target_y):
		print('Error! argument Object.move_towards called. Mark was pretty sure this method wasn\'t being used, and it would have  caused wierd bugs as currently written anyway, so he commented it out. Maybe let him know that that happened?')
	#	#vector from this object to the target, and distance
	#	dx = target_x - self.x
	#	dy = target_y - self.y
	#	distance = math.sqrt(dx ** 2 + dy ** 2)
#
#		#normalize it to length 1 (preserving direction), then round it and
#		#convert to integer so the movement is restricted to the map grid
#		if distance != 0:
#			dx = int(round(dx / distance))
#			dy = int(round(dy / distance))
#		self.move(dx, dy)


	def distance_to(self, other):
		#return the distance to another object
		dx = other.x - self.x
		dy = other.y - self.y
		return math.sqrt(dx ** 2 + dy ** 2)

	def send_to_back(self):
		#make this object be drawn first, so all others appear above it if they're in the same tile.
		global objectsArray
		objectsArray[self.x][self.y].remove(self)
		objectsArray[self.x][self.y].insert(0, self)

	def send_to_almost_back(self):
		#make this object be drawn just above the decorations but below all other objects.
		global objectsArray, decoration_count
		objectsArray[self.x][self.y].remove(self)
		objectsArray[self.x][self.y].insert(decoration_count, self)

	def send_to_front(self):
		#make this object be drawn last, so all others appear below it if they're in the same tile.
		global objectsArray
		objectsArray[self.x][self.y].remove(self)
		objectsArray[self.x][self.y].append(self)



	def stun(self):
		if self.decider:
			if self.decider.ai:
				self.decider.ai.stun()


class Location:
	def __init__(self, x,y):
		self.x = x
		self.y = y

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
		self.x2 = x + w
		self.y2 = y + h

	def center(self):
		center_x = (self.x1 + self.x2) / 2
		center_y = (self.y1 + self.y2) / 2
		return (center_x, center_y)
 
	def intersect(self, other):
		#returns true if this rectangle intersects with another one
		return (self.x1 <= other.x2 and self.x2 >= other.x1 and
		self.y1 <= other.y2 and self.y2 >= other.y1)


class Shrine:
	def __init__(self, god, cost = None):
		self.god = god
		self.visited = False
		self.upgrade = Get_Random_Upgrade()
		if cost is not None:
			self.cost = cost
		else:
			self.cost = self.upgrade.cost
		# list of possible visions for the deity?
	
	def visit(self):
		self.visited = True

	# this will get more complicated later...
	def get_cost(self):
		return self.cost


class Floor_Message:
	def __init__(self, string):
		self.string = string


class Door:
	def __init__(self, horizontal, default_looseness = 3, easy_open = False):
		self.horizontal = horizontal
		self.default_looseness = default_looseness
		self.looseness = default_looseness	# attempting to open a door has probability 2/loosness of being unsuccesful. loosness goes up with more attempts.
		self.recently_rattled = False
		self.easy_open = easy_open

	def take_damage(self, damage):
		#destroy the door!
		#if damage > 0:
		#	self.hp -= damage
		#	#check for death. if there's a death function, call it
		#	if self.hp <= 0:
		#		function = self.death_function
		#		if function is not None:
		#			function(self.owner)

		message('The door crashes down!', Color_Interesting_In_World)

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

	def open(self):		#normal doors can't be closed after opening, Just one of those things
		
		if randint( 0, self.looseness-1) < 2 and not self.easy_open:		#opening unsuccesful
			message('The door rattles.', Color_Boring_In_World)
			#message('The door rattles. Looseness = ' + str(self.looseness), libtcod.white)
			self.looseness = self.looseness + 1		#increase chance of opening in future though
			self.recently_rattled = True

		else: 
			message('The door opens', Color_Boring_In_World)

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

	def update(self):
		#decrease looseness back to default, unless someone recently tried to open me
		if self.recently_rattled == False:
			if self.looseness > self.default_looseness:
				self.looseness = self.looseness - 1
		self.recently_rattled = False



#Let's make a bunch of flowers that grow and then replenish your health or whatever, sure.
class Flower:
	def __init__(self, flower_type = 'tulip', state = 'seed', bloom_timer = DEFAULT_BLOOM_TIME, name = 'fruit', symbol = 'o'):
		self.flower_type = flower_type
		self.state = state			# possible states: seed, growing, blooming, trampled. Maybe burnt, later?
		self.bloom_timer = bloom_timer
		self.name = name
		self.symbol = symbol

	#Player can 'activate' a dormant flower to start it growing
	def activate(self):
		if self.state == 'seed':
			self.state = 'growing'
			self.name = 'growing ' + self.flower_type
			self.symbol = 'u'

	# If someone walks on the flower while it's growing, it gets trampled :(
	def tread(self):
		if self.state == 'growing':
			self.state  = 'trampled'  # :(
			self.name = 'trampled ' + self.flower_type
			self.symbol = 'x'

	# Once activated, plant starts growing until the bloom timer counts down to 0, at which point it bears fruit
	def update(self):
		if self.state == 'growing':
			self.bloom_timer -= 1
			if self.bloom_timer <= 0:
				self.state = 'blooming'
				self.name = self.flower_type
				self.symbol = 'U'

	# Someone can harvest this delicious fruit and get health?
	def harvest(self, monster):
		if self.state == 'blooming' and monster.fighter is not None:
			monster.fighter.heal(1)
			monster.fighter.cure_wounds(1)
			self.state = 'trampled'
			message(monster.name + ' healed by ' + self.name, Color_Interesting_In_World)
			self.symbol = 'x'
			









class Fighter:
	#combat-related properties and methods (monster, player, NPC).
	def __init__(self, hp, defense, power, death_function=None, attack_color = PLAYER_COLOR, faded_attack_color = PLAYER_COLOR, extra_strength = 0, recharge_rate = 1, bonus_max_charge = 0, jump_array = [], jump_recharge_time = DEFAULT_JUMP_RECHARGE_TIME, bleeds = True):
		self.max_hp = hp
		self.hp = hp
		self.defense = defense
		self.power = power
		self.death_function=death_function
		self.attack_color = attack_color
		self.faded_attack_color = faded_attack_color
		self.extra_strength = extra_strength
		self.recharge_rate = recharge_rate
		self.bonus_max_charge = bonus_max_charge
		self.jump_array = jump_array
		self.jump_recharge_time = jump_recharge_time
		self.bleeds = bleeds
		self.in_water = False

	def take_damage(self, damage):
		#apply damage if possible
		if damage > 0:
			self.hp -= damage
			#check for death. if there's a death function, call it
			if self.hp <= 0:
				function = self.death_function
				if function is not None:
					function(self.owner)

	def attack(self, target):
		#a simple formula for attack damage
		damage = self.power - target.fighter.defense

	#	if target.fighter is not None:
	#		if damage > 0:
	#		#	#make the target take some damage
	#		#	message(self.owner.name.capitalize() + ' attacks ' + target.name + ' for ' + str(damage) + ' hit points.')
	#		#	target.fighter.take_damage(damage)
	#		else:
	#		#	message(self.owner.name.capitalize() + ' attacks ' + target.name + ' but it has no effect!')

	def fully_heal(self):
		self.hp = self.max_hp

	def heal(self, amount):
		self.hp += amount
		if self.hp > self.max_hp:
			self.hp = self.max_hp

	def increase_strength(self, amount):
		self.extra_strength += amount

	def increase_recharge_rate(self, amount):
		self.recharge_rate += amount

	def increase_max_charge(self, amount):
		self.bonus_max_charge += amount

	def recharge_jumps(self):
		temp_array = []
		for i in range(len(self.jump_array)):
			temp_array.append(max(0, self.jump_array[i]-1))		#reduce charge times on all jumps
		self.jump_array = temp_array

	# check if any of the jumps in the array are at 0. If so, they are available.
	def jump_available(self):
		available = False
		for i in range(len(self.jump_array)):
			if self.jump_array[i] == 0:
				available = True
		return available

	# use up one jump and start its recharge clock
	def make_jump(self):
		jump_used = False
		for i in range(len(self.jump_array)):
			if self.jump_array[i] == 0 and jump_used == False:
				self.jump_array[i] = self.jump_recharge_time
				jump_used = True
	
	# this doe nothing, and exists purely so i can call this method on tings without knowing if they are fighters or energy_fighters.
	# probably a sign that I should overhaul some of this stuff
	def cure_wounds(self, amount):
		return True
		


class Energy_Fighter:
	# combat-related properties and methods (player).
	# trying out an exciting new 'energy system'. Use energy to attack and to jump, energy gradually recharges, but getting hit reduces your energy semi-permanently, and you die if you lose more energy than you have.
	# UPDATE: actually let's make it so that you die only if your max energy goes to 0, and losing more energy than you have doesn't kill you, just reduces your max health by more
	def __init__(self, hp, defense, power, death_function=None, attack_color = PLAYER_COLOR, faded_attack_color = PLAYER_COLOR, extra_strength = 0, recharge_rate = 1, bonus_max_charge = 0, jump_array = [], jump_recharge_time = DEFAULT_JUMP_RECHARGE_TIME, bleeds = True):
		self.max_hp = hp
		self.hp = hp
		self.defense = defense
		self.power = power
		self.death_function=death_function
		self.attack_color = attack_color
		self.faded_attack_color = faded_attack_color
		self.extra_strength = extra_strength
		self.recharge_rate = recharge_rate
		self.bonus_max_charge = bonus_max_charge
		self.jump_array = jump_array
		self.jump_recharge_time = jump_recharge_time
		self.wounds = 0
		self.bleeds = bleeds
		self.in_water = False
	#	self.adrenaline_mode = False
	#	self.adrenaline_threshold = 2
	#	self.adrenaline_level = self.max_hp

	def take_damage(self, damage):
		#apply damage if possible
		if damage > 0:
			#add wounds! these basically reduce your max health
			self.wounds += damage

			# also lose energy equal to the damage you took
			self.hp -= damage
			# if you lose more energy than you have, take extra wounds!
			if self.hp < 0:
				self.wounds += (-self.hp)
				self.hp = 0
				message("OUCH! You take extra damage at low energy.", Color_Dangerous_Combat)
			if self.wounds > self.max_hp:
				self.wounds = self.max_hp

			# is your max hp (after wounds) 0 or less? then you die!
			if self.max_hp <= self.wounds:
				function = self.death_function
				if function is not None:
					function(self.owner)


	#		#check to see if we should announce the start of ADRENALINE MODE #commented out
	#		if self.adrenaline_mode == False and self.max_hp - self.wounds < self.adrenaline_threshold:
	#			message('You feel a surge of adrenaline.', libtcod.green)
	#		self.adjust_adrenaline()
				

	def attack(self, target):
		#a simple formula for attack damage
		damage = self.power - target.fighter.defense

	#	if target.fighter is not None:
	#		if damage > 0:
	#		#	#make the target take some damage
	#		#	message(self.owner.name.capitalize() + ' attacks ' + target.name + ' for ' + str(damage) + ' hit points.')
	#		#	target.fighter.take_damage(damage)
	#		else:
	#		#	message(self.owner.name.capitalize() + ' attacks ' + target.name + ' but it has no effect!')

	def fully_heal(self):
		self.hp = self.max_hp - self.wounds

	def heal(self, amount):
		self.hp += amount
		if self.hp > self.max_hp - self.wounds:
			self.hp = self.max_hp - self.wounds

	def cure_wounds(self, amount):
		self.wounds = self.wounds - amount
		if self.wounds < 0:
			self.wounds = 0
	#	self.adjust_adrenaline()

	def increase_strength(self, amount):
		self.extra_strength += amount

	def increase_recharge_rate(self, amount):
		self.recharge_rate += amount

	def increase_max_charge(self, amount):
		self.bonus_max_charge += amount

	def recharge_jumps(self):
		temp_array = []
		for i in range(len(self.jump_array)):
			temp_array.append(max(0, self.jump_array[i]-1))		#reduce charge times on all jumps
		self.jump_array = temp_array

	## decide if we should be in ADRENALINE MODE, with the rush of energy and whatnot.
	# def adjust_adrenaline(self):
	#	if self.max_hp - self.wounds < self.adrenaline_threshold:
	#		self.adrenaline_mode = True
	#	else:
	#		self.adrenaline_mode = False


	# check if the energy fighter has enough energy to make an attack
	# rewritten a bit: ignore 'adrenaline', but always be able to attack if you are at max hp.
	# This basically gives you the same risk /reward (being super wounded = more efficient attacking) 
	# and still gets round the problem of being stuck when on low health,
	# without the confusion of adrenaline mode
	def can_attack(self, energy_cost, return_message = False):
		global player, upgrade_array

		error_message = ''
		if self.hp < min(energy_cost, self.max_hp- self.wounds):
			error_message = 'energy too low'
		elif self.in_water:
			error_message = 'in water'
			print('PSLASH')


		# do some testing for upgrades to seeif they affect whether you can attack!
		if self.owner == player:
			for power_up in upgrade_array:
				if getattr(power_up, "update_on_testing_can_attack", None) is not None:
					power_up.update_on_testing_can_attack(error_message)

		if error_message == '':
			able_to_attack = True
		else:
			able_to_attack = False

		# TODO THIS AIN'T WORKING YET

		# update able_to_attack based on upgrades
		if self.owner == player:
			for power_up in upgrade_array:
				if getattr(power_up, "allows_attack", None) is not None:
					if power_up.allows_attack() == True:
						able_to_attack = True
						error_message = ''

		
		if able_to_attack:
			return True
		else:
			if return_message == True:
				return error_message
			else:
				return False


		#if self.adrenaline_mode == False:
		#	if self.hp >= energy_cost:
		#		return True
		#	else:
		#		return False
		#else:
		#	if self.adrenaline_level >= energy_cost:
		#		return True
		#	else:
		#		return False

	#lose the required amount of energy, down to a minimum of 0
	def lose_energy(self, energy_cost):
		if energy_cost > 0:
			self.hp -= energy_cost
			if self.hp <= 0:
				self.hp = 0
	#		self.adrenaline_level -= energy_cost
	#		if self.adrenaline_level <= 0:
	#			self.adrenaline_level = 0

	#lose the required amount of energy, down to a minimum of 0
	def gain_energy(self, energy_amount):
		if energy_amount > 0:
			self.hp += energy_amount
			if self.hp > self.max_hp - self.wounds:
				self.hp = self.max_hp - self.wounds
	#		self.adrenaline_level += energy_amount
	#		# adrenaline doesn't care about wounds!
	#		if self.adrenaline_level > self.max_hp:
	#			self.adrenaline_level  = self.max_hp

	
	# check if any of the jumps in the array are at 0. If so, they are available.
	def jump_available(self):
	#	if self.adrenaline_mode == False:
		if self.hp >= self.jump_recharge_time:
			return True
		else:
			return False
	#	else:
	#		if self.adrenaline_level >= self.jump_recharge_time:
	#			return True
	#		else:
	#			return False
		#available = False
		#for i in range(len(self.jump_array)):
		#	if self.jump_array[i] == 0:
		#		available = True
		#return available

	# use up one jump and start its recharge clock
	def make_jump(self):
		self.hp = self.hp - self.jump_recharge_time
		#jump_used = False
		#for i in range(len(self.jump_array)):
		#	if self.jump_array[i] == 0 and jump_used == False:
		#		self.jump_array[i] = self.jump_recharge_time
		#		jump_used = True
		


class Decider:
	def __init__(self, ai=None):
		self.decision_made = False
		self.decision = None
		self.ai = ai
		if ai is not None:
			self.ai.owner = self

	def decide(self):
		if self.ai is not None:
			self.ai.decide()	

	def set_decision(self, decision):
		self.decision = decision
		if decision is not None:
			self.decision_made = True
	
	def refresh(self):
		self.decision_made = False
		self.decision = None

# Something that can spot the player and raise/lower the alarm
class Alarmer:
	def __init__(self, alarm_time = 4, pre_alarm_time = 1, alarm_value = 2, dead_alarm_value = 1, idle_color = color_alarmer_idle, suspicious_color = color_alarmer_suspicious, alarmed_color = color_alarmer_alarmed, assoc_fighter = None):
		self.status = 'idle'			# 5 possible statuses: inert, pre-suspicious, suspicious, raising-alarm, alarm-raised
		self.alarm_time = alarm_time		# How long you have to spot intruder for before raising alarm
		self.pre_alarm_time = pre_alarm_time	# Delayed reaction time before realizing you've spotted an intruder
		self.alarm_value = alarm_value		# How much to raise the alar by when you know 
		self.dead_alarm_value = dead_alarm_value	# How much of the alarm stays behind after you are destroyed.
		self.idle_color = idle_color
		self.suspicious_color = suspicious_color
		self.alarmed_color = alarmed_color
		self.alarm_countdown = alarm_time
		self.pre_alarm_countdown = pre_alarm_time
		self.prev_suspicious = False
		self.assoc_fighter = assoc_fighter
		

	def update(self, intruder_spotted):
		if self.status == 'suspicious':
			self.prev_suspicious = True
		else:
			self.prev_suspicious = False

		if intruder_spotted:
			if self.status =='idle':
				self.status = 'pre-suspicious'
				self.pre_alarm_countdown = self.pre_alarm_time
				if self.pre_alarm_countdown <= 0:
					self.status = 'suspicious'
			elif self.status == 'pre-suspicious':
				self.pre_alarm_countdown -= 1
				if self.pre_alarm_countdown <= 0:
					self.status = 'suspicious'
					self.alarm_countdown = self.alarm_time
			elif self.status == 'suspicious':
				self.alarm_countdown -= 1
				if self.alarm_countdown <= 0:
					self.status = 'raising-alarm'
			elif self.status ==  'raising-alarm':
				# add a bunch of health to the fighter associated with this alarmer??
				if self.assoc_fighter is not None:
					self.assoc_fighter.max_hp += 6
					self.assoc_fighter.heal(6)
				self.status = 'alarm-raised'
			# if self.status = 'alarm-raised', don't do anything

		else: 	# getting rid of the "false alarm, go to sleep" angle - think it's more interesting if the plater is incentivzed to move maybe.
			
			#if self.status =='idle', keep doing what you're doing
		#	if self.status == 'suspicious' or self.status == 'pre-suspicious':
		#		self.status = 'idle'	# false alarm, go back to sleep
		#	elif self.status ==  'raising-alarm':
			if self.status ==  'raising-alarm':
				self.status = 'alarm-raised'
			# if self.status == 'alarm-raised', keep being alarmed!
		

		
	def get_hit(self):		# If you get hit, raise the alarm if you haven't already! 
		if self.status != 'alarm-raised':
			self.status = 'raising-alarm'



class Decision:
	def __init__(self, move_decision=None, attack_decision=None, jump_decision = None):
		self.move_decision=move_decision
		if move_decision is not None:
			self.move_decision.owner = self
		self.attack_decision=attack_decision
		if attack_decision is not None:
			self.attack_decision.owner = self
		self.jump_decision=jump_decision
		if jump_decision is not None:
			self.jump_decision.owner = self

class Move_Decision:
	def __init__(self,dx,dy):
		self.dx = dx
		self.dy = dy


class Jump_Decision:
	def __init__(self,dx,dy):
		self.dx = dx
		self.dy = dy



class Attack_Decision:
	def __init__(self, attack_list):
		self.attack_list = attack_list



class BasicMonster:
	global nearest_center_to_player

	#AI for a basic monster.
	def __init__(self, weapon, guard_duty  = False, attack_dist = 1, state = 'wander-aimlessly'):
		self.recharge_time = 0
		self.stunned_time = 0
		self.weapon = weapon
		if self.weapon is not None:
			self.weapon.owner = self
		self.guard_duty = guard_duty		# monsters on 'guard duty' don't come looking for you
		self.attack_dist = attack_dist
		self.previous_center = None
		self.target_room = None
		self.ally_in_the_way_o_meter = 0		 #decreases by 1 each turn, and goes up by 3 if ally in way
		self.impatience_threshold_for_allies_being_in_the_way = 7
		self.blocked_by_door_o_meter = 0		 #decreases by 1 each turn, and goes up by 2 if blocked door in way
		self.impatience_threshold_for_doors_being_in_the_way = 4
		self.state = state
		self.target_x = player.x
		self.target_y = player.y

	def decide(self):
		#a basic monster takes its turn. If you can see it, it can see you
		decider = self.owner
		monster = decider.owner #yaaay
		# only do thing (including weapon recharge? maybe not) if not stunned
		if self.stunned_time <= 0:


			# Welcome to basic monster ai business! Let's try and get the structure of this  cleared up a bit.

			# Step 0: put some details about external stuff here?
			current_room = nearest_points_array[monster.x][monster.y]

			# Step 1: Decide your current state, and maybe a few other bits.
			self.decideState(monster)

			# Step 2: Now you know yourself, or at least your state, decide your target (either a room or a specific space).
			self.decideTarget(monster)

			# Step 3: Given the above, decide on a plan of action (a move or attack; decision depends a lot on state)
			
			# Do the things that you do when going towards a target room rather than a specific grid reference
			if self.state == 'head-towards-room' or self.state == 'wander-aimlessly':

 				self.moveTowardsRoom(monster, decider)							

			# Now do things for the other cases!
			elif self.state == 'pursue-visible-target':

				self.engagePlayer(monster, decider)



			# Update various cooldowns and counters and such
			if self.weapon:
				self.weapon.recharge()
			if self.ally_in_the_way_o_meter > 0:
				self.ally_in_the_way_o_meter = self.ally_in_the_way_o_meter - 1
			if self.blocked_by_door_o_meter > 0:
				self.blocked_by_door_o_meter = self.blocked_by_door_o_meter - 1
		if self.stunned_time > 0:
			self.stunned_time = self.stunned_time - 1

	def stun(self):
		self.stunned_time = 2

	# Step 1 of AI process: Decide your current state, and maybe a few other bits.
	def decideState(self, monster):
		# Currently planned possible states:
		# 'guard-duty'			Stay where you are till something comes along
		# 'head-towards-room'		Try and walk towards a target room (generally the one you think player is in)
		# 'wander-aimlessly'		Pick adjacent rooms at random to walk into, preferably avoiding the previous room
		# 'pursue-visible-target'	When the player is near you, go towards them! Includes attacking?	
		# 'flee-visible-danger'		Run away from a thing you can see (the player, when you're scared of them?)
	
		#keeping it pretty simple for now... pursue the player if you see them
		#if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
		if fov_map.fov[monster.x, monster.y]:
			self.state = 'pursue-visible-target'
		elif self.state == 'pursue-visible-target':	#go to room-based targeting
			self.state = 'wander-aimlessly'		
			# because we could see the player a second ago, we assule the player has just run 'round the corner' 
			# and so we think we know what roomthe player is in
			self.target_room = nearest_points_array[player.x][player.y] 	
		elif self.state == 'flee-visible-danger':
			self.state = 'wander-aimlessly'	
			# as we just ran out of sight of player, prioritise not being in the room they're in	
			self.previous_room = nearest_points_array[player.x][player.y] 	
			



	# Step 2 of AI process: Now you know your state, decide your target (either a room or a specific space).
	# Maybe generally update navigation stuff here as well?
	def decideTarget(self, monster):
		current_room = nearest_points_array[monster.x][monster.y]
		if  self.state == 'pursue-visible-target' or self.state == 'flee-visible-danger': 
			self.target_x = player.x
			self.target_y = player.y
		elif self.target_room  == None or self.target_room == current_room:	#pick a new target room if you need to...
			self.target_room  =   AI_choose_adjacent_room(self)
			self.previous_room = current_room


	# Part of Step 3: Do the things that you do when going towards a target room rather than a specific grid reference
	def moveTowardsRoom(self, monster, decider):
		# Choose an option that gets you closest to where you want to go
		((dx,dy), return_message) =  next_step_based_on_target(monster.x, monster.y, target_center = self.target_room, aiming_for_center = True, prioritise_visible = False, prioritise_straight_lines = True, rook_moves = False, request_message = True)

		# Move if possible
		block = is_blocked(monster.x+dx, monster.y+dy, care_about_doors = True,  care_about_fighters = True) 
		if block == False: 
			decider.decision = Decision(move_decision=Move_Decision(dx,dy))

		# If the door is closed, maybe try to open it (do we need to give up after a while?)
		elif block == 'closed-door':
			self.blocked_by_door_o_meter = self.blocked_by_door_o_meter + 2
			#try to open the door, maybe
			num  = randint( 0, 1)
			if num == 0:
				decider.decision = Decision(move_decision=Move_Decision(dx,dy))
			# or, if not, maybe you want to give up and try something else?
			if self.blocked_by_door_o_meter > self.impatience_threshold_for_doors_being_in_the_way:
				self.state = 'wander-aimlessly'
				self.target_room = AI_choose_adjacent_room(self)

		#if there's actually nothing to do, give up and try going somewhere new?
		if return_message == "No good options": 
			self.state = 'wander-aimlessly'
			self.target_room = AI_choose_adjacent_room(self)
				
		# if other fighters are blocking the way, eventually get impatient and go elsewhere
		elif return_message == "Fighter blocking best option":  #get annoyed by blocky coworker
			self.ally_in_the_way_o_meter = self.ally_in_the_way_o_meter + 3	
			# Why 3? To avoid cycling back and forth when there's someone in the way
			# Try going somewhere else if you've been blocked like this for a while
			if self.ally_in_the_way_o_meter > self.impatience_threshold_for_allies_being_in_the_way:
				self.state = 'wander-aimlessly'
				self.target_room = AI_choose_adjacent_room(self)

	# Part of Step 3: do the things you can do when you see the player!
	def engagePlayer(self, monster, decider):
		# First off, see if you can attack the player from where you are
		attackList = self.possibleAttackList(monster, decider)

		# Now we know if attacking is possible, and have built up a list of attacks:
		# if there are some attacks we could do, pick one
		if len(attackList) > 0:
			command_choice = random.choice(tuple(attackList))	#returns arbitrary element from candidate_set
			abstract_attack_data = self.weapon.do_attack(command_choice)
			# now do the attack! or, you know, decide to
			chosen_attack_list = process_abstract_attack_data(monster.x,monster.y, abstract_attack_data, monster)	
			decider.decision = Decision(attack_decision = Attack_Decision(attack_list=chosen_attack_list))

		# otherwise, walk towards the player if possible.
		elif monster.distance_to(player) > 1: 	#cutting this condition makes enemies move around player when they can't attack. Might be worth considering for smarter : harder enemies.
			(dx,dy) = next_step_based_on_target(monster.x, monster.y, target_x = player.x, target_y = player.y, aiming_for_center = False, prioritise_visible = True, prioritise_straight_lines = True, rook_moves = False, return_message = None)
			decider.decision = Decision(move_decision=Move_Decision(dx,dy))
	





	# returns what possible attacks you can make that would hit the player
	def possibleAttackList(self, monster, decider):
		attackList = []
		# Is the player alive and do you have enough 'weapon charge'?
		# AND are you not in water?
		if player.fighter.hp >= 0 and self.weapon.current_charge >= self.weapon.default_usage and not monster.fighter.in_water:
			# figure out the vector that the player is from you
			dist_x = self.target_x  - monster.x
			dist_y = self.target_y  - monster.y

			# ok, now see if any of your attacks could hit the player
			# TODO: optimising the weapon code to avoid all these loops might be nice some time
			for (temp_command, temp_abstract_attack_data, temp_usage) in self.weapon.command_items:
				for (temp_x,temp_y, temp_damage) in temp_abstract_attack_data:
					if temp_x == dist_x and temp_y == dist_y and temp_damage > 0:	#then this attack command could work
						# here's a bad hack to get round a bad hack
						# (avoid giving extra weight to down attacks just because there's two buttons for it)
						if temp_command != ATTCKDOWNALT:  
							attackList.append(temp_command)
							break

		return attackList


# A version of BasicMonster that has no access to level navigation data!
# For use in the tutorial, where currently no such navigation data exists
class StupidBasicMonster(BasicMonster):

	def decide(self):
		#a basic monster takes its turn. If you can see it, it can see you
		decider = self.owner
		monster = decider.owner #yaaay
		# only do thing (including weapon recharge? maybe not) if not stunned
		if self.stunned_time <= 0:

			#basically, attack the player if you can see them, and that's about it.
			# if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
			if fov_map.fov[monster.x, monster.y]:
				self.state == 'pursue-visible-target'
				self.engagePlayer(monster, decider)



			# Update various cooldowns and counters and such
			if self.weapon:
				self.weapon.recharge()
			if self.ally_in_the_way_o_meter > 0:
				self.ally_in_the_way_o_meter = self.ally_in_the_way_o_meter - 1
			if self.blocked_by_door_o_meter > 0:
				self.blocked_by_door_o_meter = self.blocked_by_door_o_meter - 1
		if self.stunned_time > 0:
			self.stunned_time = self.stunned_time - 1


#As part of an initial experiment in sorting my AI code the heck out, let's make the Boman basically have default behaviours except they like to move diagonally.
class Boman_AI(BasicMonster):
	
	def engagePlayer(self, monster, decider):
		# First off, see if you can attack the player from where you are
		attackList = self.possibleAttackList(monster, decider)

		# Now we know if attacking is possible, and have built up a list of attacks:
		# if there are some attacks we could do, pick one
		if len(attackList) > 0:
			command_choice = random.choice(tuple(attackList))	#returns arbitrary element from candidate_set
			abstract_attack_data = self.weapon.do_attack(command_choice)
			# now do the attack! or, you know, decide to
			chosen_attack_list = process_abstract_attack_data(monster.x,monster.y, abstract_attack_data, monster)	
			decider.decision = Decision(attack_decision = Attack_Decision(attack_list=chosen_attack_list))

		# otherwise, walk towards the player if possible.
		elif monster.distance_to(player) > 1: 	
			
			#take list of possible good moves, then prioritise diagonal ones
			move_shortlist = next_step_based_on_target(monster.x, monster.y, target_x = player.x, target_y = player.y, aiming_for_center = False, prioritise_visible = True, prioritise_straight_lines = False, rook_moves = False, return_message = None, request_shortlist = True)
			shorterlist = []
			for (dx,dy) in  move_shortlist:
				if dx != 0 and dy != 0:
					shorterlist.append((dx,dy))
			# are there diagonal moves? then let's say will do one of those.
			if len(shorterlist) > 0 :
				move_shortlist = shorterlist

			#Furthermore, try to restrict to moves that will let you approach the player from a diagonal direction.
			#TODO NOTE: This isn't working quite as intended yet
			opt_diagonality =  max(math.fabs(monster.x - player.x),math.fabs(monster.y - player.y))
			shorterlist = []
			for (dx,dy) in  move_shortlist:
				#how far away from being 'on the diagonal' is this move?
				temp_diagonality = math.fabs(math.fabs(monster.x + dx - player.x) - math.fabs(monster.y + dy - player.y))
				# restrict to moves that are closest to being 'on the diagonal'
				if temp_diagonality < opt_diagonality:
					shorter_list = []
					shorterlist.append((dx,dy))
				elif temp_diagonality == opt_diagonality:
					shorterlist.append((dx,dy))
			if len(shorterlist) > 0 :
				move_shortlist = shorterlist
			try:
				(dx,dy) = random.choice(tuple(move_shortlist))
			except IndexError:
				print('oh no index error!!' + str(len(move_shortlist)) + ', ' + str(move_shortlist))

			decider.decision = Decision(move_decision=Move_Decision(dx,dy))




class Rogue_AI(BasicMonster):

	# Rogue AI  uses Sai. Often attacks at a distance in hopes the player will walk into their attacks.
	# So there is some overlap with ninjas and tridentors at the moment.
	# Sadyl does not do anything particularly roguey at present

	def engagePlayer(self, monster, decider):
		
		#get data for where player is
#		abstract_attack_data = None
		xdiff = player.x - monster.x
		ydiff = player.y - monster.y
		xdiffabs = xdiff
		ydiffabs = ydiff
		xunit = 1
		yunit = 1
		if xdiff < 0:
			xdiffabs = -xdiff
			xunit = -1
		if ydiff < 0:
			ydiffabs = -ydiff 
			yunit = -1
	

		dx = None
		dy = None


		# Otherwise, do a left or right attack, depending on where the player is.

		# If x distance from player is more than 2, walk horizontally towards player.
		if xdiffabs > 2:
			dx = xunit
			dy = 0
		# If x co_ord is equal to that of the player, move left or right! We don't want to be vertically in line with the player.
		elif xdiffabs == 0:
			num =  randint( 0, 1)
			if num == 0:
				dx = xunit
				dy = 0
			else:
				dx = -xunit
				dy = 0
		# Otherwise, if the y distance is less than that of the player, walk vertically towards the player.
		elif ydiffabs > 2:
			dx = 0
			dy = yunit

		# try and do the movement preferences above, if you picked one.
		if dx is not None and dy is not None:
			# if you want to move but the preferred option is blocked, just move towards player
			if is_blocked(monster.x + dx,monster.y + dy):
				(ddx,ddy) =  Move_Towards_Visible_Player(monster.x, monster.y)
				dx = ddx
				dy = ddy
			decider.decision = Decision(move_decision=Move_Decision(dx,dy))


		# in this case you decided not to move. So you must want to attack!
		else:

			# by default, don't move. But try and do an attack as described below.
			decider.decision = Decision(move_decision=Move_Decision(0,0))

			# If the player is one or two steps from me, do one of the following attacks
			if xdiffabs <=2 and ydiffabs <= 2: 
				#if near to the player, and I have charge, then attack!
				if self.weapon.current_charge >= self.weapon.default_usage:
					attack_command = 0

					# attack to left if player is on left, or right if player on right.
					# otherwise, shouldn't normally be in this situation, but again attack up or down.
					# But maybe actually do a direct attack on player if  they are next to you? hmm.

					num =  randint( 0, 1)
					if num == 0:
						rQr = oWo
						rWr = oEo
						rEr = oDo
						rDr = oCo
						rCr = oXo
						rXr = oZo
						rZr = oAo
						rAr = oQo
					else:
						rQr = oAo
						rWr = oQo
						rEr = oWo
						rDr = oEo
						rCr = oDo
						rXr = oCo
						rZr = oXo
						rAr = oZo
					attack_array = [[oAo,oAo,oWo,oDo,oDo],
							[oAo,oAo,rWr,oDo,oDo],
							[oAo,rAr, 0 ,rDr,oDo],
							[oAo,oAo,rXr,oDo,oDo],
							[oAo,oAo,oXo,oDo,oDo]]
					attack_command = attack_array[ydiff+2][xdiff+2]


		#			num =  randint( 0, 1)
		#			if num == 0:
		#				rQr = oWo
		#				rWr = oEo
		#				rEr = oDo
		#				rDr = oCo
		#				rCr = oXo
		#				rXr = oZo
		#				rZr = oAo
		#				rAr = oQo
		#			else:
		#				rQr = oAo
		#				rWr = oQo
		#				rEr = oWo
		#				rDr = oEo
		#				rCr = oDo
		#				rXr = oCo
		#				rZr = oXo
		#				rAr = oZo
		#			attack_array = [[rQr,oWo,oWo,oWo,rEr],
		#					[oAo,rQr,rWr,rEr,oDo],
		#					[oAo,rAr, 0 ,rDr,oDo],
		#					[oAo,rZr,rXr,rCr,oDo],
		#					[rZr,oXo,oXo,oXo,rCr]]
		#			attack_command = attack_array[ydiff+2][xdiff+2]
	
					#carry out attack
					if attack_command != 0:
						abstract_attack_data = self.weapon.do_attack(attack_command)
							
					if abstract_attack_data is not None:
						temp_attack_list = process_abstract_attack_data(monster.x,monster.y, abstract_attack_data, monster)		
						decider.decision = Decision(attack_decision = Attack_Decision(attack_list=temp_attack_list))


#	
#				(dx,dy) = next_step_based_on_target(monster.x, monster.y, target_x = player.x, target_y = player.y, aiming_for_center = False, prioritise_visible = True, prioritise_straight_lines = True, rook_moves = False, return_message = None)
#				decider.decision = Decision(move_decision=Move_Decision(dx,dy))
		
	
	
class Tridentor_AI(BasicMonster):


	# Tridentor AI is bit more predictable than the BasicMonster AI would be (doesn't randomly choose between the 3 options that would fit),
	# also tries an attack if there's a step between them and the player... and maybe backs away if an attack is not possible?...
	def engagePlayer(self, monster, decider):
		
		#get data for where player is
#		abstract_attack_data = None
		xdiff = player.x - monster.x
		ydiff = player.y - monster.y
		xdiffabs = xdiff
		if xdiff < 0:
			xdiffabs = -xdiff
		ydiffabs = ydiff
		if ydiff < 0:
			ydiffabs = -ydiff 

		
		# If the player is one or two steps from me, either to a specified attack, or retreat if I have no charge 
		if xdiffabs <=2 and ydiffabs <= 2:  # or self.weapon.current_charge < self.weapon.default_usage
			#if near to the player, and I have charge, then attack!
			if self.weapon.current_charge >= self.weapon.default_usage:
				attack_command = 0
				#if the player has charge, try and hit the square where they're standing (because it's likely they'll stay still and attack me)
				# Do one of these attacks, based on where player is (try and hit them square on if they are next to you,
				# hit to either side of straight on if they are 1 step away on a cardinal axis, 
				# hit towards them if the are diagonally one step away
				attack_array = [[oQo,oXo,oXo,oXo,oEo],
						[oDo,oQo,oWo,oEo,oQo],
						[oDo,oQo, 0 ,oDo,oQo],
						[oDo,oZo,oXo,oCo,oQo],
						[oZo,oWo,oWo,oWo,oCo]]
				attack_command = attack_array[ydiff+2][xdiff+2]

				#carry out attack
				if attack_command != 0:
					abstract_attack_data = self.weapon.do_attack(attack_command)
						
				if abstract_attack_data is not None:
					temp_attack_list = process_abstract_attack_data(monster.x,monster.y, abstract_attack_data, monster)	
					decider.decision = Decision(attack_decision = Attack_Decision(attack_list=temp_attack_list))

			# can't attack but the player is next to you? then step back
			# commented out for now - too tricksy / annoying for what is basically meant to be an upgrade to the basic mook
			elif xdiffabs <=1 and ydiffabs <= 1:
			
				(dx,dy) = Run_Away_From_Visible_Player(monster.x, monster.y)
				decider.decision = Decision(move_decision=Move_Decision(dx,dy))

			# otherwise, close the distance to player 
			elif monster.distance_to(player) > 1: 
				(dx,dy) = next_step_based_on_target(monster.x, monster.y, target_x = player.x, target_y = player.y, aiming_for_center = False, prioritise_visible = True, prioritise_straight_lines = True, rook_moves = False, return_message = None)
				decider.decision = Decision(move_decision=Move_Decision(dx,dy))
		# otherwise, walk towards the player if possible.
		else:

			(dx,dy) = next_step_based_on_target(monster.x, monster.y, target_x = player.x, target_y = player.y, aiming_for_center = False, prioritise_visible = True, prioritise_straight_lines = True, rook_moves = False, return_message = None)
			decider.decision = Decision(move_decision=Move_Decision(dx,dy))
	


class Wizard_AI:
	def __init__(self, weapon):
		self.recharge_time = 0
		self.stunned_time = 0
		self.weapon = weapon
		if self.weapon is not None:
			self.weapon.owner = self
	def decide(self):

		decider = self.owner
		monster = decider.owner 

		# wizard basically has 3 modes, depending on what the charge on your weapon (the ring of power) is.
		# If there is <1 charge left, run away from the player


		if self.stunned_time <= 0:
			# if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
			if fov_map.fov[monster.x, monster.y]:
				dx = 0
				dy = 0
				#if True:			
				if self.weapon.current_charge < self.weapon.default_usage:
					(dx,dy) = Run_Away_From_Visible_Player(monster.x, monster.y)
					decider.decision = Decision(move_decision=Move_Decision(dx,dy))
			

				elif self.weapon.current_charge <= 2*self.weapon.default_usage:
					# stay still, but if the player gets near then attack
					abstract_attack_data = None
					xdiff = player.x - monster.x
					ydiff = player.y - monster.y
					xdiffabs = xdiff
					if xdiff < 0:
						xdiffabs = -xdiff
					ydiffabs = ydiff
					if ydiff < 0:
						ydiffabs = -ydiff
					if xdiff < 3 and xdiff > -3 and ydiff < 3 and ydiff > -3:
						#alright close enough, attack!!!
						if (xdiffabs > ydiffabs + 1 or ydiff == 0) and xdiff > 0:
							abstract_attack_data = self.weapon.do_attack(ATTCKRIGHT)
						elif (xdiffabs > ydiffabs + 1 or ydiff == 0) and xdiff < 0:
							abstract_attack_data = self.weapon.do_attack(ATTCKLEFT)
						elif (ydiffabs > xdiffabs + 1 or xdiff == 0) and ydiff > 0:
							abstract_attack_data = self.weapon.do_attack(ATTCKDOWN)
						elif (ydiffabs > xdiffabs + 1 or xdiff == 0) and ydiff < 0:
							abstract_attack_data = self.weapon.do_attack(ATTCKUP)

						#ok, so now x and y diff are close, so we are shooting diagonally
						elif xdiff > 0 and ydiff > 0:
							abstract_attack_data = self.weapon.do_attack(ATTCKDOWNRIGHT)
						elif xdiff > 0 and ydiff < 0:
							abstract_attack_data = self.weapon.do_attack(ATTCKUPRIGHT)
						elif xdiff < 0 and ydiff < 0:
							abstract_attack_data = self.weapon.do_attack(ATTCKUPLEFT)
						elif xdiff < 0 and ydiff > 0:
							abstract_attack_data = self.weapon.do_attack(ATTCKDOWNLEFT)

						if abstract_attack_data is not None:
							temp_attack_list = process_abstract_attack_data(monster.x,monster.y, abstract_attack_data, monster)	
							decider.decision = Decision(attack_decision = Attack_Decision(attack_list=temp_attack_list))
				
				else:
					# we have the power! Start attacking the player if they get in range and walking towards the player
					abstract_attack_data = None
					xdiff = player.x - monster.x
					ydiff = player.y - monster.y
					xdiffabs = xdiff
					if xdiff < 0:
						xdiffabs = -xdiff
					ydiffabs = ydiff
					if ydiff < 0:
						ydiffabs = -ydiff
					if xdiff < 5 and xdiff > -5 and ydiff < 5 and ydiff > -5:
						#alright close enough, attack!!!
						if (xdiffabs > ydiffabs + 1 or ydiff == 0) and xdiff > 0:
							abstract_attack_data = self.weapon.do_attack(ATTCKRIGHT)
						elif (xdiffabs > ydiffabs + 1 or ydiff == 0) and xdiff < 0:
							abstract_attack_data = self.weapon.do_attack(ATTCKLEFT)
						elif (ydiffabs > xdiffabs + 1 or xdiff == 0) and ydiff > 0:
							abstract_attack_data = self.weapon.do_attack(ATTCKDOWN)
						elif (ydiffabs > xdiffabs + 1 or xdiff == 0) and ydiff < 0:
							abstract_attack_data = self.weapon.do_attack(ATTCKUP)

						#ok, so now x and y diff are close, so we are shooting diagonally
						elif xdiff > 0 and ydiff > 0:
							abstract_attack_data = self.weapon.do_attack(ATTCKDOWNRIGHT)
						elif xdiff > 0 and ydiff < 0:
							abstract_attack_data = self.weapon.do_attack(ATTCKUPRIGHT)
						elif xdiff < 0 and ydiff < 0:
							abstract_attack_data = self.weapon.do_attack(ATTCKUPLEFT)
						elif xdiff < 0 and ydiff > 0:
							abstract_attack_data = self.weapon.do_attack(ATTCKDOWNLEFT)

						if abstract_attack_data is not None:
							temp_attack_list = process_abstract_attack_data(monster.x,monster.y, abstract_attack_data, monster)	
							decider.decision = Decision(attack_decision = Attack_Decision(attack_list=temp_attack_list))
					else:
						# if the player isn't near enough, walk towards them.
						(dx,dy) = Move_Towards_Visible_Player(monster.x, monster.y)
						decider.decision = Decision(move_decision=Move_Decision(dx,dy))



				#		# ok fine, the player's not close enough. Walk towards them then!
				#		# Just gonna copy BasicMonster ai for now...
				#		(dx,dy) = next_step_towards(monster.x, monster.y, player.x, player.y)
				#		# only walk if there's not something in the way. controversial maybe!
				#		if is_blocked(monster.x+dx, monster.y+dy) == False:
				#			decider.decision = Decision(move_decision=Move_Decision(dx,dy))
				#		# here begins a microhack to fix the AI getting stuck on corners
				#		else:
				#			xdiff = player.x - monster.x
				#			ydiff = player.y - monster.y
				#			if xdiff > 0:
				#				xdiff = 1
				#			elif xdiff < 0:
				#				xdiff = -1
	#
	#						if ydiff > 0:
	#							ydiff = 1
	#						elif ydiff < 0:
	#							ydiff = -1
	#						if is_blocked(monster.x+xdiff, monster.y+ydiff) == False:
	#							decider.decision = Decision(move_decision=Move_Decision(xdiff,ydiff))

			if self.weapon:
				self.weapon.recharge()
		if self.stunned_time > 0:
			self.stunned_time = self.stunned_time - 1



	def stun(self):
		# TODO probably wizards shouldn't be too easy to stun
		self.stunned_time = 2


class Samurai_AI:
	# a samurai with a katana! Intended to be a bit smarter than most enemies. We'll see.
	def __init__(self, weapon):
		self.recharge_time = 0
		self.stunned_time = 0
		self.weapon = weapon
		if self.weapon is not None:
			self.weapon.owner = self
	def decide(self):

		decider = self.owner
		monster = decider.owner 


		if self.stunned_time <= 0:
			#if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
			if fov_map.fov[monster.x, monster.y]:


				#outline of plan for samurai:
				# I'm going to cheat and see if the player has enough charge for their weapon. Sneaky, but maybe the samurai is a weapons expert?
				#if next to the player, and I have charge, then attack!
					#if the player has charge, try and hit the square where they're standing (because it's likely they'll stay still and attack you)
					#if the player doesn't have charge, try and cover the squares they might run away to, rather than the square they're standing in (because players tend to run if they can't fight)
				
				# if next to the player, and I don't have charge:
					#if the player has charge... try and sneak around them? aim for another square next to the player..
					# if the player has no charge, try and run into them! You'll either punch them (if that's implemented??) or at least keep up the pressure

				# if the player is far away, run towards them, obviously.

				# if the player is like 2 spaces away...???
					#if they have charge:
						#if i have charge and can reach them, then attack?
						# otherwise, circle around them! certainly don't run straight towards them like all those other idiots
					# if they don't have charge: run towards them?
			
				# ok this sounds like a plan

				dx = 0
				dy = 0

				abstract_attack_data = None
				xdiff = player.x - monster.x
				ydiff = player.y - monster.y
				xdiffabs = xdiff
				if xdiff < 0:
					xdiffabs = -xdiff
				ydiffabs = ydiff
				if ydiff < 0:
					ydiffabs = -ydiff 

				# decide whether you think the player has their weapon charge by straight up checking if the player has their weapon charged
				# Update: ok. currently there's a problem because it seems this ai method is called after the player's decided their action. So currently it thinks the player is not ready to attack only if the player is attacking right now. which is exactly the wrong time to think that...
				#New method: check and see if an attack from the player currently exists. If so, we reckon the player will not be ready to attack again. This might lead to some stupid behaviour if player projectiles ever become a thing. Easily tricked with items like the sword that can be used twice. Which is probably a relief.
				# Man, maybe it's just that I haven't figured out how to play around them yet, but samurai seem tough!
				believe_player_ready = True
				if player_just_attacked:
					believe_player_ready = False
				
				# Is the player right next to me? 
				if xdiffabs <=1 and ydiffabs <= 1:  # or self.weapon.current_charge < self.weapon.default_usage

					#if next to the player, and I have charge, then attack!
					if self.weapon.current_charge >= self.weapon.default_usage:
						attack_command = 0
						#if the player has charge, try and hit the square where they're standing (because it's likely they'll stay still and attack me)
						if believe_player_ready:
							num  = randint( 0, 2)
							if num == 0:
								attack_array = [[oQo,oQo,oWo,oEo,oEo],
										[oQo,oQo,oQo,oEo,oEo],
										[oAo,oZo, 0 ,oEo,oDo],
										[oZo,oZo,oCo,oCo,oCo],
										[oZo,oZo,oXo,oCo,oCo]]
							else:
								attack_array = [[oAo,oWo,oWo,oWo,oWo],
										[oAo,oQo,oQo,oEo,oDo],
										[oAo,oZo, 0 ,oEo,oDo],
										[oAo,oZo,oCo,oCo,oDo],
										[oXo,oXo,oXo,oXo,oDo]]
							attack_command = attack_array[ydiff+2][xdiff+2]
	
						#if the player doesn't have charge, try and cover the squares they might run away to, rather than the square they're standing in (because players tend to run if they can't fight)
						else: 
							num  = randint( 0, 2)
							if num == 0:
								attack_array = [[ 0 , 0 , 0 , 0 , 0 ],
										[ 0 ,oAo,oWo,oWo, 0 ],
										[ 0 ,oAo, 0 ,oDo, 0 ],
										[ 0 ,oXo,oXo,oDo, 0 ],
										[ 0 , 0 , 0 , 0 , 0 ]]
							else:
								attack_array = [[ 0 , 0 , 0 , 0 , 0 ],
										[ 0 ,oQo,oQo,oEo, 0 ],
										[ 0 ,oZo, 0 ,oEo, 0 ],
										[ 0 ,oZo,oCo,oCo, 0 ],
										[ 0 , 0 , 0 , 0 , 0 ]]
							attack_command = attack_array[ydiff+2][xdiff+2]
						#carry out attack
						if attack_command != 0:
							abstract_attack_data = self.weapon.do_attack(attack_command)
						
						if abstract_attack_data is not None:
							temp_attack_list = process_abstract_attack_data(monster.x,monster.y, abstract_attack_data, monster)	
							decider.decision = Decision(attack_decision = Attack_Decision(attack_list=temp_attack_list))
				
					# if next to the player, and I don't have charge, then do some movement:
					else:
						#if the player has charge... try and sneak around them? aim for another square next to the player..
						if believe_player_ready == True:
							(dx,dy) = Step_Around_Player(monster.x,monster.y)
							#(dx,dy) = Circle_Player_Anticlockwise(monster.x,monster.y)
							decider.decision = Decision(move_decision=Move_Decision(dx,dy))
						# if the player has no charge, try and run into them! You'll either punch them (if that's implemented??) or at least keep up the pressure
						else:
							decider.decision = Decision(move_decision=Move_Decision(xdiff,ydiff))
			#		(dx,dy) = Run_Away_From_Visible_Player(monster.x, monster.y)
			#		decider.decision = Decision(move_decision=Move_Decision(dx,dy))


				
				# is the player 3 squares away but might be about to attack? then spiral them... 
				elif xdiffabs <=3 and ydiffabs <= 3 and believe_player_ready:
					(dx,dy) = Circle_Player_Anticlockwise(monster.x,monster.y)
					decider.decision = Decision(move_decision=Move_Decision(dx,dy))
				#	if self.weapon.current_charge >= self.weapon.default_usage:
#
#						num  = randint( 0, 2)
#						if num == 0:
#							attack_array = [['q','q','w','e','e'],
#									['q','q','w','e','e'],
#									['a','a', 0 ,'d','d'],
#									['z','z','x','c','c'],
#									['z','z','x','c','c']]
#						else:
#							attack_array = [['a','w','w','w','w'],
#									['a','q','w','e','d'],
#									['a','a', 0 ,'d','d'],
#									['a','z','x','c','d'],
#									['x','x','x','x','d']]
#						attack_command = attack_array[ydiff+2][xdiff+2]
#						if attack_command != 0:
#							abstract_attack_data = self.weapon.do_attack(attack_command)
#					
#					if abstract_attack_data is not None:
#						temp_attack_list = process_abstract_attack_data(monster.x,monster.y, abstract_attack_data, monster)	
#						decider.decision = Decision(attack_decision = Attack_Decision(attack_list=temp_attack_list))
				
				
				# Otherwise, the player is too far away, chase them!
				else:
					# Just gonna copy BasicMonster ai for now...
					(dx,dy) = next_step_towards(monster.x, monster.y, player.x, player.y)
					# only walk if there's not something in the way. controversial maybe!
					if is_blocked(monster.x+dx, monster.y+dy) == False:
						decider.decision = Decision(move_decision=Move_Decision(dx,dy))
					# here begins a microhack to fix the AI getting stuck on corners
					else:
						xdiff = player.x - monster.x
						ydiff = player.y - monster.y
						if xdiff > 0:
							xdiff = 1
						elif xdiff < 0:
							xdiff = -1
						if ydiff > 0:
							ydiff = 1
						elif ydiff < 0:
							ydiff = -1
						if is_blocked(monster.x+xdiff, monster.y+ydiff) == False:
							decider.decision = Decision(move_decision=Move_Decision(xdiff,ydiff))
				
			if self.weapon:
				self.weapon.recharge()
		if self.stunned_time > 0:
			self.stunned_time = self.stunned_time - 1

	def stun(self):
		self.stunned_time = 2


class Ninja_AI:
	# here is a stupid ninja that thinks it's a wizard with a long-range weapon. Until I change the code
	def __init__(self, weapon):
		self.recharge_time = 0
		self.stunned_time = 0
		self.weapon = weapon
		if self.weapon is not None:
			self.weapon.owner = self
	def decide(self):

		decider = self.owner
		monster = decider.owner 

		# Ninja will:
		# Actually what will the ninja.
		# If there is no charge... nah.
		# If you have no charge, and the player is enarby, walk away? Or maybe not.
		# If you have charge, and there is one space between you and the player, attack that space.
		# If the player is next to you, walk away!

		if self.stunned_time <= 0:
			#if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
			if fov_map.fov[monster.x, monster.y]:

				dx = 0
				dy = 0

				abstract_attack_data = None
				xdiff = player.x - monster.x
				ydiff = player.y - monster.y
				xdiffabs = xdiff
				if xdiff < 0:
					xdiffabs = -xdiff
				ydiffabs = ydiff
				if ydiff < 0:
					ydiffabs = -ydiff 

				# Is the player right next to you? then run away!
				if xdiffabs <=1 and ydiffabs <= 1:  # or self.weapon.current_charge < self.weapon.default_usage

					(dx,dy) = Run_Away_From_Visible_Player(monster.x, monster.y)
					decider.decision = Decision(move_decision=Move_Decision(dx,dy))


				

				# is the player 2 squares away? Then attack the square in between!
				elif xdiffabs <=2 and ydiffabs <= 2:
					if self.weapon.current_charge >= self.weapon.default_usage:
						if xdiff == 2 and ydiff == 0:
							abstract_attack_data = self.weapon.do_attack(ATTCKRIGHT)
						elif xdiff == -2 and ydiff == 0:
							abstract_attack_data = self.weapon.do_attack(ATTCKLEFT)
						elif xdiff == 0 and ydiff == -2:
							abstract_attack_data = self.weapon.do_attack(ATTCKUP)
						elif xdiff ==0 and ydiff == 2:
							abstract_attack_data = self.weapon.do_attack(ATTCKDOWN)
						elif xdiff == 2 and ydiff == 2:
							abstract_attack_data = self.weapon.do_attack(ATTCKDOWNRIGHT)
						elif xdiff == 2 and ydiff == -2:
							abstract_attack_data = self.weapon.do_attack(ATTCKUPRIGHT)
						elif xdiff == -2 and ydiff == 2:
							abstract_attack_data = self.weapon.do_attack(ATTCKDOWNLEFT)
						elif xdiff == -2 and ydiff == -2:
							abstract_attack_data = self.weapon.do_attack(ATTCKUPLEFT)
						else:
							# okay now there are two choices for square 'in between'... pick one at random? not sure about this
							num  = randint( 0, 2)
							if xdiff == 2 and ydiff == 1:
								if num == 0:
									abstract_attack_data = self.weapon.do_attack(ATTCKRIGHT)
								elif num == 1:
									abstract_attack_data = self.weapon.do_attack(ATTCKDOWNRIGHT)
							elif xdiff == 1 and ydiff == 2:
								if num == 0:
									abstract_attack_data = self.weapon.do_attack(ATTCKDOWN)
								elif num == 1:
									abstract_attack_data = self.weapon.do_attack(ATTCKDOWNRIGHT)
							elif xdiff == -1 and ydiff == 2:
								if num == 0:
									abstract_attack_data = self.weapon.do_attack(ATTCKDOWN)
								elif num == 1:
									abstract_attack_data = self.weapon.do_attack(ATTCKDOWNLEFT)
							elif xdiff == -2 and ydiff == 1:
								if num == 0:
									abstract_attack_data = self.weapon.do_attack(ATTCKLEFT)
								elif num == 1:
									abstract_attack_data = self.weapon.do_attack(ATTCKDOWNLEFT)
							elif xdiff == -2 and ydiff == -1:
								if num == 0:
									abstract_attack_data = self.weapon.do_attack(ATTCKLEFT)
								elif num == 1:
									abstract_attack_data = self.weapon.do_attack(ATTCKUPLEFT)
							elif xdiff == -1 and ydiff == -2:
								if num == 0:
									abstract_attack_data = self.weapon.do_attack(ATTCKUP)
								elif num == 1:
									abstract_attack_data = self.weapon.do_attack(ATTCKUPLEFT)
							elif xdiff == 1 and ydiff == -2:
								if num == 0:
									abstract_attack_data = self.weapon.do_attack(ATTCKUP)
								elif num == 1:
									abstract_attack_data = self.weapon.do_attack(ATTCKUPRIGHT)
							elif xdiff == 2 and ydiff == -1:
								if num == 0:
									abstract_attack_data = self.weapon.do_attack(ATTCKRIGHT)
								elif num == 1:
									abstract_attack_data = self.weapon.do_attack(ATTCKUPRIGHT)
					
					if abstract_attack_data is not None:
						temp_attack_list = process_abstract_attack_data(monster.x,monster.y, abstract_attack_data, monster)	
						decider.decision = Decision(attack_decision = Attack_Decision(attack_list=temp_attack_list))
				
				
				# Otherwise, the player is too far away, chase them!
				else:
					# Just gonna copy BasicMonster ai for now...
					(dx,dy) = next_step_towards(monster.x, monster.y, player.x, player.y)
					# only walk if there's not something in the way. controversial maybe!
					if is_blocked(monster.x+dx, monster.y+dy) == False:
						decider.decision = Decision(move_decision=Move_Decision(dx,dy))
					# here begins a microhack to fix the AI getting stuck on corners
					else:
						xdiff = player.x - monster.x
						ydiff = player.y - monster.y
						if xdiff > 0:
							xdiff = 1
						elif xdiff < 0:
							xdiff = -1
						if ydiff > 0:
							ydiff = 1
						elif ydiff < 0:
							ydiff = -1
						if is_blocked(monster.x+xdiff, monster.y+ydiff) == False:
							decider.decision = Decision(move_decision=Move_Decision(xdiff,ydiff))
				
			if self.weapon:
				self.weapon.recharge()
		if self.stunned_time > 0:
			self.stunned_time = self.stunned_time - 1

	def stun(self):
		self.stunned_time = 2



# A rook acts like a standard enemy, except they can only walk/attack horizontally or vertically, and can attack from a distance of 2 rather than 1.
class Rook_AI:
	global nearest_center_to_player, player

	#AI for a basic monster.
	def __init__(self, weapon, guard_duty):
		self.recharge_time = 0
		self.stunned_time = 0
		self.weapon = weapon
		if self.weapon is not None:
			self.weapon.owner = self
		self.guard_duty = guard_duty

	def decide(self):
		#a basic monster takes its turn. If you can see it, it can see you
		decider = self.owner
		monster = decider.owner #yaaay
		# only do thing (including weapon recharge? maybe not) if not stunned
		if self.stunned_time <= 0:
			
			# if you can't see the player, go where you think the player is
			#if not libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
			if not fov_map.fov[monster.x, monster.y]:

				# but only if you're not on guard duty!
				if self.guard_duty == False:
					(dx,dy) = Head_Towards_Players_Room(monster.x, monster.y, rook_moves = True)
					#if is_blocked(monster.x+dx, monster.y+dy) == False:
					#	decider.decision = Decision(move_decision=Move_Decision(dx,dy))
					block = is_blocked(monster.x+dx, monster.y+dy, care_about_doors = True) 
					if block == False: 
						decider.decision = Decision(move_decision=Move_Decision(dx,dy))
					elif block == 'closed-door':
						num  = randint( 0, 1)
						if num == 0:
							decider.decision = Decision(move_decision=Move_Decision(dx,dy))
	
			else:	
				#As we've now spotted the player, stop being on guard duty
				self.guard_duty = False
				# ok first question. where is the player and how do we get to them?

				dx = 0
				dy = 0



				#move towards player if far away (3 plus) or not in a horizontal or vertical line
				if monster.distance_to(player) >= 3 or (monster.x != player.x and monster.y != player.y):

					(dx,dy) = Move_Towards_Visible_Player(monster.x, monster.y, rook_moves = True)
					decider.decision = Decision(move_decision=Move_Decision(dx,dy))

				

				#close enough, attack! (if the player is still alive.)
				elif player.fighter.hp >= 0 and self.weapon.current_charge >= self.weapon.default_usage:#   recharge_time <= 0:
					attackList = []

					(dx,dy) = next_step_towards(monster.x, monster.y, player.x, player.y)
					
					# and now we manually code what keys the monster would press based on where they want to attack.
					# yes, this isn't great code design. It's a 7drl, deal with it.
					if dx == 0 and dy == -1:
						abstract_attack_data = self.weapon.do_attack(ATTCKUP)
					elif dx == 1 and dy == 0:
						abstract_attack_data = self.weapon.do_attack(ATTCKRIGHT)
					elif dx == 0 and dy == 1:
						abstract_attack_data = self.weapon.do_attack(ATTCKDOWN)
					elif dx == -1 and dy == 0:
						abstract_attack_data = self.weapon.do_attack(ATTCKLEFT)
					else: 
						abstract_attack_data = None
					
					if abstract_attack_data is not None:
						temp_attack_list = process_abstract_attack_data(monster.x,monster.y, abstract_attack_data, monster)	
						decider.decision = Decision(attack_decision = Attack_Decision(attack_list=temp_attack_list))


			if self.weapon:
				self.weapon.recharge()
		if self.stunned_time > 0:
			self.stunned_time = self.stunned_time - 1

	def stun(self):
		self.stunned_time = 2


# A version of ROOK_AI that has no access to level navigation data!
# For use in the tutorial, where currently no such navigation data exists
class Stupid_Rook_AI(Rook_AI):

	def decide(self):
		#a basic monster takes its turn. If you can see it, it can see you
		decider = self.owner
		monster = decider.owner #yaaay
		# only do thing (including weapon recharge? maybe not) if not stunned
		if self.stunned_time <= 0:

			#basically, attack the player if you can see them, and that's about it.
			# if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
			if fov_map.fov[monster.x, monster.y]:
				self.state == 'pursue-visible-target'
				self.engagePlayer(monster, decider)



	#		# Update various cooldowns and counters and such
	#		if self.weapon:
	#			self.weapon.recharge()
	#		if self.ally_in_the_way_o_meter > 0:
	#			self.ally_in_the_way_o_meter = self.ally_in_the_way_o_meter - 1
	#		if self.blocked_by_door_o_meter > 0:
	#			self.blocked_by_door_o_meter = self.blocked_by_door_o_meter - 1
		if self.stunned_time > 0:
			self.stunned_time = self.stunned_time - 1



class Strawman_on_wheels_AI:
	def __init__(self, weapon):
		self.recharge_time = 0
		self.stunned_time = 0
		self.weapon = weapon
		if self.weapon is not None:
			self.weapon.owner = self
		num  = randint( 0, 4)
		if num == 0:
			self.direction = 'left'
		elif num == 1:
			self.direction = 'up'
		elif num == 2:
			self.direction = 'right'
		else:
			self.direction = 'down'


	def decide(self):
		#a basic monster takes its turn. If you can see it, it can see you
		decider = self.owner
		monster = decider.owner 
		# try and move in the direction you're going, otherwise reverse
		if self.direction == 'left':
			if is_blocked(monster.x-1, monster.y):
				self.direction = 'right'
				decider.decision = Decision(move_decision=Move_Decision(1,0))
			else:
				decider.decision = Decision(move_decision=Move_Decision(-1,0))
		elif 	self.direction == 'right':
			if is_blocked(monster.x+1, monster.y):
				self.direction = 'left'
				decider.decision = Decision(move_decision=Move_Decision(-1,0))
			else:
				decider.decision = Decision(move_decision=Move_Decision(1,0))
		elif self.direction == 'up':
			if is_blocked(monster.x, monster.y-1):
				self.direction = 'down'
				decider.decision = Decision(move_decision=Move_Decision(0,1))
			else:
				decider.decision = Decision(move_decision=Move_Decision(0,-1))
		elif self.direction == 'down':
			if is_blocked(monster.x, monster.y+1):
				self.direction = 'up'
				decider.decision = Decision(move_decision=Move_Decision(0,-1))
			else:
				decider.decision = Decision(move_decision=Move_Decision(0,1))	


		if self.stunned_time > 0:
			self.stunned_time = self.stunned_time - 1


	def stun(self):
		self.stunned_time = 2

class Strawman_AI:
	def __init__(self, weapon, command = ATTCKUP):
		self.recharge_time = 0
		self.stunned_time = 0
		self.weapon = weapon
		if self.weapon is not None:
			self.weapon.owner = self
		self.command = command

	def decide(self):
		#a basic monster takes its turn. If you can see it, it can see you
		decider = self.owner
		monster = decider.owner #yaaay
		# if you have a weapon, use it stupidly when you can
		if self.weapon is not None and self.stunned_time <= 0:
			if self.weapon.current_charge >= self.weapon.default_usage:
				abstract_attack_data = self.weapon.do_attack(self.command)

				if abstract_attack_data is not None:
					temp_attack_list = process_abstract_attack_data(monster.x,monster.y, abstract_attack_data, monster)	
					decider.decision = Decision(attack_decision = Attack_Decision(attack_list=temp_attack_list))
			if self.weapon:
				self.weapon.recharge()
		if self.stunned_time > 0:
			self.stunned_time = self.stunned_time - 1


	def stun(self):
		self.stunned_time = 2



# returns the next space to head into if you want to head towards the player, but can't see them (based on the last known 'center point' of player)
def Head_Towards_Players_Room(current_x, current_y, rook_moves = False):
	(dx,dy) = next_step_towards_center(current_x, current_y, nearest_center_to_player, rook_moves)
	return (dx,dy)


def Move_Towards_Visible_Player(current_x, current_y, rook_moves = False):
	(dx,dy) = next_step_towards(current_x, current_y, player.x, player.y, rook_moves)
	# only walk if there's not something in the way. controversial maybe!
	if is_blocked(current_x+dx, current_y+dy) == False:
		#decider.decision = Decision(move_decision=Move_Decision(dx,dy))
		return (dx,dy)
	# here begins a microhack to fix the AI getting stuck on corners
	else:
		xdiff = player.x - current_x
		ydiff = player.y - current_y
		if xdiff > 0:
			xdiff = 1
		elif xdiff < 0:
			xdiff = -1
		if ydiff > 0:
			ydiff = 1
		elif ydiff < 0:
			ydiff = -1
		if is_blocked(current_x+xdiff, current_y+ydiff) == False and rook_moves == False:
			return(xdiff,ydiff)
		elif rook_moves == True:
			if is_blocked(current_x, current_y+ydiff) == False and is_blocked(current_x+xdiff, current_y) == True:
				return (0, ydiff)
			elif is_blocked(current_x, current_y+ydiff) == True and is_blocked(current_x+xdiff, current_y) == False:
				return (xdiff, 0)
			elif is_blocked(current_x, current_y+ydiff) == False and is_blocked(current_x+xdiff, current_y) == False:
				num =  randint( 0, 2) 
				if num == 0:
					return (xdiff,0)
				else:
					return(0,ydiff)
			else:
				return (0,0)	
		else:
			return(0,0)

def Run_Away_From_Visible_Player(current_x, current_y):
	dx = 0
	dy = 0
	if current_x < player.x:
		dx = -1
	elif current_x > player.x:
		dx = 1
	if current_y < player.y:
		dy = -1
	elif current_y > player.y:
		dy = 1
		
	if is_blocked(current_x+dx, current_y+dy) == False:
		return (dx,dy)
		# and now let's add some 'not getting stuck on a wall' magic
	elif dy != 0 and dx != 0:
		# if trying to move diagonally, try going in one direction or the other instead
		if is_blocked(current_x, current_y+dy) == False and  is_blocked(current_x+dx, current_y) == True:
			return (0,dy)
		elif is_blocked(current_x, current_y+dy) == True and  is_blocked(current_x+dx, current_y) == False:
			return (dx,0)
		elif is_blocked(current_x, current_y+dy) == False and  is_blocked(current_x+dx, current_y) == False:
			num =  randint( 0, 2) 
			if num == 0:
				return (dx,0)
			else:
				return(0,dy)
		else:
			return (0,0)

	elif dy!= 0 and dx == 0:
		# if trying to move vertically, try going left or right instead
		num =  randint( 0, 2) 
		if num == 0:
			#bias to going left first
			if  is_blocked(current_x-1, current_y+dy) == False:
				return (-1,dy)
			elif  is_blocked(current_x+1, current_y+dy) == False:
				return(1,dy)
			elif  is_blocked(current_x-1, current_y) == False:
				return (-1,0)
			elif  is_blocked(current_x+1, current_y) == False:
				return(1,0)
			else:
				return (0,0)
		else:
			#bias to going right first
			if  is_blocked(current_x+1, current_y+dy) == False:
				return(1,dy)
			elif is_blocked(current_x-1, current_y+dy) == False:
				return(-1,dy)
			elif  is_blocked(current_x+1, current_y) == False:
				return(1,0)
			elif  is_blocked(current_x-1, current_y) == False:
				return(-1,0)
			else:
				return (0,0)

	elif dy== 0 and dx != 0:
		# if trying to move horizontally, try going left or right instead
		num =  randint( 0, 2) 
		if num == 0:
			#bias to going up first
			if  is_blocked(current_x+dx, current_y-1) == False:
				return(dx,-1)
			elif  is_blocked(current_x+dx, current_y+1) == False:
				return(dx,1)
			elif  is_blocked(current_x, current_y-1) == False:
				return(0,-1)
			elif  is_blocked(current_x, current_y+1) == False:
				return(0,1)
			else:
				return (0,0)
		else:
			#bias to going down first
			if  is_blocked(current_x+dx, current_y+1) == False:
				return(dx,1)
			elif is_blocked(current_x+dx, current_y-1) == False:
				return(dx,-1)
			elif  is_blocked(current_x, current_y+1) == False:
				return(0,1)
			elif  is_blocked(current_x, current_y-1) == False:
				return(0,-1)
			else:
				return (0,0)


#Move from one position next to the player to another position next to the player (useful for if you want to keep next to the player but don't wnt to attack them, and you think they're going to attack you)
def Step_Around_Player(current_x,current_y):
	xdiff = player.x - current_x
	ydiff = player.y - current_y
	xdiffabs = xdiff
	if xdiff < 0:
		xdiffabs = -xdiff
	ydiffabs = ydiff
	if ydiff < 0:
		ydiffabs = -ydiff

	#To start off, let's check that you are in fact next to the player. If not, something went wrong, but whatever, just run towards them.
	if xdiffabs > 1 or ydiffabs > 1:
		return Move_Towards_Visible_Player(current_x, current_y)
	else:
		#make a list of possible places in the immediate vicinity that you could go for. 
		movement_options = []
		for xmov in range(-1,2):		#xmov from -1 to +1. Have I mentioned how much of a pain I find this range function?
			for ymov in range(-1,2):
				#check a bunch of things. is it occupied, is it where the player is, is it not next to the player, is it where you are? If the answer to all these questions is no, it's a place woth jumping to.
				tempx = current_x+xmov
				tempy = current_y+ymov
				if  not is_blocked(tempx, tempy) and (tempx!= player.x or tempy != player.y) and (tempx < player.x +2 and tempx > player.x - 2 and tempy < player.y+2 and tempy > player.y-2) and (xmov !=0 or ymov !=0):
					movement_options.append((xmov,ymov))
					#I'm introducing a bias for stepping around the player diagonally, just because that seems more likely to sidestep an attack most of the time
					if xmov!= 0 and ymov != 0:
						movement_options.append((xmov,ymov))	
		# now pick an option at random
		if len(movement_options) > 0:
			choice =  randint( 0, len(movement_options)-1)
			return movement_options[choice]
		# if there's actually nowhere good to go, maybe run away? Might want to change this depending on the monster
		else:
			return  Run_Away_From_Visible_Player(current_x, current_y)

				
#While 2-3 squares away from player, run around them in a clockwise direction (slowly closing in?)
def Spiral_Player_Clockwise(current_x, current_y):
	xdiff = player.x - current_x
	ydiff = player.y - current_y
	xdiffabs = xdiff
	if xdiff < 0:
		xdiffabs = -xdiff
	ydiffabs = ydiff
	if ydiff < 0:
		ydiffabs = -ydiff

	#Are you sufficiently close to the player? If not, just run towards them.
	if xdiffabs > 3 or ydiffabs > 3:
		return Move_Towards_Visible_Player(current_x, current_y)
	else:
		# movement will be biased towards the entry in this table corresponding to your current position relative to player
		movement_preferences = [[( 1, 0),( 1, 0),( 1, 0),( 1, 0),( 1, 1),( 1, 1),( 0, 1)],
					[( 1,-1),( 1, 0),( 1, 0),( 1, 1),( 1, 1),( 0, 1),( 0, 1)],
					[( 1,-1),( 1,-1),( 1, 0),( 1, 1),( 0, 1),( 0, 1),( 0, 1)],
					[( 0,-1),( 1,-1),( 1,-1),( 0, 0),(-1, 1),(-1, 1),( 0, 1)],
					[( 0,-1),( 0,-1),( 0,-1),(-1,-1),(-1, 0),(-1, 1),(-1, 1)],
					[( 0,-1),( 0,-1),(-1,-1),(-1,-1),(-1, 0),(-1, 0),(-1, 1)],
					[( 0,-1),(-1,-1),(-1,-1),(-1, 0),(-1, 0),(-1, 0),(-1, 0)]]
		(dx,dy) = movement_preferences[-ydiff+3][-xdiff+3]
		#print "distance (" + str(xdiff) + "," + str(ydiff) + ") leading to movement (" + str(dx) + "," + str(dy) + ")."
		if not is_blocked(current_x + dx,current_y + dy):
		#	print "huh"
			return (dx,dy)
		else:	# for now, just run towards player I guess
			return Move_Towards_Visible_Player(current_x, current_y)

#While 2-3 squares away from player, run around them in an anticlockwise direction (slowly closing in?)
def Spiral_Player_Anticlockwise(current_x, current_y):
	xdiff = player.x - current_x
	ydiff = player.y - current_y
	xdiffabs = xdiff
	if xdiff < 0:
		xdiffabs = -xdiff
	ydiffabs = ydiff
	if ydiff < 0:
		ydiffabs = -ydiff

	#Are you sufficiently close to the player? If not, just run towards them.
	if xdiffabs > 3 or ydiffabs > 3:
		return Move_Towards_Visible_Player(current_x, current_y)
	else:
		# movement will be biased towards the entry in this table corresponding to your current position relative to player
		movement_preferences = [[( 0, 1),(-1, 1),(-1, 1),(-1, 0),(-1, 0),(-1, 0),(-1, 0)],
					[( 0, 1),( 0, 1),(-1, 1),(-1, 1),(-1, 0),(-1, 0),(-1,-1)],
					[( 0, 1),( 0, 1),( 0, 1),(-1, 1),(-1, 0),(-1,-1),(-1,-1)],
					[( 0, 1),( 1, 1),( 1, 1),( 0, 0),(-1,-1),(-1,-1),( 0,-1)],
					[( 1, 1),( 1, 1),( 1, 0),( 1,-1),( 0,-1),( 0,-1),( 0,-1)],
					[( 1, 1),( 1, 0),( 1, 0),( 1,-1),( 1,-1),( 0,-1),( 0,-1)],
					[( 1, 0),( 1, 0),( 1, 0),( 1, 0),( 1,-1),( 1,-1),( 0,-1)]]
		(dx,dy) = movement_preferences[-ydiff+3][-xdiff+3]
		#print "distance (" + str(xdiff) + "," + str(ydiff) + ") leading to movement (" + str(dx) + "," + str(dy) + ")."
		if not is_blocked(current_x + dx,current_y + dy):
		#	print "huh"
			return (dx,dy)
		else:	# for now, just run towards player I guess
			return Move_Towards_Visible_Player(current_x, current_y)


#While 2-3 squares away from player, run around them in a clockwise direction (never closing in?)
def Circle_Player_Clockwise(current_x, current_y):
	xdiff = player.x - current_x
	ydiff = player.y - current_y
	xdiffabs = xdiff
	if xdiff < 0:
		xdiffabs = -xdiff
	ydiffabs = ydiff
	if ydiff < 0:
		ydiffabs = -ydiff

	#Are you sufficiently close to the player? If not, just run towards them.
	if xdiffabs > 3 or ydiffabs > 3:
		return Move_Towards_Visible_Player(current_x, current_y)
	else:
		# movement will be biased towards the entry in this table corresponding to your current position relative to player
		movement_preferences = [[( 1, 0),( 1, 0),( 1, 0),( 1, 0),( 1, 1),( 1, 1),( 0, 1)],
					[( 1,-1),( 1,-1),( 1, 0),( 1, 0),( 1, 1),( 1, 1),( 0, 1)],
					[( 1,-1),( 1,-1),( 1, 0),( 1, 1),( 0, 1),( 0, 1),( 0, 1)],
					[( 0,-1),( 0,-1),( 1,-1),( 0, 0),(-1, 1),( 0, 1),( 0, 1)],
					[( 0,-1),( 0,-1),( 0,-1),(-1,-1),(-1, 0),(-1, 1),(-1, 1)],
					[( 0,-1),(-1,-1),(-1,-1),(-1, 0),(-1, 0),(-1, 1),(-1, 1)],
					[( 0,-1),(-1,-1),(-1,-1),(-1, 0),(-1, 0),(-1, 0),(-1, 0)]]
		(dx,dy) = movement_preferences[-ydiff+3][-xdiff+3]
		#print "distance (" + str(xdiff) + "," + str(ydiff) + ") leading to movement (" + str(dx) + "," + str(dy) + ")."
		if not is_blocked(current_x + dx,current_y + dy):
		#	print "huh"
			return (dx,dy)
		else:	# for now, just run towards player I guess
			return Move_Towards_Visible_Player(current_x, current_y)

#While 2-3 squares away from player, run around them in an anticlockwise direction (never slowly closing in?)
def Circle_Player_Anticlockwise(current_x, current_y):
	xdiff = player.x - current_x
	ydiff = player.y - current_y
	xdiffabs = xdiff
	if xdiff < 0:
		xdiffabs = -xdiff
	ydiffabs = ydiff
	if ydiff < 0:
		ydiffabs = -ydiff

	#Are you sufficiently close to the player? If not, just run towards them.
	if xdiffabs > 3 or ydiffabs > 3:
		return Move_Towards_Visible_Player(current_x, current_y)
	else:
		# movement will be biased towards the entry in this table corresponding to your current position relative to player
		movement_preferences = [[( 0, 1),(-1, 1),(-1, 1),(-1, 0),(-1, 0),(-1, 0),(-1, 0)],
					[( 0, 1),(-1, 1),(-1, 1),(-1, 0),(-1, 0),(-1,-1),(-1,-1)],
					[( 0, 1),( 0, 1),( 0, 1),(-1, 1),(-1, 0),(-1,-1),(-1,-1)],
					[( 0, 1),( 0, 1),( 1, 1),( 0, 0),(-1,-1),( 0,-1),( 0,-1)],
					[( 1, 1),( 1, 1),( 1, 0),( 1,-1),( 0,-1),( 0,-1),( 0,-1)],
					[( 1, 1),( 1, 1),( 1, 0),( 1, 0),( 1,-1),( 1,-1),( 0,-1)],
					[( 1, 0),( 1, 0),( 1, 0),( 1, 0),( 1,-1),( 1,-1),( 0,-1)]]
		(dx,dy) = movement_preferences[-ydiff+3][-xdiff+3]
		#print "distance (" + str(xdiff) + "," + str(ydiff) + ") leading to movement (" + str(dx) + "," + str(dy) + ")."
		if not is_blocked(current_x + dx,current_y + dy):
		#	print "huh"
			return (dx,dy)
		else:	# for now, just run towards player I guess
			return Move_Towards_Visible_Player(current_x, current_y)


class BasicAttack:
	#it's an attack. It hangs around for a second, does damage to anyone unlucky enough to be standing in it, and leaves.
	def __init__(self, damage, lifespan = 1, attacker=None):
		self.damage = damage
		self.lifespan = lifespan
		self.attacker = attacker
		self.existing = True
		if attacker.fighter:
			self.color = attacker.fighter.attack_color
			self.faded_color = attacker.fighter.faded_attack_color

	def inflict_damage(self):
		global player_hit_something, alarm_level, spawn_timer
		# only attack if the attack is still active
		if self.lifespan > 0:
			for target in objectsArray[self.owner.x][self.owner.y]:
#			for target in objects:
#				if target.x == self.owner.x and target.y == self.owner.y:
				if target.fighter is not None:
					if self.attacker is not None:
						if target is player:
							message('The ' + self.attacker.name.capitalize() + ' hits!', Color_Dangerous_Combat)	
						elif self.attacker is player:
							message('You hit the ' + target.name.capitalize() + '!', Color_Boring_Combat)
							player_hit_something = True	
						else:
							message('The ' + self.attacker.name.capitalize() + ' hits the ' + target.name.capitalize() + '!', Color_Boring_Combat)
					#add blood! maybe
					#new_blood = Object(target.x, target.y, '~', 'blood', blood_foreground_color, blocks = False, weapon = False, always_visible=False, currently_invisible = True)
					#objectsArray[target.x][target.y].append(new_blood)
					if target.fighter.bleeds:
						bgColorArray[target.x][target.y] = mergeColors(bgColorArray[target.x][target.y], blood_background_color, 0.2)
						#blood splashing around, yaay
						if (target.x > 0):
							bgColorArray[target.x-1][target.y] = mergeColors(bgColorArray[target.x-1][target.y], blood_background_color, 0.1)	
						if (target.x < MAP_WIDTH-1):
							bgColorArray[target.x+1][target.y] = mergeColors(bgColorArray[target.x+1][target.y], blood_background_color, 0.1)
						if (target.y > 0):
							bgColorArray[target.x][target.y-1] = mergeColors(bgColorArray[target.x][target.y-1], blood_background_color, 0.1)
						if (target.y < MAP_HEIGHT-1):
							bgColorArray[target.x][target.y+1] = mergeColors(bgColorArray[target.x][target.y+1], blood_background_color, 0.1)

					translated_console_set_char_background(con, target.x, target.y, self.faded_color, libtcod_BKGND_SET)
					target.fighter.take_damage(self.damage)
#					if target.name == 'security system':
#						if target.raising_alarm is False:
#							target.raising_alarm = True
#							alarm_level += 2
#							message('The security system sounds a loud alarm!')
#							# Let's also run the spawn clock forwards so a fresh wave of enemies arrives
#							spawn_timer = 1	#This is not always working as I'd like???
				elif target.door is not None and target.name != 'elevator door':
					translated_console_set_char_background(con, target.x, target.y, self.faded_color, libtcod_BKGND_SET)
					target.door.take_damage(self.damage)

				if target.alarmer is not None:
					target.alarmer.get_hit()


	def fade(self): 
		# reduce lifespan
		if self.lifespan >= 0:
			self.lifespan = self.lifespan - 1
		# if lifespan is equal to 0, keep a faint version of it around as a reminder
		if self.lifespan == 0:
			attack_object = self.owner
			attack_object.color = self.faded_color
			attack_object.name = 'attack'
			attack_object.send_to_almost_back()			
		# if lifespan is down to 0, destroy the attack
		if self.lifespan < 0:
			self.existing = False

	def find_attackee(self):
		# find the object being attacked, if any
		if self.lifespan > 0:
			for target in objectsArray[self.owner.x][self.owner.y]:
				if target.fighter:
#			for target in objects:
#				if target.fighter and target.x == self.owner.x and target.y == self.owner.y:
					return target
		return None




def process_nearest_center_points():
	global center_points, nearest_points_array
	
	print("PROCESSING NEAREST CENTER POINTS")

	for y in range(MAP_HEIGHT):
		for x in range(MAP_WIDTH):
			if  nearest_points_array[x][y] is not None:
				(temp_x, temp_y) = nearest_points_array[x][y]
				nearest_points_array[x][y] = None
				for i in range(len(center_points)):
					(point_x, point_y) =  center_points[i] 	
					if temp_x == point_x and temp_y == point_y:
						 nearest_points_array[x][y] = i
	

	
		






def next_step_towards_center(current_x, current_y, center_number, rook_moves = False):
	# next step to go to in order to reach a particular 'center point' (e.g. the middle of a room or corridor. Basically a 'we think the player is around here' marker)
	global nav_data, center_points
	
	# make a list of potential places we could go (avoid diagonals if we have rook moves)
	temp_array = []
	if current_x > 0 and nav_data[current_x-1][current_y][center_number] <  nav_data[current_x][current_y][center_number] and not is_blocked(current_x-1, current_y):
		temp_array.append((-1,0))
	if current_x < MAP_WIDTH-1 and nav_data[current_x+1][current_y][center_number] <  nav_data[current_x][current_y][center_number]and not is_blocked(current_x+1, current_y):
		temp_array.append((1,0))
	if current_y > 0 and nav_data[current_x][current_y-1][center_number] <  nav_data[current_x][current_y][center_number]and not is_blocked(current_x, current_y-1):
		temp_array.append((0, -1))
	if current_y < MAP_HEIGHT-1 and nav_data[current_x][current_y+1][center_number] <  nav_data[current_x][current_y][center_number]and not is_blocked(current_x, current_y+1):
		temp_array.append((0,1))
	if  current_x > 0 and  current_y < MAP_HEIGHT-1 and nav_data[current_x-1][current_y+1][center_number] <  nav_data[current_x][current_y][center_number]and not is_blocked(current_x-1, current_y+1) and rook_moves == False:
		temp_array.append((-1,1))
	if  current_x < MAP_WIDTH-1 and  current_y < MAP_HEIGHT-1 and nav_data[current_x+1][current_y+1][center_number] <  nav_data[current_x][current_y][center_number]and not is_blocked(current_x+1, current_y+1) and rook_moves == False:
		temp_array.append((1,1))
	if  current_x < MAP_WIDTH-1 and  current_y > 0 and nav_data[current_x+1][current_y-1][center_number] <  nav_data[current_x][current_y][center_number]and not is_blocked(current_x+1, current_y-1) and rook_moves == False:
		temp_array.append((1,-1))
	if  current_x >0 and  current_y > 0 and nav_data[current_x-1][current_y-1][center_number] <  nav_data[current_x][current_y][center_number]and not is_blocked(current_x-1, current_y-1) and rook_moves == False:
		temp_array.append((-1,-1))

	# for now, rooks will consider walking to places if they are the same distance from the center point. This is a hack to get around the fact that the distance array allows for diagonal moves, which rooks can't do, so sometimes rooks have to pass through two squares of the same distance.
	# This should mean that rooks are a lot slower to get to you but hopefully will get there in the end.
	# It's a hack. What you really want to do is have a separate distance calculation for rook moves, and also spread the calculating out over the first few moves of the level to avoid that long delay at the start of the level.
	#Update: actually it should be enough to only add the following moves if there's no current shortlist. This should avoid rooks e.g. randomly moving north when east was clearly the better option.
	if len(temp_array) == 0 and rook_moves == True:
		if current_x > 0 and nav_data[current_x-1][current_y][center_number] ==  nav_data[current_x][current_y][center_number] and not is_blocked(current_x-1, current_y):
			temp_array.append((-1,0))
		if current_x < MAP_WIDTH-1 and nav_data[current_x+1][current_y][center_number] ==  nav_data[current_x][current_y][center_number]and not is_blocked(current_x+1, current_y):
			temp_array.append((1,0))
		if current_y > 0 and nav_data[current_x][current_y-1][center_number] ==  nav_data[current_x][current_y][center_number]and not is_blocked(current_x, current_y-1):
			temp_array.append((0, -1))
		if current_y < MAP_HEIGHT-1 and nav_data[current_x][current_y+1][center_number] ==  nav_data[current_x][current_y][center_number]and not is_blocked(current_x, current_y+1):
			temp_array.append((0,1))

	# if multiple options, pick one at random. If no options, stay where we are
	if len(temp_array) > 0:
		num =  randint( 0, len(temp_array)-1)
		return temp_array[num] 
	else:
		return (0,0)



def next_step_towards(current_x, current_y, target_x, target_y, rook_moves = False):

	#vector from this object to the target, and distance
	dx = target_x - current_x
	dy = target_y - current_y
	distance = math.sqrt(dx ** 2 + dy ** 2)
		#normalize it to length 1 (preserving direction), then round it and
	#convert to integer so the movement is restricted to the map grid
	if distance != 0:
		dx = int(round(dx / distance))
		dy = int(round(dy / distance))
		if rook_moves == True:	# we can only travel in one axis if rook moves
			if dx != 0 and dy != 0:
				#randomly choose either horizontal or vertical to go with
				num =  randint( 0, 1)
				if num == 0:
					dx = 0
				elif num == 1:
					dy = 0
			
	return(dx, dy)






def next_step_based_on_target(current_x, current_y, target_x = None, target_y = None, target_center = None, aiming_for_center = False, prioritise_visible = False, prioritise_straight_lines = False, rook_moves = False, return_message = None, request_message = False, request_shortlist = False):
	# Make a list of possible moves (in future this might be set as a parameter)
	possible_moves = [(+1,0), (0,-1), (0,+1), (-1,0)]
	if rook_moves == False:
		possible_moves.append((+1,+1))
		possible_moves.append((+1,-1))
		possible_moves.append((-1,+1))
		possible_moves.append((-1,-1))
	
	# Construct list of moves that are closest to target, amongst those that are *at most* as far as current position, and are not blocked
	current_dist = distance_from_target(current_x, current_y, target_x, target_y, target_center, aiming_for_center, rook_moves)
	shortest_dist = current_dist
	shortest_fighter_dist = current_dist + 1	
	shortlist = []
	for (dx,dy) in possible_moves:
		block =  is_blocked(current_x +dx, current_y + dy, care_about_doors = False, care_about_fighters = True)	#hmmm... what's our take on doors here?
		if block == False:
			temp_dist = distance_from_target(current_x +dx, current_y + dy, target_x, target_y, target_center, aiming_for_center, rook_moves)
			if temp_dist < shortest_dist:	#oh hey new minimum
				shortlist = [(dx,dy)]	
				shortest_dist = temp_dist
			elif temp_dist == shortest_dist:	#add to shortlist
				shortlist.append((dx,dy))	
		elif block == 'blocky-fighter':			#and here we track the shortest distance of space blocked by a fighter
			temp_dist = distance_from_target(current_x +dx, current_y + dy, target_x, target_y, target_center, aiming_for_center, rook_moves)
			if temp_dist < shortest_fighter_dist:	#oh hey new minimum
				shortest_fighter_dist = temp_dist

			

	# If prioritising visible, restrict spaces visible to player, if there are any
	if prioritise_visible == True:
		shorterlist = []
		for (dx,dy) in shortlist:
			#if libtcod.map_is_in_fov(fov_map, current_x + dx, current_y + dy):
			if fov_map.fov[current_x + dx, current_y + dy]:
				shorterlist.append((dx,dy))
		if len(shorterlist) > 0:
			shortlist = shorterlist


	# If prioritising straight lines, restrict to only straight line moves if there are any
	if prioritise_straight_lines == True:
		shorterlist = []
		for (dx,dy) in shortlist:
			if dx == 0 or dy == 0:
				shorterlist.append((dx,dy))
		if len(shorterlist) > 0:
			shortlist = shorterlist

#	# Choose from remaining available options at random (should create 'wiggling' when the obvious route is blocked)
#	if len(shortlist) > 0:
#		if request_shortlist == False:
#			chosen_move = random.choice(tuple(shortlist))
#		else:
#			chosen_move = shortlist		#ugh, this hack feels ugly. But yeah, sometimes you might want a shortlist of moves
#	else:	# If there are no  good options, say this in return message
#		chosen_move = (0,0)
#		return_message = "No good options"

	# return either a random move from the shortlist or the shortlist itself, depending on whether request_shortlist is true.
	# (choosing a random thing from the list is a way to create "wiggling" when the obvious route is blocked)
	if request_shortlist == False:
		if len(shortlist) > 0:
			chosen_move = random.choice(tuple(shortlist))
		else:
			#stay still if there's no move
			chosen_move = (0,0)
	else:
		if len(shortlist) > 0:
			chosen_move = shortlist
		else:
			chosen_move = []
			chosen_move.append((0,0))		# TODO / POTENTIAL PROBLEM: Return a list with just (0,0) rather than an empty set.
							# May wish to change this later?

	if shortest_fighter_dist < shortest_dist:		#let people know that someone was standing in the way of best route
		return_message = "Fighter blocking best option"
		# print "yep"
	if request_message == True:
		return (chosen_move, return_message)
	else:
		return chosen_move

	

def distance_from_target(current_x, current_y, target_x = None, target_y = None, center_number = None, aiming_for_center = False, rook_moves = False):
	global nav_data, center_points
	if aiming_for_center == True:	#use nav data to calculate distance to a given room center
		return nav_data[current_x][current_y][center_number]
	else:		#otherwise, assume heading for a visible target across an open room
		if rook_moves == True:
			return math.fabs(current_x - target_x) + math.fabs(current_y - target_y)
		else:
			return max(math.fabs(current_x - target_x), math.fabs(current_y - target_y))





def AI_choose_adjacent_room(AI, allow_previous_room = False):
	global nearest_points_array
	try:
		monster = AI.owner.owner
		current_center = nearest_points_array[monster.x][monster.y]
		if allow_previous_room == True:
			previous_center = None
		else:
			previous_center = AI.previous_center
		return choose_adjacent_room(current_center, previous_center)
	except TypeError:
		return None

def choose_adjacent_room(current_center = 0, previous_center = None, avoid_previous_room = True):
	global room_adjacencies
	#print "current room " + str(current_center) + " adjacencies " + str(room_adjacencies[current_center]) + ", previous " + str(previous_center)
	try:
		candidate_set = room_adjacencies[current_center].copy()
		if previous_center is not None and avoid_previous_room == True:
			if previous_center in candidate_set:
		#		print "removing previous..."
				candidate_set.remove(previous_center)	

		#print "----- updated adjacencies " + str(candidate_set)
		if len(candidate_set) == 0:
			if previous_center is not None:
				return previous_center
			else:
				return current_center
		else:
			new_target = random.choice(tuple(candidate_set))	#returns arbitrary element from candidate_set
			return new_target
	except IndexError:
		return current_center

def get_names_under_mouse():
	global mouse
	#return a string with the names of all objects under the mouse
	(x, y) = (mouse.cx, mouse.cy)

	#create a list with the names of all objects at the mouse's coordinates and in FOV
#	names = [obj.name for obj in objects
#		if obj.x == x and obj.y == y 
#		and libtcod.map_is_in_fov(fov_map, obj.x, obj.y)]			#temporarily forgetting this bit for bugfixing
		#]

	#TODO: this hasn't worked properly in forever, and for now I am just commenting it out because now it's crashing the game.
	# BUt I should maybe fix it some time! probably involving the x_offset type values?
#	names = [obj.name for obj in objectsArray[x][y]
#		and libtcod.map_is_in_fov(fov_map, obj.x, obj.y)]			
#	names = ', '.join(names)  #join the names, separated by commas
	names = ''
	return names.capitalize()



# MAIN CONTROL HANDLING METHOD WOO

#def handle_keys():
def handle_keys(user_input_event):
	global fov_recompute, keys, stairs, player_weapon, game_state, player_action, player_just_attacked, favoured_by_healer, favoured_by_destroyer, tested_by_destroyer,  favoured_by_deliverer, tested_by_deliverer,  destroyer_test_count, deliverer_test_count, time_level_started, key_count, currency_count, already_healed_this_level, TEMP_player_previous_center, something_changed, current_shrine, controlHandler, control_scheme


	# key = translated_console_wait_for_keypress(True)
	key = user_input_event.key
	veekay = key	# key.vk
	key_char = user_input.char
	#if veekay == libtcod.KEY_ENTER and key.lalt:
	if veekay == 'ENTER': #and key.lalt:
	#Alt+Enter: toggle fullscreen
		something_changed = True
		translated_console_set_fullscreen(not translated_console_is_fullscreen())

	elif veekay == 'ESCAPE': #libtcod.KEY_ESCAPE:
		something_changed = True
		return 'pause' #exit game

	if game_state == 'big message':
		if veekay != 0:
			something_changed = True
			game_state = 'playing'

	elif game_state == 'end message':
		if veekay != 0:
			something_changed = True
			game_state = 'end data'


	elif game_state == 'end data':
		if veekay != 0:
			something_changed = True
			game_state = 'restartynscreen'

	elif game_state == 'restartynscreen':
		#key_char = chr(key.c) 
		if key_char == 'n':
			something_changed = True
			game_state='exit'
		elif key_char == 'y':
			something_changed = True
			restart_game()

		

	elif game_state == 'paused':
		#key_char = chr(key.c) 
		if key_char == 'q':
			something_changed = True
			game_state='exit'
		elif key_char == 'c':
			something_changed = True
			game_state = 'control screen'

	elif game_state == 'control screen':
		#key_char = chr(key.c) 
		if key_char == 'q':
			something_changed = True
			return 'pause'
		elif key_char in controlHandler.intFromLetter:
			control_num = controlHandler.intFromLetter[key_char] - 1
			# Update control scheme if we chose a new thing!
			if control_num < len(controlHandler.controlOptionsArray):
				(controlType, control_description) = controlHandler.controlOptionsArray[control_num]
				control_scheme = controlType
				controlHandler = ControlHandler(control_scheme)
				saveControlScheme()
				something_changed = True
				game_state = 'playing'
				return 'invalid-move'
				

	elif game_state == 'dead':
		#key_char = chr(key.c)
		if key_char == 'r':
			something_changed = True
			restart_game()
		elif key_char == 'q':
			something_changed = True
			game_state='exit'

	
	elif player_action == 'pickup_dialog':
		#key_char = chr(key.c)
		#print str(veekay)
		#keynum = veekay - 34	#yay magic number:

		# translate what button the player pressed into an int, if possible
		keynum = -1
		if key_char in controlHandler.intFromLetter:
			keynum = controlHandler.intFromLetter[key_char]
			
		# find list of objects that can be picked up
		weapons_found = []
		# can pick up from a larger radius if certain upgrade allow it
		pickup_radius = 0
		for power_up in upgrade_array:
			if getattr(power_up, "increase_pickup_radius", None) is not None:
				pickup_radius += power_up.increase_pickup_radius()

		# One day, I should make it so the code for deciding what can picked up happens in one place, 
		# rather than once for telling the player their options and once for interpreting their choice.
		# That day is not today.
		for dx in range (-pickup_radius,pickup_radius+1):			#ergh
			for dy in range(-pickup_radius,pickup_radius+1):
				try:
					for object in objectsArray[player.x+dx][player.y+dy]:
						if  object.weapon == True: 
							weapons_found.append(object)
				except IndexError:
					print('')



		if keynum >= 1 and keynum <= len(weapons_found):
			new_weapon = get_weapon_from_item(weapons_found[keynum-1], player.fighter.bonus_max_charge)
			old_weapon = get_item_from_weapon(player_weapon)
			player_weapon = new_weapon
			objectsArray[weapons_found[keynum-1].x][weapons_found[keynum-1].y].remove(weapons_found[keynum-1])
			# let's try that you don't drop your weapon, you throw it away entirely so you can't pick it up later.
			#drop_weapon(old_weapon)
			weapon_found = True
			if str(old_weapon.name) == "unarmed":
				message('You pick up the ' + new_weapon.name + '.', Color_Personal_Action) 
			else:
				message('You throw away your ' + old_weapon.name + ' and pick up the ' + new_weapon.name + '.', Color_Personal_Action) 
		elif veekay != None:
			game_state = 'playing'
			message('Never mind.', Color_Not_Allowed)
			#keynum = key
			#print str(libtcod.KEY_KP7)		# hang on... 41 is 7. So... 35 is 1, right? blah - 34
			return 'invalid-move'

		else:
			return 'pickup_dialog'


	elif player_action == 'upgrade shop dialog':

		if key_char == 'y':	# player has decided to buy an upgrade...
			upgrade_cost = current_shrine.get_cost()
			if currency_count >= upgrade_cost:	#then let them get the upgrade
				something_changed = True
				currency_count = currency_count - upgrade_cost
				upgrade_array.append(current_shrine.upgrade)
				message('You recieve the gift of '+ current_shrine.upgrade.name +'!', Color_Stat_Info)
				current_shrine.upgrade = None
			else:
				something_changed = True
				message('You do not have enough favour!', Color_Not_Allowed)
		elif key_char == 'n':
			something_changed = True
			message('You decide to abstain from ' + current_shrine.upgrade.name + '.', Color_Stat_Info)
		else:
			message('Never mind??', Color_Not_Allowed)

	elif player_action == 'jump_dialog':
		actionCommand = controlHandler.getGameplayCommand(veekay, key_char)
		#key_char = chr(key.c)
		# jump direction options
		#TODO HEY THIS STUFF IS HARDCODED AND SHOULD BE FIXED UP, ESPECIALLY WHAT WITH ME NO LONGER USING THIS LAYOUT:
		# I have replaced e.g. libtcod.KEY_KP7 with 'KP7'  in order to translate to tdl.
		# But anyway this should all get rewritten so I can allow adjustable controls, later.
		#if veekay == 'KP7' or veekay == 'HOME' or key_char == 't':

		temp_jump_decision = (0,0)

		if actionCommand == "MOVEUPLEFT":
			temp_jump_decision = (-2, -2)
			# player.decider.set_decision(Decision(jump_decision=Jump_Decision(-2,-2)))
		#elif veekay == 'KP8' or veekay == 'UP' or key_char == 'y':
		elif actionCommand == "MOVEUP": 
			temp_jump_decision = (0, -2)
			# player.decider.set_decision(Decision(jump_decision=Jump_Decision(0,-2)))
		#elif veekay == 'KP9' or veekay == 'PAGEUP' or key_char == 'u':
		elif actionCommand == "MOVEUPRIGHT":
			temp_jump_decision = (2, -2)
			# player.decider.set_decision(Decision(jump_decision=Jump_Decision(2,-2)))
		#elif veekay == 'KP2' or veekay == 'DOWN' or key_char == 'n':
		elif actionCommand == "MOVEDOWN":
			temp_jump_decision = (0, 2)
			# player.decider.set_decision(Decision(jump_decision=Jump_Decision(0,2)))
		#elif veekay == 'KP1' or veekay == 'END' or key_char == 'b':
		elif actionCommand == "MOVEDOWNLEFT":
			temp_jump_decision = (-2, 2)
			# player.decider.set_decision(Decision(jump_decision=Jump_Decision(-2,2)))
		#elif veekay == 'KP4' or veekay == 'LEFT' or key_char == 'g':
		elif actionCommand == "MOVELEFT":
			temp_jump_decision = (-2, 0)
			# player.decider.set_decision(Decision(jump_decision=Jump_Decision(-2,0)))
		#elif veekay == 'KP3' or veekay == 'PAGEDOWN' or key_char == 'm':
		elif actionCommand == "MOVEDOWNRIGHT":
			temp_jump_decision = (2, 2)
			# player.decider.set_decision(Decision(jump_decision=Jump_Decision(2,2)))
		#elif veekay == 'KP6' or veekay == 'RIGHT' or key_char == 'j':
		elif actionCommand == "MOVERIGHT":
			temp_jump_decision = (2, 0)
			# player.decider.set_decision(Decision(jump_decision=Jump_Decision(2,0)))
		#elif veekay == libtcod.KEY_KP5 or chr(key.c) == '.' or key_char == 'h':	
		#	message('You  perfectly still.')
		#game_state = 'playing'
		elif veekay != 0:
			game_state = 'playing'
			# message('You stand paralyzed by indecision or maybe bad programming!.')	#TODO probably change this message
			message('Never mind.', Color_Not_Allowed)
			return 'invalid-move'
		else: 
			return 'jump_dialog'
		# check if there's a wall in the way before letting player jump
		(dx,dy) = temp_jump_decision
		if map[player.x + dx][player.y + dy].blocked:
			message("There's a wall in the way!", Color_Not_Allowed)
			return 'invalid-move'
		else:
			player.decider.set_decision(Decision(jump_decision=Jump_Decision(dx,dy)))
			#upgrade_array.append(Get_Random_Upgrade())



	elif game_state == 'playing':

		actionCommand = controlHandler.getGameplayCommand(veekay, key_char)

		#key_char = chr(key.c)
		#print "walk!"
		#movement keys
		#if veekay == 'KP7' or veekay == 'HOME' or key_char == 't':
		if actionCommand == "MOVEUPLEFT":
			player.decider.set_decision(Decision(move_decision=Move_Decision(-1,-1)))
		#elif veekay == 'KP8' or veekay == 'UP' or key_char == 'y':
		elif actionCommand == "MOVEUP":
			player.decider.set_decision(Decision(move_decision=Move_Decision(0,-1)))
		#elif veekay == 'KP9' or veekay == 'PAGEUP' or key_char == 'u':
		elif actionCommand == "MOVEUPRIGHT":
			player.decider.set_decision(Decision(move_decision=Move_Decision(1,-1)))
		#elif veekay == 'KP2' or veekay == 'DOWN' or key_char == 'n':
		elif actionCommand == "MOVEDOWN":
			player.decider.set_decision(Decision(move_decision=Move_Decision(0,1)))
		#elif veekay == 'KP1' or veekay == 'END' or key_char == 'b':
		elif actionCommand == "MOVEDOWNLEFT":
			player.decider.set_decision(Decision(move_decision=Move_Decision(-1,1)))
		#elif veekay == 'KP4' or veekay == 'LEFT' or key_char == 'g':
		elif actionCommand == "MOVELEFT":
			player.decider.set_decision(Decision(move_decision=Move_Decision(-1,0)))
		#elif veekay == 'KP3' or veekay == 'PAGEDOWN' or key_char == 'm':
		elif actionCommand == "MOVEDOWNRIGHT":
			player.decider.set_decision(Decision(move_decision=Move_Decision(1,1)))
		#elif veekay == 'KP6' or veekay == 'RIGHT' or key_char == 'j':
		elif actionCommand == "MOVERIGHT":
			player.decider.set_decision(Decision(move_decision=Move_Decision(1,0)))
		#elif veekay == 'KP5' or veekay == '.' or key_char == 'h':	
		elif actionCommand == "STANDSTILL":
			message('You stand perfectly still.', Color_Personal_Action)
			
			# update the relevant upgrades, to do with standing still
			for power_up in upgrade_array:
				if getattr(power_up, "update_on_standing_still", None) is not None:
					power_up.update_on_standing_still(player, objectsArray, map)
			pass

		else:
			#test for other keys
			# key_char = chr(key.c)

			# picking up a new weapon.   Or maybe doing a thing with a plant?
			#if key_char == 'p':
			if actionCommand == "PICKUP":

				
				# by default, only pickup things directly underneath the player.
				# but power ups can increase the pickup radius 
				pickup_radius = 0
				for power_up in upgrade_array:
					if getattr(power_up, "increase_pickup_radius", None) is not None:
						pickup_radius += power_up.increase_pickup_radius()

				weapons_found = []
				plants_found = []
				weapon_found = False
				keys_found = []
				favours_found = []
				for dx in range (-pickup_radius,pickup_radius+1):			#ergh
					for dy in range(-pickup_radius,pickup_radius+1):
						#print ("trying ")
						try:
							for object in objectsArray[player.x + dx][player.y + dy]:
								if  object.weapon == True: 
									weapons_found.append(object)
								if object.name == 'key': 
									keys_found.append(object)
								if object.name == 'favour token': 
									favours_found.append(object)
								if object.plant is not None:
									plants_found.append(object)
						except IndexError:
							print('')


				#keys take priority over weapons. I'm just calling it. Would rather not make the submenu happen.
				if len(keys_found) > 0:
					message('You snatch up the key.', Color_Personal_Action)
					key_count = key_count + len(keys_found)
					for ki in keys_found:
						objectsArray[ki.x][ki.y].remove(ki)	
				#similarly, favours take priority over weapons but after keys.
				elif len(favours_found) > 0:
					message('You take the favour token.', Color_Personal_Action)
					currency_count = currency_count + len(favours_found)
					for fa in favours_found:
						objectsArray[fa.x][fa.y].remove(fa)	
				# TODO: make it so you pick up  fruits / plants / seeds / whatever in order to heal, rather than automatically.
			#STILL TODO KEEP A KEY COUNT AND MAKE IT AFFECT ELEVATOR OPENING
				elif len(weapons_found) == 1:
					new_weapon = get_weapon_from_item(weapons_found[0], player.fighter.bonus_max_charge)
					old_weapon = get_item_from_weapon(player_weapon)
					player_weapon = new_weapon
					objectsArray[weapons_found[0].x][weapons_found[0].y].remove(weapons_found[0])
					# let's try that you don't drop your weapon, you throw it away entirely so you can't pick it up later.
					#drop_weapon(old_weapon)
					weapon_found = True
					if str(old_weapon.name) == "unarmed":
						message('You pick up the ' + new_weapon.name + '.', Color_Personal_Action) 
					else:
						message('You throw away your ' + old_weapon.name + ' and pick up the ' + new_weapon.name + '.', Color_Personal_Action) 
				elif  len(weapons_found) > 1:
					message_string = ('Pick up what? (')
					count = 1
					for weapon_item in weapons_found:
						if count <= 26: #don't bother printing more than 26 things to pick up
							message_string = message_string + ( controlHandler.letterFromInt[count] + '. ' + weapon_item.name + ' ')
						count += 1
					message_string = message_string + ')'
					message(message_string, Color_Menu_Choice)
					return 'pickup_dialog'
					#handle_keys()	# why do I get the feeling I am going to regret this
				elif len(plants_found) >= 1:
					for plant_object in plants_found:
						if plant_object.plant.state == 'seed':
								plant_object.plant.activate()
								message('A sapling emerges as you poke the seed.', Color_Interesting_In_World)
				else:
				#if weapon_found == False:
					message('Nothing to pick up', Color_Not_Allowed)
					return 'invalid-move'	


			#elif key_char == JUMP:
			#elif veekay == 'SPACE':	#libtcod.KEY_SPACE:		#todo make this mappable somehow
			elif actionCommand == "JUMP":
				canJump = player.fighter.jump_available()
				if canJump:
					message_string = 'Jump in which direction?'
					message(message_string, Color_Menu_Choice)
					return 'jump_dialog'
				else:
					message_string = 'Your legs are too tired to jump.'
					message(message_string, Color_Not_Allowed)
					return 'invalid-move'

			#attacky keys!
			else :			
	

#				if key_char in player_weapon.command_list:
				if actionCommand in { "ATTCKUPLEFT","ATTCKUP","ATTCKUPRIGHT","ATTCKRIGHT","ATTCKDOWNRIGHT","ATTCKDOWN","ATTCKDOWNLEFT","ATTCKLEFT", "ATTCKDOWNALT"}:
					return process_player_attack(actionCommand)

		#		abstract_attack_data = player_weapon.do_attack(key_char)
		#		if abstract_attack_data is not None:
		#		#	if player_recharge_time <= 0:
		#			temp_attack_list = process_abstract_attack_data(player.x,player.y, abstract_attack_data, player)	
		#			player.decider.set_decision(Decision(attack_decision = Attack_Decision(attack_list=temp_attack_list)))
		#
		#		elif key_char in player_weapon.command_list and player_weapon.durability <= 0:
		#			message('Your ' +  str(player_weapon.name) + ' is broken!')
		#			return 'didnt-take-turn'
		#
		#		elif key_char in player_weapon.command_list and player_weapon.current_charge < player_weapon.default_usage:
		#			message('Attack used up; can attack again in ' + str(player_weapon.default_usage - player_weapon.current_charge) + ' seconds.', libtcod.orange)
		#			return 'didnt-take-turn'

				elif key_char == 'o':
					# is there a shrine here?
					shrine_here = False
					for obj in objectsArray[player.x][player.y]:
						if obj is not player and obj.shrine is not None:
							shrine_here = True
							current_shrine = obj.shrine
							break
					if shrine_here == True:
						current_god = current_shrine.god
						message('You close your eyes and focus your mind.', Color_Personal_Action)
						current_shrine.visit()

						if current_shrine.upgrade is not None:
							message('A small god appears before you.', Color_Interesting_In_World)
							message_string = '\"For a small display of faith, I will grant you the boon of ' + current_shrine.upgrade.name +'!\"'
							message(message_string, Color_Message_In_World)
							message_string = '\"' + current_shrine.upgrade.verbose_description +'\"'
							message(message_string, Color_Message_In_World)
							message_string = 'Would you like some ' + current_shrine.upgrade.name + ' ('+ str(current_shrine.get_cost()) +' favour)? y/n'
							message(message_string, Color_Menu_Choice)
							return 'upgrade shop dialog'
						else:
							message('... but nothing happens.', Color_Boring_In_World)
						#handle_keys()	# why do I get 

						# Commenting out this deity interaction stuff now... very sad

		#				message('You hear the voice of ' + current_god.name + ' whisper to you...')
		#				message(current_god.first_prayer_message, current_god.color)
		#				#message('\"Be at peace, my child. I watch over all who come to me with faith in their hearts.\"', libtcod.orange)

		#				favoured_by_healer = False
		#				favoured_by_destroyer = False
		#				tested_by_destroyer = False
		#				favoured_by_deliverer = False
		#				tested_by_deliverer = False
		#				if current_god.god_type.type == 'healer':
		#					if already_healed_this_level == False:
		#						if player.fighter.hp < player.fighter.max_hp:
		#							already_healed_this_level = True
		#							#player.fighter.heal(3)
		#							player.fighter.cure_wounds(1)
		#							message("You feel a little better")
		#							player.fighter.fully_heal()
		#					else:
		#						message('\"Sadly I can do no more for you at this moment. But hold on to your faith, and it shall be well rewarded.\"', color_warning)
		#					favoured_by_healer = True
		#				elif current_god.god_type.type == 'destroyer':
		#					tested_by_destroyer = True
		#					#destroyer_test_count = 10
		#					destroyer_test_count = lev_set.max_monsters
		#				elif current_god.god_type.type == 'deliverer':
		#					# do a test: did we get to the shrine quickly enough?
		#					if (game_time - time_level_started) > 190:
		#						message('\"Hang on a sec, actually you already took too long to get here. Sorry!\"', color_warning)
		#					else:
		#						tested_by_deliverer = True
		#						deliverer_test_count = 200 - (game_time-time_level_started)		#TODO put these kind of values in gods.py






					else:
						message('There is no shrine here.', Color_Not_Allowed)
						return 'invalid-move'


				elif key_char == 'l':
					message('You think it\'s time to blow this scene.', Color_Personal_Action)
					current_center = nearest_points_array[player.x][player.y]
					if current_center is not None:
						target_center = choose_adjacent_room(current_center,  previous_center = TEMP_player_previous_center)
						TEMP_player_previous_center = current_center
						(point_x, point_y) =  center_points[target_center]
						player.x = point_x
						player.y = point_y 
					else:
						message('However, you\'re not really sure where this scene is', Color_Not_Allowed )

				else:
					return 'didnt-take-turn'




def create_room(room):
	global map, spawn_points, center_points, nearest_points_array

	(new_x, new_y) = room.center()
	center_points.append((new_x,new_y))

	#go through the tiles in the rectangle and make them passable
	for x in range(room.x1 + 1, room.x2):
		for y in range(room.y1 + 1, room.y2):
			map[x][y].blocked = False
			map[x][y].block_sight = False
			nearest_points_array[x][y] = (new_x, new_y)


def create_elevator(elevator):
	# like creating a room, but with a spawn point!
	global map, spawn_points, center_points, nearest_points_array


	(new_x, new_y) = elevator.center()
	center_points.append((new_x,new_y))
	spawn_points.append((new_x,new_y))

	#go through the tiles in the rectangle and make them passable
	for x in range(elevator.x1 + 1, elevator.x2):
		for y in range(elevator.y1 + 1, elevator.y2):
			map[x][y].blocked = False
			map[x][y].block_sight = False
			nearest_points_array[x][y] = (new_x, new_y)



def create_h_tunnel(x1, x2, y):
	global map, nearest_points_array, center_points
	if nearest_points_array[x2][y] is None:
		center_points.append((x2,y))
	for x in range(min(x1, x2), max(x1, x2) + 1):
		map[x][y].blocked = False
		map[x][y].block_sight = False
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

def create_v_tunnel(y1, y2, x):
	global map, nearest_points_array, center_points
	if nearest_points_array[x][y2] is None:
		center_points.append((x,y2))
	#vertical tunnel
	for y in range(min(y1, y2), max(y1, y2) + 1):
		map[x][y].blocked = False
		map[x][y].block_sight = False
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


def place_objects(room):
	global game_level_settings, dungeon_level, god_healer, god_destroyer, god_deliverer
	
	lev_set = game_level_settings.get_setting(dungeon_level)

	max_room_monsters = lev_set.max_room_monsters

	#choose random number of monsters
	num_monsters = randint( 0, max_room_monsters)


	for i in range(num_monsters):
	#for i in range(50):
		#choose random spot for this monster
		x = randint( room.x1+1, room.x2-1)
		y = randint( room.y1+1, room.y2-1)

		#only place it if the tile is not blocked
		if not is_blocked(x, y):


			total_enemy_prob = lev_set.total_enemy_prob
			enemy_probabilities = lev_set.enemy_probabilities

			enemy_name = 'none'
			num = randint(0, total_enemy_prob)
			for (name, prob) in enemy_probabilities:
				#print( '(' + name + ',' + str(prob) + ')')
				if num <= prob:
					enemy_name = name
					break
				else:
					num -= prob
					

			monster = create_monster(x,y,name)
			objectsArray[x][y].append(monster)
			worldEntitiesList.append(monster)

	# on first level, in in 2 chance of a weapon appearing in a room I guess
	if dungeon_level == 0:
		num = randint( 0, 2)
		if num == 0:
			x = randint( room.x1+1, room.x2-1)
			y = randint( room.y1+1, room.y2-1)
			new_weapon = Object(x,y, 's', 'sword', default_weapon_color, blocks = False, weapon = True, always_visible = True)
			drop_weapon(new_weapon)
			#objects.append(new_weapon)
			#new_weapon.send_to_back()
		elif num == 1:
			x = randint( room.x1+1, room.x2-1)
			y = randint( room.y1+1, room.y2-1)
			new_weapon = Object(x,y, 'f', 'sai', default_weapon_color, blocks = False, weapon = True, always_visible = True)
			drop_weapon(new_weapon)
			#objects.append(new_weapon)
			#new_weapon.send_to_back()

	# on higher levels, maybe there are shrines? Maybe??
	else:
		num = randint(0,18)
		if num == 0:
			(shrine_x, shrine_y) = room.center()
			new_shrine = Object(shrine_x, shrine_y, '&', 'shrine', default_altar_color, blocks=False, shrine= Shrine(god_healer), always_visible=True) 		
			#new_shrine = Object(shrine_x, shrine_y, '&', 'shrine to ' + god_healer.name, default_altar_color, blocks=False, shrine= Shrine(god_healer), always_visible=True) 		
			objectsArray[shrine_x][shrine_y].append(new_shrine)
			shrine.cost += dungeon_level - 2
			new_shrine.send_to_back()
		elif num == 1:
			(shrine_x, shrine_y) = room.center()
			new_shrine = Object(shrine_x, shrine_y, '&', 'shrine', default_altar_color, blocks=False, shrine= Shrine(god_destroyer), always_visible=True) 		
			#new_shrine = Object(shrine_x, shrine_y, '&', 'shrine to ' + god_destroyer.name, default_altar_color, blocks=False, shrine= Shrine(god_destroyer), always_visible=True) 		
			objectsArray[shrine_x][shrine_y].append(new_shrine)
			shrine.cost += dungeon_level - 2
			new_shrine.send_to_back()
		elif num == 2:
			(shrine_x, shrine_y) = room.center()
			new_shrine = Object(shrine_x, shrine_y, '&', 'shrine', default_altar_color, blocks=False, shrine= Shrine(god_deliverer), always_visible=True) 		
			#new_shrine = Object(shrine_x, shrine_y, '&', 'shrine to ' + god_deliverer.name, default_altar_color, blocks=False, shrine= Shrine(god_deliverer), always_visible=True) 		
			objectsArray[shrine_x][shrine_y].append(new_shrine)
			shrine.shrine.cost += dungeon_level - 2
			new_shrine.send_to_back()



def create_monster(x,y, name, guard_duty = False):
	global number_alarmers
	if name == 'strawman':
		# let's make a strawman!
		strawman_component = Fighter(hp=1, defense=0, power=1, death_function=monster_death,  attack_color = color_swordsman, faded_attack_color = color_swordsman, bleeds = False)
		ai_component = Strawman_AI(weapon = None)
		decider_component = Decider(ai_component)
		monster = Object(x, y, 'A', 'strawman', color_swordsman, blocks=True, fighter=strawman_component, decider=decider_component)

	elif name == 'flailing strawman':
		# let's create a strawman that can theoretically do damage!
		strawman_component = Fighter(hp=1, defense=0, power=1, death_function=monster_death,  attack_color = color_axe_maniac, faded_attack_color = color_axe_maniac, bleeds = False)
		ai_component = Strawman_AI(weapon = Weapon_Sai())
		decider_component = Decider(ai_component)
		monster = Object(x, y, 'A', 'strawman', color_axe_maniac, blocks=True, fighter=strawman_component, decider=decider_component)	

	elif name == 'strawman on wheels':
		# let's create a strawman that can move around!
		strawman_component = Fighter(hp=1, defense=0, power=1, death_function=monster_death,  attack_color = color_boman, faded_attack_color = color_boman, bleeds = False)
		ai_component = Strawman_on_wheels_AI(weapon = None)
		decider_component = Decider(ai_component)
		monster = Object(x, y, 'A', 'strawman on wheels', color_boman, blocks=True, fighter=strawman_component, decider=decider_component)
				
	elif name == 'swordsman':
		#create an orc
		fighter_component = Fighter(hp=1, defense=0, power=1, death_function=monster_death, attack_color = color_swordsman, faded_attack_color = color_swordsman)
		ai_component = BasicMonster(weapon = Weapon_Sword(), guard_duty= guard_duty)
		decider_component = Decider(ai_component)
		monster = Object(x, y, 'S', 'swordsman', color_swordsman, blocks=True, fighter=fighter_component, decider=decider_component)

	elif name == 'stupid swordsman':
		#create an orc
		fighter_component = Fighter(hp=1, defense=0, power=1, death_function=monster_death, attack_color = color_swordsman, faded_attack_color = color_swordsman)
		ai_component = StupidBasicMonster(weapon = Weapon_Sword(), guard_duty= guard_duty)
		decider_component = Decider(ai_component)
		monster = Object(x, y, 'S', 'swordsman', color_swordsman, blocks=True, fighter=fighter_component, decider=decider_component)


	elif name == 'boman':
		#create a troll
		fighter_component = Fighter(hp=3, defense=0, power=1, death_function=monster_death, attack_color = color_boman, faded_attack_color = color_boman)
		ai_component = Boman_AI(weapon = Weapon_Staff(), guard_duty= guard_duty)
		decider_component = Decider(ai_component)
		monster = Object(x, y, 'B', 'boman', color_boman, blocks=True, fighter=fighter_component, decider=decider_component)


	elif name == 'rook':
		#create a rook! That's a guy with a spear who only moves in four directions
		fighter_component = Fighter(hp=3, defense=0, power=1, death_function=monster_death, attack_color = color_rook, faded_attack_color = color_rook)
		ai_component = Rook_AI(weapon = Weapon_Spear(), guard_duty = guard_duty)
		decider_component = Decider(ai_component)
		monster = Object(x, y, 'R', 'rook', color_rook, blocks=True, fighter=fighter_component, decider=decider_component)

#	elif name == 'stupid rook':
#		#create a rook! That's a guy with a spear who only moves in four directions
#		fighter_component = Fighter(hp=3, defense=0, power=1, death_function=monster_death, attack_color = color_rook, faded_attack_color = color_rook)
#		ai_component = Stupid_Rook_AI(weapon = Weapon_Spear(), guard_duty = guard_duty)
#		decider_component = Decider(ai_component)
#		monster = Object(x, y, 'R', 'rook', color_rook, blocks=True, fighter=fighter_component, decider=decider_component)


	elif name == 'nunchuck fanatic':
		#create a troll
		fighter_component = Fighter(hp=2, defense=0, power=1, death_function=monster_death, attack_color = color_boman, faded_attack_color = color_boman)
		ai_component = BasicMonster(weapon = Weapon_Nunchuck(), guard_duty= guard_duty, attack_dist = 2)
		decider_component = Decider(ai_component)
		monster = Object(x, y, 'F', 'nunchuck fanatic', color_boman, blocks=True, fighter=fighter_component, decider=decider_component)


	elif name == 'axe maniac':
		#create a guy with an axe!
		fighter_component = Fighter(hp=3, defense=0, power=1, death_function=monster_death, attack_color = color_axe_maniac, faded_attack_color = color_axe_maniac)
		ai_component = BasicMonster(weapon = Weapon_Axe(), guard_duty = guard_duty)
		decider_component = Decider(ai_component)
		monster = Object(x, y, 'M', 'axe maniac', color_axe_maniac, blocks=True, fighter=fighter_component, decider=decider_component)

	elif name == 'samurai':
		#create a guy with an axe!
		fighter_component = Fighter(hp=5, defense=0, power=1, death_function=monster_death, attack_color = color_axe_maniac, faded_attack_color = color_axe_maniac)
		ai_component = Samurai_AI(weapon = Weapon_Katana())
		decider_component = Decider(ai_component)
		monster = Object(x, y, 'Z', 'samurai', color_axe_maniac, blocks=True, fighter=fighter_component, decider=decider_component)

	elif name == 'tridentor':
		#create a guy with an axe!
		fighter_component = Fighter(hp=2, defense=0, power=1, death_function=monster_death, attack_color = color_tridentor, faded_attack_color = color_tridentor)
		ai_component = Tridentor_AI(weapon = Weapon_Trident(), guard_duty = guard_duty)
		decider_component = Decider(ai_component)
		monster = Object(x, y, 'T', 'tridentor', color_tridentor, blocks=True, fighter=fighter_component, decider=decider_component)


	elif name == 'rogue':
		#create a guy with an axe!
		fighter_component = Fighter(hp=2, defense=0, power=1, death_function=monster_death, attack_color = color_rogue, faded_attack_color = color_rogue)
		ai_component = Rogue_AI(weapon = Weapon_Sai(), guard_duty = guard_duty)
		decider_component = Decider(ai_component)
		monster = Object(x, y, 'K', 'rogue', color_rogue, blocks=True, fighter=fighter_component, decider=decider_component)



	elif name == 'hammer sister':
		#create a lady with a hammer!
		fighter_component = Fighter(hp=3, defense=0, power=1, death_function=monster_death, attack_color = color_boman, faded_attack_color = color_boman)
		ai_component =  Ninja_AI(weapon = Weapon_Hammer())
		decider_component = Decider(ai_component)
		monster = Object(x, y, 'H', 'hammer sister', color_boman, blocks=True, fighter=fighter_component, decider=decider_component)


	elif name == 'ninja':
		#create a sneaky ninja!
		fighter_component = Fighter(hp=2, defense=0, power=1, death_function=monster_death, attack_color = color_ninja, faded_attack_color = color_ninja)
		ai_component = Ninja_AI(weapon = Weapon_Dagger())
		decider_component = Decider(ai_component)
		monster = Object(x, y, 'N', 'ninja', color_ninja, blocks=True, fighter=fighter_component, decider=decider_component)


	elif name == 'wizard':
		#create a wizard!
		fighter_component = Fighter(hp=10, defense=0, power=1, death_function=monster_death, attack_color = color_wizard, faded_attack_color = color_wizard)
		ai_component = Wizard_AI(weapon = Weapon_Ring_Of_Power())
		decider_component = Decider(ai_component)
		monster = Object(x, y, 'W', 'wizard', color_wizard, blocks=True, fighter=fighter_component, decider=decider_component)



	elif name == 'security system':
		# let's make a security system! It stays where it is and doesn't attack! In fact it's basically a strawman with more health.
		strawman_component = Fighter(hp=1, defense=0, power=1, death_function=monster_death,  attack_color =color_swordsman, faded_attack_color = color_swordsman, bleeds = False)
		ai_component = Strawman_AI(weapon = None)
		decider_component = Decider(ai_component)
		alarmer_component = Alarmer(assoc_fighter = strawman_component)
		monster = Object(x, y, 'O', 'security system', color_alarmer_idle, blocks=True, fighter=strawman_component, decider=decider_component, alarmer = alarmer_component, always_visible = True)



	else:
		monster = None
	
	if monster.alarmer is not None:
		number_alarmers += 1

	return monster



def create_strawman(x,y, weapon, command):
	# let's create a strawman that can theoretically do damage!
	strawman_component = Fighter(hp=1, defense=0, power=1, death_function=monster_death,  attack_color = color_axe_maniac, faded_attack_color = color_axe_maniac, bleeds = False)
	ai_component = Strawman_AI(get_weapon_from_name(weapon), command)		
	decider_component = Decider(ai_component)
	monster = Object(x, y, 'A', 'strawman', color_axe_maniac, blocks=True, fighter=strawman_component, decider=decider_component)
	return monster


#todo probably add objectsarray as a global here? and then find the place to initialise it
def make_map():
	global map, background_map, stairs, game_level_settings, dungeon_level, spawn_points, elevators, center_points, nearest_points_array, room_adjacencies, MAP_HEIGHT, MAP_WIDTH, number_alarmers, camera, alarm_level, key_count, currency_count, lev_set, decoration_count, TEMP_player_previous_center, objectsArray, bgColorArray, worldAttackList, worldEntitiesList

	lev_gen = Level_Generator()

	lev_set = game_level_settings.get_setting(dungeon_level)
	level_data = lev_gen.make_level(dungeon_level, lev_set)

	number_alarmers = 0		# how many things in the level do stuff with the alarm? If this becomes 0, all alarms stuff

	map = level_data.map
	background_map = level_data.background_map
	player.x = level_data.player_start_x
	player.y = level_data.player_start_y
	camera.x = player.x
	camera.y = player.y
	nearest_points_array = level_data.nearest_points_array
	center_points = level_data.center_points
	spawn_points = level_data.spawn_points
	object_data = level_data.object_data
	elevators = level_data.elevators
	room_adjacencies = level_data.room_adjacencies
	MAP_WIDTH = len(map)
	MAP_HEIGHT = len(map[0])

	#TODO NOTE: think we can initalise objectsarray here.
	objectsArray = []
	print("DOING STUFF WITH MAKE MAP")
	for x in range(MAP_WIDTH):
		objectsRowArray = []
		objectsArray.append(objectsRowArray)
#		objectsArray[x] = []
		for y in range(MAP_HEIGHT):
			objectsColumnArray = []
			objectsArray[x].append(objectsColumnArray)
#			objectsArray[x][y] = []

	worldAttackList = []	## a list of attacks in the world (these are also stored in objectArray)
	worldEntitiesList = []	## list of non-attack objects that have to get updated / do things, e.g. deciders. (also stored in objectArray)

	process_nearest_center_points()
	initialize_nav_data()
	#calculate_nav_data()

	bgColorArray = []
	print("DOING MORE STUFF WITH MAKE MAP")
	for x in range(MAP_WIDTH):
		bgColorRowArray = []
		bgColorArray.append(bgColorRowArray)
		for y in range(MAP_HEIGHT):
			if map[x][y].blocked:
				bgColorColumnColor = color_light_wall
			else:
				if background_map[x][y] == 0:
					bgColorColumnColor = color_light_ground
				elif background_map[x][y] == 2:
					bgColorColumnColor = color_light_ground_alt
				else:
					bgColorColumnColor = color_light_ground
				
			bgColorArray[x].append(bgColorColumnColor)

	# print( 'color maybe is' + str(color_light_wall.r))	


	TEMP_player_previous_center = None

	alarm_level = 1
	key_count = 0
	decoration_count = 0

	# now create objects from object_data! This code resorting thing is actually getting kind of fun now
	for od in object_data:
		if od.name == 'stairs':
			stairs = Object(od.x, od.y, '<', 'stairs', PLAYER_COLOR, always_visible=True)
			objectsArray[od.x][od.y].append(stairs)
			stairs.send_to_back()  #so it's drawn below the monsters
		elif od.name == 'weapon':
			weapon = get_item_from_name(od.x,od.y, od.info)
			objectsArray[od.x][od.y].append(weapon)
			weapon.send_to_back()
		elif od.name == 'monster' or od.name == 'boss':		# maybe these cases will be treated differently in future
			monster = create_monster(od.x,od.y, od.info, guard_duty = True)
			objectsArray[od.x][od.y].append(monster)
			worldEntitiesList.append(monster)
			# Hackiest of all hacks - make the tutorial rook drop a key
			if dungeon_level == 0:
				if od.info == 'security system':
					monster.drops_key = True
		elif od.name == 'strawman':
			strawman = create_strawman(od.x,od.y,od.info, od.more_info)
			objectsArray[od.x][od.y].append(strawman)
			worldEntitiesList.append(strawman)
		elif od.name == 'shrine':
			#get altar color - gonna make it depend on the background of the tile it's on.
			altar_color = color_light_ground_alt
			if background_map[od.x][od.y] == 2:
				altar_color = color_light_ground
			num = randint( 0, 2) 
			if num == 0:
				#shrine = Object(od.x, od.y, '&', 'shrine to ' + god_healer.name, altar_color, blocks=False, shrine= Shrine(god_healer), always_visible=True) 	
				shrine = Object(od.x, od.y, '&', 'shrine', altar_color, blocks=False, shrine= Shrine(god_healer), always_visible=True) 	
			elif num == 1:
				shrine = Object(od.x, od.y, '&', 'shrine', altar_color, blocks=False, shrine= Shrine(god_destroyer), always_visible=True) 
				#shrine = Object(od.x, od.y, '&', 'shrine to ' + god_destroyer.name, altar_color, blocks=False, shrine= Shrine(god_destroyer), always_visible=True) 
			else: 
				shrine = Object(od.x, od.y, '&', 'shrine', altar_color, blocks=False, shrine= Shrine(god_deliverer), always_visible=True) 
				#shrine = Object(od.x, od.y, '&', 'shrine to ' + god_deliverer.name, altar_color, blocks=False, shrine= Shrine(god_deliverer), always_visible=True) 
			shrine.shrine.cost += dungeon_level - 2
			objectsArray[od.x][od.y].append(shrine)
			shrine.send_to_back()
		elif  od.name == 'security system':
			monster = create_monster(od.x,od.y, 'security system', guard_duty = True)
			if od.info == 'drops-key':
				monster.drops_key = True
			objectsArray[od.x][od.y].append(monster)
			worldEntitiesList.append(monster)
			#number_alarmers += 1			#Now doing this elsewhere..
		elif  od.name == 'door'or od.name == 'easydoor':
			if od.info == 'horizontal':
				door = Object(od.x, od.y, '+', 'door', default_door_color, blocks=True, door = Door(horizontal = True), always_visible=True) 
				map[od.x][od.y].block_sight = True
				objectsArray[od.x][od.y].append(door)
				worldEntitiesList.append(door)
			elif od.info == 'vertical':
				door = Object(od.x, od.y, '+', 'door', default_door_color, blocks=True, door = Door(horizontal = False), always_visible=True) 	
				map[od.x][od.y].block_sight = True
				objectsArray[od.x][od.y].append(door)
				worldEntitiesList.append(door)
			if od.name == 'easydoor':		# a door that doesn't stick!!
				door.door.easy_open = True
			# TODO MAKE PATHFINDING TAKE DOORS INTO ACCOUNT AT SOME POINT
		elif od.name == 'key':
			new_key = Object(od.x, od.y, '*', 'key', PLAYER_COLOR, blocks = False, weapon = False, always_visible=True)
			objectsArray[od.x][od.y].append(new_key)
		elif od.name == 'water':
			new_water = Object(od.x, od.y, '~', 'water', water_foreground_color, blocks = False, weapon = False, always_visible=True)
			objectsArray[od.x][od.y].append(new_water)
		elif od.name == 'plant':
			flower_part = Flower(flower_type = od.info, state = 'blooming')
			new_plant = Object(od.x, od.y, 'U', flower_part.name, default_flower_color, blocks = False, plant = flower_part,  always_visible=True)
			objectsArray[od.x][od.y].append(new_plant)
			worldEntitiesList.append(new_plant)
		elif od.name == 'message':
			message_color = color_light_ground_alt
			if background_map[od.x][od.y] == 2:
				message_color = color_light_ground
			floor_message = Object(od.x, od.y, '~', 'message', message_color, blocks=False, floor_message = Floor_Message(od.info))
			objectsArray[od.x][od.y].append(floor_message)
			floor_message.send_to_back()
		elif od.name == 'decoration':
			floor_message = Object(od.x, od.y, od.info, 'decoration', default_decoration_color, blocks=False, always_visible=True)
			objectsArray[od.x][od.y].append(floor_message)
			floor_message.send_to_back()
			decoration_count += 1
			

	# elevator data because elevators are complicated! Do you know how to build an elevator? I sure don't!
	for ele in elevators:
		ele.special_door_list = []
		for ele_door in ele.doors:
			door = Object(ele_door.x, ele_door.y, '+', 'elevator door', color_axe_maniac, blocks=True, door = Door(horizontal = ele_door.door.horizontal), always_visible=True) 
			map[ele_door.x][ele_door.y].block_sight = True			
			objectsArray[ele_door.x][ele_door.y].append(door)
			worldEntitiesList.append(door)
			ele.special_door_list.append(door)



	#at the end, put objects in the right display order?

	print("DOING YET MORE STUFF WITH MAKE MAP")
	for y in range(MAP_HEIGHT):
		for x in range(MAP_WIDTH):
			reorder_objects(x,y)

			



def initialize_nav_data():
	global map, center_points, nav_data, nav_data_changed, distance_between_center_points, room_adjacencies

	print ("INTIALIZING NAV DATA")

	big_M = MAP_HEIGHT * MAP_WIDTH
	NUMBER_POINTS = len(center_points)

	# nav data gives distance of each point from each room center
	nav_data = [[[ big_M
		for p  in range(NUMBER_POINTS)]
			for y in range(MAP_HEIGHT) ]
				for x in range(MAP_WIDTH)]

	# distance_between_center_points gives distance of each room center from each room center 
	distance_between_center_points = [[ big_M
		for p  in range(NUMBER_POINTS)]
			for q in range(NUMBER_POINTS) ]


	for n in range(NUMBER_POINTS):
		# each center point is distance 0 from itself
		(x,y) = center_points[n]
		nav_data[x][y][n] = 0
		distance_between_center_points[n][n] = 0
		# we assume the distance between center points is the sum ? of their x distance and y distance
		#print(room_adjacencies)
		if len(room_adjacencies) > n:
			for m in room_adjacencies[n]:
				(other_x, other_y) = center_points[m]
				distance_between_center_points[n][m] = math.fabs(x - other_x) + math.fabs(y - other_y)

	# Now update distance_between_center_points until we have (a rough estimate of) the distance between each pair of center points
	max_number_of_loops = NUMBER_POINTS*NUMBER_POINTS
	anything_changed = False
	for r in range(max_number_of_loops):
		for p in range(NUMBER_POINTS):
			for n in range(NUMBER_POINTS):
				if len(room_adjacencies) > n:
					for m in room_adjacencies[n]:
						if distance_between_center_points[n][p] > distance_between_center_points[n][m] + distance_between_center_points[m][p]:
							distance_between_center_points[n][p] = distance_between_center_points[n][m] + distance_between_center_points[m][p]
							anything_changed = True
		if anything_changed:
			anything_changed = False
		else:
			break


	# Now estimate distances of all points from centers, based on distances between center points
	for p  in range(len(center_points)):
		for y in range(MAP_HEIGHT):
			for x in range(MAP_WIDTH):
				# get co-ords of nearest center
				center_num = nearest_points_array[x][y]
				if center_num is not None:
					(cen_x, cen_y) = center_points[center_num]
					nav_data[x][y][p] = 	distance_between_center_points[center_num][p] 	+ max(math.fabs(x - cen_x), math.fabs(y - cen_y))


	# update distances of points from centers, based on current estimated distances from adjacent centers.
	for p  in range(len(center_points)):
		for y in range(MAP_HEIGHT):
			for x in range(MAP_WIDTH):
				center_num = nearest_points_array[x][y]
				# get co-ords of nearest center
				if map[x][y].blocked == False and  center_num is not None:
					current_best = nav_data[x][y][p]	# our current best guess for distance of (x,y) from center p
					if len(room_adjacencies) > center_num:
						for m in room_adjacencies[center_num]:
							temp_dist = nav_data[x][y][m] + distance_between_center_points[m][p] 
							if temp_dist < current_best:
								current_best = temp_dist
					nav_data[x][y][p] = current_best
		

	nav_data_changed = True

	update_nav_data()


def update_nav_data():

#def calculate_nav_data():
	# come up with a nav data thing that calculates the distances to a bunch of checkpoints!
	global map, center_points, nav_data, nav_data_changed, room_adjacencies

#	# nav data is 3d array
#	# for x \in [MAP_WIDTH[, y \in [MAP_HEIGHT], p in [Number of center points].
#	# nav_data[x,y,p] is the length of a shortest path from (x,y) to point p
#
#	big_M = MAP_HEIGHT * MAP_WIDTH
#	NUMBER_POINTS = len(center_points)
#	nav_data = [[[ big_M
#		for p  in range(NUMBER_POINTS)]
#			for y in range(MAP_HEIGHT) ]
#				for x in range(MAP_WIDTH)]
#
#	for n in range(NUMBER_POINTS):
#		(x,y) = center_points[n]
#		nav_data[x][y][n] = 0

	# only do anything if we have reason to belief the nav data needs updating
	if nav_data_changed:
		
		print ("UPDATING NAVE DATA")

		# new plan.. 

		anything_changed = False


		# new plan: we only calculate distances to center points of adjacent rooms.
		# then we kind of bolt other data on later.
		#for r in range(MAP_HEIGHT*MAP_WIDTH*NUMBER_POINTS):
		for r in range(max_nav_data_loops):#horse
			for y in range(MAP_HEIGHT):
				for x in range(MAP_WIDTH):
					if map[x][y].blocked == False:
						center_num = nearest_points_array[x][y]
						# get co-ords of nearest center
						if map[x][y].blocked == False and  center_num is not None:
							if len(room_adjacencies) > center_num:
								center_list = list(room_adjacencies[center_num])
								center_list.append(center_num)
								for p in center_list:	# only figure outadjcencies for these
									if x > 0:
										if nav_data[x-1][y][p] + 1 < nav_data[x][y][p] and map[x-1][y].blocked == False:
											nav_data[x][y][p] = nav_data[x-1][y][p] + 1
											anything_changed = True
									if x < MAP_WIDTH-1:
										if nav_data[x+1][y][p] + 1 < nav_data[x][y][p] and map[x+1][y].blocked == False:
											nav_data[x][y][p] = nav_data[x+1][y][p] + 1
											anything_changed = True
									if y > 0:
										if nav_data[x][y-1][p] + 1 < nav_data[x][y][p] and map[x][y-1].blocked == False:
											nav_data[x][y][p] = nav_data[x][y-1][p] + 1
											anything_changed = True
									if y < MAP_HEIGHT-1:
										if nav_data[x][y+1][p] + 1 < nav_data[x][y][p] and map[x][y+1].blocked == False:
											nav_data[x][y][p] = nav_data[x][y+1][p] + 1
											anything_changed = True
		
									if x > 0 and y > 0:
										if nav_data[x-1][y-1][p] + 1 < nav_data[x][y][p] and map[x-1][y-1].blocked == False:
											nav_data[x][y][p] = nav_data[x-1][y-1][p] + 1
											anything_changed = True
									if x < MAP_WIDTH-1 and y > 0:
										if nav_data[x+1][y-1][p] + 1 < nav_data[x][y][p] and map[x+1][y-1].blocked == False:
											nav_data[x][y][p] = nav_data[x+1][y-1][p] + 1
											anything_changed = True
									if x > 0 and y < MAP_HEIGHT-1:
										if nav_data[x-1][y+1][p] + 1 < nav_data[x][y][p] and map[x-1][y+1].blocked == False:
											nav_data[x][y][p] = nav_data[x-1][y+1][p] + 1
											anything_changed = True
									if x < MAP_WIDTH-1 and y < MAP_HEIGHT-1:
										if nav_data[x+1][y+1][p] + 1 < nav_data[x][y][p] and map[x+1][y+1].blocked == False:
											nav_data[x][y][p] = nav_data[x+1][y+1][p] + 1
											anything_changed = True

#
#		#for r in range(MAP_HEIGHT*MAP_WIDTH*NUMBER_POINTS):
#		for r in range(max_nav_data_loops):#horse
#			for p  in range(len(center_points)):
#				for y in range(MAP_HEIGHT):
#					for x in range(MAP_WIDTH):
#						if map[x][y].blocked == False:
#							if x > 0:
#								if nav_data[x-1][y][p] + 1 < nav_data[x][y][p] and map[x-1][y].blocked == False:
#									nav_data[x][y][p] = nav_data[x-1][y][p] + 1
#									anything_changed = True
#							if x < MAP_WIDTH-1:
#								if nav_data[x+1][y][p] + 1 < nav_data[x][y][p] and map[x+1][y].blocked == False:
#									nav_data[x][y][p] = nav_data[x+1][y][p] + 1
#									anything_changed = True
#							if y > 0:
#								if nav_data[x][y-1][p] + 1 < nav_data[x][y][p] and map[x][y-1].blocked == False:
#									nav_data[x][y][p] = nav_data[x][y-1][p] + 1
#									anything_changed = True
#							if y < MAP_HEIGHT-1:
#								if nav_data[x][y+1][p] + 1 < nav_data[x][y][p] and map[x][y+1].blocked == False:
#									nav_data[x][y][p] = nav_data[x][y+1][p] + 1
#									anything_changed = True
#		
#							if x > 0 and y > 0:
#								if nav_data[x-1][y-1][p] + 1 < nav_data[x][y][p] and map[x-1][y-1].blocked == False:
#									nav_data[x][y][p] = nav_data[x-1][y-1][p] + 1
#									anything_changed = True
#							if x < MAP_WIDTH-1 and y > 0:
#								if nav_data[x+1][y-1][p] + 1 < nav_data[x][y][p] and map[x+1][y-1].blocked == False:
#									nav_data[x][y][p] = nav_data[x+1][y-1][p] + 1
#									anything_changed = True
#							if x > 0 and y < MAP_HEIGHT-1:
#								if nav_data[x-1][y+1][p] + 1 < nav_data[x][y][p] and map[x-1][y+1].blocked == False:
#									nav_data[x][y][p] = nav_data[x-1][y+1][p] + 1
#									anything_changed = True
#							if x < MAP_WIDTH-1 and y < MAP_HEIGHT-1:
#								if nav_data[x+1][y+1][p] + 1 < nav_data[x][y][p] and map[x+1][y+1].blocked == False:
#									nav_data[x][y][p] = nav_data[x+1][y+1][p] + 1
#									anything_changed = True
			if anything_changed:
				anything_changed = False		#check it again!
			else: 
				# if actually nothing changed, we can mark the nav data as done.
				nav_data_changed = False		
				#print( 'nav data finished after ' + str(r) + ' iterations')
				break


	
	
		# okay, I think that concludes calculating the distance to things? Let's see.
		# actually wait let's then do this again:
		# update distances of points from centers, based on current estimated distances from adjacent centers.
		for p  in range(len(center_points)):
			for y in range(MAP_HEIGHT):
				for x in range(MAP_WIDTH):
					center_num = nearest_points_array[x][y]
					# get co-ords of nearest center
					if map[x][y].blocked == False and  center_num is not None:
						current_best = nav_data[x][y][p]	# our current best guess for distance of (x,y) from 	center p
						if len(room_adjacencies) > center_num:
							for m in room_adjacencies[center_num]:
								temp_dist = nav_data[x][y][m] + distance_between_center_points[m][p] 
								if temp_dist < current_best:
									current_best = temp_dist
						nav_data[x][y][p] = current_best
	#nav_data_changed = False		# temp hack, will probably break things
	
	
def is_blocked(x, y, care_about_doors = False, generally_ignore_doors = True, care_about_fighters = False, generally_ignore_fighters = False):
	#first test the map tile
	if map[x][y].blocked:
		return True


	#now check for any blocking objects
	for object in objectsArray[x][y]:
		if object.blocks:
			if object.door is not None:
				if care_about_doors == True:
					return 'closed-door'
				elif generally_ignore_doors == False:
					return True
			elif object.fighter is not None:
				if care_about_fighters == True:
					return 'blocky-fighter'
				elif generally_ignore_fighters == False:
					return True
		#	elif object.name == 'swordsman':
		#		print "blocky swordsman"
		#		return True
			else:
				return True

	return False




def player_move_or_attack(dx, dy):
	global fov_recompute
 
	#the coordinates the player is moving to/attacking
	x = player.x + dx
	y = player.y + dy
 
	#try to find an attackable object there
	target = None
	for object in objectsArray[x][y]:
		if object.fighter:
			target = object
			break
 
	#attack if target found, move otherwise
	if target is not None:
		player.fighter.attack(target)
	else:
		player.move(dx, dy)
		fov_recompute = True



#Processing player attack, woop woo! we want the decision for whether an attack is possible to belong to the player's Fighter class rather than the weapon itself; we're putting the wrapper for all that stuff around here.
def process_player_attack(actionCommand):
	global upgrade_array

	# little adjustment that might not be necessary
	if actionCommand == "ATTCKDOWNALT":
		actionCommand = "ATTCKDOWN"

	#print('you pressed ' + str(key_char))

	if player_weapon.durability <= 0:
		if player_weapon.name == 'unarmed':
			message('You have no weapon!', Color_Not_Allowed)
		else:
			message('Your ' +  str(player_weapon.name) + ' is broken!', Color_Not_Allowed)
		return 'invalid-move'
	# check whether the weapon can do this kind of attack
	# probably this should be a separate command in the weapons class, but that would mean repeating yet more code or cleaning up how the weapon code exists, and I am too lazy to do either right now
	command_recognised = False
	for (com, data, usage) in player_weapon.command_items:
		if com == actionCommand:
			command_recognised = True
	if command_recognised == False:
		if player_weapon.name == 'unarmed':
			message('You have no weapon!', Color_Not_Allowed)
		else:
			message('You can\'t use a ' + str(player_weapon.name) + ' like that!', Color_Not_Allowed)
		return 'invalid-move'
		 

	else:
		energy_cost = player_weapon.get_usage_cost(actionCommand) + 1   #let's try and make weapons a bit harder to use...
		can_attack =  player.fighter.can_attack(energy_cost, return_message = True)

		# if able, do the attack!
		if can_attack == True:

			# Add extra bonus strength maybe! TODO: Probably put in own method later
			# For now, we are going to try: extra strength when next to a wall
			bonus_strength = 0

			# update the relevant upgrades
			# todo: this probably doesn't go here ultimately
			for power_up in upgrade_array:
				if getattr(power_up, "update_on_player_attack_choice", None) is not None:
					power_up.update_on_player_attack_choice(player, objectsArray, map, player_weapon)

			# get extra strength from the relevant upgrades
			for power_up in upgrade_array:
				if getattr(power_up, "affect_strength_at_attack_choice", None) is not None:
					bonus_strength += power_up.affect_strength_at_attack_choice()


		#	#let's do another bonus! standing on a shrine
		#	on_shrine = False
		#	for ob in objectsArray[player.x][player.y]:
		#		if ob.shrine is not None:
		#			print "+1 strength for being on an altar"
		#			bonus_strength += 1

			abstract_attack_data = player_weapon.do_energy_attack(actionCommand)
			temp_attack_list = process_abstract_attack_data(player.x,player.y, abstract_attack_data, player, bonus_strength)	
			player.decider.set_decision(Decision(attack_decision = Attack_Decision(attack_list=temp_attack_list)))
			player.fighter.lose_energy(energy_cost)
		
		#Note: this code might need to change in future if we decide to have other reasons for not being able to attack
		elif can_attack == 'energy too low':
			#message('Attack used up; can attack again in ' + str(player_weapon.default_usage - player_weapon.current_charge) + ' seconds.', libtcod.orange)
			message('You are too tired to attack', Color_Not_Allowed)
			return 'invalid-move'
		elif can_attack == 'in water':
			message('You are too busy treading water to attack', Color_Not_Allowed)
			return 'invalid-move'
		else:
			message('Error: cannot attack', Color_Not_Allowed)
			return 'invalid-move'

def process_abstract_attack_data(x,y,abstract_attack_data, attacker=None, bonus_strength = 0):
	# given data (i,j, val) from an abstract attack, produce an attack at co-ordinates x_i, y_j with damage val.
	# this function mainly exists because I am a bad programmer and can't figure out how to get the weapons file to recognise Attacks...
	temp_attack_list = []
	temp_color = color_swordsman  # libtcod.dark_red
	if attacker is not None:
		if attacker.fighter:
			temp_color = attacker.fighter.attack_color
	# not having this condition leads to the wierd event handling issues leaf to game-crashing bugs.
	# Let's add this condition so we can investigate the wierd handling issues a bit, and/or find another game-crashing bug
	if abstract_attack_data is not None:	
		for (i,j,val) in abstract_attack_data:
			# adjust attack for position, and also extra strength from the fighter.
			temp_attack = Object(x+i, y+j, '#', 'attack', temp_color, blocks=False, attack= BasicAttack(val + attacker.fighter.extra_strength + bonus_strength, attacker=attacker))
			temp_attack_list.append(temp_attack)
	return temp_attack_list

	

def player_death(player):
	#the game ended!
	global game_state
	message('You collapse to the floor...', Color_Dangerous_Combat)
	message('Press R to restart, Q to quit', Color_Menu_Choice)
	game_state = 'dead'
 
	#for added effect, transform the player into a corpse!
	player.char = '%'
	#player.color = libtcod.dark_red
 
def monster_death(monster):
	global garbage_list, favoured_by_healer, tested_by_destroyer, favoured_by_destroyer, tested_by_deliverer, favoured_by_deliverer, destroyer_test_count, deliverer_test_count, number_alarmers, alarm_level
	# drop the weapon the monster was carrying, if it had one.
	if monster.decider:
		if monster.decider.ai:
			if monster.decider.ai.weapon:
				if monster.name != 'strawman':
					item = get_item_from_weapon(monster.decider.ai.weapon, monster)
					# 30% chance of dropping?? If it's not a special item
					if item.name == 'ring of power':
						drop_weapon(item)
						reorder_objects(item.x, item.y)
					else:
						num = randint(0, 100)
						if num <= CHANCE_OF_ENEMY_DROP:
							drop_weapon(item)
							reorder_objects(item.x,item.y)
	

	#transform it into a nasty corpse! it doesn't block, can't be
	#attacked and doesn't move
	#if monster.name == 'security system':
	if monster.alarmer is not None:
		number_alarmers -= 1
		message(monster.name.capitalize() + ' is destroyed!', color_warning)
		if monster.alarmer.status != 'alarm-raised':
			message("Success! Defeated a " + monster.name.capitalize() + ' without triggering an alarm.', Color_Stat_Info)
		#decrease the alarm level alittle bit! Unless that was the last one, in which case set it to 0
		if number_alarmers > 0:
			if alarm_level > 0 and monster.alarmer.status == 'alarm-raised':
				alarm_level += (-monster.alarmer.alarm_value + monster.alarmer.dead_alarm_value)
				message('The alarms get a little quieter.', Color_Interesting_In_World)
		else:
			alarm_level = 0
			message('A sudden silence descends as the alarms stop.', Color_Interesting_In_World)

		# Temp hack, probably: if thismonster is an alarmer (i.e. a security system), make it drop currency?

		favour_object = Object(monster.x, monster.y, '$', 'favour token', color_tridentor, blocks = False,  always_visible=True)
		objectsArray[monster.x][monster.y].append(favour_object) 
		reorder_objects(monster.x, monster.y)


	else:	
		message(monster.name.capitalize() + ' is dead!', Color_Interesting_Combat)
	monster.char = '%'
	monster.color = default_weapon_color
	monster.blocks = False
	monster.fighter = None
	monster.decider = None
	monster.name = 'dying ' + monster.name
	monster.send_to_back()
	garbage_list.append(monster)

	#monster may drop a key?
	if monster.drops_key == True:
		new_key = Object(monster.x,monster.y, '*', 'key', PLAYER_COLOR, blocks = False, weapon = False, always_visible=True)
		objectsArray[monster.x][monster.y].append(new_key)
		# trigger a draw order cleanup, because otherwise you get enemies hiding under keys
		reorder_objects(monster.x, monster.y)

	#killing a monster affects some test stuff for the god of destruction
	if tested_by_destroyer:
		if destroyer_test_count > 0:
			destroyer_test_count -= 1
		if destroyer_test_count <= 0:
			tested_by_destroyer = False
			favoured_by_destroyer = True
			favoured_by_healer = False






def next_level():
	global dungeon_level, objectsArray, game_state, current_big_message, lev_set, favoured_by_healer, favoured_by_destroyer, favoured_by_deliverer, tested_by_deliverer, enemy_spawn_rate, deliverer_test_count, time_level_started, elevators, alarm_level, key_count, currency_count, spawn_timer,  already_healed_this_level, player, player_weapon, upgrade_array

	# doing some test saving
	save_game()


	#Go to the end screen if you just beat the final level woo!
	if lev_set.final_level is True:
		beat_game()	

	#moving to next level has affects for Taylor the Deliverer!
	if tested_by_deliverer and deliverer_test_count >= 0:
		favoured_by_deliverer = True




	#message("New ability: " + new_upgrade.name + ". " + new_upgrade.verbose_description, color_energy)


	# if leaving the tutorial, reset the players health + energy, and give them a fresh sword
	if dungeon_level == 0:
		print ("leaving tutorial, resetting player stats")
		player.fighter.hp = STARTING_ENERGY
		player.fighter.wounds = 0
		player_weapon = Weapon_Sword()
		#player_weapon = Weapon_Sai()
		#player_weapon = Weapon_Nunchuck()
		currency_count = STARTING_CURRENCY
		upgrade_array = []
	
		# give player a test upgrade?
		new_upgrade = Get_Test_Upgrade()
		upgrade_array.append(new_upgrade)



	dungeon_level += 1
	alarm_level = dungeon_level + 1
	key_count = 0
	time_level_started = game_time
	message('You ascend to the next level!', Color_Stat_Info)
	if favoured_by_healer == True:
		message('You hear the voice of ' + god_healer.name, Color_Interesting_In_World)
		message('\"Behold my child! Faith in me shall always be rewarded.\"', Color_Message_In_World)
		player.fighter.max_hp = player.fighter.max_hp + 1
		player.fighter.cure_wounds(3)
		player.fighter.fully_heal()
		#player.fighter.heal(5)
		message('You feel rejuvenated!', Color_Stat_Info)
		favoured_by_healer = False

	if favoured_by_destroyer == True:
		message('You hear the voice of ' + god_destroyer.name, Color_Interesting_In_World)
		message('\"Your destruction pleases me. I shall grant you a boon!\"', Color_Message_In_World)
		#player.fighter.fully_heal()
		player.fighter.increase_strength(1)
		message('You feel stronger!', Color_Stat_Info)
		favoured_by_destroyer = False

	if favoured_by_deliverer == True:
		message('You hear the voice of ' + god_deliverer.name, Color_Interesting_In_World)
		message('\"Good job! Here\'s your reward. Have fun with it!\"', Color_Message_In_World)
		#player.fighter.increase_recharge_rate(1)
		# make the player always have an increased max charge on their weapon
		player.fighter.increase_max_charge(1)
		player_weapon.max_charge = player_weapon.max_charge + 1
		message('You feel faster!', Color_Stat_Info)
		favoured_by_deliverer = False
		tested_by_deliverer = False

	already_healed_this_level = False



	#objects = []
	make_map()
	objectsArray[player.x][player.y].append(player)
	worldEntitiesList.append(player)
	print( 'heyo (' + str(player.x) + ',' + str(player.y))	

   	#make_map()  #create a fresh new level!
	#objects = [player]				#TODO/NOTE: When changing to 'objectsArray', this might cause problems?
							# Think it's enough to move this to after make_map(), and then use player's x and y
							# well... there might be an issue of initialising arrays as well...


	x_offset = int(camera.x-(SCREEN_WIDTH + MESSAGE_PANEL_WIDTH)/2)
	y_offset = int(camera.y-(SCREEN_HEIGHT-PANEL_HEIGHT)/2)
	for yOff in range(ACTION_SCREEN_HEIGHT):
		y = yOff + y_offset
		for xOff in range(ACTION_SCREEN_WIDTH):
			x = xOff + x_offset + ACTION_SCREEN_X
			if (y >= MAP_HEIGHT or x>= MAP_WIDTH):
				translated_console_set_char_background(con, x, y, color_big_alert, color_big_alert)
			else:
				if y in range(MAP_HEIGHT) and x in range(MAP_WIDTH):
					map[x][y].explored = False
					translated_console_set_char_background(con, x, y, color_fog_of_war, libtcod_BKGND_SET)

#	for y in range(SCREEN_HEIGHT):
#		for x in range(SCREEN_WIDTH):
#			if (y >= MAP_HEIGHT or x>= MAP_WIDTH):
#				#map[x][y].explored = False
#				translated_console_set_char_background(con, x, y, color_big_alert, color_big_alert)
#				#print "blah (" + str(x) + "," + str(y) + ")" 
#			else:
#				map[x][y].explored = False
#				translated_console_set_char_background(con, x, y, color_fog_of_war, libtcod_BKGND_SET)
#				#print "bloo (" + str(x) + "," + str(y) + ")" 


	initialize_fov()


	lev_set = game_level_settings.get_setting(dungeon_level)
	enemy_spawn_rate = lev_set.enemy_spawn_rate
	spawn_timer = decide_spawn_time(enemy_spawn_rate,alarm_level)

	#for ele in elevators:			#open the doors when the level starts?
	#	ele.set_doors_open(True)
	#DOESN'T WORK, SO YOU HAVE TO WAIT A TURN BEFORE THE DOORS OPEN. WHICH IS ANNOYING

	#current_big_message = "As you ascend the stairs, you inwardly breathe a sigh of relief. The trials of the floor below you are now in the past, but what dangers lie up ahead? Your enemies only seem to be getting more deadly the closer you get to your nemesis. You think back to the wise words of your mentor: \"Stick 'em with the pointy end.\""

	#game_state  = 'big message'


# Figure out how often enemies should spawn, based on overall rate for this floor, and the alarm level.
# Originally was just one divided by the other; now it's going to be something a bit more tierd, hopefully?
# Update: might have been my fault for not making it visible to the player, but I  wasn't really feeling the tiered system.
# Going back to 'faster with higher alarm'; 
# I have some ideas about how to make it more exicitng to avoid alarms so am going to make alarm level more of a threat?
def decide_spawn_time(enemy_spawn_rate,alarm_level):
	return int(4*enemy_spawn_rate/alarm_level)

#	# spawn very rarely (i mean, ideally not at all but whatevs) if alarm level is 0.
#	if alarm_level == 0:
#		return 100 * enemy_spawn_rate
#	elif alarm_level <= 2:
#		return 2*enemy_spawn_rate
#	elif alarm_level <= 6:
#		return enemy_spawn_rate
#	else:
#		return int(4*enemy_spawn_rate/alarm_level)




def beat_game():
	global dungeon_level, objectsArray, game_state, current_big_message
	#current_big_message = "As you ascend the stairs, the air around you crackles with electricity. Reaching the rooftop of the building, you stare into the sunrise of a beautiful new day. With the wizard defeated and the ring of power in your hands, there is no one to stand in your way. This city will be yours!"
	game_state  = 'end message'


def initialize_fov():
	global fov_recompute, fov_map
	fov_recompute = True

	print ("INITIALISING FOV")

	#create the FOV map, according to the generated map
	#fov_map = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
	fov_map = libtcod.map.Map(MAP_WIDTH, MAP_HEIGHT)
	for y in range(MAP_HEIGHT):
		for x in range(MAP_WIDTH):
			#libtcod.map_set_properties(fov_map, x, y, not map[x][y].block_sight, not map[x][y].blocked)
			#libtcod.map_set_properties(fov_map, x, y, not map[x][y].block_sight, not map[x][y].blocked)

            		# TODO If things end up looking really wierd, it might be because the lines below are wrong
			fov_map.walkable[x, y] = not map[x][y].blocked
			fov_map.transparent[x, y] = not map[x][y].block_sight

	#print "FOV intialized"


def get_weapon_from_item(item, bonus_max_charge= 0):
	global current_big_message, game_state
	name = item.name
	return get_weapon_from_name(name, bonus_max_charge)

def get_weapon_from_name(name, bonus_max_charge = 0):
	if name == 'sword':
		#new_weapon =  Weapon_Wierd_Sword()
		new_weapon =  Weapon_Sword()
	elif name == 'dagger':
		new_weapon =  Weapon_Dagger()
	elif name == 'bo staff':
		#new_weapon =  Weapon_Wierd_Staff()
		new_weapon =  Weapon_Staff()
	elif name == 'spear':
		new_weapon =  Weapon_Spear()
	elif name == 'sai':
		new_weapon =  Weapon_Sai()
	elif name == 'nunchaku':
		new_weapon =  Weapon_Nunchuck()
	elif name == 'axe':
		new_weapon =  Weapon_Axe()
	elif name == 'katana':
		new_weapon =  Weapon_Katana()
	elif name == 'hammer':
		new_weapon =  Weapon_Hammer()
	elif name == 'trident':
		new_weapon =  Weapon_Trident()
	elif name == 'ring of power':
		new_weapon =  Weapon_Ring_Of_Power()
	else:
		new_weapon = None

	if new_weapon is not None:
		new_weapon.max_charge = new_weapon.max_charge + bonus_max_charge
	
	return new_weapon

def get_item_from_weapon(weapon, dropper=None):
	if dropper is None:
		dropper = player
	name = weapon.name
	return get_item_from_name(dropper.x, dropper.y, name)

#	char = '?'
#	object = None
#	if name == 'sword':
#		char = 's'
#	elif name == 'dagger':
#		char = 'd' 
#	elif name == 'bo staff':
#		char = 'b'
#	elif name == 'sai':
#		char = 'f'
#	elif name == 'axe':
#		char = 'x'
#	elif name == 'ring of power':
#		char = 'o'
#	object = Object(dropper.x, dropper.y, char, name, default_weapon_color, blocks=False, weapon = True)
#	return object

def get_item_from_name(x,y, name):
	#if dropper is None:
	#	dropper = player
	#name = weapon.name
	char = '?'
	object = None
	if name == 'sword':
		char = 's'
	elif name == 'dagger':
		char = 'd' 
	elif name == 'bo staff':
		char = 'b'
	elif name == 'spear':
		char = 'l'
	elif name == 'sai':
		char = 'f'
	elif name == 'nunchaku':
		char = 'n'
	elif name == 'axe':
		char = 'x'
	elif name == 'katana':
		char = 'k'
	elif name == 'hammer':
		char = 'h'
	elif name == 'trident':
		char = 't'
	elif name == 'ring of power':
		char = 'o'
	object = Object(x, y, char, name, default_weapon_color, blocks=False, weapon = True, always_visible = True)
	return object



def drop_weapon(weapon_item):
	weapon_name = weapon_item.name
	weapon_x = weapon_item.x
	weapon_y = weapon_item.y
	# check to see if there's already an item with the same name in this location
	copy_found = False
	for object in objectsArray[weapon_x][weapon_y]:
		if object.name == weapon_name:
			copy_found = True

	# only drop the item if there isn't an item with the same name in this location.
	if copy_found == False:
		objectsArray[weapon_x][weapon_y].append(weapon_item)
		weapon_item.send_to_back()


def create_shrine(x,y,god_type):
		global god_healer, god_destroyer, god_deliverer
		god = None
		if god_type == 'healer':
			god = god_healer
		if god_type == 'destroyer':
			god = god_destroyer
		if god_type == 'deliverer':
			god = god_deliverer
		new_shrine = Object(x, y, '&', 'shrine to ' + god.name, default_altar_color, blocks=False, shrine= Shrine(god), always_visible=True)
		objectsArray[x][y].append(new_shrine)
		new_shrine.send_to_back()



def restart_game(): 	#TODO OKAY SO THERE IS A WIERD BUG WHERE WHEN YOU RESTART THE GAME IT DOESN'T KNOW THAT THE FINAL LEVEL IS THE FINAL LEVEL??? OK GOOD NEWS THOUGH IT ONLY SEEMS TO BE IF THE FINAL LEVEL IS THE FIRST LEVEL? MAYBE? SO HOPEFULLY WE CAN JUST LEAVE IT
	global dungeon_level

	dungeon_level = 0
	alarm_level = 1
	key_count = 0
	currency_count = STARTING_CURRENCY
	make_map()  #create a fresh new level!
	print("DOING RESTQRT GQME")
	for y in range(MAP_HEIGHT):
		for x in range(MAP_WIDTH):
			map[x][y].explored = False
			translated_console_set_char_background(con, x, y, color_fog_of_war, libtcod_BKGND_SET)
	initialize_fov()
	initialise_game()






#def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color):
#	#render a bar (HP, experience, etc). first calculate the width of the bar
#	bar_width = int(float(value) / maximum * total_width)
#
#	#render the background first
#	libtcod.console_set_default_background(panel, back_color)
#	libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)
#
#	#now render the bar on top
#	libtcod.console_set_default_background(panel, bar_color)
#	if bar_width > 0:
#		libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)
#
#	#finally, some centered text with the values
#	libtcod.console_set_default_foreground(panel, default_text_color)
#	translated_console_print_ex(panel, x + total_width / 2, y, libtcod_BKGND_NONE, libtcod_CENTER,
#	name + ': ' + str(value) + '/' + str(maximum))
		


def message(new_msg, color = default_text_color):

	print(str(color))

	# Turn hashtag shortcuts into actual key commands
	new_msg = translateCommands(new_msg)

	#split the message if necessary, among multiple lines
	new_msg_lines = textwrap.wrap(new_msg, MSG_WIDTH)

	for line in new_msg_lines:
		#if the buffer is full, remove the first line to make room for the new one
		if len(game_msgs) == MSG_HEIGHT:
			del game_msgs[0]

		#add the new line as a tuple, with the text and the color
		game_msgs.append( (line, color) )


# searches through a string for strings of the form '#COMMAND#, and replaces them with the result of looking up COMMAND in the control handler.
def translateCommands(msg):
	global controlHandler


	searchForHashtags = True
	while searchForHashtags == True:
		# find the next command string, if one exists
		firstHashtag = -1
		nextHashtag = -1
		firstHashtag = msg.find('#')
		if firstHashtag == -1:
			searchForHashtags = False
		else:
			nextHashtag = msg[firstHashtag+1:].find('#') + firstHashtag
		if nextHashtag == -1:
			searchForHashtags = False
		else:
			command_substring = msg[firstHashtag +1: nextHashtag+1]
			# Look up the control string corresponding to this command
			print ("Found hashtag " + command_substring)
			replacement_string = "?"
			if command_substring in controlHandler.controlLookup:
				replacement_string = controlHandler.controlLookup[command_substring]
			elif command_substring in controlHandler.menuDictionary:
				replacement_string = controlHandler.menuDictionary[command_substring]
		
			# replace the command string with the control string, and then keep looking for hastags
			new_msg = msg[:firstHashtag] + replacement_string + msg[nextHashtag+2:]
			msg = new_msg
			searchForHashtags = True
	return msg
	#controlLookup
	#menuDictionary

def pause_screen():
	global test_save_message, gameSaveDataHandler, play_count

	# print the pause screen I guess 
	translated_console_set_default_background(pause_menu, default_background_color)
	translated_console_clear(pause_menu)
	translated_console_set_default_foreground(pause_menu, default_text_color)
	translated_console_print_ex_center(pause_menu, SCREEN_WIDTH/2, 2, libtcod_BKGND_NONE, libtcod_CENTER,
	'The game is paused')
	translated_console_print_ex_center(pause_menu, SCREEN_WIDTH/2, 4, libtcod_BKGND_NONE, libtcod_CENTER,
	'Press Esc to unpause, C to change controls or Q to quit')
	#translated_console_print_ex(pause_menu, SCREEN_WIDTH/2, 3, libtcod_BKGND_NONE, libtcod_CENTER,
	#test_save_message)
	translated_console_print_ex_center(pause_menu, SCREEN_WIDTH/2, 6, libtcod_BKGND_NONE, libtcod_CENTER,
	"This is play number " + str(play_count))
	
	translated_console_print_ex_center(pause_menu, SCREEN_WIDTH/2, 8, libtcod_BKGND_NONE, libtcod_CENTER,
	'-------------------------------------------------------')
	# Add a list of what upgrades the player has
	current_line = 10
	for upgrade in upgrade_array:
		if current_line < SCREEN_HEIGHT:
			translated_console_print_ex_center(pause_menu, SCREEN_WIDTH/2, current_line, libtcod_BKGND_NONE, libtcod_CENTER, 
			upgrade.name + ': ' + upgrade.tech_description)
			current_line += 2



	#blit the contents of "pause_menu" to the root console
	#libtcod.console_blit(pause_menu, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
	root_console.blit(pause_menu, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)	


def control_screen():
	global test_save_message, gameSaveDataHandler, play_count, controlHandler

	# print the pause screen I guess 
	translated_console_set_default_background(pause_menu, default_background_color)
	translated_console_clear(pause_menu)
	translated_console_set_default_foreground(pause_menu, default_text_color)
	translated_console_print_ex_center(pause_menu, SCREEN_WIDTH/2, 2, libtcod_BKGND_NONE, libtcod_CENTER,
	'Control Settings')
	translated_console_print_ex_center(pause_menu, SCREEN_WIDTH/2, 4, libtcod_BKGND_NONE, libtcod_CENTER,
	'Select a control scheme, or press Esc to return to pause menu')

	translated_console_print_ex_center(pause_menu, SCREEN_WIDTH/2, 6, libtcod_BKGND_NONE, libtcod_CENTER,
	'-------------------------------------------------------')

	
	# Add a list of available options
	current_line = 8
	for i in range(len(controlHandler.controlOptionsArray)):
		(control_code, control_description) = controlHandler.controlOptionsArray[i]
		control_option_string = controlHandler.letterFromInt[i+1] + ": " + control_description
		translated_console_print_ex(pause_menu, int(SCREEN_WIDTH/4), current_line, libtcod_BKGND_NONE, libtcod_CENTER, 
		control_option_string)
		current_line += 2



	#blit the contents of "pause_menu" to the root console
	#libtcod.console_blit(pause_menu, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
	root_console.blit(pause_menu, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)	

def big_message(string):	

	#split the message if necessary, among multiple lines
	new_msg_lines = textwrap.wrap(string, MSG_WIDTH)


	# print the big message
	translated_console_set_default_background(pause_menu, default_background_color)
	translated_console_clear(pause_menu)
	translated_console_set_default_foreground(pause_menu, default_text_color)
	y = 2
	for line in new_msg_lines:
		translated_console_print_ex_center(pause_menu, SCREEN_WIDTH/2, y, libtcod_BKGND_NONE, libtcod_CENTER, line)
		y = y + 1

	#blit the contents of "pause_menu" to the root console
	#libtcod.console_blit(pause_menu, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
	root_console.blit(pause_menu, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)

def end_message():
	global current_big_message
	
	current_big_message = "As you ascend the stairs, THE MIGHTY MIGHTY STAIRS, the air around you crackles with electricity. Reaching the rooftop of the building, you stare into the sunrise of a beautiful new day. With the wizard defeated and the ring of power in your hands, there is no one to stand in your way. \n This city will be yours!"
	string = current_big_message

	#split the message if necessary, among multiple lines
	new_msg_lines = textwrap.wrap(string, MSG_WIDTH)


#	# print the big message
#	libtcod.console_set_default_background(pause_menu, default_background_color)
#	libtcod.console_clear(pause_menu)
#	libtcod.console_set_default_foreground(pause_menu, default_text_color)

	pause_menu.clear(fg=default_text_color, bg=default_background_color)

	y = 2
	for line in new_msg_lines:
		# libtcod.console_print_ex(pause_menu, SCREEN_WIDTH/2, y, libtcod_BKGND_NONE, libtcod_CENTER, line)
		pause_menu.draw_str(int(SCREEN_WIDTH/2), y, line, fg=default_text_color, bg=None)

		y = y + 1

	#blit the contents of "pause_menu" to the root console
#	libtcod.console_blit(pause_menu, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
	root_console.blit(pause_menu, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)
	

def end_data_message():
	global current_big_message, player_weapon, game_time

	string = current_big_message
	data_string = "You ascended the tower with the " + player_weapon.name + " in " + str(game_time) + " seconds."

#split the message if necessary, among multiple lines
	new_msg_lines = textwrap.wrap(string, MSG_WIDTH)
	new_data_msg_lines = textwrap.wrap(data_string, MSG_WIDTH)

	# print the big message
	#libtcod.console_set_default_background(pause_menu, default_background_color)
	#libtcod.console_clear(pause_menu)
	#libtcod.console_set_default_foreground(pause_menu, default_text_color)
	pause_menu.clear(fg = default_text_color, bg = default_background_color)

	y = 2
	for line in new_msg_lines:
		#libtcod.console_print_ex(pause_menu, SCREEN_WIDTH/2, y, libtcod_BKGND_NONE, libtcod_CENTER, line)
		pause_menu.draw_str(int(SCREEN_WIDTH/2), y, line, bg = None, fg = default_text_color) #, libtcod_CENTER)
		y = y + 1
	y = y + 2

	for line in new_data_msg_lines:
		# libtcod.console_print_ex(pause_menu, SCREEN_WIDTH/2, y, libtcod_BKGND_NONE, libtcod_CENTER, line)
		pause_menu.draw_str(int(SCREEN_WIDTH/2), y, line, bg = None, fg = default_text_color) #, libtcod_CENTER)
		y = y + 1

	#blit the contents of "pause_menu" to the root console
	# libtcod.console_blit(pause_menu, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
	root_console.blit(pause_menu, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)
	

def restartynscreen():
	global current_big_message, player_weapon, game_time

	string = current_big_message
	data_string = "You ascended the tower with the " + player_weapon.name + " in " + str(game_time) + " seconds."
	query_string = "Would you like to play again? (y/n)"	

#split the message if necessary, among multiple lines
	new_msg_lines = textwrap.wrap(string, MSG_WIDTH)
	new_data_msg_lines = textwrap.wrap(data_string, MSG_WIDTH)
	new_query_msg_lines = textwrap.wrap(query_string, MSG_WIDTH)


	# print the big message
	#libtcod.console_set_default_background(pause_menu, default_background_color)
	#libtcod.console_clear(pause_menu)
	#libtcod.console_set_default_foreground(pause_menu, default_text_color)
	pause_menu.clear(fg = default_text_color, bg = default_background_color)
	y = 2
	for line in new_msg_lines:
		# libtcod.console_print_ex(pause_menu, SCREEN_WIDTH/2, y, libtcod_BKGND_NONE, libtcod_CENTER, line)
		pause_menu.draw_str(int(SCREEN_WIDTH/2), y, line, bg = None, fg = default_text_color)#, libtcod_CENTER)
		y = y + 1
	y = y + 2
	for line in new_data_msg_lines:
		# libtcod.console_print_ex(pause_menu, SCREEN_WIDTH/2, y, libtcod_BKGND_NONE, libtcod_CENTER, line)
		pause_menu.draw_str(int(SCREEN_WIDTH/2), y, line, bg = None, fg = default_text_color)#, libtcod_CENTER)
		y = y + 1
	y = y+2
	for line in new_query_msg_lines:
		# libtcod.console_print_ex(pause_menu, SCREEN_WIDTH/2, y, libtcod_BKGND_NONE, libtcod_CENTER, line)
		pause_menu.draw_str(int(SCREEN_WIDTH/2), y, line, bg = None, fg = default_text_color)#, libtcod_CENTER)
		y = y + 1

	#blit the contents of "pause_menu" to the root console
	# libtcod.console_blit(pause_menu, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
	root_console.blit(pause_menu, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)

def render_all():

	global fov_map, color_dark_wall, color_light_wall
	global color_dark_ground, color_light_ground, color_light_ground_alt
	global fov_recompute, bgColorArray

	if fov_recompute:
		#recompute FOV if needed (the player moved or something)
		fov_recompute = False
		# libtcod.map_compute_fov(fov_map, player.x, player.y, TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)
		fov_map.compute_fov(player.x, player.y, fov=FOV_ALGO, radius=TORCH_RADIUS, light_walls=FOV_LIGHT_WALLS)

	update_camera()
	#x_offset = camera.x-SCREEN_WIDTH/2
	x_offset = int(camera.x-(SCREEN_WIDTH + MESSAGE_PANEL_WIDTH)/2)
	#y_offset = camera.y-SCREEN_HEIGHT/2
	y_offset = int(camera.y-(SCREEN_HEIGHT-PANEL_HEIGHT)/2)

	#for y in range(SCREEN_HEIGHT):
	#	for x in range(SCREEN_WIDTH):
	##		libtcod.console_set_char_background(con, x, y, color_fog_of_war, libtcod_BKGND_SET)
	#		con.draw_char(x, y, None, fg=None, bg=color_fog_of_war)

	for y in range(ACTION_SCREEN_HEIGHT):
		for x in range(ACTION_SCREEN_WIDTH):
			con.draw_char(x + ACTION_SCREEN_X, y, None, fg=None, bg=color_fog_of_war)

	#go through all tiles, and set their background color according to the FOV
#	print("'fixed':	 UPDATING BACKGROUNDS AS PART OF RENDER_ALL")
	#for y in range(MAP_HEIGHT):
	#	for x in range(MAP_WIDTH):
	for yOff in range(ACTION_SCREEN_HEIGHT):
		y = yOff + y_offset
		if y in range(MAP_HEIGHT):
			for xOff in range(ACTION_SCREEN_WIDTH):
				x = xOff + x_offset + ACTION_SCREEN_X
				if x in range(MAP_WIDTH):
					#visible = True # temporary hack to test enemy navigation
					visible = fov_map.fov[x, y]
					wall = map[x][y].blocked 	#block_sight
					
					#if False:
					if not visible:
						#if it's not visible right now, the player can only see it if it's explored	
						if map[x][y].explored:
						#if True: 	#temp making walls and such visible to check enemy behaviour
							#it's out of the player's FOV
							if wall:
								con.draw_char(x - x_offset, y - y_offset, None, fg = None, bg =color_dark_wall)
								# libtcod.console_set_char_background(con, x - x_offset, y - y_offset, color_dark_wall, libtcod_BKGND_SET)
							else:
								con.draw_char(x - x_offset, y - y_offset, None, fg = None, bg =color_dark_ground)
								# libtcod.console_set_char_background(con, x - x_offset, y - y_offset, color_dark_ground, libtcod_BKGND_SET)
						else: 					
							con.draw_char(x - x_offset, y - y_offset, None, fg = None, bg =color_fog_of_war)
							#libtcod.console_set_char_background(con, x - x_offset, y - y_offset, color_fog_of_war, libtcod_BKGND_SET)
					else:
						#todo update based on some desired background colors
						#libtcod.console_set_char_background(con, x - x_offset, y - y_offset, bgColorArray[x][y], libtcod_	BKGND_SET)		
						con.draw_char(x - x_offset, y - y_offset, None, fg = None, bg =bgColorArray[x][y])
				
	
			#			if wall:
			#				libtcod.console_set_char_background(con, x - x_offset, y - y_offset, bgColorArray[x][y], libtcod_BKGND_SET  )
			#				libtcod.console_set_char_background(con, x - x_offset, y - y_offset, color_light_wall, libtcod_BKGND_SET  )
			#			else:
			#				libtcod.console_set_char_background(con, x - x_offset, y - y_offset, color_light_ground, libtcod_BKGND_SET )
					
						map[x][y].explored = True


	# do some background type stuff based, on whether someone has just been attacked.
#	print("'fixed':	 MORE UPDATING BACKGROUNDS AS PART OF RENDER_ALL")

	for yOff in range(ACTION_SCREEN_HEIGHT):
		y = yOff + y_offset
		if y in range(MAP_HEIGHT):
			for xOff in range(ACTION_SCREEN_WIDTH):
				x = xOff + x_offset + ACTION_SCREEN_X
				if x in range(MAP_WIDTH):
					for object in objectsArray[x][y]:
						#if libtcod.map_is_in_fov(fov_map, x, y) == True:
						if fov_map.fov[x, y] == True:
							if object.name == 'water':
								#libtcod.console_set_char_background(con, object.x - x_offset, object.y - y_offset, water_background_color, libtcod_BKGND_SET )
								con.draw_char(object.x - x_offset, object.y - y_offset, None, fg = None, bg = water_background_color)
							if object.name == 'blood':
								# libtcod.console_set_char_background(con, object.x - x_offset, object.y - 	y_offset, blood_background_color, libtcod_BKGND_SET )
								con.draw_char(object.x - x_offset, object.y - y_offset, None, fg = None, bg = water_background_color)
							# ok but if there's attacks draw those instead
							for other_object in objectsArray[x][y]:
								if object is not other_object:
									if object.attack is not None and other_object.fighter is not None:
										# libtcod.console_set_char_background(con, object.x - x_offset, object.y - y_offset, object.attack.faded_color, libtcod_BKGND_SET )
										con.draw_char(object.x - x_offset, object.y - y_offset, None, fg = None, bg = object.attack.faded_color)

						# DRAW ALL THE THINGS
						object.draw()

		#	for object in objects:
		#		if libtcod.map_is_in_fov(fov_map, object.x, object.y) == True:
		#			for other_object in objects:
		#				if object is not other_object and object.x == other_object.x and object.y == other_object.y:
		#					if object.attack is not None and other_object.fighter is not None:
		#						libtcod.console_set_char_background(con, object.x - x_offset, object.y - 	y_offset, object.attack.faded_color, libtcod_BKGND_SET )
		#			if object.name == 'water':
		#				libtcod.console_set_char_background(con, object.x - x_offset, object.y - y_offset, water_background_color, libtcod_BKGND_SET )
		#			if object.name == 'blood':
		#				libtcod.console_set_char_background(con, object.x - x_offset, object.y - y_offset, blood_background_color, libtcod_BKGND_SET )
		#
		#	for object in objects:
		#		#if object != player:
		#		object.draw()
		#	#player.draw()
		#	


	player.send_to_front()			
	

#	libtcod.console_blit(con, 0, 0, MAP_WIDTH, MAP_HEIGHT, 0, 0, 0)
#	libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
	root_console.blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)
	

	
	# write GUI stuff to "panel"
	create_GUI_panel()
	create_message_panel()


def create_GUI_panel():
	global fov_map, color_dark_wall, color_light_wall
	global color_dark_ground, color_light_ground, color_light_ground_alt
	global fov_recompute, bgColorArray
	global game_level_settings, dungeon_level
	global controlHandler
	global upgrade_array


	lev_set = game_level_settings.get_setting(dungeon_level)

	#GUI STUFF
	#prepare to render the GUI panel
	#libtcod.console_set_default_background(panel, default_background_color)
	#libtcod.console_clear(panel)
	panel.clear(fg = default_text_color, bg= default_background_color)

	# Three subpanels within this panel. From left to right: attack panel, player panel, level panel
	# Suprise 4th panel: upgrades ?
	attack_panel_width = 20
	player_panel_width = 20
	level_panel_width = 20
	upgrade_panel_width = 13
	attack_panel_x = 1
	player_panel_x = attack_panel_x + attack_panel_width + 1
	level_panel_x = player_panel_x + player_panel_width + 1
	upgrade_panel_x = SCREEN_WIDTH - upgrade_panel_width


	#ATTACK PANEL STUFF
	#change color based on weapon status
	attack_panel_default_color = default_text_color
	if player_weapon.durability <= 0:
		attack_panel_default_color = color_big_alert
	elif player_weapon.durability <= WEAPON_FAILURE_WARNING_PERIOD:
		attack_panel_default_color = color_warning
	elif player_weapon.current_charge < player_weapon.default_usage:
		attack_panel_default_color = color_tridentor


	#libtcod.console_set_default_foreground(panel, attack_panel_default_color)
	if len(player_weapon.name) <= attack_panel_width - 10:
		# libtcod.console_print_ex(panel, attack_panel_x, 1, libtcod_BKGND_NONE, libtcod_LEFT,
	#'Weapon: ' + str(player_weapon.name).upper())
		panel.draw_str(attack_panel_x, 1, ('Weapon: ' + str(player_weapon.name).upper()), fg=attack_panel_default_color, bg=None)

	else:
		#libtcod.console_print_ex(panel, attack_panel_x, 1, libtcod_BKGND_NONE, libtcod_LEFT,
	#str(player_weapon.name).upper())
		panel.draw_str(attack_panel_x, 1, ('Weapon: ' + str(player_weapon.name).upper()), fg=attack_panel_default_color, bg=None)

	# list some attacks out.
	attack_list = str(player_weapon.command_list)
	#libtcod.console_print_ex(panel, attack_panel_x, 3, libtcod_BKGND_NONE, libtcod_LEFT, "Attacks:")
	panel.draw_str(attack_panel_x, 3, "Attacks:", fg=attack_panel_default_color, bg=None)
	## set colors based on weapon durability
	#if player_weapon.durability <= 0:
	#		libtcod.console_set_default_foreground(panel, libtcod.orange)
	#elif player_weapon.durability <= WEAPON_FAILURE_WARNING_PERIOD:
	#		libtcod.console_set_default_foreground(panel, libtcod.orange)
	#else: 
	#		libtcod.console_set_default_foreground(panel, libtcod.white)
		


	#Here's a little bit of hackery to  make this code  rewrite a bit less tedious or at least more interesting.
	command_display_list = []
	command_display_list.append((-1,-1,controlHandler.singleCharacterControlLookup["ATTCKUPLEFT"],ATTCKUPLEFT))
	command_display_list.append((0,-1,controlHandler.singleCharacterControlLookup["ATTCKUP"],ATTCKUP))
	command_display_list.append((1,-1,controlHandler.singleCharacterControlLookup["ATTCKUPRIGHT"],ATTCKUPRIGHT))
	command_display_list.append((1,0,controlHandler.singleCharacterControlLookup["ATTCKRIGHT"],ATTCKRIGHT))
	command_display_list.append((1,1,controlHandler.singleCharacterControlLookup["ATTCKDOWNRIGHT"],ATTCKDOWNRIGHT))
	command_display_list.append((0,1,controlHandler.singleCharacterControlLookup["ATTCKDOWN"],ATTCKDOWN))
	command_display_list.append((-1,1,controlHandler.singleCharacterControlLookup["ATTCKDOWNLEFT"],ATTCKDOWNLEFT))
	command_display_list.append((-1,0,controlHandler.singleCharacterControlLookup["ATTCKLEFT"],ATTCKLEFT))

	for(x_adjust, y_adjust, command_str, attck_str) in  command_display_list:
		# only display the command if an attack exists for it? that's the idea anyway.
		command_recognised = False
		for (com, data, usage) in player_weapon.command_items:
			if com == attck_str:
				command_recognised = True
		if command_recognised == True:
			panel.draw_char(int(attack_panel_x + attack_panel_width/2 + 2*x_adjust) , 4 + y_adjust, command_str, bg=None, fg=attack_panel_default_color)
	# Commented out: could have a symbol to mean 'no attack available' here, 
	# but I think that's a bad idea given various puntuation can get used as actual commands
	#	else:
	#		panel.draw_char(int(attack_panel_x + attack_panel_width/2 + 2*x_adjust) , 4 + y_adjust, '-', bg=None, fg=attack_panel_default_color)



#	if ATTCKUPLEFT in attack_list:
#			libtcod.console_print_ex(panel, attack_panel_x + attack_panel_width/2 - 2, 3, libtcod_BKGND_NONE, libtcod_CENTER,
#		ATTCKUPLEFT)
#
#	if ATTCKUP in attack_list:
#			libtcod.console_print_ex(panel, attack_panel_x + attack_panel_width/2, 3, libtcod_BKGND_NONE, libtcod_CENTER,
#		ATTCKUP)
#
#	if ATTCKUPRIGHT in attack_list:
#			libtcod.console_print_ex(panel, attack_panel_x + attack_panel_width/2 + 2, 3, libtcod_BKGND_NONE, libtcod_CENTER,
#		ATTCKUPRIGHT)
#
#	if ATTCKLEFT in attack_list:
#			libtcod.console_print_ex(panel, attack_panel_x + attack_panel_width/2 - 2, 4, libtcod_BKGND_NONE, libtcod_CENTER,
#		ATTCKLEFT)
#
#
#	if ATTCKRIGHT in attack_list:
#			libtcod.console_print_ex(panel, attack_panel_x + attack_panel_width/2 + 2, 4, libtcod_BKGND_NONE, libtcod_CENTER,
#		ATTCKRIGHT)
#
#		
#	if ATTCKDOWNLEFT in attack_list:
#			libtcod.console_print_ex(panel, attack_panel_x + attack_panel_width/2 - 2, 5, libtcod_BKGND_NONE, libtcod_CENTER,
#		ATTCKDOWNLEFT)
#
#	if ATTCKDOWN in attack_list:
#			libtcod.console_print_ex(panel, attack_panel_x + attack_panel_width/2, 5, libtcod_BKGND_NONE, libtcod_CENTER,
#		ATTCKDOWN)
#
#	if ATTCKDOWNRIGHT in attack_list:
#			libtcod.console_print_ex(panel, attack_panel_x + attack_panel_width/2 + 2, 5, libtcod_BKGND_NONE, libtcod_CENTER,
#		ATTCKDOWNRIGHT)
#	libtcod.console_set_default_foreground(panel, attack_panel_default_color)

	# Display weapon charge details.
	#libtcod.console_print_ex(panel, attack_panel_x, 6, libtcod_BKGND_NONE, libtcod_LEFT,	'Weight: ' + str(player_weapon.get_default_usage_cost() + 1))
	panel.draw_str(int(attack_panel_x) , 6, 'Weight: ' + str(player_weapon.get_default_usage_cost() + 1), bg=None, fg=attack_panel_default_color)

	#uncharged_color = libtcod.blue
	#insufficient_charge_color = libtcod.red
	#charge_color = libtcod.green
	#bonus_charge_color = libtcod.darker_green
	#libtcod.console_print_ex(panel, attack_panel_x, 6, libtcod_BKGND_NONE, libtcod_LEFT,	'Charge:')
	#if player_weapon.current_charge < player_weapon.default_usage:
	#	libtcod.console_set_default_foreground(panel, insufficient_charge_color)
	#	for i in range(player_weapon.current_charge):
	#		libtcod.console_print_ex(panel, attack_panel_x + 7 + i, 6, libtcod_BKGND_NONE, libtcod_LEFT, '*')
	#else:
	#	libtcod.console_set_default_foreground(panel, bonus_charge_color)
	#	for i in range(player_weapon.current_charge - player_weapon.default_usage):
	#		libtcod.console_print_ex(panel, attack_panel_x + 7 + i, 6, libtcod_BKGND_NONE, libtcod_LEFT, '*')
	#	libtcod.console_set_default_foreground(panel, charge_color)
	#	for i in range(player_weapon.current_charge - player_weapon.default_usage, player_weapon.current_charge):
	#		libtcod.console_print_ex(panel, attack_panel_x + 7 + i, 6, libtcod_BKGND_NONE, libtcod_LEFT, '*')
	#
	#libtcod.console_set_default_foreground(panel, uncharged_color)
	#for i in range(player_weapon.current_charge, player_weapon.max_charge):
	#	libtcod.console_print_ex(panel, attack_panel_x + 7 + i, 6, libtcod_BKGND_NONE, libtcod_LEFT,
	#'*')


	
	#libtcod.console_set_default_foreground(panel, attack_panel_default_color)

#	if player_weapon.current_charge < player_weapon.default_usage:
#	else:
#	libtcod.console_print_ex(panel, attack_panel_x, 6, libtcod_BKGND_NONE, libtcod_LEFT,
#	'Charge:** ' + str(player_weapon.current_charge) + '/' + str(player_weapon.max_charge) + ' (req:' + str(player_weapon.default_usage) + ')')

	current_text_color = default_text_color
	if player_weapon.durability <= WEAPON_FAILURE_WARNING_PERIOD and player_weapon.durability > 0:
		#libtcod.console_set_default_foreground(panel, color_warning)
		current_text_color = color_warning
	elif player_weapon.durability <= 0:
		#libtcod.console_set_default_foreground(panel, color_big_alert)
		current_text_color = color_big_alert
	#libtcod.console_print_ex(panel, attack_panel_x, 7, libtcod_BKGND_NONE, libtcod_LEFT,
	#'Durability: ' + str(player_weapon.durability))
	panel.draw_str(int(attack_panel_x) , 7, 'Durability: ' + str(player_weapon.durability), bg=None, fg=current_text_color)


	#PLAYER PANEL STUFF

	#show the player's energy stats
	energy_color = color_energy
	non_energy_color = color_faded_energy
	wound_color = color_big_alert	
#	adrenaline_color = libtcod.green
#	non_adrenaline_color = libtcod.darker_green
#	if player.fighter.adrenaline_mode == False:
	#libtcod.console_print_ex(panel, player_panel_x, 1, libtcod_BKGND_NONE, libtcod_LEFT, "Energy:")
	panel.draw_str(player_panel_x, 1, "Energy:", bg=None, fg=default_text_color)
	for i in range(player.fighter.max_hp):
		#if i < player.fighter.wounds:
		#	libtcod.console_set_default_foreground(panel, wound_color)
		#	libtcod.console_print_ex(panel, player_panel_x + 7 + i, 1, libtcod_BKGND_NONE, libtcod_LEFT, '*')
		#elif i < player.fighter.wounds + player.fighter.hp:			
		#	libtcod.console_set_default_foreground(panel, energy_color)
		#	libtcod.console_print_ex(panel, player_panel_x + 7 + i, 1, libtcod_BKGND_NONE, libtcod_LEFT, '*')
		#else: 
		#	libtcod.console_set_default_foreground(panel, non_energy_color)
		#	libtcod.console_print_ex(panel, player_panel_x + 7 + i, 1, libtcod_BKGND_NONE, libtcod_LEFT, '.')

		if i <  player.fighter.hp:			
			translated_console_set_default_foreground(panel, energy_color)
			translated_console_print_ex(panel, player_panel_x + 7 + i, 1, libtcod_BKGND_NONE, libtcod_LEFT, '*')
		elif i < player.fighter.max_hp - player.fighter.wounds:
			translated_console_set_default_foreground(panel, non_energy_color)
			translated_console_print_ex(panel, player_panel_x + 7 + i, 1, libtcod_BKGND_NONE, libtcod_LEFT, '.')
		else:
			translated_console_set_default_foreground(panel, wound_color)
			translated_console_print_ex(panel, player_panel_x + 7 + i, 1, libtcod_BKGND_NONE, libtcod_LEFT, '\\')


#	else:
#		libtcod.console_set_default_foreground(panel, adrenaline_color)
#		libtcod.console_print_ex(panel, player_panel_x, 1, libtcod_BKGND_NONE, libtcod_LEFT, "ENERGY:")
#		for i in range(player.fighter.max_hp):
#			if i < player.fighter.adrenaline_level:
#				libtcod.console_set_default_foreground(panel, adrenaline_color)
#				libtcod.console_print_ex(panel, player_panel_x + 7 + i, 1, libtcod_BKGND_NONE, libtcod_LEFT, '*')
#			#elif i < player.fighter.wounds + player.fighter.hp:			
#			#	libtcod.console_set_default_foreground(panel, adrenaline_color)
#			#	libtcod.console_print_ex(panel, player_panel_x + 7 + i, 1, libtcod_BKGND_NONE, libtcod_LEFT, '*')
#			else: 
#				libtcod.console_set_default_foreground(panel, non_adrenaline_color)
#				libtcod.console_print_ex(panel, player_panel_x + 7 + i, 1, libtcod_BKGND_NONE, libtcod_LEFT, '.')


			

	#render_bar(player_panel_x, 1, BAR_WIDTH, 'HP', player.fighter.hp, player.fighter.max_hp - player.fighter.wounds,
	#libtcod.light_red, libtcod.darker_red)

	#display some sweet moves!
	#Here's a little bit of hackery to  make this code  rewrite a bit less tedious or at least more interesting.
	command_display_list = []
	command_display_list.append((-1,-1,controlHandler.singleCharacterControlLookup["MOVEUPLEFT"]))
	command_display_list.append((0,-1,controlHandler.singleCharacterControlLookup["MOVEUP"]))
	command_display_list.append((1,-1,controlHandler.singleCharacterControlLookup["MOVEUPRIGHT"]))
	command_display_list.append((1,0,controlHandler.singleCharacterControlLookup["MOVERIGHT"]))
	command_display_list.append((1,1,controlHandler.singleCharacterControlLookup["MOVEDOWNRIGHT"]))
	command_display_list.append((0,1,controlHandler.singleCharacterControlLookup["MOVEDOWN"]))
	command_display_list.append((-1,1,controlHandler.singleCharacterControlLookup["MOVEDOWNLEFT"]))
	command_display_list.append((-1,0,controlHandler.singleCharacterControlLookup["MOVELEFT"]))
	command_display_list.append((0,0,controlHandler.singleCharacterControlLookup["STANDSTILL"]))

	translated_console_set_default_foreground(panel, default_text_color)
	translated_console_print_ex(panel, player_panel_x, 3, libtcod_BKGND_NONE, libtcod_LEFT, "Moves:")
	for(x_adjust, y_adjust, command_str) in  command_display_list:
		#panel.draw_char(int(attack_panel_x + attack_panel_width/2 + 2*x_adjust) , 4 + y_adjust, command_str, bg=None, fg=attack_panel_default_color)
		
		translated_console_print_ex(panel, int(player_panel_x + player_panel_width/2 + 2*x_adjust), 4 + y_adjust, libtcod_BKGND_NONE, libtcod_CENTER, command_str)

#	translated_console_print_ex(panel, player_panel_x + player_panel_width/2 - 2, 3, libtcod_BKGND_NONE, libtcod_CENTER, '7')
#	translated_console_print_ex(panel, player_panel_x + player_panel_width/2, 3, libtcod_BKGND_NONE, libtcod_CENTER, '8')
#	translated_console_print_ex(panel, player_panel_x + player_panel_width/2 + 2, 3, libtcod_BKGND_NONE, libtcod_CENTER, '9')
#	translated_console_print_ex(panel, player_panel_x + player_panel_width/2 - 2, 4, libtcod_BKGND_NONE, libtcod_CENTER, '4')
#	translated_console_print_ex(panel, player_panel_x + player_panel_width/2, 4, libtcod_BKGND_NONE, libtcod_CENTER, '.')
#	translated_console_print_ex(panel, player_panel_x + player_panel_width/2 + 2, 4, libtcod_BKGND_NONE, libtcod_CENTER, '6')
#	translated_console_print_ex(panel, player_panel_x + player_panel_width/2 - 2, 5, libtcod_BKGND_NONE, libtcod_CENTER, '1')
#	translated_console_print_ex(panel, player_panel_x + player_panel_width/2, 5, libtcod_BKGND_NONE, libtcod_CENTER, '2')
#	translated_console_print_ex(panel, player_panel_x + player_panel_width/2 + 2, 5, libtcod_BKGND_NONE, libtcod_CENTER, '3')


#	#Display some stuff about jumps, woo!
#	jump_charged_color = libtcod.orange
#	jump_uncharged_color = libtcod.red
#	if  len(player.fighter.jump_array) > 0:
#		libtcod.console_print_ex(panel, player_panel_x, 7, libtcod_BKGND_NONE, libtcod_LEFT, "Jumps:")
#		for i in range(len(player.fighter.jump_array)):
#			if player.fighter.jump_array[i] == 0:
#				libtcod.console_set_default_foreground(panel, jump_charged_color)
#				libtcod.console_print_ex(panel, player_panel_x + 6 + i, 7, libtcod_BKGND_NONE, libtcod_LEFT, '*')
#			else:
#				libtcod.console_set_default_foreground(panel, jump_uncharged_color)
#				libtcod.console_print_ex(panel, player_panel_x + 6 + i, 7, libtcod_BKGND_NONE, libtcod_LEFT, '*')


	#LEVEL PANEL STUFF
	translated_console_set_default_foreground(panel, default_text_color)
	translated_console_print_ex(panel, level_panel_x, 1, libtcod_BKGND_NONE, libtcod_LEFT,
	'Time:   ' + str(game_time))
	translated_console_print_ex(panel, level_panel_x, 2, libtcod_BKGND_NONE, libtcod_LEFT,
	'Floor:  ' + str(dungeon_level))
	translated_console_print_ex(panel, level_panel_x, 3, libtcod_BKGND_NONE, libtcod_LEFT,
	'Alarm:  ' + str(alarm_level))
	translated_console_print_ex(panel, level_panel_x, 4, libtcod_BKGND_NONE, libtcod_LEFT,
	'Keys:   ' + str(key_count) + '/' + str(lev_set.keys_required))
	translated_console_print_ex(panel, level_panel_x, 5, libtcod_BKGND_NONE, libtcod_LEFT,
	'Favour: ' + str(currency_count))


	if favoured_by_healer:
		translated_console_print_ex(panel, level_panel_x + BAR_WIDTH/2, 8, libtcod_BKGND_NONE, libtcod_CENTER,
		'Favoured by ' + god_healer.name)

	elif favoured_by_destroyer:
		translated_console_print_ex(panel, level_panel_x + BAR_WIDTH/2, 8, libtcod_BKGND_NONE, libtcod_CENTER,
		'Favoured by ' + god_destroyer.name)

	elif tested_by_destroyer:
		translated_console_print_ex(panel, level_panel_x + BAR_WIDTH/2, 8, libtcod_BKGND_NONE, libtcod_CENTER,
		'Tested by ' + god_destroyer.name + '(' + str(destroyer_test_count) + ')')

	elif favoured_by_deliverer:	# actually for the deliverer you probably never get this message, right? If the mission is to complete level quickly?
		translated_console_print_ex(panel, level_panel_x + BAR_WIDTH/2, 8, libtcod_BKGND_NONE, libtcod_CENTER,
		'Favoured by ' + god_deliverer.name)

	elif tested_by_deliverer:
		translated_console_print_ex(panel, level_panel_x + BAR_WIDTH/2, 8, libtcod_BKGND_NONE, libtcod_CENTER,
		'Tested by ' + god_deliverer.name + '(' + str(deliverer_test_count) + ')')

	#display names of objects under the mouse  #commenting out for now!
	#libtcod.console_set_default_foreground(panel, libtcod.light_gray)
	#libtcod.console_print_ex(panel, 1, 0, libtcod_BKGND_NONE, libtcod_LEFT, get_names_under_mouse())




	# Surprise upgrade panel stuff!
	upgrade_count = len(upgrade_array)
	if upgrade_count > 0 and upgrade_count < 22:
		translated_console_print_ex_center(panel, SCREEN_WIDTH - int(upgrade_panel_width/2) -2, 1, libtcod_BKGND_NONE, libtcod_CENTER,
		'Upgrades:')

	upg_offset = 0
	if upgrade_count > 15 and upgrade_count < 22:
		upg_offset = -1
	elif upgrade_count >= 22:
		upg_offset = -2

	for j in range (10):  # (int((upgrade_count+3)/3)):
		if 3+j + upg_offset < PANEL_HEIGHT:
			for i in range (3):
				if 3*j + i < upgrade_count:

					temp_upgrade = upgrade_array[3*j + i]
					if temp_upgrade.status == 'dormant':
						translated_console_set_default_foreground(panel, default_text_color)
						translated_console_set_default_background(panel, default_background_color)
					elif temp_upgrade.status == 'enabled':
						translated_console_set_default_foreground(panel, color_energy)
						translated_console_set_default_background(panel, default_background_color)
					elif temp_upgrade.status == 'active':
						translated_console_set_default_foreground(panel, default_background_color)
						translated_console_set_default_background(panel, color_energy)
					else: 
						translated_console_set_default_foreground(panel, default_text_color)
						translated_console_set_default_background(panel, default_background_color)
				#	if temp_upgrade.activated:
				#		translated_console_set_default_foreground(panel, default_background_color)
				#		translated_console_set_default_background(panel, color_energy)
				#	else: 
				#		translated_console_set_default_foreground(panel, default_text_color)
				#		translated_console_set_default_background(panel, default_background_color)

					translated_console_print_ex(panel, upgrade_panel_x + i*4, 3+j+upg_offset, libtcod_BKGND_NONE, 						libtcod_CENTER,	temp_upgrade.code)
	
	translated_console_set_default_foreground(panel, default_text_color)
	translated_console_set_default_background(panel, default_background_color)
				

#default_background_color = 	(vfw,vfw,vfw)	#(0,0,0)
#default_text_color = 		(vsf,vsf,vsf)	#(255,255,255)
#color_energy = 			(v_p,v_p,v_p)	#(0,255,255)
#color_faded_energy = 		(vsf,vsf,vsf)	#	(0,0,255)
#color_warning = 		(v_p,v_p,v_p)	#	(255,127,0)
#color_big_alert = 		(v_p,v_p,v_p)	#(255,0,0)

		

#		for power_up in upgrade_array:
#			if getattr(power_up, "upgrade_player_stats_once", None) is not None:
#				power_up.upgrade_player_stats_once(player)





	#blit the contents of "panel" to the root console
	#libtcod.console_blit(panel, 0, 0, SCREEN_WIDTH, PANEL_HEIGHT, 0, 0, PANEL_Y)
	root_console.blit(panel, 0, PANEL_Y, SCREEN_WIDTH, PANEL_HEIGHT, 0, 0)


# Here is where all the messages go
def create_message_panel():

	#GUI STUFF
	#prepare to render the GUI panel
	translated_console_set_default_background(message_panel, default_background_color)
	translated_console_clear(message_panel)	
	
	#print the game messages, one line at a time
	y = 0
	for (line, color) in game_msgs:
		translated_console_set_default_foreground(message_panel, color)
		translated_console_print_ex(message_panel, 1, y, libtcod_BKGND_NONE, libtcod_LEFT, line)
		#libtcod.console_print_ex(message_panel, MSG_X, y, libtcod_BKGND_NONE, libtcod_LEFT, line)
		y += 1 


	#blit the contents of "message_panel" to the root console
	#libtcod.console_blit(message_panel, 0, 0, SCREEN_WIDTH, MESSAGE_PANEL_HEIGHT, 0, 0, 0)
	# libtcod.console_blit(message_panel, 0, 0, MESSAGE_PANEL_WIDTH, MESSAGE_PANEL_HEIGHT, 0, 0, 0)
	root_console.blit(message_panel, 0, 0, MESSAGE_PANEL_WIDTH, MESSAGE_PANEL_HEIGHT, 0, 0)


def update_camera():
	global camera, player

	if camera.x < player.x - CAMERA_FOCUS_WIDTH/2:
		camera.x = player.x - CAMERA_FOCUS_WIDTH/2
	elif camera.x > player.x + CAMERA_FOCUS_WIDTH/2:
		camera.x = player.x + CAMERA_FOCUS_WIDTH/2

	if camera.y < player.y - CAMERA_FOCUS_HEIGHT/2:
		camera.y = player.y - CAMERA_FOCUS_HEIGHT/2
	elif camera.y > player.y + CAMERA_FOCUS_HEIGHT/2:
		camera.y = player.y + CAMERA_FOCUS_HEIGHT/2

#	camera.x = player.x
#	camera.y = player.y


def reorder_objects(x,y):		#TODO REJIGGER THIS SO IT TAKES A SINGLE X,Y CO-OORD AS ARGUMENT AND REORDERS FOR THAT CO-ORD
	#rearrange the world objects so they appear in the correct order.
	#for now that order is: moving objects like the player and enemies drawn last, then 'keys', then weapons, then static objects like shrines and messages. Ummmm how do I do this
	global objectsArray		
	# Rough plan: move all the keys to the back. then, move all the weapons to the back. then, move all the non-movey things to do the back.
	# Identifying elements to move is currently done in a very janky object-specific way, and is likely to break when I add new objects.
	total = len(objectsArray[x][y])
	#index = total -1
	#step 1: move all keys to back
	index = 0
	while index < total: 				# >= 0:	
		#print str(objects[index].name)
		ob = objectsArray[x][y][index]
		if ob.name == 'key':
			ob.send_to_back()
		index = index + 1 
	#step 1.5: move all favour tokens to back
	index = 0
	while index < total: 				# >= 0:	
		#print str(objects[index].name)
		ob = objectsArray[x][y][index]
		if ob.name == 'favour token':
			ob.send_to_back()
		index = index + 1 
	#step 2: move all weapons to back
	index = 0
	while index < total: 				# >= 0:	
		#print str(objects[index].name)
		ob = objectsArray[x][y][index]
		if ob.weapon == True:
			ob.send_to_back()
		index = index + 1 

	#step 3: move all non-movey backroundy stuff (non-key, non-weapon, non-obstructey), except for decorations and attacks, to back
	index = 0
	while index < total: 				# >= 0:	
		#print str(objects[index].name)
		ob = objectsArray[x][y][index]
		if ob.blocks == False and ob.weapon == False and ob.name != 'key' and ob.name != 'decoration' and not ob.attack:
			ob.send_to_back()
		index = index + 1 	

	#step 3.5: move all attacks to back
	index = 0
	while index < total: 				# >= 0:	
		#print str(objects[index].name)
		ob = objectsArray[x][y][index]
		if ob.attack:
			ob.send_to_back()
		index = index + 1 


	#step 3.625: move all plants to back
	index = 0
	while index < total: 				# >= 0:	
		#print str(objects[index].name)
		ob = objectsArray[x][y][index]
		if ob.plant:
			ob.send_to_back()
		index = index + 1 

	#step 3.75: move all water and blood to back? I need to start finding a better way to do this maybe.
	index = 0
	while index < total: 				# >= 0:	
		ob = objectsArray[x][y][index]
		if ob.name == 'water' or ob.name == 'blood':
			ob.send_to_back()
		index = index + 1 

	#step 4: finally, decorations, the lowest of the low.
	index = 0
	while index < total: 				# >= 0:	
		#print str(objects[index].name)
		ob = objectsArray[x][y][index]
		if ob.name == 'decoration':
			ob.send_to_back()
		index = index + 1 
	# Well; let's see if this works..

def clear_onscreen_objects():
	global objectsArray, camera
	x_offset = int(camera.x-(SCREEN_WIDTH + MESSAGE_PANEL_WIDTH)/2)
	y_offset = int(camera.y-(SCREEN_HEIGHT-PANEL_HEIGHT)/2)
	for yOff in range(ACTION_SCREEN_HEIGHT):
		y = yOff + y_offset
		if y in range(MAP_HEIGHT):
			for xOff in range(ACTION_SCREEN_WIDTH):
				x = xOff + x_offset + ACTION_SCREEN_X
				if x in range(MAP_WIDTH):
					for object in objectsArray[x][y]:
						object.clear()


def setColorScheme(colorScheme = 'default'):
	global colorHandler
	global color_dark_wall, color_light_wall, color_dark_ground, color_light_ground, color_light_ground_alt, color_fog_of_war, default_altar_color, default_door_color, default_message_color, default_decoration_color, water_background_color, water_foreground_color, blood_background_color, blood_foreground_color, default_flower_color, default_weapon_color
	global PLAYER_COLOR, color_swordsman, color_boman, color_rook, color_axe_maniac, color_tridentor, color_rogue, color_ninja, color_wizard, color_alarmer_idle, color_alarmer_suspicious, color_alarmer_alarmed
	global default_background_color, default_text_color, color_energy, color_faded_energy, color_warning, color_big_alert
	global 	Color_Message_In_World,	Color_Menu_Choice, Color_Not_Allowed, Color_Dangerous_Combat, Color_Interesting_Combat, Color_Boring_Combat, Color_Interesting_In_World, Color_Boring_In_World,	Color_Stat_Info, Color_Personal_Action
	
	levelColors = colorHandler.levelColors
	
	color_dark_wall = levelColors['color_dark_wall']
	color_light_wall = levelColors['color_light_wall']
	color_dark_ground = levelColors['color_dark_ground']
	color_light_ground = levelColors['color_light_ground']
	color_light_ground_alt = levelColors['color_light_ground_alt']
	color_fog_of_war = levelColors['color_fog_of_war']
	default_altar_color = levelColors['default_altar_color']
	default_door_color = levelColors['default_door_color']
	default_message_color = levelColors['default_message_color']
	default_decoration_color = levelColors['default_decoration_color']
	water_background_color = levelColors['water_background_color']
	water_foreground_color = levelColors['water_foreground_color']
	blood_background_color = levelColors['blood_background_color']
	blood_foreground_color = levelColors['blood_foreground_color']

	# collectiable e.g. weapons and plants and keys
	default_flower_color = levelColors['default_flower_color']
	default_weapon_color = levelColors['default_weapon_color']

	# enemies, including player
	PLAYER_COLOR = levelColors['PLAYER_COLOR']
	color_swordsman = levelColors['color_swordsman']
	color_boman = levelColors['color_boman']
	color_rook = levelColors['color_rook']
	color_axe_maniac = levelColors['color_axe_maniac']
	color_tridentor = levelColors['color_tridentor']
	color_rogue = levelColors['color_rogue']
	color_ninja = levelColors['color_ninja']
	color_wizard = levelColors['color_wizard']
	color_alarmer_idle = levelColors['color_alarmer_idle']
	color_alarmer_suspicious = levelColors['color_alarmer_suspicious']
	color_alarmer_alarmed = levelColors['color_alarmer_alarmed']


	menuColors = colorHandler.menuColors
	# text colors
	default_background_color = menuColors['default_background_color']
	default_text_color = menuColors['default_text_color']
	color_energy = menuColors['color_energy']
	color_faded_energy = menuColors['color_faded_energy']
	color_warning = menuColors['Interesting_Combat']#['color_warning']
	color_big_alert = menuColors['Dangerous_Combat']#['color_big_alert']

	Color_Message_In_World = menuColors['Message_In_World']		# e.g. messages on floor, deities or elevators talking to you
	Color_Menu_Choice = menuColors['Menu_Choice']		# when the player has to input an option from mutliple choices
	Color_Not_Allowed = menuColors['Not_Allowed']		# when a player action is invalid or prevented
	Color_Dangerous_Combat = menuColors['Dangerous_Combat']	# when bad things happen in combat, like dying or getting hit
	Color_Interesting_Combat = menuColors['Interesting_Combat']		# notable combat stuff like enemies dying
	Color_Boring_Combat = menuColors['Boring_Combat']		# Run of the mill combat stuff. you hit an enemy. yawn
	Color_Interesting_In_World = menuColors['Interesting_In_World']	# Events of note happening in the world. Like alarms going off
	Color_Boring_In_World = menuColors['Boring_In_World']		# everyday occurences like doors opening
	Color_Stat_Info = menuColors['Stat_Info']			# info about not-in-the-world stuff like gaining energy
	Color_Personal_Action = menuColors['Personal_Action']		# Things the player does that aren't combat "you pick up the sword" etc



def mergeColors(initial_color, new_color, mix_level = 0.5):

	(initial_color_r, initial_color_g, initial_color_b) = initial_color
	(new_color_r, new_color_g, new_color_b) = new_color
	rval = initial_color_r * (1- mix_level) + new_color_r * mix_level
	gval = initial_color_g * (1- mix_level) + new_color_g * mix_level
	bval = initial_color_b * (1- mix_level) + new_color_b * mix_level
	return (int(round(rval)), int(round(gval)), int(round(bval)))


	#rval = initial_color.r * (1- mix_level) + new_color.r * mix_level
	#gval = initial_color.g * (1- mix_level) + new_color.g * mix_level
	#bval = initial_color.b * (1- mix_level) + new_color.b * mix_level
	#return libtcod.Color(int(round(rval)), int(round(gval)), int(round(bval)))


def save_game():	
	global gameSaveDataHandler, play_count
	#with shelve.open('savegame.dat', 'n') as data_file:		
	#	data_file['test_string'] = "hello I'm a test string"

#	file = open("testfile.txt","w") 
#
#	file.write("Hello World\n") 
#	file.write("This is our new text file\n") 
#	file.write("and this is another line.\n") 
#	file.write("Why? Because we can.\n") 
#
#	file.close() 

	play_count = play_count + 1
	gameSaveDataHandler.updateTestFileDataValue("FLD_PLAY_COUNT", play_count)
	gameSaveDataHandler.saveTestFileData()
	gameSaveDataHandler.saveControlData()


def saveControlScheme():
	global gameSaveDataHandler, control_scheme
	gameSaveDataHandler.updateControlDataValue("CONTROL_SCHEME", control_scheme)
	gameSaveDataHandler.saveControlData()
	

def load_game():
	global gameSaveDataHandler, play_count
	global test_save_message
	global control_scheme
	#if not os.path.isfile('savegame.dat'):		#may have to add .db when building with cxfreeze, because reasons?
	#	test_save_message = "woops, file not fou-ound!"
	#else:	
	#	with shelve.open('savegame.dat', 'r') as data_file:	#may have to add .db when building with cxfreeze, because reasons?
	#		test_save_message = data_file['test_string']

#	file = open("testfile.txt", "r") 
#	print (file.read()) 
#	file.close()

	gameSaveDataHandler = SaveDataHandler()
	gameSaveDataHandler.loadData()
	testFileData = gameSaveDataHandler.getTestFileData()
	play_count = int(testFileData["FLD_PLAY_COUNT"])
	controlData = gameSaveDataHandler.getControlData()
	control_scheme = controlData["CONTROL_SCHEME"]

def initialise_game():
	global current_big_message, game_msgs, game_level_settings, dungeon_level, game_time, spawn_timer, player, player_weapon, objectsArray, game_state, player_action, con, enemy_spawn_rate, favoured_by_healer, favoured_by_destroyer, tested_by_destroyer,  favoured_by_deliverer, tested_by_deliverer,  god_healer, god_destroyer, god_deliverer, camera, alarm_level, already_healed_this_level, something_changed, upgrade_array, currency_count, controlHandler, colorHandler, control_scheme
	current_big_message = 'You weren\'t supposed to see this'


	# load stuff. yay, I'm testing loading and saving
	load_game()

	#Initialise controls
	controlHandler = ControlHandler(control_scheme)

	colorHandler = ColorHandler('lobbyTest')  #('adjustedOriginal')
	setColorScheme()


	#create the list of game messages and their colors, starts empty
	game_msgs = []
	something_changed = True
	
	game_level_settings = Level_Settings()
	dungeon_level = 0	#SO HEY currently there is a game-crashing flaw on the first level because room_adjacencies is not properly initialised, that's great
	alarm_level = 1
	god_healer = God(god_type = God_Healer())
	favoured_by_healer = False
	god_destroyer = God(god_type = God_Destroyer())
	tested_by_destroyer = False
	favoured_by_destroyer = False
	god_deliverer = God(god_type = God_Deliverer())
	tested_by_deliverer = False
	favoured_by_deliverer = False
	already_healed_this_level = False
	currency_count = STARTING_CURRENCY
	game_time = 1
	
	#create object representing the player
	fighter_component = Energy_Fighter(hp=STARTING_ENERGY, defense=2, power=5, death_function=player_death, jump_array = [0,0,0,0])
	#fighter_component = Fighter(hp=10, defense=2, power=5, death_function=player_death, jump_array = [0,0,0,0])
	decider_component = Decider()
	player = Object(0, 0, '@', 'player', PLAYER_COLOR, blocks=True, fighter=fighter_component, decider=decider_component)
	camera = Location(player.x, player.y)


	#TODO TEMP THINGUMMY: for right now we're creating a single special powerup thing, and ultimately this stuff needs to be in a proper array and all that
	#upgrade_choice = randint( 0, 1)
	#if upgrade_choice == 0:
	#	starting_upgrade = WallHugger()
	#else:	
	#	starting_upgrade =  Mindfulness()
	#upgrade_array = [starting_upgrade]

	upgrade_array = []
	
	#starting_upgrade = Perfectionist()		#for when you want to test a new uprade
	#upgrade_array.append(starting_upgrade)

	#upgrade_array.append(Amphibious())
	#upgrade_array.append(NeptunesBlessing())
	#another_upgrade = Mindfulness()
	#upgrade_array.append(another_upgrade)
	
	#WEAPON SELECT
	player_weapon = Weapon_Unarmed()
	#player_weapon = Weapon_Sword()
	#player_weapon = Weapon_Spear()
	#player_weapon = Weapon_Staff()
	#player_weapon = Weapon_Wierd_Staff()
	#player_weapon = Weapon_Katana()
	#player_weapon = Weapon_Dagger()
	
	#objects = []
	make_map()
	objectsArray[player.x][player.y].append(player)	
	worldEntitiesList.append(player)
	print('howdy (' + str(player.x) + ',' + str(player.y))
	for object in objectsArray[player.x][player.y]:
		print(object.name)

	#the list of objects starting with the player
#	objects = [player]				#TODO/NOTE: When changing to 'objectsArray', this might cause problems?
							# Think it's enough to move this to after make_map(), and then use player's x and y
	
	initialize_fov()
	
	game_state = 'playing'
	player_action = None
	
	#a warm welcoming message!
	message('Welcome! Use #MOVEUPLEFT#, #MOVEUP#, #MOVEUPRIGHT#, #MOVERIGHT#, #MOVEDOWNRIGHT#, #MOVEDOWN#, #MOVEDOWNLEFT#, #MOVELEFT# to move, #ATTCKUPLEFT#, #ATTCKUP#, #ATTCKUPRIGHT#, #ATTCKRIGHT#, #ATTCKDOWNRIGHT#, #ATTCKDOWN#, #ATTCKDOWNLEFT#, #ATTCKLEFT# to attack, #PICKUP# to pick up a new weapon. Press #PAUSE# to access the pause menu, including control options. Go up for a tutorial, or step into the elevator on your left to go to Floor 1.', Color_Message_In_World)

	# Here is an annoying hack. One-off special check for floor messages just so we can check if there's one when the game starts.
	objects_here = [obj for obj in objectsArray[player.x][player.y]
			if obj is not player]
	names = [obj.name for obj in objects_here if obj.floor_message is None and obj.name is not 'water' and obj.name is not 'decoration'  and obj.name is not 'blood']  #todo: get a better way of not including certain objects in this list
	possible_commands = []
	floor_message_found = False
	floor_message_text = ''
	for obj in objects_here:
		if floor_message_found == False and obj.floor_message is not None:
			floor_message_text = obj.floor_message.string
			floor_message_found = True		
	if floor_message_found == True:  
		message('You see a message on the floor:', Color_Interesting_In_World)
		message('\"' + floor_message_text + '\"', Color_Message_In_World)
		print (str(Color_Interesting_In_World))


	#temporarily commenting out, WHICH IS AN EXTRA BAD IDEA
	#libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE,key,mouse)
	#print('6')
	render_all()
	translated_console_flush()




#libtcod.console_set_custom_font('arial12x12.png', libtcod.FONT_TYPE_GREYSCALE | libtcod	.FONT_LAYOUT_TCOD)


#libtcod.console_set_custom_font('arial14test2.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)

# tdl version
	
#For some reason, this font choice makes all the text into alien giberish, the doors become fikkin mars symbols, and there's no player character.  (Maybe something to do with the fact that I added a custom font?)
#libtcod.set_font('arial14x14.png', greyscale=True, altLayout=True)

# If we use this font, everything looks fine but it's way too small. Also the controls do nothing and time advances at an alarming speed, but I think that's due to me commenting out other stuff elsewhere.
#libtcod.set_font('arial10x10.png', greyscale=True, altLayout=True)

# This font might be best so far... not super keen since it still looks different to what I had before, but it might grow on me.
# It is quite easy to parse in terms of the action screen. Less readable in terms of game messages.
# (I wonder if it's possible to change the fonts on different sub-consoles...)
# libtcod.set_font('terminal16x16.png', greyscale=True, altLayout=False)
font_choice = 'terminal16x16.png'

#But hang on maybe I just need to change the 'altLayout' settings to make my original file work...
#libtcod.set_font('arial14x14.png', greyscale=True, altLayout=False)
# Oh hey it does work! Good to have you back, custom font. But now I'm reminded that I nevergot the things to align properly, and yeah, I should probably change it anyway.



# Trying now to specfiy the font location in such a way that it can always be found, no matter where you call 7DRL2015.py from.
# Which is trickier than you might think.

import sys, os

print ('sys.argv[0] =' + sys.argv[0]) 
pathname = os.path.dirname(sys.argv[0])       
print ('path = ' + pathname)
fontpath = os.path.join(pathname,  font_choice)
print ('font file = ' + fontpath)
libtcod.set_font(fontpath, greyscale=True, altLayout=False)



#libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)
#tdl version
root_console = libtcod.init(SCREEN_WIDTH, SCREEN_HEIGHT, title='Sword Dancer')

# tdl version
con = libtcod.Console(MAP_WIDTH, MAP_HEIGHT)
panel = libtcod.Console(SCREEN_WIDTH, PANEL_HEIGHT)
message_panel = libtcod.Console(SCREEN_WIDTH, MESSAGE_PANEL_HEIGHT)
pause_menu = libtcod.Console(SCREEN_WIDTH, SCREEN_HEIGHT)
#con = libtcod.console_new(MAP_WIDTH, MAP_HEIGHT)
#panel = libtcod.console_new(SCREEN_WIDTH, PANEL_HEIGHT)
#message_panel = libtcod.console_new(SCREEN_WIDTH, MESSAGE_PANEL_HEIGHT)
#pause_menu = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)


# cutting out mouse stuff for now, because it hasn't worked in a while.
# may come back to it once i have everything working with tdl. but for now, it's not worth porting faulty code
# mouse = libtcod.Mouse()
mouse = None
#TEMP COMMENTING OUT OH GOD
#key = libtcod.Key()
key = None


#TEMP COMMENTING OUT OH GOD
# libtcod.sys_set_fps(LIMIT_FPS) 

initialise_game()


lev_set = game_level_settings.get_setting(dungeon_level)

enemy_spawn_rate = lev_set.enemy_spawn_rate
spawn_timer = decide_spawn_time(enemy_spawn_rate,alarm_level)

time_since_last_elevator_message = 0

ready_for_next_level = False

libtcod.set_fps(30)

# So for future reference, this code prints the numbers 1 to 9:
#for num in range(1,10):
#	print str(num)

internal_loop_count = 0

# Main loop!
while not translated_console_is_window_closed():


	garbage_list = []	#list of things (e.g. dead bodies) to delete from objects list at the end of the loop

#	libtcod.console_put_char(con, playerx, playery, ' ', libtcod_BKGND_NONE)
	#for object in objects:
	#	object.clear()

#	print ("'fixed'  CLEARING OBJECTS")
#	for y in range(MAP_HEIGHT):
#		for x in range(MAP_WIDTH):
#			for object in objectsArray[x][y]:
#				object.clear()
	clear_onscreen_objects()
	#get player decisions and handle keys and exit game if needed
	
	#trying to adapt the code from the tdl tutorial to this game. Let's see how much stuff this breaks:

	user_input = None
	# ok so adding the line below seems to sort out the bugs when jumping or attacking. But we still have the problem that if you hold down a direction for too long the player character will start moving in that direction for several frames.
	# there's clearly some issue of a... input memory not being cleared, or something. But that wouldn't explain why you get actual game crashing bugs. (i mean pressing the same attack button does not crash the game...)
	#libtcod.event.wait(timeout = 0.005, flush = True)
	
	#what if we... do the wait thing instead?
	#user_input = libtcod.event.key_wait()
	#nope

	#temp_list = libtcod.event.get()
	
	#for event in temp_list: #libtcod.event.get():
	#	#print('heyo ' + str(event))
	#	if event.type == 'KEYDOWN' and user_input == None:
	#		print('HALLO ' + str(event))
	#		user_input = event
	#		break
	#else:
	#	user_input = None



	# Well hello.
	# This  hack below is to deal with the fact that I could never figure out how to clear the event queue properly.
	# Which meant that besides some game-crashing bugs (whch I think are mostly fixed, and more to do with trying to 
	# parse 'text' events improperly), the character would keep moving for too long if you held the key down for a bit,
	# because the game was working through the backlog of 'keydown' events.
	# So now what we do is just manually get the events out, until there's none left.
	# Probably inefficient, and almost certainly not how I was meant to do it. But the other things I tried didn't work.
	
	while True:
		for temp_event in libtcod.event.get():
			event = temp_event
			if event.type == 'KEYDOWN' and user_input == None:
				# for now we just care about non-TEXT events I think. But later we might care about text events
				# (e.g. for handling menu choices? I unno.)
				if event.type != 'TEXT':
					#print('HALLO ' + str(event))
					user_input = event
		
		if user_input is not None:
			break



	#if not user_input:
	#	continue

	#testing this out to see if stuff works.
	#it does not
	# libtcod.event.wait(timeout = 0.05, flush = True)

	#print('internal loop count = ' + str(internal_loop_count) +  ', game_time = ' + str(game_time) + str(user_input))
	internal_loop_count += 1

	#print('key press?' + str(game_time)) # str(libtcod.get_fps()))



	#temporarily commenting out, WHICH IS AN EXTRA BAD IDEA
	# player_action = handle_keys()
	#print('handling ' + str(user_input))
	player_action = handle_keys(user_input)
	if player_action == 'pause':
		something_changed = True
		if game_state == 'playing' or game_state == 'control screen':
			game_state = 'paused'
		elif game_state == 'paused' or game_state == 'big message':
			game_state = 'playing'
	#	break

	# Game things happen woo!
	elif game_state == 'playing' and player_action != 'didnt-take-turn' and  player_action != 'invalid-move' and player_action != 'pickup_dialog' and player_action != 'upgrade shop dialog' and player_action != 'jump_dialog' :
		
		
		game_time += 1
		spawn_timer -= 1
		update_nav_data()

		player_hit_something = False
		player_clashed_something = False
		player_got_hit = False
		player_just_jumped = False
		number_hit_by_player = 0

		if nearest_points_array[player.x][player.y] is not None:
			nearest_center_to_player =  nearest_points_array[player.x][player.y]


		# delete attacks from the past?! This is a fix because attacks seem to be hanging around longer than I'd like, may cause problems further down the line...
		#deletionList = []


	#	print ("DELETING ATTACJS")		
	#	for y in range(MAP_HEIGHT):
	#		for x in range(MAP_WIDTH):
	#			
	#			deletionList = []
	#			for object in objectsArray[x][y]:
	#	#for object in objects:
	#				if object.attack:
	#					object.attack.fade()
	#					if object.attack.existing == False:
	#						deletionList.append(object)
	#			# deleting attacks that have happened
	#			for object in objectsArray[x][y]:
	#				object.clear()
	#			for object in deletionList:
	#				objectsArray[object.x][object.y].remove(object)


#		print ("'fixed'  DELETING ATTACJS")
		deletionList = []
		for object in worldAttackList:
			if object.attack:
				object.attack.fade()
				if object.attack.existing == False:
					deletionList.append(object)
		for object in deletionList:
			x = object.x
			y = object.y
			# deleting attacks that have happened
			for other_object in objectsArray[x][y]:
				other_object.clear()
			objectsArray[x][y].remove(object)
			if object in worldAttackList:
				worldAttackList.remove(object)

			#let monsters take their decisions
	#	for object in objects:
#		print ("'fixed'  DOING DECISIONS")		
		#for y in range(MAP_HEIGHT):
		#	for x in range(MAP_WIDTH):
		#		for object in objectsArray[x][y]:
		#			if object.decider:
		#				object.decider.decide()

		for object in worldEntitiesList:
			if object.decider:
				object.decider.decide()

		


		#now everyone has decided things, things can happen
	
		#the passing of time is important for the Taylor the Deliverer!
		if tested_by_deliverer:
			if deliverer_test_count > 0:
				deliverer_test_count = deliverer_test_count - 1
			else:
				tested_by_deliverer = False




		
		# decide if there are any 'punch targets'. This is an ordered pair consisting of a fighter wants to move into a space, and another fighter that is currently in that space. If the second fighter doesn't move, they're gonna get punched!
		# also decide if anyone is trying to open a door! (By walking into it)
		potential_punch_list = []
		potential_open_list = []


#		print ("'fixed'  DECIDING ABOUT PUNCH TARGETS")		
		for object in worldEntitiesList:
			if object.decider:
				x = object.x
				y = object.y
				if object.decider.decision is not None:
					if object.decider.decision.move_decision is not None:
						md = object.decider.decision.move_decision
						if md.dx != 0 or md.dy != 0:	# let's not have people punch themselves just by standing still.
							target_x = object.x + md.dx
							target_y = object.y + md.dy	
							for victim in objectsArray[target_x][target_y]:
								# try to punch if there's a fighter in this square
								if victim.fighter:
									# the following code checks that the victim isn't actually Attacking the puncher	
									valid_target = True
									if victim.decider.decision and victim.decider.decision.attack_decision:
										victim_attacks = victim.decider.decision.attack_decision.attack_list
										for vic_attack in victim_attacks:
											if vic_attack.x == object.x and vic_attack.y == object.y:
												valid_target = False
									if valid_target == True:
										potential_punch_list.append((object, victim))
								#try to open if there's a (non-elevator) door in this square
								if victim.door and victim.name != 'elevator door' and victim.x == target_x and victim.y == target_y:
									potential_open_list.append((object, victim))
									#print str(victim.name)

								
#		for y in range(MAP_HEIGHT):
#			for x in range(MAP_WIDTH):
#				for object in objectsArray[x][y]:
#		#for object in objects:
#					if object.decider:
#						if object.decider.decision is not None:
#							if object.decider.decision.move_decision is not None:
#								md = object.decider.decision.move_decision
#								if md.dx != 0 or md.dy != 0:	# let's not have people punch themselves just by standing still.
#									target_x = object.x + md.dx
#									target_y = object.y + md.dy	
#									for victim in objectsArray[target_x][target_y]:
#										# try to punch if there's a fighter in this square
#										if victim.fighter:
#											# the following code checks that the victim isn't actually Attacking the puncher	
#											valid_target = True
#											if victim.decider.decision and victim.decider.decision.attack_decision:
#												victim_attacks = victim.decider.decision.attack_decision.attack_list
#												for vic_attack in victim_attacks:
#													if vic_attack.x == object.x and vic_attack.y == object.y:
#														valid_target = False
#											if valid_target == True:
#												potential_punch_list.append((object, victim))
#										#try to open if there's a (non-elevator) door in this square
#										if victim.door and victim.name != 'elevator door' and victim.x == target_x and victim.y == target_y:
#											potential_open_list.append((object, victim))
#											#print str(victim.name)





		# firstly movement happens
		# player always moves first
		if player.decider:
			if player.decider.decision is not None:
				if player.decider.decision.move_decision is not None:
					md = player.decider.decision.move_decision
					if map[player.x + md.dx][player.y + md.dy].blocked:
						message ("You walk into a wall.", Color_Personal_Action)
					player.move(md.dx, md.dy)
				elif player.decider.decision.jump_decision is not None:
					jd = player.decider.decision.jump_decision
					# Check for things between the player and where they want to be,
					# and see if they are things that block the player or can be jumped over.
					# For now, assumes all jumps are of length 2;
					# Will need to be changed if different jumps come in.
					tempx = 0
					if jd.dx == -2:
						tempx = -1
					elif jd.dx == 2:
						tempx = 1
					tempy = 0
					if jd.dy == -2:
						tempy = -1
					elif jd.dy == 2:
						tempy = 1
					somethingInWay = False
					jumpee = None		#The thing you're jumping over...
					if player.fighter.jump_available() == False:
						message("Your legs are too tired to jump!", Color_Not_Allowed )
					elif map[player.x + tempx][player.y + tempy].blocked:
						somethingInWay = True
						message("There's a wall in the way!!!", Color_Not_Allowed )
					else: 
						#check for doors, and/or find the thing the player is jumping over.
						for ob in objectsArray[player.x + tempx][player.y + tempy]:
							if ob.door:
								somethingInWay = True
							if ob.fighter:
								jumpee = ob	
						if somethingInWay == True:
							message("There's a door in the way!", Color_Not_Allowed )
					if somethingInWay == False:
						if map[player.x + jd.dx][player.y + jd.dy].blocked:
							message ("You leap gracefully into a wall.", Color_Personal_Action)
							player.move(tempx, tempy)
						else:
							if jumpee is not None:
								message ("You leap over the " + jumpee.name + "\'s head!", Color_Personal_Action)
						player.fighter.make_jump()
						player.move(jd.dx, jd.dy)
						player_just_jumped = True
	
				# check for player trampling plants. This is not where it should go...
				for other_object in objectsArray[player.x][player.y]:	
					if other_object.plant is not None:
						other_object.plant.tread()
						# also I guess get health maybe???
						other_object.plant.harvest(player)



	 	# move other objects.
		# first, make a list of objects to move (because naively going through objectsArray and moving everything at each grid reference can lead to objects getting moved multiple times
		
#		print ("'FIXED'  GETTING LIST OF MOVERS")
		mover_list = []
		for object in worldEntitiesList:
			if object.decider and object is not player:
				if object.decider.decision is not None:
					if object.decider.decision.move_decision is not None:
						mover_list.append(object)


#		mover_list = []
#		for y in range(MAP_HEIGHT):
#			for x in range(MAP_WIDTH):
#				for object in objectsArray[x][y]:
##		for object in objects:
#					if object.decider and object is not player:
#						if object.decider.decision is not None:
#							if object.decider.decision.move_decision is not None:
#								mover_list.append(object)


		for object in mover_list:
			md = object.decider.decision.move_decision
			object.move(md.dx, md.dy)			#TODO NOTE: hey this is going to be interesting
			# also maybe trample some plants while you're here
			for other_object in objectsArray[object.x][object.y]:	
				if other_object.plant is not None:
					other_object.plant.tread()
					# also I guess get health maybe???
					if object.fighter:
						other_object.plant.harvest(object)

		


		# do some messages saying what you see here!
		#names = [obj.name for obj in objects
		#	if obj.x == player.x and obj.y == player.y and obj is not player]
		objects_here = [obj for obj in objectsArray[player.x][player.y]
			if obj is not player]
		names = [obj.name for obj in objects_here if obj.floor_message is None and obj.name is not 'water' and obj.name is not 'decoration'  and obj.name is not 'blood']  #todo: get a better way of not including certain objects in this list
		possible_commands = []

		weapon_found = False
		key_found = False
		favour_found = False
		stairs_found = False
		shrine_found = False
		floor_message_found = False
	
		floor_message_text = ''
		for obj in objects_here:
			if weapon_found == False and obj.weapon == True:
				weapon_found = True
			if key_found == False and obj.name == 'key':
				key_found = True
			if favour_found == False and obj.name == 'favour token':
				favour_found = True
			if stairs_found == False and obj.name == 'stairs':
				stairs_found = True
				possible_commands.append('< to ascend')
			if shrine_found == False and obj.shrine is not None:
				shrine_found = True
			if floor_message_found == False and obj.floor_message is not None:
				floor_message_text = obj.floor_message.string
				floor_message_found = True


		if weapon_found or key_found or favour_found:	
			possible_commands.append(controlHandler.controlLookup["PICKUP"] + ' to pick up')
		if shrine_found:
			possible_commands.append(controlHandler.controlLookup["MEDITATE"] +  ' to meditate')
			
		if floor_message_found == True and player.decider.decision is not None and (player.decider.decision.move_decision is not None or player.decider.decision.jump_decision is not None): # trying to make it so messages don't repeat themselves
			message('You see a message on the floor:', Color_Interesting_In_World)
			message('\"' + floor_message_text + '\"', Color_Message_In_World)

		if len(names) > 0:
			names = ', '.join(names)
			possible_commands = ', '.join(possible_commands)
			temp_message = 'You see a ' + names + ' here (' + possible_commands + ').'
			message(temp_message, Color_Boring_In_World)





		# draw things in their new places
		if player.decider.decision:
			if player.decider.decision.move_decision or player.decider.decision.jump_decision:			
				fov_recompute = True


#		print ('fixed'  "CLEARING OBJECTS AGAIN")
		#for y in range(MAP_HEIGHT):
		#	for x in range(MAP_WIDTH):
		#		for object in objectsArray[x][y]:
		##for object in objects:
		#			object.clear()
		clear_onscreen_objects()


		translated_console_set_default_foreground(con, default_text_color)
		#temporarily commenting out, WHICH IS AN EXTRA BAD IDEA
		#libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE,key,mouse)
		#print('1')
		render_all()
		translated_console_flush()

		#put in a pause before drawing the other stuff?
		time.sleep(0.05)

		
		#update elevator so they know whether to shut their doors
		time_since_last_elevator_message = time_since_last_elevator_message + 1
		player_can_see_elevator_opening = False
		for ele in elevators:
			elevator_occupied = False
			player_in_elevator = False
			player_near_elevator = False
			player_in_doorway = False
			for (x,y) in ele.spawn_points:
				if is_blocked(x, y):
					elevator_occupied = True
				if player.x == x and player.y == y:
					player_in_elevator = True
				if player.x <= x+ ELEVATOR_DISTANCE_CHECK and player.x >= x -ELEVATOR_DISTANCE_CHECK and player.y <= y + ELEVATOR_DISTANCE_CHECK and player.y >= y - ELEVATOR_DISTANCE_CHECK:
					player_near_elevator = True
					# if player not authorised, tell them so. Unless they've been spoken at by an elevator recently.
					if time_since_last_elevator_message > 10 and not ele.player_authorised :
						message("\"Access to the next floor is restricted by security. " + str(lev_set.keys_required) + " keys required.\"", Color_Message_In_World)
						time_since_last_elevator_message = 0
			for (x,y) in ele.door_points:
				if player.x == x and player.y == y:
					player_in_doorway = True				
			ele.update(elevator_occupied, player_in_elevator, player_near_elevator, player_in_doorway)
			if ele.doors_opening == True:
				#play a 'ding' noise if the player can see the doors opening
				for door in ele.special_door_list:
					# if libtcod.map_is_in_fov(fov_map, door.x, door.y):
					if fov_map.fov[door.x, door.y]:
						player_can_see_elevator_opening = True


				#close the doors!				
				for door in ele.special_door_list:
					door.currently_invisible = True
					door.blocks = False
					map[door.x][door.y].block_sight = False	
					map[door.x][door.y].blocked = False	
				nav_data_changed = True
				initialize_fov()
			elif ele.doors_closing == True:
				#print "doors closing"
				#close the doors!				
				for door in ele.special_door_list:
					door.currently_invisible = False
					door.blocks = True
					map[door.x][door.y].block_sight = True	
					map[door.x][door.y].blocked = True						
				nav_data_changed = True
				initialize_fov()
			if (player_in_elevator and ele.ready_to_go_up == True):
				#print "next level maybe?"
				ready_for_next_level = True

		#play a "ding" if the player can see elevator doors opening?
		if player_can_see_elevator_opening:
			message("Ding!", Color_Message_In_World)

		# update elevators with whether the player is authorized - for now this is just based on whether there are security systems around.
		# later this process will become a bit more complicated (and might be folded into Elevator.update)
		level_complete = False
		if lev_set.boss is not None:
			level_complete = True
			#check for bosses?
			print ("CHECKING FOR BOSSES")
			for object in worldEntitiesList:
				#for object in objects:
				if object.name == lev_set.boss:
					level_complete = False


#			print ("CHECKING FOR BOSSES")
#			for y in range(MAP_HEIGHT):
#				for x in range(MAP_WIDTH):
#					for object in objectsArray[x][y]:
#		#for object in objects:
#						if object.name == lev_set.boss:
#							level_complete = False

		#elif number_security_systems <= 0:
		#	level_complete = True
		elif lev_set.keys_required <= key_count:
			level_complete = True
		if level_complete is True:
			for ele in elevators:
				if not ele.player_authorised:
					ele.set_player_authorisation(True)

		# now do punchings!
		for (puncher, victim) in potential_punch_list:
			# check if the victim is where the puncher was expecting
			if victim.x == puncher.x + puncher.decider.decision.move_decision.dx and victim.y == puncher.y +  puncher.decider.decision.move_decision.dy:
				victim.stun()
				message ('The ' + puncher.name + ' punches the ' + victim.name + ' in the face! The ' + victim.name + ' is stunned!')




		# now do door openings!
		for (opener, victim) in potential_open_list:
			if victim.door is not None:
				#print "opening door"
				victim.door.open()
				# Here is another terrible hack, to make it so an alarmer actually spots you when you open a door on it
				# libtcod.map_compute_fov(fov_map, player.x, player.y, TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)
				fov_map.compute_fov(player.x, player.y, fov=FOV_ALGO, radius=TORCH_RADIUS, light_walls=FOV_LIGHT_WALLS)



		spotted = False

		#UPDATE THE ALARMERS AND OTHER THINGS
#		print ("'fixed' UPDATING ALARMERS AND OTHER THINGS")
		#also track what alarmer is closest to recognizing you
		large_count_down_val = 1000
		temp_alarm_countdown = large_count_down_val
		for ob in worldEntitiesList:
		#UPDATE THE ALARMERS
			if ob.alarmer is not None:
				if fov_map.fov[ob.x, ob.y]:	
					ob.alarmer.update(True)
					spotted = True
					# keep track of shortest alarm count still ongoing
					if ob.alarmer.alarm_countdown > 0 and ob.alarmer.alarm_countdown < temp_alarm_countdown:
						temp_alarm_countdown = ob.alarmer.alarm_countdown 
				else: 
					ob.alarmer.update(False)

		#UPDATE THE DOORS
			if ob.door is not None:
				ob.door.update()

		#UPDATE THE PLANTS
			if ob.plant is not None:
				ob.plant.update()
				ob.name = ob.plant.name	#hey this is probably not the most efficient way to do this
				ob.char = ob.plant.symbol

		if temp_alarm_countdown < large_count_down_val:
			message(str(temp_alarm_countdown) + " seconds from being recognized.", Color_Stat_Info)

		# LET'S MAKE SOME THINGS LEAVE A BLOOD TRAIL? FOR 'FUN'??
		# Actually I don't like it. Might be a thing to try if you have a more open level and a need to 'track' something?
		#	if ob.fighter is not None:
		#		if ob.fighter.hp == 1 and ob.fighter.max_hp > 1 and ob.fighter.bleeds:
		#			#blood splashing around, yaay
		#			bgColorArray[ob.x][ob.y] = mergeColors(bgColorArray[ob.x][ob.y], blood_background_color, 0.2)	

#		#UPDATE THE ALARMERS
#		print ("UPDATING ALARMERS")
#		for y in range(MAP_HEIGHT):
#			for x in range(MAP_WIDTH):
#				for ob in objectsArray[x][y]:
#		#for object in objects:
#	#	for ob in objects:
#					if ob.alarmer is not None:
#						#if libtcod.map_is_in_fov(fov_map, ob.x, ob.y):	
#						if fov_map.fov[ob.x, ob.y]:	
#							# print('a llama (' + str(ob.x) + ',' + str(ob.y) + ') ' + str(ob.alarmer.status))
#							ob.alarmer.update(True)
#							spotted = True
#						else: 
#							ob.alarmer.update(False)
#
#		#UPDATE THE DOORS
#					if ob.door is not None:
#						ob.door.update()
#
#		#UPDATE THE PLANTS
#					if ob.plant is not None:
#						ob.plant.update()
#						ob.name = ob.plant.name	#hey this is probably not the most efficient way to do this
#						ob.char = ob.plant.symbol


		#UPDATE THE UPGRADES THAT AFFECT PLAYER STATS ONCE AND THEN STOP; I'M NOT SURE WHERE ELSE TO PUT THIS	
		for power_up in upgrade_array:
			if getattr(power_up, "upgrade_player_stats_once", None) is not None:
				power_up.upgrade_player_stats_once(player)



		#if spotted == True:
		#	print "Alarmage status: spotted"
		#else: 
		#	print "Alarmage status: NOT spotted"

		# now create attacks!
		deletionList = []
#		print ("'fixed'  CREATING ATTAKS")
		for object in worldEntitiesList:
			if object.decider:
				if object.decider.decision is not None:
					if object.decider.decision.attack_decision is not None:
						attack_list = object.decider.decision.attack_decision.attack_list
						for attack in attack_list:
							try:
								objectsArray[attack.x][attack.y].append(attack)	
								worldAttackList.append(attack)
								attack.send_to_front()
							except IndexError:		#todo: check that this is the right thing to catch...
								print('')


#		for y in range(MAP_HEIGHT):
#			for x in range(MAP_WIDTH):
#				for object in objectsArray[x][y]:
#		#for object in objects:
#					if object.decider:
#						if object.decider.decision is not None:
#							if object.decider.decision.attack_decision is not None:
#								attack_list = object.decider.decision.attack_decision.attack_list
#								for attack in attack_list:
#									try:
#										objectsArray[attack.x][attack.y].append(attack)	
#										worldAttackList.append(attack)
#										attack.send_to_front()
#									except IndexError:		#todo: check that this is the right thing to catch...
#										print('')




		player_just_attacked = False
		if player.decider.decision is not None:
			if player.decider.decision.attack_decision is not None:
				player_attack_list = player.decider.decision.attack_decision.attack_list
				if len(attack_list) > 0:
					player_just_attacked = True

		#if player_just_attacked:
		#	print('the player just attacked!')

		# draw things with the attacks!
#		print("'FIXED'  MORE OBJECT CLEARING, WHICH I GUESS HAS SOMETHING TO DO WITH DRAWING")
		#for y in range(MAP_HEIGHT):
		#	for x in range(MAP_WIDTH):
		#		for object in objectsArray[x][y]:
		##for object in objects:
		#			object.clear()
		clear_onscreen_objects()
		translated_console_set_default_foreground(con, default_text_color)

		#temporarily commenting out, WHICH IS AN EXTRA BAD IDEA
		# libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE,key,mouse)
		#print('2')
		render_all()
		translated_console_flush()
		#put in a pause before drawing the other stuff?
		time.sleep(0.05)

		# process attacks!
		
		#first, for reasons, deal with attacks that no longer exist

		deletionList = []
#		for object in objects:
#		print("'fixed' DELETING ATTACKS, AGAIN?")
#		for y in range(MAP_HEIGHT):
#			for x in range(MAP_WIDTH):
#				for object in objectsArray[x][y]:
#					if object.attack:
#						if object.attack.existing == False:
#							deletionList.append(object)		print ("DELETING ATTACJS")
		for object in worldAttackList:
			if object.attack:
				if object.attack.existing == False:
					deletionList.append(object)

		


		# check how many enemies the player has hit, and 
		# check if the player is getting 'hit' (whether or not the attack gets deflected)

		all_player_attacks_on_target = True		# thing to test whether all player attacks hit
		#print("'fied' CHECKING IF PLAYER GOT HIT")
		for object in worldAttackList:
			if object.attack:
				x = object.x
				y = object.y
				attackee = object.attack.find_attackee()
				if attackee == player:
					player_got_hit = True
				elif object.attack.attacker == player:
					if attackee is not None:
						number_hit_by_player += 1
					else:
						all_player_attacks_on_target = False



#		for y in range(MAP_HEIGHT):
#			for x in range(MAP_WIDTH):
#				for object in objectsArray[x][y]:
#		#for object in objects:
#					if object.attack:
#						attackee = object.attack.find_attackee()
#						if attackee == player:
#							player_got_hit = True
#						elif object.attack.attacker == player:
#							if attackee is not None:
#								number_hit_by_player += 1
#							else:
#								all_player_attacks_on_target = False
		# Update relevant upgrades
		for power_up in upgrade_array:
			if getattr(power_up, "update_based_on_player_accuracy", None) is not None:
				power_up.update_based_on_player_accuracy(all_player_attacks_on_target)
								


		# attacks 'bouncing' off each other (when an attack from A hits B and vice versa, neither attack damages)
		#clashing_pairs_list = []
		#deletionList = []
#		for object in objects:

#		for y in range(MAP_HEIGHT):
#			for x in range(MAP_WIDTH):
#				for object in objectsArray[x][y]:
#					if object.attack:
#						attackee = object.attack.find_attackee()	
#						for yy in range(MAP_HEIGHT):
#							for xx in range(MAP_WIDTH):
#								for other_object in objectsArray[xx][yy]:
#						#for other_object in objects:
#									# perform a check to ensure each unordered pair only gets processed once
#									if object.x < other_object.x or (object.x == other_object.x and object.y <= other_object.y):
#										if other_object.attack and other_object.attack.attacker == attackee:
#											other_attackee = other_object.attack.find_attackee()
#											if other_attackee == object.attack.attacker:
#												# so now we have two fighters attacking each other
#												clashing_pairs_list.append((object, other_object))
#												# deletion happens, because the attacks "cancel each other out"
#												deletionList.append(object)
#												deletionList.append(other_object)
#												message('Clash! The ' + attackee.name + ' and ' + other_attackee.name + '\'s attacks bounce off each other!')
#												if attackee is player or other_attackee is player:
#													player_clashed_something = True


#		print("'fixed' PROCESSING ATTACK CLASHES")

		for object in worldAttackList:
			x = object.x
			y = object.y
			if object.attack:
				#determine the attacker and attackee in this scenario
				attacker = object.attack.attacker
				attackee = object.attack.find_attackee()
				#now, is the attackee also attacking the attacker?	
				for other_object in objectsArray[attacker.x][attacker.y]:
					if other_object.attack:	#so attacker is  definitely being attacked by something...
						other_attacker = other_object.attack.attacker
						if other_attacker == attackee:	# then attacker IS being attacked by attackee!
							# so now we have two fighters attacking each other
							#check to make sure same pair of attacks don't get noted twice:
							if attacker.x < attackee.x or (attacker.x == attackee.x and attacker.y < attackee.y):
								#clashing_pairs_list.append((object, other_object))
								# deletion happens, because the attacks "cancel each other out"
								deletionList.append(object)
								deletionList.append(other_object)
								message('Clash! The ' + attacker.name + ' and ' + attackee.name + '\'s attacks bounce off each other!', Color_Interesting_Combat)
								if attacker is player or attackee is player:
									player_clashed_something = True
#		for y in range(MAP_HEIGHT):
#			for x in range(MAP_WIDTH):
#				for object in objectsArray[x][y]:
#					if object.attack:
#						#determine the attacker and attackee in this scenario
#						attacker = object.attack.attacker
#						attackee = object.attack.find_attackee()
#						#now, is the attackee also attacking the attacker?	
#						for other_object in objectsArray[attacker.x][attacker.y]:
#							if other_object.attack:	#so attacker is  definitely being attacked by something...
#								other_attacker = other_object.attack.attacker
#								if other_attacker == attackee:	# then attacker IS being attacked by attackee!
#									# so now we have two fighters attacking each other
#									#check to make sure same pair of attacks don't get noted twice:
#									if attacker.x < attackee.x or (attacker.x == attackee.x and attacker.y < attackee.y):
#										#clashing_pairs_list.append((object, other_object))
#										# deletion happens, because the attacks "cancel each other out"
#										deletionList.append(object)
#										deletionList.append(other_object)
#										message('Clash! The ' + attacker.name + ' and ' + attackee.name + '\'s attacks bounce off each other!', Color_Interesting_Combat)
#										if attacker is player or attackee is player:
#											player_clashed_something = True


		#for object in objects:
	#	print ("'fixed'  YET MORE OBJECT CLEARING")
		#for y in range(MAP_HEIGHT):
		#	for x in range(MAP_WIDTH):
		#		for object in objectsArray[x][y]:
		#			object.clear()
		clear_onscreen_objects()
		for object in deletionList:
			try:
				objectsArray[object.x][object.y].remove(object)
			except ValueError:
				print('object already removed from lissssssst')
			if object in worldAttackList:
				worldAttackList.remove(object)
		deletionList = []

		## regular old attacks just happening
		#deletionList = []
#		for object in objects:
#		print ("'fixed'  YMAKING ATTACKS HAPPEN")
		for object in worldAttackList:
			x = object.x
			y = object.y
			if object.attack:
				# Increase attack strengths from upgrades. whoof; this is a bit cycle hungry
				for power_up in upgrade_array:
					if getattr(power_up, "affect_strength_of_individual_attack", None) is not None:
						power_up.affect_strength_of_individual_attack(player, object)
				object.attack.inflict_damage()
				object.attack.fade()
				# todo fix??? to make attack highlighting work properly. I commented out these lines and added a reorder. I am scared that this is secretly going to break something
#				if object.attack.existing == False:
#					deletionList.append(object)
				reorder_objects(x,y) 

#		for y in range(MAP_HEIGHT):
#			for x in range(MAP_WIDTH):
#				for object in objectsArray[x][y]:
#					if object.attack:
#						# Increase attack strengths from upgrades. whoof; this is a bit cycle hungry
#						for power_up in upgrade_array:
#							if getattr(power_up, "affect_strength_of_individual_attack", None) is not None:
#								power_up.affect_strength_of_individual_attack(player, object)
#						object.attack.inflict_damage()
#						object.attack.fade()
#						# todo fix??? to make attack highlighting work properly. I commented out these lines and added a reorder. I am scared that this is secretly going to break something
#		#				if object.attack.existing == False:
#		#					deletionList.append(object)
#						reorder_objects(x,y) 
				

		# deleting attacks that have happened
#		for object in objects:
#		print ("'fixed' DELETING HAPPENED ATTACKS")
		#for y in range(MAP_HEIGHT):
		#	for x in range(MAP_WIDTH):
		#		for object in objectsArray[x][y]:
		#			object.clear()
		clear_onscreen_objects()
		for object in deletionList:
			#here's a lazy hack for some things being in list twice i guess
			try:
				objectsArray[object.x][object.y].remove(object)
			except ValueError:
				print('object already removed from list')
			if object in worldAttackList:
				worldAttackList.remove(object)

		#recharge player attack charge. this probably shouldn't go here ultimately
		#if player_recharge_time > 0:
		#	player_recharge_time = player_recharge_time - 1
		player_weapon.recharge(player.fighter.recharge_rate)
	




		# refresh the player's energy
		# design question: when should this refresh? maybe it's only if you haven't done an attack? if you haven't been hurt?
		if (player_just_attacked == False and player_got_hit == False and player_just_jumped == False):
			recharge_rate = 1  			#by default
			# bonus recharge from upgrades:
			for power_up in upgrade_array:
				if  getattr(power_up, "affect_rate_of_energy_recharge", None) is not None:
					recharge_rate += power_up.affect_rate_of_energy_recharge()
			player.fighter.gain_energy(recharge_rate)

		# bonus recharge for combos
		if number_hit_by_player > 1:
			bonus = number_hit_by_player - 1
			player.fighter.gain_energy(bonus)
			message("Combo! +" + str(bonus) + " energy", Color_Stat_Info)
	
			


		
		#weapon degradation time!
		if( player_hit_something == True or player_clashed_something == True) and player_weapon.durability > 0:
			degredation = 0
			if player_clashed_something:
				degredation = 2
			else:
				degredation = 1
			if player_weapon.durability - degredation  <= WEAPON_FAILURE_WARNING_PERIOD and player_weapon.durability > WEAPON_FAILURE_WARNING_PERIOD:
				message("Your "  + player_weapon.name + " is close to breaking!", Color_Interesting_Combat)
			player_weapon.durability -= degredation
			if player_weapon.durability <= 0:
				message("Your " + player_weapon.name + " breaks!", Color_Dangerous_Combat)
		

		# clean up stuff
		for object in garbage_list:
			objectsArray[object.x][object.y].remove(object)				#TODO NOTE: Think this should work the usual way? i.e objectarray[x][y].remove...
			if object in worldEntitiesList:
				worldEntitiesList.remove(object)
			if object in worldAttackList:
				worldAttackList.remove(object)
		
		#refresh decisions!
		#for object in objects:
 #		print("'fixed'  REFRESHING DECISIONS")
		for object in worldEntitiesList:
			if object.decider:
				x = object.x
				y = object.y
				#check for water here
				water_here = False	
				for other_object in objectsArray[object.x][object.y]:
					if other_object.name == 'water':
						water_here = True
				object.decider.refresh()
				if object.fighter:
					object.fighter.in_water = water_here



#		for y in range(MAP_HEIGHT):
#			for x in range(MAP_WIDTH):
#				water_here = False
#	
#				for object in objectsArray[x][y]:
#					if object.name == 'water':
#						water_here = True
#
#				for object in objectsArray[x][y]:
#					if object.decider:	
#						object.decider.refresh()
#					if object.fighter:
#						object.fighter.in_water = water_here


		


		# Now do alarm soundings! and other alarmer-based stuff
#		for ob in objects:

#		print ("'fixed' UPDATING ALARMERS")	
		for ob in worldEntitiesList:
			if ob.alarmer is not None:
				#prev_suspicious = (ob.alarmer.status == 'suspicious')	# ugh what horrible code
				# first, update the alarmer
		
				#ob.alarmer.update(libtcod.map_is_in_fov(fov_map, ob.x, ob.y))
				# next, do things depending on the alarmer's state
				if ob.alarmer.status == 'idle' or  ob.alarmer.status == 'pre-suspicious':
					ob.color = ob.alarmer.idle_color
				elif ob.alarmer.status == 'suspicious':
					if ob.alarmer.prev_suspicious == False:
						message('The ' + ob.name + ' is suspicious!', Color_Interesting_In_World)	
						ob.color = ob.alarmer.suspicious_color
				elif ob.alarmer.status == 'raising-alarm':
					alarm_level += ob.alarmer.alarm_value
					spawn_timer = 1		#run the  spawn clock forwards so new enemies appear
					message('The ' + ob.name + ' sounds a loud alarm!', Color_Interesting_In_World)
					ob.color = ob.alarmer.alarmed_color
				elif ob.alarmer.status == 'alarm-raised':
					ob.color =  color_alarmer_alarmed #ob.alarmer.alarmed_color	

#		for y in range(MAP_HEIGHT):
#			for x in range(MAP_WIDTH):
#				for ob in objectsArray[x][y]:
#					if ob.alarmer is not None:
#						#prev_suspicious = (ob.alarmer.status == 'suspicious')	# ugh what horrible code
#
#						# first, update the alarmer
#				
#						#ob.alarmer.update(libtcod.map_is_in_fov(fov_map, ob.x, ob.y))
#
#						# next, do things depending on the alarmer's state
#						if ob.alarmer.status == 'idle' or  ob.alarmer.status == 'pre-suspicious':
#							ob.color = ob.alarmer.idle_color
#						elif ob.alarmer.status == 'suspicious':
#							if ob.alarmer.prev_suspicious == False:
#								message('The ' + ob.name + ' is suspicious!', Color_Interesting_In_World)	
#								ob.color = ob.alarmer.suspicious_color
#
#						elif ob.alarmer.status == 'raising-alarm':
#							alarm_level += ob.alarmer.alarm_value
#							spawn_timer = 1		#run the  spawn clock forwards so new enemies appear
#							message('The ' + ob.name + ' sounds a loud alarm!', Color_Interesting_In_World)
#							ob.color = ob.alarmer.alarmed_color
#						elif ob.alarmer.status == 'alarm-raised':
#							ob.color =  color_alarmer_alarmed #ob.alarmer.alarmed_color	




		# oh let's start creating enemies at random intervals? 
		#if alarm_level > 0 and spawn_timer % (enemy_spawn_rate/alarm_level) == 0: #and number_security_systems > 0:
		if alarm_level > 0 and spawn_timer <= 0:
			#reset timer
			spawn_timer = decide_spawn_time(enemy_spawn_rate,alarm_level)

		#	reorder_objects() #temp test
		#	print('tick')
		#	print('enemy spawn rate = ' + str(enemy_spawn_rate))
		#	print('total enemy prob = ' + str(lev_set.total_enemy_prob))
		#	print('enemy probabilites = ' + str( lev_set.enemy_probabilities))
#			for (x,y) in spawn_points:

			# check if level is complete
			level_complete = False
			if lev_set.boss is not None:
				level_complete = True
				#check for bosses?
#				for object in objects:

#				print ("'fixed' CHECKING FOR BOSS AGAIN")
				for object in worldEntitiesList:
					if object.name == lev_set.boss:
						level_complete = False

#				print ("CHECKING FOR BOSS AGAIN")
#				for y in range(MAP_HEIGHT):
#					for x in range(MAP_WIDTH):
#						for object in objectsArray[x][y]:
#							if object.name == lev_set.boss:
#								level_complete = False
			#elif number_security_systems <= 0:
			#	level_complete = True
			elif lev_set.keys_required <= key_count:
				level_complete = True

			# are there too many monsters?
			total_monsters = 0
#			for object in objects:

#			print ("'fixed' COUNTING MONSTERS")
			for object in worldEntitiesList:
				if object.fighter is not None and object.name != 'strawman' and object.name != 'flailing strawman' and object.name != 'strawman on wheels':
					total_monsters = total_monsters + 1


#			print ("COUNTING MONSTERS")
#			for y in range(MAP_HEIGHT):
#				for x in range(MAP_WIDTH):
#					for object in objectsArray[x][y]:
#						if object.fighter is not None:
#							total_monsters = total_monsters + 1

			# print ("ummm " + str(total_monsters) + " vs " + str( lev_set.max_monsters))

			# if level_complete == False and    #currently commented out because it stops spawning when you have enough keys
			# probably the 'level_complete' stuff should be looked at and possibly taken out altogether
			if total_monsters < lev_set.max_monsters:		#otherwise, stop the spawning

				elevator_shortlist = []
				if lev_set.level_type == 'arena':	#pick one elvator at random
					choice =  randint( 0, len(elevators)-1)
					elevator_shortlist.append(elevators[choice])
				else:					# do all elevators at once
					elevator_shortlist = elevators
				for ele in elevator_shortlist:
					#pick a random spawn point from those available
	
					num =  randint( 0, len(ele.spawn_points)-1)
					(x,y) = ele.spawn_points[num] 
					#for (x,y) in ele.spawn_points:
					if not is_blocked(x, y):
						#print('ding')
	#ELEVATOR SPAWNING MONKEY HORSESHOE
						total_enemy_prob = lev_set.total_enemy_prob
						enemy_probabilities = lev_set.enemy_probabilities
						enemy_name = 'none'
						num = randint(0, total_enemy_prob)
						for (name, prob) in enemy_probabilities:
						#	print('hi')
							#print('(' + name + ',' + str(prob) + ')')
							if num <= prob:
								enemy_name = name
#								print('tick' + str(x) + ',' + str(y) + ' ' + name)
								monster = create_monster(x,y, name)
								objectsArray[x][y].append(monster)
								worldEntitiesList.append(monster)
								break
							else:
								num -= prob
				#	#open the doors!
				#	for door in ele.special_door_list:
				#		door.currently_invisible = True
				#		door.blocks = False
				#		map[door.x][door.y].block_sight = False	
				#		map[door.x][door.y].blocked = False	
				#	nav_data_changed = True
				#	initialize_fov()
	


		# finally... go to the next level maybe?
		if ready_for_next_level == True:
			ready_for_next_level = False
			next_level()
	
		# reorder_objects()	#TODO probably put this somewhere else?
		#print('4.5')
		render_all()
		translated_console_flush()
	#num_monsters = randint( 0, max_room_monsters)


		# reset upgrade statuses to 'dormant' ? this is probably not where this goes...
		for upgrade in upgrade_array:
			upgrade.status = 'dormant'

#


	elif game_state == 'playing' and player_action == 'pickup_dialog' or player_action == 'upgrade shop dialog':
		#print('3')
		render_all()
		translated_console_flush()


	elif game_state == 'playing' and player_action == 'jump_dialog':
		#print('4')
		render_all()
		translated_console_flush()


	# I think this goes here: want to draw stuff if there's a "you can't do that" message
	elif game_state == 'playing' and player_action == 'invalid-move':
		print('oog')
		render_all()
		translated_console_flush()


	# I guess let's draw things once more?	
#	for object in objects:

#	print ("'fixed'  ONE MORE CLEAR/DRAW FOR THE ROAD")
	#for y in range(MAP_HEIGHT):
	#	for x in range(MAP_WIDTH):
	#		for object in objectsArray[x][y]:
	#			object.clear()
	clear_onscreen_objects()
# 	TODO; I'm commenting this out without replacing it, might cause huge issues!
#	libtcod.console_set_default_foreground(con, default_text_color)
	
	

	#temporarily commenting out, WHICH IS AN EXTRA BAD IDEA
	# libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE,key,mouse)


	if something_changed:
		if game_state == 'paused':
			pause_screen()
		elif game_state == 'control screen':
			control_screen()
		elif game_state == 'big message':
			big_message(current_big_message)
		elif game_state == 'end message':
			end_message()
		elif game_state == 'end data':
			end_data_message()
		elif game_state == 'restartynscreen':
			restartynscreen()
		elif game_state == 'exit':
			break
		else:
			print('8' + game_state)
			render_all()
		translated_console_flush()
	
	something_changed = False




	# how it will go:

	# get decision from player (handle_keys)

	# all other objects (orat least ais?) make decision

	# process all the movement, based on decisions

	# briefly display new position of things in dungeon

	# create attacks, based on decisions

	# resolve attacks - who got hit, what things got deflected

	#display attacks lit up in red?

	# resolve other actions (punches?)

	# display new state of map (attacks faded out a bit)


	#ok no problem, right.




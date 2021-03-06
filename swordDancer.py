import tdl as libtcod
#from libtcod.map import Map
#import libtcodpy as libtcod
import time
import math
import textwrap
import random
#import shelve 	# for saving and loading			# TODO possibly cut; doesn't seem to play nice with cxfreeze
from random import randint
from weapons import Weapon_Unarmed, Weapon_Sword, Weapon_Staff, Weapon_Spear, Weapon_Dagger, Weapon_Strawhands, Weapon_Sai, Weapon_Sai_Alt, Weapon_Nunchuck, Weapon_Axe, Weapon_Katana, Weapon_Hammer, Weapon_Wierd_Sword, Weapon_Wierd_Staff, Weapon_Trident, Weapon_Ring_Of_Power, Weapon_Shiv, Weapon_Broom, Weapon_Pike, Weapon_Halberd, Weapon_Gun
from levelSettings import Level_Settings
from levelGenerator import Level_Generator
from gods import God, God_Healer, God_Destroyer, God_Deliverer
from powerUps import PowerUp, WallHugger, Mindfulness, NeptunesBlessing, Amphibious, Perfectionist, Get_Random_Upgrade, Get_Test_Upgrade, InstantaneousStrength, Rejuvenation
from saveDataHandler import SaveDataHandler #, SaveDatum
from controlHandler import ControlHandler
from colorHandler import ColorHandler
from enemyArtHandler import EnemyArtHandler
# from object import Object  #Nope

SCREEN_WIDTH = 70
SCREEN_HEIGHT = 39

LIMIT_FPS = 20
frame_pause = 0.05
frame_attack_pause = 0.07

VERSION_STRING = 'Version 0.0.1.0.0'

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

ALARMER_RANGE = 5

CHANCE_OF_ENEMY_DROP = 30

STARTING_ENERGY  = 10

DEFAULT_JUMP_RECHARGE_TIME = 4		#40
DEFAULT_BLOOM_TIME = 37

STARTING_CURRENCY = 2 #2


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
color_white = (255,255,255)
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
color_faerie = 	(v_e,v_e,v_e)	#	(0,0, 255)		#libtcod.blue
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
Color_Route_Guidance=(v_p,v_p,v_p)		# Telling the player where to go, in particular when exits open



# TODO integrate mouse panel colors with the color handler
Color_Mouseover_Background = (220,220,230)
Color_Mouseover_Foreground = (30,30,20)

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








####################################
#
#
#	WELCOME TO OBJECT LAND
#
#
####################################





class Object:
	#this is a generic object: the player, a monster, an item, the stairs...
	#it's always represented by a character on screen.
	def __init__(self, x, y, char, name, color, blocks=False, jumpable = True, always_visible=False, fighter=None, decider=None, attack=None, weapon = False, progenitor = None, shrine = None, floor_message = None, currently_invisible = False, alarmer = None, plant = None, drops_key = False, phantasmal = False, getting_burned = False, aflame = False, immune_to_fire = False, exists_in_map = True, mouseover = None, tags = set()):  #raising_alarm = False): # door = None, 
		self.x = x
		self.y = y
		self.char = char
		self.name = name
		self.blocks = blocks
		self.jumpable = jumpable
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
		self.progenitor = progenitor #the object that spawned this one (if applicable)
		self.shrine = shrine
		if self.shrine:
			self.shrine.owner = self
		self.floor_message = floor_message
		if self.floor_message:
			self.floor_message.owner = self
		#self.door = door
		#if self.door:
		#	self.door.owner = self
		self.plant = plant
		if self.plant:
			self.plant.owner = self
		self.currently_invisible = currently_invisible	# I am introducing this as a hack 
								#to make elevator doors go away. Instead of actually going away, 									#they'll be made invisible, not blocking and not blocking light
								# (different from being invisible). Video games!
		self.exists_in_map = exists_in_map

		#self.raising_alarm = raising_alarm
		self.alarmer = alarmer
		self.drops_key = drops_key
		self.phantasmal = phantasmal
		self.mouseover = mouseover
		if self.mouseover == None:
			self.mouseover = self.name + " TODO"
		self.tags = tags

		self.getting_burned = getting_burned
		self.aflame = aflame
		self.immune_to_fire = immune_to_fire
		self.pushMomentum = 0


#	# TODO: ultimately this move should be deprecated? Use attemptMove instead
#	def move(self, dx, dy, ignore_doors = False):	
#		global objectsArray, FinalPreDrawEvents
#									#TODO will need to update objectarry
#		if not is_blocked(self.x + dx, self.y + dy, generally_ignore_doors = ignore_doors):
#			#move by the given amount
#			old_x = self.x
#			old_y = self.y
#			new_x = self.x + dx
#			new_y = self.y + dy
#			self.x = new_x
#			self.y = new_y
#			# print('HI! iM AT (' + str(old_x) + ',' + str(old_y) + ') and want to go to (' + str(new_x) + ',' + str(new_y) + ')')
#			# Update objectsArray so that self is in the right list
#			objectsArray[new_x][new_y].append(self)
#			objectsArray[old_x][old_y].remove(self)



	# MovementPhase event
	def attemptMove(self, dx, dy):
		global objectsArray, fov_recompute #, FinalPreDrawEvents
		old_x = self.x
		old_y = self.y
		new_x = self.x + dx
		new_y = self.y + dy
	


		# check to see if there are objects in the new space that block
		blocking_object = None
		for obj in objectsArray[new_x][new_y]:
			if obj.blocks:
				blocking_object = obj
				obj.getWalkedInto(self)

		if blocking_object == None:
			#test to see if there is just a straight up wall blocking.
			if map[new_x][new_y].blocked:
				# don't walk
				# if this was the player, tell them they walked into a wall
				if self is player:
					message ("You walk into a wall.", Color_Personal_Action)
				#if we were pushed, stop being pushed
				self.pushMomentum = 0
			else:
				# do the actual movement
				self.x = new_x
				self.y = new_y
				objectsArray[new_x][new_y].append(self)
				objectsArray[old_x][old_y].remove(self)
				# in addition, recalculate fov and report objects here if the player has just moved
				if self is player:
					argset = (new_x, new_y)
					FinalPreDrawEvents.append((report_objects_here, argset))
					fov_recompute = True

				# Also! check for projectiles?
				for obj in objectsArray[new_x][new_y]:
					if 'projectile' in obj.tags and obj is not self:
						if obj.attacksOnHit:
							#print ('owowowowow at (' + str(new_x) + ',' + str(new_y) + ')')
							obj.destroyOnImpact()


	# MovementPhase event
	def attemptJump(self, dx, dy):
		global fov_recompute

		# check for obstacles.

		blockedByWall = False
		nearestObstacle = None
		old_x = self.x
		old_y = self.y
		target_x = self.x + dx
		target_y = self.y + dy
		final_x = target_x
		final_y = target_y
		# for now this only works on straight line or diagonal jumps. If we start having knights move jumps or something, we'll have to rethink
		if math.fabs(dx) == 0 or math.fabs(dy) == 0 or math.fabs(dx) == math.fabs(dy):
			xSign = getSign(dx)
			ySign = getSign(dy)
			i = 1;
			while i <= max(math.fabs(dx), math.fabs(dy)):
			
				# check the next space out
				space_x = self.x + i*xSign
				space_y = self.y + i*ySign
				if map[space_x][space_y].blocked:
					blockedByWall = True
					final_x = self.x + (i-1)*xSign
					final_y = self.y + (i-1)*ySign
					break
				else:
					# check for blocking, objects
					for obj in objectsArray[space_x][space_y]:
						# blocking objects are only a problem if they'renot jumpable, or they're where we're trying to get to
						if obj.blocks and (not obj.jumpable or i == max(math.fabs(dx), math.fabs(dy))):
							nearestObstacle = obj
							final_x = self.x + (i-1)*xSign
							final_y = self.y + (i-1)*ySign
							break
				# Hey I forgot to increase i!
				i += 1

		if final_x != self.x or final_y != self.y:
			# do the actual movement
			self.x = final_x
			self.y = final_y
			objectsArray[final_x][final_y].append(self)
			objectsArray[old_x][old_y].remove(self)
			# in addition,  recalculate fov and report objects here if the player has just moved
			if self is player:
				argset = (final_x, final_y)
				FinalPreDrawEvents.append((report_objects_here, argset))
				fov_recompute = True

		
		# Now that we know where the player will end up and what they'll jump over, we can tell them about it
		# first describe some of the things you jump over
		if final_x != old_x or final_y != old_y:
			xSign = getSign(dx)
			ySign = getSign(dy)
			i = 1
			while i < max(math.fabs(final_x - old_x), math.fabs(final_y - old_y)):
				# report on interesting things here, which you are jumping o'er 
				
				space_x = old_x + i*xSign
				space_y = old_y + i*ySign
				print ("leaping through " + str(space_x) + "," + str(space_y))
				for obj in objectsArray[space_x][space_y]:
					if obj.fighter:
						message ("You leap over the " + obj.name + "\'s head!", Color_Personal_Action)
					elif obj.name == 'fire':
						message ("You leap through the flames!", Color_Personal_Action)
				i+=1


		# Now, if we didn't quite get where we wanted, report on what we jumped into
		if final_x != target_x or final_y != target_y:
			if nearestObstacle is not None:
				message ("You collide with the " + nearestObstacle.name + "!", Color_Personal_Action)
			else: 
				message ("You leap gracefully into a wall.", Color_Personal_Action)

		return

	def attemptPickup(self, args):
		(items_to_pickup) = args
		for item in items_to_pickup:
			if item.exists_in_map:
				print (self.name + " picking up " + item.name)

				item.getPickedUp(self)




	def draw(self, render_mode = None, bg_color = None):
		global camera

		#x_offset = camera.x-SCREEN_WIDTH/2
		x_offset = int(camera.x-(SCREEN_WIDTH + MESSAGE_PANEL_WIDTH)/2)
		#y_offset = camera.y-SCREEN_HEIGHT/2
		y_offset = int(camera.y-(SCREEN_HEIGHT-PANEL_HEIGHT)/2)
		#only show if it's visible to the player; or it's set to "always visible" and on an explored tile
		# also don't draw it if it's set to 'currently invisible'


		# Here's a special thing. Fire randomizes its appearance every time it gets drawn in the attack step
		if render_mode is not None and render_mode == 'attack-step':
			if self.name == 'fire':
				self.char = 384 + randint(0,1)
			elif self.name == 'firepit':
				self.char = 370 + randint(0,1)

		#if True:	# temporary hack to test enemy navigation
		if (fov_map.fov[self.x, self.y] or (self.always_visible and map[self.x][self.y].explored)) and not self.currently_invisible:

			#set the color and then draw the character that represents this object at its position
			con.draw_char(self.x - x_offset, self.y - y_offset, self.char, bg=bg_color, fg = self.color)



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


#	def move_towards(self, target_x, target_y):
#		print('Error! argument Object.move_towards called. Mark was pretty sure this method wasn\'t being used, and it would have  caused wierd bugs as currently written anyway, so he commented it out. Maybe let him know that that happened?')
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



	def createActionEventDetails(self):
		global 	PreliminaryEvents, MovementPhaseEvents, AttackPhaseEvents, DamagePhaseEvents, MiscPhaseEvents, FinalPreDrawEvents, FinalPostDrawEvents
		return

#	def getPreliminaryEvents(self):
#		return []
#
#	def getMovementPhaseEvents(self):
#		return []
#
#	def getAttackPhaseEvents(self):
#		return []
#
#	def getDamgePhaseEvents(self):
#		return []
#
#	def getMiscPhaseEvents(self):
#		return []
#
#	def getFinalPreDrawEvents(self):
#		return []
#
#	def getFinalPostDrawEvents(self):
#		return []


	def getHit(self,attack):
		print (self.name + ' getting hit')
		if self.fighter:
			self.fighter.take_damage(attack.damage)
			# highlight in the appropriate color
			# Commenting THIS line out because it caused an enemy to get hit twice. Bad times!
			#self.send_to_front()
			#self.draw(bg_color = attack.color)
		return


	def getWalkedInto(self,walker):
		return
	

	def getPickedUp(self,picker):
		global player_weapon, objectsArray, key_count, currency_count, lev_set

		# things can only be picked up if they are in the map
		if self.exists_in_map :

			if self.weapon == True:

				# TODO:maybe make dropping old weapons happen?

				# picker gets a new weapon! Yay! 
				new_weapon = get_weapon_from_item(self, picker.fighter.bonus_max_charge)

				if picker is player:
					old_weapon = get_item_from_weapon(player_weapon)
					# messaging!
					if str(old_weapon.name) == "unarmed":
						message('You pick up the ' + new_weapon.name + '.', Color_Personal_Action) 
					else:
						message('You throw away your ' + old_weapon.name + ' and pick up the ' + new_weapon.name + '.', Color_Personal_Action)
					player_weapon = new_weapon

				else:
					old_weapon = get_item_from_weapon(picker.weapon)
					# messaging!
					if str(old_weapon.name) == "unarmed":
						localMessage('The ' + picker.owner.name +  ' picks up the ' + new_weapon.name + '.', Color_Personal_Action, picker.owner.x, picker.owner.y, Color_Interesting_In_World) 
					else:
						localMessage('The ' + picker.owner.name + ' throws away their ' + old_weapon.name + ' and picks up the ' + new_weapon.name + '.', picker.owner.x, picker.owner.y, Color_Interesting_In_World)
					picker.weapon = new_weapon



				# take this item off the map
				self.exists_in_map = False
				objectsArray[self.x][self.y].remove(self)


			elif self.plant is not None:
				self.plant.tread()
				if picker is player:
					message('You pick up the ' + self.name + ' and eat it.', Color_Personal_Action)
					self.plant.harvest(player)
					garbage_list.append(self)
				elif picker.fighter:
					localMessage('The ' + picker.name + ' picks up the ' + self.name + ' and eats it.', picker.x, picker.y, Color_Personal_Action)
					self.plant.harvest(picker)
					garbage_list.append(self)


				# take this item off the map
				self.exists_in_map = False
				objectsArray[self.x][self.y].remove(self)


			elif self.name =='key':
				# currently only the player can interact with keys
				if picker is player:
					message('You snatch up the key.', Color_Personal_Action)
					key_count += 1

					if key_count >= lev_set.keys_required:
						message("You have enough keys, the exits are now open!", Color_Interesting_In_World)

					
					# take this item off the map
					self.exists_in_map = False
					objectsArray[self.x][self.y].remove(self)	
			elif self.name ==  'favour token':
				# currently only player can interact with favour tokens
				if picker is player:
					message('You take the favour token.', Color_Personal_Action)
					currency_count += 1

					
					# take this item off the map
					self.exists_in_map = False
					objectsArray[self.x][self.y].remove(self)






		#	new_weapon = get_weapon_from_item(weapons_found[keynum-1], player.fighter.bonus_max_charge)
		#	old_weapon = get_item_from_weapon(player_weapon)
		#	player_weapon = new_weapon
		#	objectsArray[weapons_found[keynum-1].x][weapons_found[keynum-1].y].remove(weapons_found[keynum-1])
		#	# let's try that you don't drop your weapon, you throw it away entirely so you can't pick it up later.
		#	#drop_weapon(old_weapon)
		#	weapon_found = True
		#	if str(old_weapon.name) == "unarmed":
		#		message('You pick up the ' + new_weapon.name + '.', Color_Personal_Action) 
		#	else:
		#		message('You throw away your ' + old_weapon.name + ' and pick up the ' + new_weapon.name + '.', Color_Personal_Action)


		return


	def destroy(self, args):
		#print("DESTROY DESTROY DESTROY " + self.name + " at (" + str(self.x) + "," + str(self.y) + ")\n")
		#print(str(objectsArray[self.x][self.y]))
		self.remove_from_game()

	def remove_from_game(self):
		global garbage_list
		self.blocks = False
		self.fighter = None
		self.decider = None
		self.clear()
		self.send_to_back()
		garbage_list.append(self)

	
	def modern_move(self, args):
		(dx,dy) = args
		self.attemptMove(dx,dy)


	
	def modern_jump(self, args):
		(dx,dy) = args
		if self.fighter:
			# check to see if we are capable of jumping (should be, but good to double check)
			if self.fighter.jump_available():
				# This line just makes the fighter component pay the energy cost for jumping
				self.fighter.make_jump()
				# This line makes all the jumping actually happen!
				self.attemptJump(dx,dy)
			else:
				message('Your legs are just too tired to jump.', Color_Not_Allowed)


	def attemptPush(self, args):
		global MovementPhaseEvents
		(direction, force) = args
		(dx,dy) =  getVectorFromDirectionAndSpeed (direction, 1)
		self.pushMomentum = force
		argset = (dx,dy)
		MovementPhaseEvents.append((self.doPush, argset))
	
	def doPush(self, args):
		global MovementPhaseEvents
		(dx,dy) = args
		if self.pushMomentum > 0 and self in objectsArray[self.x][self.y]:	# only push if object is still where we think it is;
											# otherwise wierd stuff can happen
			self.attemptMove(dx,dy)
		self.pushMomentum -= 1
		if self.pushMomentum > 0:
			MovementPhaseEvents.append((self.doPush, args))



# currently this class does nothing! It's not hooked up to anything! Woo!
class ModernAttack(Object):

	def __init__(self, x, y, color, attacker = None, damage = 1, direction = None, lifespan = 1, force = 0):

		Object.__init__(self, x, y, '#', 'attack', color, blocks=False,  tags = {'attack'})


		if attacker is not None:
			mouseover = "A space where " + attacker.name + " just attacked."
		else: 
			mouseover = "A space where an attack just happened."

		self.attacker = attacker 
		self.damage = damage
		self.direction = direction
		self.force = force		#physical force that pushes enemies around the map!
		self.lifespan = lifespan
		self.deflected = False		# set to true when attacks 'clash of each other' 
		self.checkForDeflection()

		
		argset = None
		DamagePhaseEvents.append((self.dealDamage, argset))
		FinalPostDrawEvents.append((self.fadeAway, argset))
		# TODO add 'check for deflections' method and call it here
		


	def checkForDeflection(self):
		global player_clashed_something
		#search for... hmmm hang on

		# See if there is an attack on the space where my attacker is. If so, see if any of those  attacks have their attacker in the space I am attacking. If that happens, we have a clash!

		if self.attacker:
			attacker_x = self.attacker.x
			attacker_y = self.attacker.y
			
			for object in objectsArray[attacker_x][attacker_y]:
				if 'attack' in object.tags:
					if object.attacker:
						if object.attacker.x == self.x and object.attacker.y == self.y:	#then we have a clash!
							#self.deflected = True
							#object.deflected = True
							self.deflect()
							object.deflect()
							if self.attacker is player or object.attacker is player:
								player_clashed_something = True
							#message('Clash!111one The ' + object.attacker.name + ' and ' + self.attacker.name + '\'s attacks bounce off each other!', Color_Interesting_Combat)
							localMessage('Clash! The ' + object.attacker.name + ' and ' + self.attacker.name + '\'s attacks bounce off each other!', self.x, self.y, Color_Interesting_Combat)
	

	# mark attack as deflected (and also reduce force if 
	def deflect(self):
		if not self.deflected:
			self.deflected = True
			if self.force > 0:
				self.force -= 1		# TODO: may want to divide in half (and round down) instead

	def dealDamage(self,argset):
		global player_hit_something, upgrade_array, number_hit_by_player, MovementPhaseEvents

		# possibly update strength if we have an upgrade that does that (and this is the player's attack)
		if self.attacker is player:
			for power_up in upgrade_array:
				if getattr(power_up, "affect_strength_of_individual_attack", None) is not None:
					power_up.affect_strength_of_individual_attack(player, self)

		
		# only do the attack if it has not been deflected
		if not self.deflected:
	
			#print(self.attacker.name + " attack hitting shennanigans")
			for object in objectsArray[self.x][self.y]:
				if 'attack' not in object.tags:		#Attacks can't hit each other! I bet I forget this and try to do something with attacks hitting each other at some point in the future.
					#print(self.attacker.name + " attack hitting " + object.name)
			

					# May want to check this / add an explicit tag later, but for now, things can get hit
					# if and only if they block or have an associated fighter component.
					if object.blocks or object.fighter:

						# print messages about hits happening
						if object is player:
							message('The ' + self.attacker.name.capitalize() + ' hits!', Color_Dangerous_Combat)	
						elif self.attacker is player:
							message('You hit the ' + object.name.capitalize() + '!', Color_Boring_Combat)
							player_hit_something = True
							number_hit_by_player += 1
						else:
							message('The ' + self.attacker.name.capitalize() + ' hits the ' + object.name.capitalize() + '!', Color_Boring_Combat)


					if object.fighter and object.fighter.bleeds:
						splash_color = blood_background_color
						#if object is player:
						#	splash_color = blood_background_color
						#else:
						#	splash_color = object.fighter.attack_color
						
						bgColorArray[object.x][object.y] = mergeColors(bgColorArray[object.x][object.y], splash_color, 0.2)
						#blood splashing around, yaay
						if (object.x > 0):
							bgColorArray[object.x-1][object.y] = mergeColors(bgColorArray[object.x-1][object.y], splash_color, 0.1)	
						if (object.x < MAP_WIDTH-1):
							bgColorArray[object.x+1][object.y] = mergeColors(bgColorArray[object.x+1][object.y], splash_color, 0.1)
						if (object.y > 0):
							bgColorArray[object.x][object.y-1] = mergeColors(bgColorArray[object.x][object.y-1], splash_color, 0.1)
						if (object.y < MAP_HEIGHT-1):
							bgColorArray[object.x][object.y+1] = mergeColors(bgColorArray[object.x][object.y+1], splash_color, 0.1)




					if object.blocks or object.fighter:
						object.getHit(self)
					#translated_console_set_char_background(con, object.x, object.y, self.faded_color, libtcod_BKGND_SET)

			# Send this attack to the back so other things can be visible!?
			#self.send_to_back()
			reorder_objects(self.x, self.y)			

		# otherwise, reorder objects anyway because otherwise the things going to be drawed under the attack and we don't want that
		else:
			reorder_objects(self.x,self.y)
			# also, we still want to count a clashed attack towards the player hit things.
			if self.attacker is player:
				for object in objectsArray[self.x][self.y]:
					if 'attack' not in object.tags and (object.blocks or object.fighter):
						number_hit_by_player += 1	
		


		# experimental thing: do a push?
		if self.force > 0 and self.direction is not None:
			#print("DIRECTIONS (and force), I AHVE THEM")
			for object in objectsArray[self.x][self.y]:
				if 'attack' not in object.tags:
					if object.blocks or object.fighter:
						argset = (self.direction, self.force)
						MovementPhaseEvents.append((object.attemptPush, argset))		



	def fadeAway(self, argset):	# FinalPostDrawEvents phase
		self.lifespan -= 1
		if self.lifespan <= 0: 
			self.remove_from_game()
		else:	# keep attacking, at reduced lifespan
			argset = None
			#print("NON-FADY ATTACK ALERT")
			DamagePhaseEvents.append((self.dealDamage, argset))
			FinalPostDrawEvents.append((self.fadeAway, argset))
			# delete the attack woo!

		#Hey here's another thing. What's the right way to check whether something is an (object of the type we are interested in?)
		# I kind of want to do a 'flags' system? Or keywrods? I like having a list of keywords rather than individual flags because it means I don't keep having to go back to the Object class and add a new field every time I want a new type of object.  But is it actually better from a design / runtime persepctive?
		# I suspect a dict that keywords thingsto  true or false might be better than a list that the program has to search through in order to see if a given keyword is in the list.
		# just a question of, how does dict handle 'default values'?

		# ok based on a thing online it looks like Set is actually the thing I want. Cos, you know, I don't care about order and I don't care about mapping keys to values.


		# OK I should actually give this some thought
	

		#attack= BasicAttack(val + attacker.fighter.extra_strength + bonus_strength, attacker=attacker)

		

		# Ok maybe there is another phase we have to add?

		# Process attack decisions?
		# Attacks appear in the world! Here they are
		# Attacks have the opportunity to deflect each other
		# Attacks... do damage to the thing they are on??
		# Things.... take damage???,
		# In next rund's preliminary phase, attakcs disappear???
		
		# Ok so really are 'do damage' and 'take damage' separate stages, is really the question i have
		# Herrrmmm....  So I can imagine that in some theoretical future time down the road,
		# we might want to have entities be able to 'resist' certain types of attacks.
		# And that's the sort of thing that should be handled by a method within the entity itself.
		# So certainly you do want a method called 'take damage' that is probably separate from a method 'do damage' belonign to attacks.
		# *but* that doesn't mean they have to happen at separate times really! This can all happen in the damage phase. The attack does it damagey method which causes the victime to call its take damagey method, and the attack goes away and thinks "i did the damage, good job me', and the victim thinks 'i resisted the damage because of my wand of water resistance or whatever, go me". And it seems like the taking damage method doesn't really need to wait and see what happens elsewhere in the damage stage? unless you get a thing that says like you resist damage if you killed an enemy this turn or something, or whatever. Which seems (a) complicated and (b) not a great design, and maybe i come up with some better very complicated idea down the road but for the time being it's not worth coding for that eventuality. like I think the 'attacks clashing off each other' thing is probably as complex as we're going to get on that front.
		
		# So:
		# Attack phase: Add attacks to world based on processing attack data. As attacks appear they have the possibility of 'deflecting' other attacks that have already appeared (if the two attacks are hitting each others owners)
		# Damage phase: attacks that are not'deflected' do damage to the things they are on. Deflected attacks disappear?
		# Misc phase: things bleed?
		
		# preliminary phase of next round: attacks disapear (except maybe for attacks that hang around, if we ever decide to do that)
		# ok cool!



class Fire(Object):

	def __init__(self, x, y, infinite = False):  #raising_alarm = False):
		global AttackPhaseEvents
		Object.__init__(self, x, y, 384 + randint(0,1), 'fire', fire_color, blocks = False, weapon = False, always_visible=False, mouseover = "WUH WOH.")
		argset = (self.x,self.y)
		AttackPhaseEvents.append((self.burnThings, argset))
		self.fuel = 45 + randint(0,10)
		self.infinite = infinite


	def getActionEvent(self):
		return self.spread


	def getActionEventDetails(self):
		argset = (self.x,self.y)
		return [(self.spread, argset), (self.burnThings, argset)]


	def createActionEventDetails(self):
		global AttackPhaseEvents, MiscPhaseEvents
		argset = (self.x,self.y)


		AttackPhaseEvents.append((self.burnThings, argset))
		#FinalPreDrawEvents.append((self.spread, argset))		# TEMP CANCELLED OUT FIRE SPREADING
		
		#return [(self.spread, argset), (self.burnThings, argset)]
		


	def burnThings(self, argset):
		global MiscPhaseEvents
		for object in objectsArray[self.x][self.y]:
			if object.immune_to_fire == False and object is not self:
				#hurt the thing with fire!
				#first report a messag about it
				if object is player:
					message('You get burned!', Color_Dangerous_Combat)
				elif object.fighter or object.name == 'firepit':
					localMessage('The ' + object.name.capitalize() + ' gets burned!', self.x, self.y, Color_Boring_Combat)
				
				if object.fighter:
					object.fighter.take_damage(1)	# for now, fire just does 1 damage to everything
				#elif object.door: 
				#	object.door.take_damage(1)
				elif object.name == 'firepit':
					object.take_damage(1)	

				# also extinguish yourself if on water
				if object.name == 'water':
					self.fuel = 0
		if not self.infinite:
			self.fuel -= 1			
		if self.fuel <= 0:
			MiscPhaseEvents.append((self.destroy, argset))


	def spread(self, argset):

		(arg_x, arg_y) = argset

		if randint(0,1) == 0:
			#choose a random space near me
			dx = randint(0,2) - 1
			dy = randint(0,2) - 1
	
			# spread to self.dx,self.y+dy, if possible
			try:	
				new_fire_x = self.x + dx
				new_fire_y = self.y + dy
				if map[new_fire_x][new_fire_y].blocked == False:
					fire_already_here = False
					for ob in objectsArray[new_fire_x][new_fire_y]:
						if ob.name == 'fire':
							fire_already_here = True
					if not fire_already_here:
						# create new fire!
						#print("spreading with args (" + str(arg_x) + ", " + str(arg_y) + ") at (" + str(self.x) + "," +  str(self.y) + ") to (" + str(new_fire_x) + "," + str(new_fire_y) + ")")
						new_fire = Fire(new_fire_x,new_fire_y)
						objectsArray[new_fire_x][new_fire_y].append(new_fire)
						worldEntitiesList.append(new_fire)

			
			except IndexError:
				return "Out of play area"

		#Object.__init__(self, x=x, y=y, char = 217, name = 'fire', color = , blocks=False, always_visible=False, fighter=None, decider=None, attack=None, weapon = False, shrine = None, floor_message = None, door = None, currently_invisible = False, alarmer = None, plant = None, drops_key = False, phantasmal = False, getting_burned = False, aflame = False, mouseover = 'Too burny!')



class Firepit(Object):
	
	def __init__(self, x, y):

		Object.__init__(self, x, y, 370 + randint(0,1), 'firepit', fire_color, blocks = True, weapon = False, always_visible=False, mouseover = "Mmmm, burny.")





	def getHit(self, attack):
		#explode!
		arg_set = (self.x, self.y)
		MiscPhaseEvents.append((self.explode, arg_set))


	def take_damage(self, damage_val):
		if damage_val > 0:
			#explode!
			arg_set = (self.x, self.y)
			MiscPhaseEvents.append((self.explode, arg_set))

	def explode(self, arg_set):
#		global objectsArray, worldEntitiesList
		message('boom')
		message('The ' + self.name + ' explodes', Color_Boring_Combat)
		for x in range (self.x - 2, self.x+3):
			for y in range (self.y - 2, self.y + 3):
				if x >= 0  and x < MAP_WIDTH and y >= 0  and y < MAP_HEIGHT and ((x-self.x)*(x-self.x)) + ((y-self.y)*(y-self.y)) <= 4 and not map[x][y].blocked:
					fire_already_here = False
					for ob in objectsArray[x][y]:
						if ob.name == 'fire':
							fire_already_here = True
					if not fire_already_here:
						#new_fire = Object(x, y, 317 + randint(0,1), 'fire', fire_color, blocks = False, weapon = False, always_visible=False, mouseover = "Uh oh.")
						new_fire = Fire(x,y)
						#new_fire = Fire(x,y)
						objectsArray[x][y].append(new_fire)
						worldEntitiesList.append(new_fire)

					#	for other_object in objectsArray[x][y]:
					#		if other_object.door:
					#			other_object.aflame = True
					#			worldEntitiesList.append(other_object)	#ugh what is this code
						
		garbage_list.append(self)



	
class Door(Object):
	def __init__(self, x, y, easy_open = False):

		Object.__init__(self, x, y, 368, 'door', default_door_color, blocks=True, always_visible=True, jumpable = False, mouseover = "Walk into this door or attack it to open. (Sometimes you need to give it a bit of welly.)")
		map[self.x][self.y].block_sight = True
		# decide stickiness - when it hits 0, door will automatically open when walked into
		if easy_open or randint( 0, 1) == 0:
			self.stickiness = 0		# a lot of the time doors just open!
		else:
			self.stickiness = randint( 0, 1)  + randint( 0, 1)  + randint( 0, 1)  + randint( 0, 1) 


	def getHit(self,attack):
		global fov_recompute


		message('The door crashes down!', Color_Interesting_In_World)

		self.visible = False
		self.blocks = False
		self.jumpable = True
		self.send_to_back()
		objectsArray[self.x][self.y].remove(self)
		garbage_list.append(self)
		
		#update the map to say that this square isn't blocked, and update the nav data
		map[self.x][self.y].blocked = False
		map[self.x][self.y].block_sight = False
		
		nav_data_changed = True
		initialize_fov()		# this is ok, right? update the field of view stuff
		fov_recompute = True



	def getWalkedInto(self,walker):	#normal doors can't be closed after opening, Just one of those things
		

		if self.stickiness > 0:
			localMessage('The door rattles.', self.x, self.y, Color_Boring_In_World)
			self.stickiness -= 1
		else:
			localMessage('The door opens', self.x, self.y, Color_Boring_In_World)
			# open the door! For now this is the same as destroying it

			self.visible = False
			self.blocks = False
			self.jumpable = True
			self.send_to_back()
			objectsArray[self.x][self.y].remove(self)
			garbage_list.append(self)
			
			#update the map to say that this square isn't blocked, and update the nav data
			map[self.x][self.y].blocked = False
			map[self.x][self.y].block_sight = False
			
			nav_data_changed = True
			initialize_fov()		# this is ok, right? update the field of view stuff
			fov_recompute = True

# LIke a door, but for elevators! I need to overwrite a bunch of methods and probably add some as well here. 
class ElevatorDoor(Door):
	def __init__(self, x,y,owner):
		Door.__init__(self, x,y)
		self.char = '+'
		self.owner = owner
		map[self.x][self.y].block_sight = False		# gonna experiment with making these things let you see to the other side.


class ExitArrow(Object):
	def __init__(self, x,y, direction):
		symbol = 24
		if direction == 'up':
			symbol = 24
		elif direction == 'down':
			symbol = 25
		elif direction == 'right':
			symbol = 26
		elif direction == 'left':
			symbol = 27
		Object.__init__(self, x, y, symbol, 'exit arrow', default_altar_color, blocks=False,  mouseover = "Go here to win!")
		self.visible = False

	def update(self, level_complete = False):
		global game_time
		if level_complete and game_time % 2 == 0:
			self.always_visible = True
			self.visible = True
			self.color = color_boman
		else:
			self.always_visible = False
			self.visible = False
			self.color = default_altar_color


class EnemyDispenser(Object):
	def __init__(self, x, y, enemy_type = 'None'):
		Object.__init__(self, x, y, char = 9, name = 'Dispenser', color = color_white, mouseover = "Bad Things come out of this Hole.", tags = ['listener'], always_visible = True)
		self.status = 'idle'
		self.cooldown_timer = 1
		self.cooldown_length = 20
		self.progency = []	# list of (currently alive?) enemies this dispenser has spawned
		self.max_progency = 4

	def notify(self):
		self.color = color_alarmer_alarmed
		self.status = 'activated'
	

	def update(self):
		global FinalPostDrawEvents
		if self.status == 'activated':
			# OH boy add let's make some enemies happen maybe!
			if self.cooldown_timer > 0:
				self.cooldown_timer -= 1
			else:
				#Spawn enemies
				argset = (self.x,self.y)
				PreliminaryEvents.append((self.spawn_enemy, argset))
				
		elif self.cooldown_timer > 1 :	
# have a 1 second delay for the next time this dispenser gets activated
			self.cooldown_timer -= 1

		if self.status == 'idle':
			self.color = color_white
		# become idle ?  basically unless we here an alaamr on the enxt turn we'll stop doing things
		self.status = 'idle'



	#Preliminaryphase ? - spawn an enemy here!
	def spawn_enemy(self, args):
		global worldEntitiesList, lev_set

		# first check whether anything is standing 'on top of' the dispenser, because if so we have to not dispense things
		obstruction = False
		for object in objectsArray[self.x][self.y]:
			if object is not self and object.blocks:
				obstruction = True
		# if there's an obstruction, don't spawn
		if obstruction:
			# Also add 1 to the timer just so things don't spawn the *second* you step off.
			self.cooldown_timer += 1
		else:
		
			# Next up, a check for too many monsters!
			# are there too many monsters?
			total_monsters = 0
#					for object in objects:
#					print ("'fixed' COUNTING MONSTERS")
			#for object in worldEntitiesList:
			#	if object.fighter is not None and object.name != 'strawman' and object.name != 'flailing strawman' and object.name != 'strawman on wheels':
			#		total_monsters = total_monsters + 1



			# Do a check for too many enemies
			#if total_monsters < lev_set.max_monsters:		#if two many enemies, stop the spawning
			if len(self.progency) < self.max_progency:
				# spawn an enemy! currently based on level enemy probabilities
				total_enemy_prob = lev_set.total_enemy_prob
				enemy_probabilities = lev_set.enemy_probabilities
				enemy_name = 'none'
				num = randint(0, total_enemy_prob)
				for (name, prob) in enemy_probabilities:
					if num <= prob:
						enemy_name = name
						monster = create_monster(self.x,self.y, name)
						objectsArray[self.x][self.y].append(monster)
						worldEntitiesList.append(monster)
						self.progency.append(monster)
						monster.progenitor = self
						break
					else:
						num -= prob
				# since we did a spawn, reset the timer
				self.cooldown_timer = self.cooldown_length




class Projectile(Object):
	def __init__(self, x, y, char, name, color, mouseover, tags = set(), shooter = None, direction = 'right', speed = 1, momentum = 1000, damage = 1, bounces = False, attacksOnHit = True, passesThroughJumpables = False): 
		global MovementPhaseEvents
		self.shooter = shooter
		self.direction = direction
		self.speed = speed
		self.momentum = momentum
		self.damage = 1
		self.bounces = bounces
		self.attacksOnHit = attacksOnHit
		self.passesThroughJumpables = passesThroughJumpables
		tags.add('projectile')
		Object.__init__(self, x, y, char, name, color,  mouseover = mouseover, tags = tags)
		self.shooter = shooter			# the entity that shot this object (not the weapon used...)
		self.marked_for_destruction = False


	# start the projectile moving! moved this out of the initialization method because i think it was causing bugs
	def fire(self):
		(dx,dy) = getVectorFromDirectionAndSpeed (self.direction, self.speed)
		argset = (dx,dy)
		MovementPhaseEvents.append((self.projectile_move, argset))

	# very similar to object.attemptJump, but with some adjustments for the busy life of a projectile (TODO make adjustments)
	# TODO add code for passing through enemies and bouncing off walls (e.g. for grenades)
	def projectile_move(self, argset):
		(dx,dy) = argset
		blockedByWall = False
		nearestObstacle = None
		old_x = self.x
		old_y = self.y
		target_x = self.x + dx
		target_y = self.y + dy
		stop_x = target_x
		stop_y = target_y
		bounce_x = target_x
		bounce_y = target_y

	
		if not self.marked_for_destruction:	#hopefully this stops wierd bugs caused by trying to move a projectile after it's meant to have been destroyed
	
			print("nyoom AT (" + str(self.x) + "," + str(self.y) + ")")
			print(str(objectsArray[self.x][self.y]))	
	
			# for now this only works on straight line or diagonal jumps. If we start having knights move jumps or something, we'll have to rethink
			if (math.fabs(dx) == 0 or math.fabs(dy) == 0 or math.fabs(dx) == math.fabs(dy) and self.momentum > 0):
				xSign = getSign(dx)
				ySign = getSign(dy)
				i = 1;
				while i <= max(math.fabs(dx), math.fabs(dy)):
				
					# check the next space out
					space_x = self.x + i*xSign
					space_y = self.y + i*ySign
					if map[space_x][space_y].blocked:
						blockedByWall = True
						bounce_x = self.x + (i-1)*xSign
						bounce_y = self.y + (i-1)*ySign
						stop_x = self.x + i*xSign
						stop_y = self.y + i*ySign
						break
					else:
						# check for blocking, objects
						for obj in objectsArray[space_x][space_y]:
							# blocking objects are only a problem if they'renot jumpable, or they're where we're trying to get to
							if obj.blocks and (not (obj.jumpable and self.passesThroughJumpables) or i == max(math.fabs(dx), math.fabs(dy))):
								nearestObstacle = obj
								bounce_x = self.x + (i-1)*xSign
								bounce_y = self.y + (i-1)*ySign
								stop_x = self.x + i*xSign
								stop_y = self.y + i*ySign
								break
					# Hey I forgot to increase i!
					i += 1

			if stop_x != self.x or stop_y != self.y:
				# do the actual movement
				# TODO: update if thing is bouncing rather than exploding on impact?
				print("move " + str(self.x) + "," + str(self.y) + " -- " + str(stop_x) + "," + str(stop_y))
				self.x = stop_x
				self.y = stop_y
				if self not in objectsArray[stop_x][stop_y]:
					objectsArray[stop_x][stop_y].append(self)		# APPEND 1
				if self in objectsArray[old_x][old_y]:
					objectsArray[old_x][old_y].remove(self)


#				# in addition,  recalculate fov and report objects here if the player has just moved
#				if self is player:
#					argset = (final_x, final_y)
#					FinalPreDrawEvents.append((report_objects_here, argset))
#					fov_recompute = True

		


			# Now, if we didn't quite get where we wanted, report on what we jumped into
			if bounce_x != target_x or bounce_y != target_y:
				if self.attacksOnHit:
					#print ('boyoyoyoyoyom at(' + str(self.x) + ',' + str(self.y) + ')')
					self.destroyOnImpact()
				# TODO: implemnt bouncing if object is bouncey
	
			# Keep moving, if momentum allows it
			self.momentum = self.momentum - 1
			if self.momentum > 0:			
				(dx,dy) = getVectorFromDirectionAndSpeed (self.direction, self.speed)
				argset = (dx,dy)
				print(str(self.momentum))
				MovementPhaseEvents.append((self.projectile_move, argset))
			return

	def destroyOnImpact(self):
		self.momentum = 0	# stop infinite looping hopefully
		self.marked_for_destruction = True	# stop bullets wiedly hanging around hopefully?
		MiscPhaseEvents.append((self.destroy, argset))



		
class Bullet(Projectile):

	def __init__(self, x, y, tags = set(), shooter = None, direction = 'right', damage = 1) : 
		Projectile.__init__(self, x, y, '.', 'bullet', shooter.color, "WOOSH", tags, shooter, direction, speed = 1, momentum = 1000, damage = 1, bounces = False, attacksOnHit = True, passesThroughJumpables = False)



	def destroyOnImpact(self):
		global objectsArray, worldAttackList
		print("DESTROYING BULLET AT (" + str(self.x) + "," + str(self.y) + ")")
		print(str(objectsArray[self.x][self.y]))
		self.momentum = 0	# stop infinite looping hopefully
		self.marked_for_destruction = True	# stop bullets wiedly hanging around hopefully?
		MiscPhaseEvents.append((self.destroy, argset))
		attack = ModernAttack(x = self.x, y = self.y, color = self.color, attacker = self, damage = self.damage, direction = self.direction)		#very tempt hack hopefully
		objectsArray[attack.x][attack.y].append(attack)	
		worldAttackList.append(attack)
		attack.send_to_front()



# todo write actual code (in the Projectile class) for bouncing off walls.
# For now it's fine because we're just having droppable, non-moving grenades. Butt later there may be grenade launchers
class Grenade(Projectile):

	def __init__(self, x, y, tags = set(), shooter = None, direction = 'none', damage = 1, momentum = 1, timer = 5) : 
		global FinalPreDrawEvents
		if shooter is not None:
			color = shooter.color
		else:
			color = color_white
		Projectile.__init__(self, x, y, '.', 'grenade', color, "tick, tick, tick.", tags, shooter, direction, speed = 1, momentum = momentum, damage = 1, bounces = True, attacksOnHit = False, passesThroughJumpables = False)
		self.timer = timer
		argset = (self.x,self.y)
		
		# start a countdown
		FinalPreDrawEvents.append((self.countdown , argset))


	# count down to explodey time
	def countdown(self, args):	# FinalPreDrawEvents phase
		global MiscPhaseEvents, FinalPreDrawEvents
		if self.timer > 0:
			self.timer -= 1
			FinalPreDrawEvents.append((self.countdown , args))
		else:

			MiscPhaseEvents.append((self.explode, args))

	def explode(self, arg_set): # MiscPhaseEvents
		message('boom')
		message('The ' + self.name + ' explodes', Color_Boring_Combat)
		for x in range (self.x - 2, self.x+3):
			for y in range (self.y - 2, self.y + 3):
				if x >= 0  and x < MAP_WIDTH and y >= 0  and y < MAP_HEIGHT and ((x-self.x)*(x-self.x)) + ((y-self.y)*(y-self.y)) <= 4 and not map[x][y].blocked:
					fire_already_here = False
					for ob in objectsArray[x][y]:
						if ob.name == 'fire':
							fire_already_here = True
					if not fire_already_here:
						new_fire = Fire(x,y)
						objectsArray[x][y].append(new_fire)
						worldEntitiesList.append(new_fire)

						
		garbage_list.append(self)
			

class Water_Grenade(Grenade):

	def explode(self, arg_set): # MiscPhaseEvents
		message('boom')
		message('The ' + self.name + ' splooshes', Color_Boring_Combat)
		for x in range (self.x - 2, self.x+3):
			for y in range (self.y - 2, self.y + 3):
				if x >= 0  and x < MAP_WIDTH and y >= 0  and y < MAP_HEIGHT and ((x-self.x)*(x-self.x)) + ((y-self.y)*(y-self.y)) <= 4 and not map[x][y].blocked:
					water_already_here = False
					for ob in objectsArray[x][y]:
						if ob.name == 'water':
							water_already_here = True
					if not water_already_here:
						new_water = Object(x, y, 352, 'water', water_foreground_color, blocks = False, weapon = False, always_visible=True, mouseover = "A pool of water. Most people can't attack while swimming.")
						objectsArray[x][y].append(new_water)

						
		garbage_list.append(self)
			

####################################
#
#
#	NOW LEAVING OBJECT LAND
#
#
####################################















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

# Commenting out because we no longer want doors to be a component of objects, we want them to be an object themselves.
# Make way for the future, baby!
#class Door:
#	# update: increasing door lossness, because these things stick slightly too often
#	def __init__(self, horizontal, default_looseness = 4, easy_open = False):
#		self.horizontal = horizontal
#		self.default_looseness = default_looseness
#		self.looseness = default_looseness	# attempting to open a door has probability 2/loosness of being unsuccesful. loosness goes up with more attempts.
#		self.recently_rattled = False
#		self.easy_open = easy_open
#
#	def take_damage(self, damage):
#		#destroy the door!
#		#if damage > 0:
#		#	self.hp -= damage
#		#	#check for death. if there's a death function, call it
#		#	if self.hp <= 0:
#		#		function = self.death_function
#		#		if function is not None:
#		#			function(self.owner)
#
#		message('The door crashes down!', Color_Interesting_In_World)
#
#		door = self.owner
#		door.blocks = False
#		door.door = None
#		door.send_to_back()
#		garbage_list.append(door)
#		
#		#update the map to say that this square isn't blocked, and update the nav data
#		map[door.x][door.y].blocked = False
#		map[door.x][door.y].block_sight = False
#		
#		nav_data_changed = True
#		initialize_fov()		# this is ok, right? update the field of view stuff
#
#	def open(self):		#normal doors can't be closed after opening, Just one of those things
#		
#		if randint( 0, self.looseness-1) < 2 and not self.easy_open:		#opening unsuccesful
#			localMessage('The door rattles.', self.x, self.y, Color_Boring_In_World)
#			#message('The door rattles. Looseness = ' + str(self.looseness), libtcod.white)
#			self.looseness = self.looseness + 1		#increase chance of opening in future though
#			self.recently_rattled = True
#
#		else: 
#			localMessage('The door opens', self.x, self.y, Color_Boring_In_World)
#
#			door = self.owner
#			door.blocks = False
#			door.door = None
#			door.send_to_back()
#			garbage_list.append(door)
#			
#			#update the map to say that this square isn't blocked, and update the nav data
#			map[door.x][door.y].blocked = False
#			map[door.x][door.y].block_sight = False
#			
#			nav_data_changed = True
#			initialize_fov()		# this is ok, right? update the field of view stuff
#
##	def update(self):
##		#decrease looseness back to default, unless someone recently tried to open me
##		# UPDATE:cutting this. Why would you be so strict about door looseness?
##		if self.recently_rattled == False:
##			if self.looseness > self.default_looseness:
##				self.looseness = self.looseness - 1
##		self.recently_rattled = False



#Let's make a bunch of flowers that grow and then replenish your health or whatever, sure.
class Flower:
	def __init__(self, flower_type = 'tulip', state = 'seed', bloom_timer = DEFAULT_BLOOM_TIME, name = 'fruit', symbol = 291):
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
		global garbage_list
		if self.state == 'growing':
			self.state  = 'trampled'  # :(
			self.name = 'trampled ' + self.flower_type
			self.symbol = 'x'


			#self.send_to_back()
			#garbage_list.append(self.owner)

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
			localMessage(monster.name + ' healed by ' + self.name, monster.x, monster.y, Color_Interesting_In_World)
			self.symbol = 'x'
			









class Fighter:
	#combat-related properties and methods (monster, player, NPC).
	def __init__(self, hp, defense, power, death_function=None, attack_color = PLAYER_COLOR, faded_attack_color = PLAYER_COLOR, extra_strength = 0, recharge_rate = 1, bonus_max_charge = 0, jump_array = [], jump_recharge_time = DEFAULT_JUMP_RECHARGE_TIME, bleeds = True):
		self.max_hp = hp + 1		# new thing! every enemy can heal up to one extra.
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
	# trying out an exciting new 'energy drone'. Use energy to attack and to jump, energy gradually recharges, but getting hit reduces your energy semi-permanently, and you die if you lose more energy than you have.
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
		global player_just_jumped
		self.hp = self.hp - self.jump_recharge_time
		player_just_jumped = True
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


	def processDecisions(self):
		global MovementPhaseEvents, AttackPhaseEvents, sloMoAttack
		#do some stuff

		if self.decision is not None:
			if self.decision.move_decision: 
				argset = (self.decision.move_decision.dx, self.decision.move_decision.dy)
				MovementPhaseEvents.append((self.owner.modern_move, argset))
				
			if self.decision.jump_decision:
				argset = (self.decision.jump_decision.dx, self.decision.jump_decision.dy)
				MovementPhaseEvents.append((self.owner.modern_jump, argset))
			if self.decision.attack_decision:
				argset = (self.decision.attack_decision.attack_list, self.decision.attack_decision.force)
				AttackPhaseEvents.append((self.makeAttacks, argset))
				if fov_map.fov[self.owner.x,self.owner.y]:
					sloMoAttack = True;
			if self.decision.projectile_decision:
				argset = (self.decision.projectile_decision.projectile_list)
				AttackPhaseEvents.append((self.makeProjectiles, argset))
				#if fov_map.fov[self.owner.x,self.owner.y]:
				#	sloMoAttack = True;
			if self.decision.pickup_decision:
				argset = (self.decision.pickup_decision.items_to_pickup)
				MovementPhaseEvents.append((self.owner.attemptPickup, argset))
			if self.decision.buy_decision:
				argset = (self.decision.buy_decision.seller)
				PreliminaryEvents.append((self.attemptBuy, argset))


	# Commit to spending currency on an upgrade, and get it! (currently only works for player)
	def attemptBuy(self, args):
		global currency_count, upgrade_array
		(seller) = args
		upgrade_cost = seller.get_cost()

		if self.owner is player:
			currency_count = currency_count - upgrade_cost
			upgrade_array.append(seller.upgrade)
			message('You recieve the gift of '+ seller.upgrade.name +'!', Color_Stat_Info)
			# TODO: possibly put this in a separate method for shrines? but basically yeah you have taken the upgrade from the seller.
			seller.upgrade = None
		return


	def makeAttacks(self, args):	# Attack Phase
		global objectsArray, worldAttackList, worldEntitiesList, player_just_attacked
		(attack_list, force) = args
		# todo make this do all the attackey making stuff
		# Aha, this thing has not been done.
		for attack_object in attack_list:
			try:
				attack_data = attack_object.attack
				attack = ModernAttack(x = attack_object.x, y = attack_object.y, color = attack_object.color, attacker = attack_data.attacker, damage = attack_data.damage, direction = attack_data.direction, force = force)		#very tempt hack hopefully
				objectsArray[attack.x][attack.y].append(attack)	
				worldAttackList.append(attack)
				attack.send_to_front()
			except IndexError:		#todo: check that this is the right thing to catch...
				print('')	

		
		if self.owner == player:
			player_just_attacked = True
			# temp thing: let's also shoot a bullet
			#new_bullet = Bullet(player.x + 1, player.y, shooter =  player, direction = 'right', damage = 1)
			#objectsArray[player.x + 1][player.y].append(new_bullet)

			# if player attacked, check to see if all attacks were on target	
			#message("doin an attack")
			checkForPlayerAttackAccuracy()
		return


	def makeProjectiles(self, args):	# Attack Phase
		global objectsArray, worldAttackList, worldEntitiesList, player_just_attacked
		(projectile_list) = args
		# todo make this do all the attackey making stuff
		# Aha, this thing has not been done.
		for projectile in projectile_list:

			#print("tryna make projectile at (" + str(projectile.x) + "," + str(projectile.y) + ")") 
			try:
				#attack_data = attack_object.attack
				#attack = ModernAttack(x = attack_object.x, y = attack_object.y, color = attack_object.color, attacker = attack_data.attacker, damage = attack_data.damage)		#very tempt hack hopefully
				objectsArray[projectile.x][projectile.y].append(projectile)	
				#worldAttackList.append(attack)		# TODO: should we add theprojectile to world entities list?
				projectile.send_to_front()
				projectile.fire()
			except IndexError:		#todo: check that this is the right thing to catch...
				print('')	

		
		if self.owner == player:
			player_just_attacked = True
			# if player attacked, check to see if all attacks were on target	
			#message("doin a shoot")
			#checkForPlayerAttackAccuracy()
		return


# Something that can spot the player and raise/lower the alarm
class Alarmer:
	def __init__(self, alarm_time = 4, pre_alarm_time = 1, alarm_value = 2, dead_alarm_value = 1, idle_color = color_alarmer_idle, suspicious_color = color_alarmer_suspicious, alarmed_color = color_alarmer_alarmed, idle_char = 320, suspicious_char = 321,  alarmed_char = 322,  assoc_fighter = None):
		self.status = 'idle'			# 5 possible statuses: inert, pre-suspicious, suspicious, raising-alarm, alarm-raised
		self.alarm_time = alarm_time		# How long you have to spot intruder for before raising alarm
		self.pre_alarm_time = pre_alarm_time	# Delayed reaction time before realizing you've spotted an intruder
		self.alarm_value = alarm_value		# How much to raise the alar by when you know 
		self.dead_alarm_value = dead_alarm_value	# How much of the alarm stays behind after you are destroyed.
		self.idle_color = idle_color
		self.suspicious_color = suspicious_color
		self.alarmed_color = alarmed_color
		self.idle_char = idle_char
		self.suspicious_char = suspicious_char
		self.alarmed_char = alarmed_char
		self.alarm_countdown = alarm_time
		self.pre_alarm_countdown = pre_alarm_time
		self.prev_suspicious = False
		self.assoc_fighter = assoc_fighter
		self.listeners =[]	# a set of nearby objects listening to this alarmer
		self.listeners_set = False
		self.alarmer_range = ALARMER_RANGE

	def update(self, intruder_spotted):

		# First things first, get a set of listeners if that hasn't been done already.
		if not self.listeners_set:
			
			for x in range(self.owner.x - self.alarmer_range, self.owner.x + self.alarmer_range + 1):   # The +1 is because range(a,b) does everything from a to b-1 inclusive
				for y in range(self.owner.y - self.alarmer_range, self.owner.y + self.alarmer_range + 1):
					if x >= 0  and x < MAP_WIDTH and y >= 0 and y < MAP_HEIGHT:
						for ob in objectsArray[x][y]:  
							if 'listener' in ob.tags:
								self.listeners.append(ob)
			self.listeners_set = True

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
					self.assoc_fighter.max_hp += 5#6
					self.assoc_fighter.heal(5)	#6
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


		# IN any case, if the alarm is being raised, look for listeners to tell about it!
		if self.status == 'alarm-raised':
			for listener in self.listeners:
				listener.notify()
		
	def get_hit(self):		# If you get hit, raise the alarm if you haven't already! 
		if self.status != 'alarm-raised':
			self.status = 'raising-alarm'



class Decision:
	def __init__(self, move_decision=None, attack_decision=None, projectile_decision = None, jump_decision = None, pickup_decision = None, buy_decision = None):
		self.move_decision=move_decision
		if move_decision is not None:
			self.move_decision.owner = self
		self.attack_decision=attack_decision
		if attack_decision is not None:
			self.attack_decision.owner = self
		self.projectile_decision=projectile_decision
		if projectile_decision is not None:
			self.projectile_decision.owner = self
		self.jump_decision=jump_decision
		if jump_decision is not None:
			self.jump_decision.owner = self
		self.pickup_decision=pickup_decision		# pickup_decision is just a boolean I think? Update: Nuh-uh
		if  pickup_decision is not None:
			self.pickup_decision.owner = self
		self.buy_decision=buy_decision
		if buy_decision is not None:
			self.buy_decision.owner = self

class Move_Decision:
	def __init__(self,dx,dy):
		self.dx = dx
		self.dy = dy


class Jump_Decision:
	def __init__(self,dx,dy):
		self.dx = dx
		self.dy = dy


class Pickup_Decision:
	def __init__(self,items_to_pickup):
		self.items_to_pickup = items_to_pickup


# for now, Buy_Decision only really handles cases where the seller has just one item for one price.
class Buy_Decision:
	def __init__(self, seller):
		self.seller= seller



class Attack_Decision:
	def __init__(self, attack_list, force):
		self.attack_list = attack_list
		self.force = force


class Projectile_Decision:
	def __init__(self, projectile_list):
		self.projectile_list = projectile_list



class BasicMonster:
	global nearest_center_to_player, objectsArray

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
		if self.guard_duty:
			self.state = 'guard-duty'
		self.target_x = player.x
		self.target_y = player.y
		self.scared_of_water = False
		phobia_choice = randint(0,1)
		if phobia_choice == 1:
			self.scared_of_water = True


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
			if self.state == 'hungry':
				self.pursueFood(monster, decider)
			elif self.state == 'head-towards-room' or self.state == 'wander-aimlessly':

 				self.moveTowardsRoom(monster, decider)							

			# Now do things for the other cases!
			elif self.state == 'pursue-visible-target':

				self.engagePlayer(monster, decider)

			# I *think* that if state is 'guard-guty', the enemy just won't do anything


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

		# new thing: see if there is a plant here
		plant_here = False
		for obj in objectsArray[monster.x][monster.y]:
			if obj.plant is not None:
				plant_here = True
				break
		# bit of a cheat here - make it so enemies only pick up fruit when you can see them.
		if plant_here and monster.fighter.hp < monster.fighter.max_hp and fov_map.fov[monster.x, monster.y]:
			self.state = 'hungry'
		elif fov_map.fov[monster.x, monster.y]:
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
		((dx,dy), return_message) =  next_step_based_on_target(monster.x, monster.y, target_center = self.target_room, aiming_for_center = True, prioritise_visible = False, prioritise_straight_lines = True, rook_moves = False, request_message = True, avoid_water = self.scared_of_water)

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
			decider.decision = Decision(attack_decision = Attack_Decision(attack_list=chosen_attack_list, force=self.weapon.force))

		# otherwise, walk towards the player if possible.
		elif monster.distance_to(player) > 1: 	#cutting this condition makes enemies move around player when they can't attack. Might be worth considering for smarter : harder enemies.
			(dx,dy) = next_step_based_on_target(monster.x, monster.y, target_x = player.x, target_y = player.y, aiming_for_center = False, prioritise_visible = True, prioritise_straight_lines = True, rook_moves = False, return_message = None, avoid_water = self.scared_of_water)
			decider.decision = Decision(move_decision=Move_Decision(dx,dy))
	
	# Part of Step 3: do the things you can do when you've decided you want food!
	# For now, this just consists of picking up the fruit at your feet if there is one, but this may change later
	def pursueFood(self, monster, decider):
		plant_here = False
		chosen_plant = None
		for obj in objectsArray[monster.x][monster.y]:
			if obj.plant is not None:
				plant_here = True
				chosen_plant = obj
				break
		if plant_here:
			decider.decision = Decision(pickup_decision=Pickup_Decision([obj]))
			




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





# Just like BasicMonster, except that moving towards the player happens with... 1 in 2 chance? when distance 1 away
class Cautious_AI(BasicMonster):

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
			decider.decision = Decision(attack_decision = Attack_Decision(attack_list=chosen_attack_list, force=self.weapon.force))

		# otherwise, walk towards the player if possible.
		elif monster.distance_to(player) > 2: 	
			(dx,dy) = next_step_based_on_target(monster.x, monster.y, target_x = player.x, target_y = player.y, aiming_for_center = False, prioritise_visible = True, prioritise_straight_lines = True, rook_moves = False, return_message = None, avoid_water = self.scared_of_water)
			decider.decision = Decision(move_decision=Move_Decision(dx,dy))

		elif monster.distance_to(player) > 1 and randint(0,1) == 1:	# This is where the caution comes in!
			(dx,dy) = next_step_based_on_target(monster.x, monster.y, target_x = player.x, target_y = player.y, aiming_for_center = False, prioritise_visible = True, prioritise_straight_lines = True, rook_moves = False, return_message = None, avoid_water = self.scared_of_water)
			decider.decision = Decision(move_decision=Move_Decision(dx,dy))



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
			decider.decision = Decision(attack_decision = Attack_Decision(attack_list=chosen_attack_list, force=self.weapon.force))

		# otherwise, walk towards the player if possible.
		elif monster.distance_to(player) > 1: 	
			
			#take list of possible good moves, then prioritise diagonal ones
			move_shortlist = next_step_based_on_target(monster.x, monster.y, target_x = player.x, target_y = player.y, aiming_for_center = False, prioritise_visible = True, prioritise_straight_lines = False, rook_moves = False, return_message = None, request_shortlist = True,  avoid_water = self.scared_of_water)
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
					opt_diagonality = temp_diagonality		#hey did I just forget to add this before?
				elif temp_diagonality == opt_diagonality:
					shorterlist.append((dx,dy))
			if len(shorterlist) > 0 :
				move_shortlist = shorterlist
			try:
				(dx,dy) = random.choice(tuple(move_shortlist))
			except IndexError:
				print('oh no index error!!' + str(len(move_shortlist)) + ', ' + str(move_shortlist))

			decider.decision = Decision(move_decision=Move_Decision(dx,dy))


#Crane_AI acts like BasicMonster, but (a) moves slower, and (b) never moves to be adjacent to the player, so they only end up attacking if the player approaches them (for range 1 weapons anyway)
class Crane_AI(BasicMonster):

	def __init__(self, weapon, guard_duty  = False, attack_dist = 1, state = 'wander-aimlessly'):
		BasicMonster.__init__(self, weapon, guard_duty, attack_dist, state)
		# cutting the 'pausing' idea for now, at least for this enemy
		#self.pausing = True
		self.pausing = False


	# Crane overall acts quite similar to basicMonster, but slower - movement only happens every other turn.
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
			if self.state == 'hungry':
				self.pursueFood(monster, decider)
			elif self.state == 'head-towards-room' or self.state == 'wander-aimlessly':
				if not self.pausing:

 					self.moveTowardsRoom(monster, decider)	

				# cutting the 'pausing' idea for now, at least for this enemy
				#self.pausing = not self.pausing					

			# Now do things for the other cases!
			elif self.state == 'pursue-visible-target':

				self.engagePlayer(monster, decider)

			# I *think* that if state is 'guard-guty', the enemy just won't do anything


			# Update various cooldowns and counters and such
			if self.weapon:
				self.weapon.recharge()
			if self.ally_in_the_way_o_meter > 0:
				self.ally_in_the_way_o_meter = self.ally_in_the_way_o_meter - 1
			if self.blocked_by_door_o_meter > 0:
				self.blocked_by_door_o_meter = self.blocked_by_door_o_meter - 1
		if self.stunned_time > 0:
			self.stunned_time = self.stunned_time - 1


	# Crane avoids moving directlynext to player, and moves slower, but otherwise acts like basicMonster			
	def engagePlayer(self, monster, decider):

		
		xdiff = player.x - monster.x
		ydiff = player.y - monster.y
		# First off, see if you can attack the player from where you are
		attackList = self.possibleAttackList(monster, decider)

		# Now we know if attacking is possible, and have built up a list of attacks:
		# if there are some attacks we could do, pick one
		if len(attackList) > 0:
			command_choice = random.choice(tuple(attackList))	#returns arbitrary element from candidate_set
			abstract_attack_data = self.weapon.do_attack(command_choice)
			# now do the attack! or, you know, decide to
			chosen_attack_list = process_abstract_attack_data(monster.x,monster.y, abstract_attack_data, monster)	
			decider.decision = Decision(attack_decision = Attack_Decision(attack_list=chosen_attack_list, force=self.weapon.force))

		# Crane only approaches player if to do so wouldn't bring them next to the player. Also, slowly?
		# tried a bunch of modifications to this behaviour to make them still a threat if left completely alone
		# elif math.fabs(xdiff) > 2 or math.fabs(ydiff) > 2 :
		# elif math.fabs(xdiff) > 2 or math.fabs(ydiff) > 2 or (math.fabs(xdiff) == math.fabs(ydiff)):
		elif (math.fabs(xdiff) > 2 or math.fabs(ydiff) > 2 or (randint(0,2) == 0)) and (max(math.fabs(xdiff),math.fabs(ydiff)) > 1 ):
			# cutting the 'pausing' idea for now, at least for this enemy.
			if not self.pausing:
				(dx,dy) = next_step_based_on_target(monster.x, monster.y, target_x = player.x, target_y = player.y, aiming_for_center = False, prioritise_visible = True, prioritise_straight_lines = True, rook_moves = False, return_message = None,  avoid_water = self.scared_of_water)
				decider.decision = Decision(move_decision=Move_Decision(dx,dy))
#				self.pausing = True
#			else:
#				self.pausing = False		
			

#Like the Boman AI, but more so.Tryand move diagonally, but AVOID GETTING NON-DIAGONALLY ADJACENT TO PLAYER. Or at least move if that happens.
class Dove_AI(BasicMonster):
	
	def engagePlayer(self, monster, decider):
		# First off, see if you can attack the player from where you are
		attackList = self.possibleAttackList(monster, decider)



		xdiff = player.x - monster.x
		ydiff = player.y - monster.y

		# Now we know if attacking is possible, and have built up a list of attacks:
		# if there are some attacks we could do, pick one
		if len(attackList) > 0:
			command_choice = random.choice(tuple(attackList))	#returns arbitrary element from candidate_set
			abstract_attack_data = self.weapon.do_attack(command_choice)
			# now do the attack! or, you know, decide to
			chosen_attack_list = process_abstract_attack_data(monster.x,monster.y, abstract_attack_data, monster)	
			decider.decision = Decision(attack_decision = Attack_Decision(attack_list=chosen_attack_list, force=self.weapon.force))




		# otherwise, walk towards the player if possible.
		#elif monster.distance_to(player) > 2: 	
		elif math.fabs(xdiff) > 2 or math.fabs(ydiff) > 2:
			
			#take list of possible good moves, then prioritise diagonal ones
			move_shortlist = next_step_based_on_target(monster.x, monster.y, target_x = player.x, target_y = player.y, aiming_for_center = False, prioritise_visible = True, prioritise_straight_lines = False, rook_moves = False, return_message = None, request_shortlist = True,  avoid_water = self.scared_of_water)
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
					opt_diagonality = temp_diagonality		#hey did I just forget to add this before?
				elif temp_diagonality == opt_diagonality:
					shorterlist.append((dx,dy))
			if len(shorterlist) > 0 :
				move_shortlist = shorterlist
			try:
				(dx,dy) = random.choice(tuple(move_shortlist))
			except IndexError:
				print('oh no index error!!' + str(len(move_shortlist)) + ', ' + str(move_shortlist))

			decider.decision = Decision(move_decision=Move_Decision(dx,dy))

		else:	#if close to player, movement depends on exact positions. but bascially we're trying to line up a diagonal attack.		# movement will be biased towards the entry in this table corresponding to your current position relative to player


			clockwise_prefs =      [[( 0, 0),( 0, 1),(-1, 1),( 0, 1),( 0, 0)],
						[( 1, 0),( 0, 0),(-1, 0),( 0, 0),(-1, 0)],
						[( 1, 1),( 0, 1),( 0, 0),( 0,-1),(-1,-1)],
						[( 1, 0),( 0, 0),( 1, 0),( 0, 0),(-1, 0)],
						[( 0, 0),( 0,-1),( 1,-1),( 0,-1),( 0, 0)]]

			anticlockwise_prefs =  [[( 0, 0),( 0, 1),( 1, 1),( 0, 1),( 0, 0)],
						[( 1, 0),( 0, 0),( 1, 0),( 0, 0),(-1, 0)],
						[( 1,-1),( 0,-1),( 0, 0),( 0, 1),(-1, 1)],
						[( 1, 0),( 0, 0),(-1, 0),( 0, 0),(-1, 0)],
						[( 0, 0),( 0,-1),(-1,-1),( 0,-1),( 0, 0)]]
			movement_preferences = clockwise_prefs
			secondary_preferences = anticlockwise_prefs
			# commenting out because whatever, let the enemies that have a bias. similar reasoning to making rooks less random.
			#num =  randint( 0, 1)
			#if num == 0:
			#	movement_preferences = anticlockwise_prefs
			#	secondary_preferences = clockwise_prefs

			(dx,dy) = movement_preferences[-ydiff+2][-xdiff+2]
			#print("DOVE: based on ydiff " + str(ydiff) + " and xdiff " + str(xdiff) + ", I want to do (" + str(dx) + "," + str(dy) + ")")
			#print "distance (" + str(xdiff) + "," + str(ydiff) + ") leading to movement (" + str(dx) + "," + str(dy) + ")."
			if not is_blocked(monster.x + dx, monster.y + dy):
			#	print "huh"
				decider.decision = Decision(move_decision=Move_Decision(dx,dy))
			else:
				(dx,dy) = secondary_preferences[-ydiff+2][-xdiff+2]
				if not is_blocked(monster.x + dx, monster.y + dy):
				#	print "huh"
					decider.decision = Decision(move_decision=Move_Decision(dx,dy))
				else:	# for now, just run towards player I guess
					#print("DOVEBLOCKD")
					(dx,dy) = Move_Towards_Visible_Player(monster.x, monster.y)
					decider.decision = Decision(move_decision=Move_Decision(dx,dy))



# Tries to get in line with the player (either horizontally, vertically or diagonally?) and then shoot at them, mostly regardless of distance
# (will probably have some max distance of like 10 or 15 just to avoid too much shooting from offscreen...)
class Gunslinger_AI(BasicMonster):

	# Part of Step 3: do the things you can do when you see the player!
	def engagePlayer(self, monster, decider):
		# First off, see if you can attack the player from where you are
		# (which happens if  you are in a direct line with the player, with no blocking objects in between)
		attackList = self.possibleAttackList(monster, decider)


		# figure out the vector that the player is from you
		dist_x = self.target_x  - monster.x
		dist_y = self.target_y  - monster.y
		xSign = getSign(dist_x)
		ySign = getSign(dist_y)

		# Now we know if attacking is possible, and have built up a list of attacks:
		# if there are some attacks we could do, pick one
		if len(attackList) > 0:
			command_choice = random.choice(tuple(attackList))	#returns arbitrary element from candidate_set
			abstract_projectile_data = self.weapon.do_projectile_attack(command_choice)
			# now do the attack! or, you know, decide to
			chosen_projectile_list = process_abstract_projectile_data(monster.x,monster.y, abstract_projectile_data, monster)	
			decider.decision = Decision(projectile_decision = Projectile_Decision(projectile_list=chosen_projectile_list))

		# if we can't attack bcause we're not in line, try and get in line
		elif dist_x != 0 and dist_y != 0 and math.fabs(dist_x) != math.fabs(dist_y):

			# either try and reduce y distance or x distance. If one is not possible, try to other
			if not fov_map.fov[monster.x + xSign, monster.y] or is_blocked(monster.x + xSign, monster.y):
				# try to reduce y distance
				decider.decision = Decision(move_decision=Move_Decision(0, ySign))
			elif not fov_map.fov[monster.x, monster.y +ySign] or is_blocked(monster.x, monster.y +ySign):
				# try to reduce x distance
				decider.decision = Decision(move_decision=Move_Decision(xSign, 0))

			# otherwise, try and line up either the horizontal/vertical shot or the diagonal shot, whichever is nearest
			elif math.fabs(dist_x) < math.fabs(dist_y):
				# case where the horizontal shot is easiest to line up
				if math.fabs(dist_x) <=  math.fabs(dist_y) - math.fabs(dist_x):
					# try to reduce x distance
					decider.decision = Decision(move_decision=Move_Decision(xSign,0))
				# case where the diagonal shot is easier to line up
				else:
					# try to reduce y distance
					decider.decision = Decision(move_decision=Move_Decision(0, ySign))
			else:
				# case where the vertical shot is easiest to line up
				if math.fabs(dist_y) <=  math.fabs(dist_x) - math.fabs(dist_y):
					# try to reduce y distance
					decider.decision = Decision(move_decision=Move_Decision(0, ySign))
				# case where the diagonal shot is easier to line up
				else:
					# try to reduce x distance
					decider.decision = Decision(move_decision=Move_Decision(xSign,0))
					


		# otherwise (there's something in the way), walk towards the player if possible.
		elif monster.distance_to(player) > 2: 	#cutting this condition makes enemies move around player when they can't attack. Might be worth considering for smarter : harder enemies.
			(dx,dy) = next_step_based_on_target(monster.x, monster.y, target_x = player.x, target_y = player.y, aiming_for_center = False, prioritise_visible = True,  return_message = None, avoid_water = self.scared_of_water)
			decider.decision = Decision(move_decision=Move_Decision(dx,dy))



	# Returns a list of possible attacks that might hit the player 
	# (this basically being, the attack that points in the direction of the player, if you are in line with the player and there's nothing in the way)
	def possibleAttackList(self, monster, decider):
		attackList = []
		# Is the player alive and do you have enough 'weapon charge'?
		# AND are you not in water?
		if player.fighter.hp >= 0 and self.weapon.current_charge >= self.weapon.default_usage and not monster.fighter.in_water:
			# figure out the vector that the player is from you
			dist_x = self.target_x  - monster.x
			dist_y = self.target_y  - monster.y

			# can only attack if the target is in a direct vertical, horizontal or diagonal line
			if (dist_x == 0 and dist_y != 0) or (dist_y == 0 and dist_x != 0) or math.fabs(dist_x) == math.fabs(dist_y):

				# Now check to see if there are any obstacles in the way
				# (code here is similar to that used in attemptJump, except we don't do a check on the target space.
				# Should be agnostic with regard to direction of target (as long as it's in a straight line)

				xSign = getSign(dist_x)
				ySign = getSign(dist_y)
				i = 1;
				blocked = False
				while i < max(math.fabs(dist_x), math.fabs(dist_y)):
				
					# check the next space out
					space_x = monster.x + i*xSign
					space_y = monster.y + i*ySign
					if map[space_x][space_y].blocked:
						blocked = True
						break
					else:
						# check for blocking, objects
						for obj in objectsArray[space_x][space_y]:
							# don't make special allowances for jumpable objects - bullets don't care
							if obj.blocks: #and (not obj.jumpable or i == max(math.fabs(dx), math.fabs(dy))):
								blocked = True
								break
					# Hey I forgot to increase i!
					i += 1

				# The above should have checked that there's nothing in the way that will block the bullet
				if not blocked:
					# now that we are in line and that  there is nothing in the way, just have to figure out which line we are in
					if dist_x == 0 and dist_y < 0:
						attackList.append(ATTCKUP)
					if dist_x == 0 and dist_y > 0:
						attackList.append(ATTCKDOWN)
					if dist_x < 0 and dist_y == 0:
						attackList.append(ATTCKLEFT)
					if dist_x > 0 and dist_y == 0:
						attackList.append(ATTCKRIGHT)
	
					if dist_x < 0 and dist_y < 0:
						attackList.append(ATTCKUPLEFT)
					if dist_x > 0 and dist_y < 0:
						attackList.append(ATTCKUPRIGHT)
					if dist_x < 0 and dist_y > 0:
						attackList.append(ATTCKDOWNLEFT)
					if dist_x > 0 and dist_y > 0:
						attackList.append(ATTCKDOWNRIGHT)

		#print (str(attackList))
		return attackList


# Like the basic AI, but the eagle attacks towards the player when standing next to them, even though the player isn't in range for that attack
class Eagle_AI(BasicMonster):

	# returns what possible attacks you can make that would hit the player.
	# This is a little different for the eagle - attack in direction of player if they are right next to you, even though your weapon doesn't hit like that.
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

			# extra thing for eagle - add attacks toward adjacent square if player is there
			if dist_x == 1 and dist_y == 1:
				attackList.append(ATTCKDOWNRIGHT)
			elif dist_x == 0 and dist_y == 1:
				attackList.append(ATTCKDOWN)
			elif dist_x == -1 and dist_y == 1:
				attackList.append(ATTCKDOWNLEFT)
			elif dist_x == -1 and dist_y == 0:
				attackList.append(ATTCKLEFT)
			elif dist_x == -1 and dist_y == -1:
				attackList.append(ATTCKUPLEFT)
			elif dist_x == 0 and dist_y == -1:
				attackList.append(ATTCKUP)
			elif dist_x == 1 and dist_y == -1:
				attackList.append(ATTCKUPRIGHT)
			elif dist_x == 1 and dist_y == 0:
				attackList.append(ATTCKRIGHT)

		return attackList



#Greenhorn_AI basically acts like Basic AI, but 1. doesn't pick uo food, and 2. only attacks every other turn (which makes a difference when there's swords)
class Greenhorn_AI(BasicMonster):

	def __init__(self, weapon, guard_duty  = False, attack_dist = 1, state = 'wander-aimlessly'):
		BasicMonster.__init__(self, weapon, guard_duty, attack_dist, state)
		# cutting the 'pausing' idea for now, at least for this enemy
		#self.pausing = True
		self.just_attacked = False

	# Deciding step is just like BasicMonster, except we ignore food
	def decideState(self, monster):
		# Currently planned possible states:
		# 'guard-duty'			Stay where you are till something comes along
		# 'head-towards-room'		Try and walk towards a target room (generally the one you think player is in)
		# 'wander-aimlessly'		Pick adjacent rooms at random to walk into, preferably avoiding the previous room
		# 'pursue-visible-target'	When the player is near you, go towards them! Includes attacking?	
		# 'flee-visible-danger'		Run away from a thing you can see (the player, when you're scared of them?)
	
		#keeping it pretty simple for now... pursue the player if you see them
		#if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

		# new thing: see if there is a plant here
		plant_here = False
		for obj in objectsArray[monster.x][monster.y]:
			if obj.plant is not None:
				plant_here = True
				break
		# bit of a cheat here - make it so enemies only pick up fruit when you can see them.
		#if plant_here and monster.fighter.hp < monster.fighter.max_hp and fov_map.fov[monster.x, monster.y]:
		#	self.state = 'hungry'
		# el
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
			

	# Engaging player is same as BasicMonster, except you can't attack two turns in a row (even if the weapon would allow it)
	def engagePlayer(self, monster, decider):
		# First off, see if you can attack the player from where you are
		attackList = self.possibleAttackList(monster, decider)

		# Now we know if attacking is possible, and have built up a list of attacks:
		# if there are some attacks we could do, pick one
		if len(attackList) > 0 and self.just_attacked == False:
			command_choice = random.choice(tuple(attackList))	#returns arbitrary element from candidate_set
			abstract_attack_data = self.weapon.do_attack(command_choice)
			# now do the attack! or, you know, decide to
			chosen_attack_list = process_abstract_attack_data(monster.x,monster.y, abstract_attack_data, monster)	
			decider.decision = Decision(attack_decision = Attack_Decision(attack_list=chosen_attack_list, force=self.weapon.force))
			self.just_attacked = True

		# otherwise, walk towards the player if possible.
		elif monster.distance_to(player) > 1: 	#cutting this condition makes enemies move around player when they can't attack. Might be worth considering for smarter : harder enemies.
			(dx,dy) = next_step_based_on_target(monster.x, monster.y, target_x = player.x, target_y = player.y, aiming_for_center = False, prioritise_visible = True, prioritise_straight_lines = True, rook_moves = False, return_message = None,  avoid_water = self.scared_of_water)
			decider.decision = Decision(move_decision=Move_Decision(dx,dy))
			self.just_attacked = False

		else:
			self.just_attacked = False
			

# Like a greenhorn with dodgy wiring, sometimes forgets to love or attack
class Greenhorn_Erratic_AI(Greenhorn_AI):

	# Engaging player is same as BasicMonster, except you can't attack two turns in a row (even if the weapon would allow it)
	def engagePlayer(self, monster, decider):
		# First off, see if you can attack the player from where you are
		attackList = self.possibleAttackList(monster, decider)

		# Now we know if attacking is possible, and have built up a list of attacks:
		# if there are some attacks we could do, pick one
		if len(attackList) > 0 and self.just_attacked == False and randint(0,2) != 0:	# Add 1 in 3 chance of failure
			command_choice = random.choice(tuple(attackList))	#returns arbitrary element from candidate_set
			abstract_attack_data = self.weapon.do_attack(command_choice)
			# now do the attack! or, you know, decide to
			chosen_attack_list = process_abstract_attack_data(monster.x,monster.y, abstract_attack_data, monster)	
			decider.decision = Decision(attack_decision = Attack_Decision(attack_list=chosen_attack_list, force=self.weapon.force))
			self.just_attacked = True

		# otherwise, walk towards the player if possible.
		elif monster.distance_to(player) > 2 or (monster.distance_to(player) > 1 and randint(0,2) == 0): 	#Add 2 in 3 chance of failure at a certain distance
			(dx,dy) = next_step_based_on_target(monster.x, monster.y, target_x = player.x, target_y = player.y, aiming_for_center = False, prioritise_visible = True, prioritise_straight_lines = True, rook_moves = False, return_message = None,  avoid_water = self.scared_of_water)
			decider.decision = Decision(move_decision=Move_Decision(dx,dy))
			self.just_attacked = False

		else:
			self.just_attacked = False


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
				#if near to the player, and I have charge, and am not in water, then attack!
				if self.weapon.current_charge >= self.weapon.default_usage and not monster.fighter.in_water:
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
						decider.decision = Decision(attack_decision = Attack_Decision(attack_list=temp_attack_list, force=self.weapon.force))


#	
#				(dx,dy) = next_step_based_on_target(monster.x, monster.y, target_x = player.x, target_y = player.y, aiming_for_center = False, prioritise_visible = True, prioritise_straight_lines = True, rook_moves = False, return_message = None)
#				decider.decision = Decision(move_decision=Move_Decision(dx,dy))


# "Ninja crane" approaches the player, but at distance 2 they don't come any closer, just attack in the player's direction if able.
class Ninja_Crane_AI(BasicMonster):


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
				# Do one of these attacks, based on where player is
				# For now, I'm happy to make the crane biased toward horizontal attacks
				attack_array = [[oAo,oWo,oWo,oWo,oDo],
						[oAo,oAo,oWo,oDo,oDo],
						[oAo,oAo, 0 ,oDo,oDo],
						[oAo,oAo,oXo,oDo,oDo],
						[oAo,oXo,oXo,oXo,oDo]]
				attack_command = attack_array[ydiff+2][xdiff+2]
				# alt pattern you might want to do for reasons of symmetry?


				#carry out attack
				if attack_command != 0:
					abstract_attack_data = self.weapon.do_attack(attack_command)
						
				if abstract_attack_data is not None:
					temp_attack_list = process_abstract_attack_data(monster.x,monster.y, abstract_attack_data, monster)	
					decider.decision = Decision(attack_decision = Attack_Decision(attack_list=temp_attack_list, force=self.weapon.force))

		# otherwise, walk towards the player if possible.
		else:

			(dx,dy) = next_step_based_on_target(monster.x, monster.y, target_x = player.x, target_y = player.y, aiming_for_center = False, prioritise_visible = True, prioritise_straight_lines = True, rook_moves = False, return_message = None,   avoid_water = self.scared_of_water)
			decider.decision = Decision(move_decision=Move_Decision(dx,dy))

		
	
	
class Tridentor_AI(BasicMonster):

	def __init__(self, weapon, guard_duty  = False, attack_dist = 1, state = 'wander-aimlessly'):
		BasicMonster.__init__(self, weapon, guard_duty, attack_dist, state)
		# cutting the 'pausing' idea for now, at least for this enemy
		#self.pausing = True
		self.scared_of_water = False


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
					decider.decision = Decision(attack_decision = Attack_Decision(attack_list=temp_attack_list, force=self.weapon.force))

			# can't attack but the player is next to you? then step back
			# commented out for now - too tricksy / annoying for what is basically meant to be an upgrade to the basic mook
			elif xdiffabs <=1 and ydiffabs <= 1:
			
				(dx,dy) = Run_Away_From_Visible_Player(monster.x, monster.y)
				decider.decision = Decision(move_decision=Move_Decision(dx,dy))

			# otherwise, close the distance to player 
			elif monster.distance_to(player) > 1: 
				(dx,dy) = next_step_based_on_target(monster.x, monster.y, target_x = player.x, target_y = player.y, aiming_for_center = False, prioritise_visible = True, prioritise_straight_lines = True, rook_moves = False, return_message = None,  avoid_water = self.scared_of_water)
				decider.decision = Decision(move_decision=Move_Decision(dx,dy))
		# otherwise, walk towards the player if possible.
		else:

			(dx,dy) = next_step_based_on_target(monster.x, monster.y, target_x = player.x, target_y = player.y, aiming_for_center = False, prioritise_visible = True, prioritise_straight_lines = True, rook_moves = False, return_message = None, avoid_water = self.scared_of_water)
			decider.decision = Decision(move_decision=Move_Decision(dx,dy))
	


#  A lovely faerie that wanders around and would never harm anyone! and, eventually, will hopefully give you a  bonus if you can catch it
class Faerie_AI(BasicMonster):

	# faeries aren't scared of water. They can fly!
	def __init__(self, weapon, guard_duty  = False, attack_dist = 1, state = 'wander-aimlessly'):
		BasicMonster.__init__(self, weapon, guard_duty, attack_dist, state)
		# cutting the 'pausing' idea for now, at least for this enemy
		#self.pausing = True
		self.scared_of_water = False

	#Basically a faerie always wonders round aimlessly and never bothers about any of that "engage the player" stuff
	def decideState(self, monster):
		self.state = 'wander-aimlessly'
		self.previous_room = nearest_points_array[player.x][player.y] 	

	# movement is basically the same as for BasicMonster, except hopefully we can ignore doors? maybe?
	def moveTowardsRoom(self, monster, decider):
		# Choose an option that gets you closest to where you want to go
		((dx,dy), return_message) =  next_step_based_on_target(monster.x, monster.y, target_center = self.target_room, aiming_for_center = True, prioritise_visible = False, prioritise_straight_lines = True, rook_moves = False, request_message = True, avoid_water = self.scared_of_water)

		# Move if possible
		block = is_blocked(monster.x+dx, monster.y+dy, care_about_doors = False,  care_about_fighters = True) 
		if block == False: 
			decider.decision = Decision(move_decision=Move_Decision(dx,dy))

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
							decider.decision = Decision(attack_decision = Attack_Decision(attack_list=temp_attack_list, force=self.weapon.force))
				
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
							decider.decision = Decision(attack_decision = Attack_Decision(attack_list=temp_attack_list, force=self.weapon.force))
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
							decider.decision = Decision(attack_decision = Attack_Decision(attack_list=temp_attack_list, force=self.weapon.force))
				
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
						decider.decision = Decision(attack_decision = Attack_Decision(attack_list=temp_attack_list, force=self.weapon.force))
				
				
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
# Controversial update! Making the rook prefer vertical movement over horizontal movement,
# in the hopes of reducing the "this enemy is too random" annoyance
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

					(dx,dy) = Move_Towards_Visible_Player(monster.x, monster.y, rook_moves = True, bias = 'vertical')
					decider.decision = Decision(move_decision=Move_Decision(dx,dy))

				

				#close enough, attack! (if the player is still alive.) (and you can attack) (and are not in water)
				elif player.fighter.hp >= 0 and self.weapon.current_charge >= self.weapon.default_usage and not monster.fighter.in_water:#   recharge_time <= 0:
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
						decider.decision = Decision(attack_decision = Attack_Decision(attack_list=temp_attack_list, force=self.weapon.force))


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
					decider.decision = Decision(attack_decision = Attack_Decision(attack_list=temp_attack_list, force=self.weapon.force))
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


def Move_Towards_Visible_Player(current_x, current_y, rook_moves = False, bias = None):
	(dx,dy) = next_step_towards(current_x, current_y, player.x, player.y, rook_moves, bias = bias)
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
				# if there are two equal options to choose between, choose one randomly. Unless you have a bias
				if bias == 'horizontal':
					return (xdiff,0)
				elif bias == 'vertical':
					#print('ROOKVERT')
					return(0,ydiff)
				else:
					#print('ROOKanomaly')
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
	def __init__(self, damage, lifespan = 1, attacker=None, direction = None):
		self.damage = damage
		self.lifespan = lifespan
		self.attacker = attacker
		self.existing = True
		if attacker.fighter:
			self.color = attacker.fighter.attack_color
			self.faded_color = attacker.fighter.faded_attack_color
		self.direction = direction

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
#					if target.name == 'security drone':
#						if target.raising_alarm is False:
#							target.raising_alarm = True
#							alarm_level += 2
#							message('The security drone sounds a loud alarm!')
#							# Let's also run the spawn clock forwards so a fresh wave of enemies arrives
#							spawn_timer = 1	#This is not always working as I'd like???
				#elif target.door is not None and target.name != 'elevator door':
				#	translated_console_set_char_background(con, target.x, target.y, self.faded_color, libtcod_BKGND_SET)
				#	target.door.take_damage(self.damage)

				elif target.name == 'firepit':
					#target.take_damage(self.damage)
					target.explode((self.owner.x,self.owner.y))	#temp hack hack hack


					#new_fire = Fire(self.owner.x,self.owner.y)
					#objectsArray[self.owner.x][self.owner.y].append(new_fire)
					#worldEntitiesList.append(new_fire)
					#message('Fire shit happens!', Color_Interesting_Combat)
					#for x in range (target.x - 2, target.x+3):
					#	for y in range (target.y - 2, target.y + 3):
					#		if x >= 0  and x < MAP_WIDTH and y >= 0  and y < MAP_HEIGHT and not map[x][y].blocked:
					#			new_fire = Object(x, y, 317 + randint(0,1), 'fire', fire_color, blocks = False, weapon = False, always_visible=False, mouseover = "Uh oh.")
					#			#new_fire = Fire(x,y)
					#			objectsArray[x][y].append(new_fire)
					#			for other_object in objectsArray[x][y]:
					#				if other_object.door:
					#					other_object.aflame = True
					#					worldEntitiesList.append(other_object)	#ugh what is this code
						
					
					#garbage_list.append(target)

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
	
	#print("PROCESSING NEAREST CENTER POINTS")

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



def next_step_towards(current_x, current_y, target_x, target_y, rook_moves = False, bias = None):

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
				# if there are two equal options to choose between, choose one randomly. Unless you have a bias
				if bias == 'horizontal':
					dy = 0
				elif bias == 'vertical':
					dx = 0
				else:
					#randomly choose either horizontal or vertical to go with
					num =  randint( 0, 1)
					if num == 0:
						dx = 0
					elif num == 1:
						dy = 0
			
	return(dx, dy)






def next_step_based_on_target(current_x, current_y, target_x = None, target_y = None, target_center = None, aiming_for_center = False, prioritise_visible = False, prioritise_straight_lines = False, rook_moves = False, return_message = None, request_message = False, request_shortlist = False, avoid_water = False):


	# First off, if we are meant to be aiming for a target center but target center is None for whatever reason, just stand still
	if aiming_for_center and target_center == None:
		if request_message == True:
			return ((0,0), "No target center specified")
		else:
			return (0,0)

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
		block =  is_blocked(current_x +dx, current_y + dy, care_about_doors = False, care_about_fighters = True, avoid_water = avoid_water)	#hmmm... what's our take on doors here?
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


def getSign(num):
	if num == 0:
		return 0
	elif num > 0:
		return 1
	else:
		return -1



def getVectorFromDirectionAndSpeed(direction, speed):


	if direction == 'upleft':
		vector = (-speed, -speed)
	elif direction == 'up': 
		vector = (0, -speed)
	elif direction == 'upright':
		vector = (speed, -speed)
	elif direction == 'right':
		vector = (speed, 0)
	elif direction == 'downright':
		vector = (speed, speed)
	elif direction == 'down':
		vector = (0, speed)
	elif direction == 'downleft':
		vector = (-speed, speed)
	elif direction == 'left':
		vector = (-speed, 0)
	elif direction == 'none':
		vector = (0,0)

	return vector



def get_mouseover_text():
	global mouse_coord_x, mouse_coord_y
	global PANEL_Y, ACTION_SCREEN_X, MESSAGE_PANEL_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT, PANEL_HEIGHT
	global camera
	
	return_text = "MICE ARE COOL (" + str(mouse_coord_x) + ", " + str(mouse_coord_y) + ")"

	if mouse_coord_y >= PANEL_Y:
		return_text = get_info_panel_mouseover_text(mouse_coord_x, mouse_coord_y - PANEL_Y)
	elif mouse_coord_x < MESSAGE_PANEL_WIDTH:
		return_text = get_message_panel_mouseover_text(mouse_coord_x, mouse_coord_y)

	else:
		x_offset = int(camera.x-(SCREEN_WIDTH + MESSAGE_PANEL_WIDTH)/2)
		y_offset = int(camera.y-(SCREEN_HEIGHT-PANEL_HEIGHT)/2)
		#I think (x_offset, y_offset) gives the map co-ordinate of the space visible in sequare (0,0) of the action window
		return_text = get_action_screen_mouseover_text(x_offset + mouse_coord_x, y_offset + mouse_coord_y)

	return return_text




def get_message_panel_mouseover_text(x,y):
	return "Message Panel (" + str(x) + "," + str(y) + ")"

def get_action_screen_mouseover_text(x,y):

	# It's possible the mouse is outside the map.
	try:	
		# Case 1: this part of map has been explored
		if map[x][y].explored:
			# Case 1a: It's a wall!
			if map[x][y].blocked:
				return "Wall"
			
			else:
				#Case 1b: Area is currently visible
				if fov_map.fov[x, y]:
					stack_depth = len(objectsArray[x][y])
					if stack_depth> 0:
						return objectsArray[x][y][stack_depth - 1].name.capitalize() + ": " + objectsArray[x][y][stack_depth - 1].mouseover
					else:
						return "Empty space"
						#return "dunno (" + str(x) + "," + str(y) + ") (" + str(player.x) + "," + str(player.y) + ")" 
				else:
					# Case 1c: Area is explored but not currently visible
					top_visible_object = None
					for obj in objectsArray[x][y]:
						if obj.always_visible:
							top_visible_object = obj
					if top_visible_object is not None:
						return top_visible_object.name.capitalize() + ": " + top_visible_object.mouseover
					else:
						return "Previously explored area"

		# Case 2: this area has not been explored
		else: 
			return "Unexplored area"

	except IndexError:
		return "Out of play area"

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
	global fov_recompute, keys, stairs, player_weapon, game_state, player_action, player_action_before_pause, player_just_attacked, favoured_by_healer, favoured_by_destroyer, tested_by_destroyer,  favoured_by_deliverer, tested_by_deliverer,  destroyer_test_count, deliverer_test_count, time_level_started, key_count, currency_count, already_healed_this_level, TEMP_player_previous_center, something_changed, current_shrine, controlHandler, control_scheme, shrine_list, purchase_selected_shrine
	global SHOW_FAVOUR


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
		
		if game_state == 'playing':				# w o w ,   w h a t   a
			player_action_before_pause = player_action	# b a d   h a c k
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
			player_action = player_action_before_pause
		elif key_char == 't' and dungeon_level == 0:
			something_changed = True
			game_state = 'playing'
			player_action = player_action_before_pause
			load_test_level()

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


			# TODO put the below in a new movement phase method that gets called by processing a pickup decision

			items_to_pickup = [weapons_found[keynum-1]]
			player.decider.set_decision(Decision(pickup_decision=Pickup_Decision(items_to_pickup)))

			
		#	new_weapon = get_weapon_from_item(weapons_found[keynum-1], player.fighter.bonus_max_charge)
		#	old_weapon = get_item_from_weapon(player_weapon)
		#	player_weapon = new_weapon
		#	objectsArray[weapons_found[keynum-1].x][weapons_found[keynum-1].y].remove(weapons_found[keynum-1])
		#	# let's try that you don't drop your weapon, you throw it away entirely so you can't pick it up later.
		#	#drop_weapon(old_weapon)
		#	weapon_found = True
		#	if str(old_weapon.name) == "unarmed":
		#		message('You pick up the ' + new_weapon.name + '.', Color_Personal_Action) 
		#	else:
		#		message('You throw away your ' + old_weapon.name + ' and pick up the ' + new_weapon.name + '.', Color_Personal_Action) 
		elif veekay != None:
			game_state = 'playing'
			message('Never mind.', Color_Not_Allowed)
			#keynum = key
			#print str(libtcod.KEY_KP7)		# hang on... 41 is 7. So... 35 is 1, right? blah - 34
			return 'invalid-move'

		else:
			return 'pickup_dialog'


	elif player_action == 'upgrade-shop-dialog-sales-pitch':


		control_num = -1
		if key_char in controlHandler.intFromLetter:
			control_num = controlHandler.intFromLetter[key_char]

		#if key_char == 'y':	# player has decided to buy an upgrade...
		if control_num == 1 or key_char == 'y' or key_char == 'Y':	# player has decided to buy an upgrade...
			upgrade_cost = current_shrine.get_cost()
			if currency_count >= upgrade_cost:	#then let them get the upgrade

				
				#message("Are you sure???? Y/N", Color_Menu_Choice)
				player.decider.set_decision(Decision(buy_decision=Buy_Decision(current_shrine)))

				something_changed = True
				
				# TODO: put following in a preliminary phase method?
				#currency_count = currency_count - upgrade_cost
				#upgrade_array.append(current_shrine.upgrade)
				#message('You recieve the gift of '+ current_shrine.upgrade.name +'!', Color_Stat_Info)
				#current_shrine.upgrade = None
				#return 'upgrade-shop-dialog-confirm'
			else:
				something_changed = True
				message('You do not have enough favour!', Color_Not_Allowed)
				if not SHOW_FAVOUR:
					SHOW_FAVOUR = True
		elif control_num == 2:
			DescribeCatalog(current_shrine)
			return 'upgrade-shop-dialog-catalog'


		#elif key_char == 'n':
		else:
			something_changed = True
			message('You decide to abstain from ' + current_shrine.upgrade.name + '.', Color_Stat_Info)
		#else:
		#	message('Never mind??', Color_Not_Allowed)

	elif player_action == 'upgrade-shop-dialog-catalog':


		control_num = -1
		if key_char in controlHandler.intFromLetter:
			control_num = controlHandler.intFromLetter[key_char]

		# reconstruct the list of available shrines/upgrades,to see if the player selected one
		available_shrine_list = []
		for temp_shrine in shrine_list:
			if temp_shrine.visited and temp_shrine.upgrade is not None:
				available_shrine_list.append(temp_shrine)
		if control_num >0 and control_num <= len(available_shrine_list):
			# try and buy the upgrade at shrine number control_num-1. 
			# Actually just choose one and then either tell the player they don't have enough currency, 
			# or ask them to confirm their choice (and give them details)
			
			purchase_selected_shrine = available_shrine_list[control_num - 1]
			upgrade_cost = purchase_selected_shrine.get_cost()
			if currency_count >= upgrade_cost:	#then tell them about the upgrade and ask to confirm

				DescribeConfirmationRequest(purchase_selected_shrine)
				#something_changed = True
				return 'upgrade-shop-dialog-confirm'
				
			else:
				something_changed = True
				message('You do not have enough favour!', Color_Not_Allowed)
				if not SHOW_FAVOUR:
					SHOW_FAVOUR = True
		else:
			message('Not today.')

	elif player_action == 'upgrade-shop-dialog-confirm':

		control_num = -1
		if key_char in controlHandler.intFromLetter:
			control_num = controlHandler.intFromLetter[key_char]

		if control_num == 1  or key_char == 'y' or key_char == 'Y':
			# try and buy the upgrade under consideration
			upgrade_cost = purchase_selected_shrine.get_cost()
			if currency_count >= upgrade_cost:	#then tell them about the upgrade and ask to confirm

				player.decider.set_decision(Decision(buy_decision=Buy_Decision(purchase_selected_shrine)))
				something_changed = True
				
			else:
				something_changed = True
				message('You do not have enough favour!', Color_Not_Allowed)
				if not SHOW_FAVOUR:
					SHOW_FAVOUR = True

		else:
			message('Not today.')
		something_changed = True

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
		# check if the first space in this jump is blocked by something unjumpable
		(dx,dy) = temp_jump_decision
		xSign = getSign(dx)
		ySign = getSign(dy)
		
		# check the next space out
		space_x = player.x + xSign
		space_y = player.y + ySign
		if map[space_x][space_y].blocked:
			message("There's a wall in the way!", Color_Not_Allowed)
			return 'invalid-move'
		else:
			# check for blocking, objects
			for obj in objectsArray[space_x][space_y]:
				# blocking objects are only a problem if they'renot jumpable, or they're where we're trying to get to
				if obj.blocks and not obj.jumpable :				
					message("There's a " + obj.name + " in the way!", Color_Not_Allowed)
					return 'invalid-move'
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

				items_to_pickup = []
				
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
				if len(keys_found) > 0 and len(favours_found) == 0:

					items_to_pickup = keys_found
					# TODO: put in a movement phase methods
					#message('You snatch up the key.', Color_Personal_Action)
					#key_count = key_count + len(keys_found)
					#for ki in keys_found:
					#	objectsArray[ki.x][ki.y].remove(ki)	
				#similarly, favours take priority over weapons but after keys.
				elif len(keys_found) == 0 and len(favours_found) > 0:



					items_to_pickup = favours_found
					## TODO: put in a movement phase methods
					#message('You take the favour token.', Color_Personal_Action)
					#currency_count = currency_count + len(favours_found)
					#for fa in favours_found:
					#	objectsArray[fa.x][fa.y].remove(fa)	
				elif len(keys_found) > 0 and len(favours_found) > 0:

					items_to_pickup = keys_found + favours_found
					# TODO: put in a movement phase methods
					#message('You pick up the key and favour token.', Color_Personal_Action)
					#key_count = key_count + len(keys_found)
					#for ki in keys_found:
					#	objectsArray[ki.x][ki.y].remove(ki)
					#currency_count = currency_count + len(favours_found)
					#for fa in favours_found:
					#	objectsArray[fa.x][fa.y].remove(fa)
				elif len(plants_found) > 0:

					items_to_pickup = plants_found
					
					# TODO: put in a movement phase methods
					#for pl in plants_found:
					#	message('You pick up the ' + pl.name + ' and eat it.', Color_Personal_Action)
					#	pl.plant.harvest(player)
					#	garbage_list.append(pl)
				# TODO: make it so you pick up  fruits / plants / seeds / whatever in order to heal, rather than automatically.
			#STILL TODO KEEP A KEY COUNT AND MAKE IT AFFECT ELEVATOR OPENING
				elif len(weapons_found) == 1:

					items_to_pickup = weapons_found
					# TODO: put in a movement phase methods
					#new_weapon = get_weapon_from_item(weapons_found[0], player.fighter.bonus_max_charge)
					#old_weapon = get_item_from_weapon(player_weapon)
					#player_weapon = new_weapon
					#objectsArray[weapons_found[0].x][weapons_found[0].y].remove(weapons_found[0])
					#
					## let's try that you don't drop your weapon, you throw it away entirely so you can't pick it up later.#
					##drop_weapon(old_weapon)
					#weapon_found = True
					#if str(old_weapon.name) == "unarmed":
					#	message('You pick up the ' + new_weapon.name + '.', Color_Personal_Action) 
					#else:
					#	message('You throw away your ' + old_weapon.name + ' and pick up the ' + new_weapon.name + '.', Color_Personal_Action) 
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
				#elif len(plants_found) >= 1:
				#	for plant_object in plants_found:
				#		if plant_object.plant.state == 'seed':
				#				plant_object.plant.activate()
				#				message('A sapling emerges as you poke the seed.', Color_Interesting_In_World)

				if len(items_to_pickup) > 0:
					# Set player pickup decision based on chosen set of items
					player.decider.set_decision(Decision(pickup_decision=Pickup_Decision(items_to_pickup)))

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


			elif actionCommand == "DROP":
				# gonna be very lazy here buttt
				choice =  randint( 0, 1)
				if choice == 0:
					new_grenade = Grenade(player.x, player.y)
				else:
					new_grenade = Water_Grenade(player.x, player.y)
				drop_item(new_grenade)
				message("You drop a " + new_grenade.name + ".", Color_Personal_Action)

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

						#if current_shrine.upgrade is not None:
						if not current_shrine.visited:
							current_shrine.visit()
							DescribeSalesPitch(current_shrine)
							#message('A small god appears before you.', Color_Interesting_In_World)
							#message_string = '\"For a small display of faith, I will grant you the boon of ' + current_shrine.upgrade.name +'!\"'
							#message(message_string, Color_Message_In_World)
							#message_string = '[' + current_shrine.upgrade.name +':' + current_shrine.upgrade.tech_description +']'
							#message(message_string, Color_Personal_Action)
							#message_string = '\"' + current_shrine.upgrade.verbose_description +'\"'
							#message(message_string, Color_Message_In_World)
							#message_string = 'Would you like some ' + current_shrine.upgrade.name + ' ('+ str(current_shrine.get_cost()) +' favour)? y/n'
							#message(message_string, Color_Menu_Choice)
							return 'upgrade-shop-dialog-sales-pitch'
						else:
							# figure out what there would be to display in a catalog
							available_shrine_list = []
							for temp_shrine in shrine_list:
								if temp_shrine.visited and temp_shrine.upgrade is not None:
									available_shrine_list.append(temp_shrine)
							if len(available_shrine_list) > 0:
								message('The small god gives you a small nod.', Color_Interesting_In_World)
								DescribeCatalog(current_shrine)
								return 'upgrade-shop-dialog-catalog'
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





def DescribeSalesPitch(shrine):  # Shop text associated with 'upgrade-shop-dialog-sales-pitch'
	#message('HEY DO YOU WANT THE THING.', Color_Interesting_In_World)

	message('A small god appears before you.', Color_Interesting_In_World)
	message_string = '\"A new worshipper! For a small display of faith, I will grant you the boon of ' + shrine.upgrade.name +'!\"'
	message(message_string, Color_Message_In_World)
	#message_string = '\"For a small display of faith, I will grant you the boon of ' + shrine.upgrade.name +'!\"'
	#message(message_string, Color_Message_In_World)
	message_string = '[' + shrine.upgrade.name +':' + shrine.upgrade.tech_description +']'
	message(message_string, Color_Personal_Action)
	#message_string = '\"' + shrine.upgrade.verbose_description +'\"'
	#message(message_string, Color_Message_In_World)
	message_string = 'Would you like some ' + shrine.upgrade.name + ' ('+ str(shrine.get_cost()) +' favour)?'
	message(message_string, Color_Menu_Choice)

	message_string = controlHandler.letterFromInt[1] + ': Yes please'
	message(message_string, Color_Menu_Choice)
	message_string =  controlHandler.letterFromInt[2] + ': Show options from other shrines'
	message(message_string, Color_Menu_Choice)
	message_string =  '#JUMP#: No thanks'	# here's some hacky coding. The command for jump also means 'leave menu', and that's hard-coded??? because I wanted both commands to be space but my control system isn't really set up to assign two commands to the same key.
	message(message_string, Color_Menu_Choice)

def DescribeCatalog(shrine): # Shop text associated with 'upgrade-shop-dialog-catalog'
	global shrine_list

	message('\"Make your choice...\"', Color_Message_In_World)
	# make a list of shrines on this level that the player has visited, that have upgrades available
	available_shrine_list = []
	for temp_shrine in shrine_list:
		# TODO: add checking for having been visited
		if temp_shrine.visited and temp_shrine.upgrade is not None:
			available_shrine_list.append(temp_shrine)

	for i in range(len(available_shrine_list)):
		#safety valve: if there are more than 26 shrines we don't try to report them all because controlHandler.letterFromInt would throw an error i think
		if i < 26:
			temp_shrine = available_shrine_list[i]
			message_string = controlHandler.letterFromInt[i+1] +  ". " + temp_shrine.upgrade.name + '('+ str(temp_shrine.get_cost()) +' favour)'
			message(message_string, Color_Menu_Choice)
	message_string =  '#JUMP#: Nothing today thanks'	# here's some hacky coding. The command for jump also means 'leave menu', and that's hard-coded??? because I wanted both commands to be space but my control system isn't really set up to assign two commands to the same key.
	message(message_string, Color_Menu_Choice)
	


def DescribeConfirmationRequest(shrine): # Shop text associated with 'upgrade-shop-dialog-confirm'. 'shrine' is the shrine you aretrying to purchase from, not necessarily the shrine you are standing at?
	message('\"Are you certain?\"', Color_Message_In_World)
	message_string = '[' + shrine.upgrade.name +':' + shrine.upgrade.tech_description +']'
	message(message_string, Color_Personal_Action)
	#message_string = '\"' + shrine.upgrade.verbose_description +'\"'
	#message(message_string, Color_Message_In_World)
	message_string = 'Aquire ' + shrine.upgrade.name + ' ('+ str(shrine.get_cost()) +' favour)?'
	message(message_string, Color_Menu_Choice)

	message_string = controlHandler.letterFromInt[1] + ': Yes please'
	message(message_string, Color_Menu_Choice)
	message_string =  '#JUMP#: No thanks'	# here's some hacky coding. The command for jump also means 'leave menu', and that's hard-coded??? because I wanted both commands to be space but my control system isn't really set up to assign two commands to the same key.
	message(message_string, Color_Menu_Choice)



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
			new_shrine = Object(shrine_x, shrine_y, '&', 'shrine4', default_altar_color, blocks=False, shrine= Shrine(god_healer), always_visible=True) 		
			#new_shrine = Object(shrine_x, shrine_y, '&', 'shrine to ' + god_healer.name, default_altar_color, blocks=False, shrine= Shrine(god_healer), always_visible=True) 		
			objectsArray[shrine_x][shrine_y].append(new_shrine)
			shrine.cost += dungeon_level - 2
			new_shrine.send_to_back()
		elif num == 1:
			(shrine_x, shrine_y) = room.center()
			new_shrine = Object(shrine_x, shrine_y, '&', 'shrine5', default_altar_color, blocks=False, shrine= Shrine(god_destroyer), always_visible=True) 		
			#new_shrine = Object(shrine_x, shrine_y, '&', 'shrine to ' + god_destroyer.name, default_altar_color, blocks=False, shrine= Shrine(god_destroyer), always_visible=True) 		
			objectsArray[shrine_x][shrine_y].append(new_shrine)
			shrine.cost += dungeon_level - 2
			new_shrine.send_to_back()
		elif num == 2:
			(shrine_x, shrine_y) = room.center()
			new_shrine = Object(shrine_x, shrine_y, '&', 'shrine6', default_altar_color, blocks=False, shrine= Shrine(god_deliverer), always_visible=True) 		
			#new_shrine = Object(shrine_x, shrine_y, '&', 'shrine to ' + god_deliverer.name, default_altar_color, blocks=False, shrine= Shrine(god_deliverer), always_visible=True) 		
			objectsArray[shrine_x][shrine_y].append(new_shrine)
			shrine.shrine.cost += dungeon_level - 2
			new_shrine.send_to_back()



def create_monster(x,y, name, guard_duty = False):
	global number_alarmers
	global enemyArtHandler
	(data_name, data_symbol, data_color, data_description) = enemyArtHandler.getEnemyArtData(name)
	if name == 'strawman':
		# let's make a strawman!
		strawman_component = Fighter(hp=1, defense=0, power=1, death_function=monster_death,  attack_color = data_color, faded_attack_color = data_color, bleeds = False)
		ai_component = Strawman_AI(weapon = None)
		decider_component = Decider(ai_component)
		monster = Object(x, y, data_symbol, data_name, color_white, blocks=True, fighter=strawman_component, decider=decider_component, mouseover = data_description)
#"A training dummy. Does no attacks.")

	elif name == 'flailing strawman':
		# let's create a strawman that can theoretically do damage!
		strawman_component = Fighter(hp=1, defense=0, power=1, death_function=monster_death,  attack_color = data_color, faded_attack_color = data_color, bleeds = False)
		ai_component = Strawman_AI(weapon = Weapon_Sai())
		decider_component = Decider(ai_component)
		monster = Object(x, y, data_symbol, data_name, color_white, blocks=True, fighter=strawman_component, decider=decider_component, mouseover = data_description)
#"A training dummy with a weapon strapped to it. Watch out!")	

	elif name == 'strawman on wheels':
		# let's create a strawman that can move around!
		strawman_component = Fighter(hp=1, defense=0, power=1, death_function=monster_death,  attack_color = data_color, faded_attack_color = data_color, bleeds = False)
		ai_component = Strawman_on_wheels_AI(weapon = None)
		decider_component = Decider(ai_component)
		monster = Object(x, y, data_symbol, data_name, color_white, blocks=True, fighter=strawman_component, decider=decider_component, mouseover = data_description)
#mouseover = "A moving target to test your hand-eye co-ordination.")
				
	elif name == 'swordsman':
		#create an orc
		fighter_component = Fighter(hp=1, defense=0, power=1, death_function=monster_death, attack_color = color_swordsman, faded_attack_color = color_swordsman)
		ai_component = BasicMonster(weapon = Weapon_Sword(), guard_duty= guard_duty)
		decider_component = Decider(ai_component)
		monster = Object(x, y, 'S', 'swordsman', color_swordsman, blocks=True, fighter=fighter_component, decider=decider_component, mouseover =  "Fast and aggressive. Goes down in one hit.")



	elif name == 'stupid swordsman':
		#create an orc
		fighter_component = Fighter(hp=1, defense=0, power=1, death_function=monster_death, attack_color = color_swordsman, faded_attack_color = color_swordsman)
		ai_component = StupidBasicMonster(weapon = Weapon_Sword(), guard_duty= guard_duty)
		decider_component = Decider(ai_component)
		monster = Object(x, y, 'S', 'swordsman', color_swordsman, blocks=True, fighter=fighter_component, decider=decider_component, mouseover =  "I think I took all these out of the game. If you're reading this I guess I was wrong!")


	elif name == 'boman':
		#create a troll
		fighter_component = Fighter(hp=3, defense=0, power=1, death_function=monster_death, attack_color = data_color, faded_attack_color = data_color)
		ai_component = Boman_AI(weapon = Weapon_Staff(), guard_duty= guard_duty)
		decider_component = Decider(ai_component)
		monster = Object(x, y, data_symbol, data_name, color_white, blocks=True, fighter=fighter_component, decider=decider_component, mouseover = data_description)
#"Dangerous up close, with a diagonal attack.")


	elif name == 'greenhorn':
		#create a troll
		fighter_component = Fighter(hp=1, defense=0, power=1, death_function=monster_death, attack_color = data_color, faded_attack_color = data_color)
		ai_component = Greenhorn_AI(weapon = Weapon_Sword(), guard_duty= guard_duty)
		decider_component = Decider(ai_component)
		monster = Object(x, y, data_symbol, data_name, color_white, blocks=True, fighter=fighter_component, decider=decider_component, mouseover = data_description)
		# "This enemy is just excited to be here.")


	elif name == 'greenhorn-aggro':
		#create a troll
		fighter_component = Fighter(hp=1, defense=0, power=1, death_function=monster_death, attack_color = data_color, faded_attack_color = data_color)
		ai_component = BasicMonster(weapon = Weapon_Sword(), guard_duty= guard_duty)
		decider_component = Decider(ai_component)
		monster = Object(x, y, data_symbol, data_name, color_white, blocks=True, fighter=fighter_component, decider=decider_component, mouseover = data_description)


	elif name == 'greenhorn-cautious':
		#create a troll
		fighter_component = Fighter(hp=1, defense=0, power=1, death_function=monster_death, attack_color = data_color, faded_attack_color = data_color)
		ai_component = Greenhorn_Erratic_AI(weapon = Weapon_Sword(), guard_duty= guard_duty)
		decider_component = Decider(ai_component)
		monster = Object(x, y, data_symbol, data_name, color_white, blocks=True, fighter=fighter_component, decider=decider_component, mouseover = data_description)

	elif name == 'rook':
		#create a rook! That's a guy with a spear who only moves in four directions
		fighter_component = Fighter(hp=3, defense=0, power=1, death_function=monster_death, attack_color = color_rook, faded_attack_color = color_rook)
		ai_component = Rook_AI(weapon = Weapon_Spear(), guard_duty = guard_duty)
		decider_component = Decider(ai_component)
		monster = Object(x, y, 'R', "Rook", color_rook, blocks=True, fighter=fighter_component, decider=decider_component, mouseover = "Can't move diagonally, but woe betide anyone who takes them head on.")

	elif name == 'albatross':
		fighter_component = Fighter(hp=1, defense=0, power=1, death_function=monster_death, attack_color = color_swordsman, faded_attack_color = color_swordsman)
		ai_component = BasicMonster(weapon = Weapon_Shiv(), guard_duty= guard_duty)
		decider_component = Decider(ai_component)
		monster = Object(x, y, 'S', 'swordsman', color_swordsman, blocks=True, fighter=fighter_component, decider=decider_component, mouseover =  "Loves stabbing things.")


	elif name == 'bustard':
		fighter_component = Fighter(hp=2, defense=0, power=1, death_function=monster_death, attack_color = data_color, faded_attack_color = data_color)
		ai_component = Rook_AI(weapon = Weapon_Spear(), guard_duty = guard_duty)
		decider_component = Decider(ai_component)
		monster = Object(x, y, data_symbol, data_name, color_white, blocks=True, fighter=fighter_component, decider=decider_component, mouseover = data_description) #"The tower's elite robot security force. Can't move or attack diagonally.")


	elif name == 'crane':
		fighter_component = Fighter(hp=3, defense=0, power=1, death_function=monster_death, attack_color = data_color, faded_attack_color = data_color)
		#ai_component = Ninja_Crane_AI(weapon = Weapon_Broom(), guard_duty = guard_duty)
		ai_component = BasicMonster(weapon = Weapon_Broom(), guard_duty= guard_duty)
		decider_component = Decider(ai_component)
		monster = Object(x, y, data_symbol, data_name, color_white, blocks=True, fighter=fighter_component, decider=decider_component, mouseover = data_description)# "Likes to hedge their bets by attacking multiple spaces at once. Not concerned about hitting co-workers.")


	elif name == 'dove':
		#create a troll
		fighter_component = Fighter(hp=3, defense=0, power=1, death_function=monster_death, attack_color = data_color, faded_attack_color = data_color)
		ai_component = Dove_AI(weapon = Weapon_Pike(), guard_duty= guard_duty)
		decider_component = Decider(ai_component)
		monster = Object(x, y, data_symbol, data_name, color_white, blocks=True, fighter=fighter_component, decider=decider_component, mouseover = data_description)# "Looooooves diagonals.")

	elif name == 'eagle':
		#create a guy with an axe!
		fighter_component = Fighter(hp=2, defense=0, power=1, death_function=monster_death, attack_color = data_color, faded_attack_color = data_color)
		ai_component = Eagle_AI(weapon = Weapon_Halberd(), guard_duty = guard_duty)
		decider_component = Decider(ai_component)
		monster = Object(x, y, data_symbol, data_name, color_white, blocks=True, fighter=fighter_component, decider=decider_component, mouseover = data_description)# "Long range attacker. You probably need to stand back further than you think.")


	elif name == 'falcon':
		#create a guy with an axe!
		fighter_component = Fighter(hp=3, defense=0, power=1, death_function=monster_death, attack_color = data_color, faded_attack_color = data_color)
		ai_component = BasicMonster(weapon = Weapon_Sai(), guard_duty = guard_duty)
		decider_component = Decider(ai_component)
		monster = Object(x, y, data_symbol, data_name, color_white, blocks=True, fighter=fighter_component, decider=decider_component, mouseover = data_description)  #"Wields two weapons. One weapon is aimed at you. The other one, who knows.")



	elif name == 'gunslinger':
		#create a guy with an gun!
		fighter_component = Fighter(hp=1, defense=0, power=1, death_function=monster_death, attack_color = data_color, faded_attack_color = data_color)
		ai_component = Gunslinger_AI(weapon = Weapon_Gun(), guard_duty = guard_duty)
		decider_component = Decider(ai_component)
		monster = Object(x, y, data_symbol, data_name, color_white, blocks=True, fighter=fighter_component, decider=decider_component, mouseover = data_description)  


#	elif name == 'stupid rook':
#		#create a rook! That's a guy with a spear who only moves in four directions
#		fighter_component = Fighter(hp=3, defense=0, power=1, death_function=monster_death, attack_color = color_rook, faded_attack_color = color_rook)
#		ai_component = Stupid_Rook_AI(weapon = Weapon_Spear(), guard_duty = guard_duty)
#		decider_component = Decider(ai_component)
#		monster = Object(x, y, 'R', 'rook', color_rook, blocks=True, fighter=fighter_component, decider=decider_component)


	elif name == 'nunchuck fanatic':
		#create a troll
		fighter_component = Fighter(hp=2, defense=0, power=1, death_function=monster_death, attack_color = data_color, faded_attack_color = data_color)
		ai_component = BasicMonster(weapon = Weapon_Nunchuck(), guard_duty= guard_duty, attack_dist = 2)
		decider_component = Decider(ai_component)
		monster = Object(x, y, data_symbol, data_name, color_white, blocks=True, fighter=fighter_component, decider=decider_component, mouseover = data_description) 
		# "It's frankly a miracle they haven't hit themselves with it yet.")


	elif name == 'axe maniac':
		#create a guy with an axe!
		fighter_component = Fighter(hp=3, defense=0, power=1, death_function=monster_death,  attack_color = data_color, faded_attack_color = data_color)
		ai_component = BasicMonster(weapon = Weapon_Axe(), guard_duty = guard_duty)
		decider_component = Decider(ai_component)
		monster = Object(x, y, data_symbol, data_name, color_white, blocks=True, fighter=fighter_component, decider=decider_component, mouseover = data_description) 
		# "Bad news.")

	elif name == 'samurai':
		#create a guy with an axe!
		fighter_component = Fighter(hp=5, defense=0, power=1, death_function=monster_death, attack_color = color_axe_maniac, faded_attack_color = color_axe_maniac)
		ai_component = Samurai_AI(weapon = Weapon_Katana())
		decider_component = Decider(ai_component)
		monster = Object(x, y, 'Z', 'samurai', color_axe_maniac, blocks=True, fighter=fighter_component, decider=decider_component, mouseover = "A cautious, patient killer.")

	elif name == 'tridentor':
		#create a n aquatic enemy!
		fighter_component = Fighter(hp=2, defense=0, power=1, death_function=monster_death, attack_color = data_color, faded_attack_color = data_color)
		ai_component = Tridentor_AI(weapon = Weapon_Trident(), guard_duty = guard_duty)
		decider_component = Decider(ai_component)
		monster = Object(x, y, data_symbol, data_name, color_white, blocks=True, fighter=fighter_component, decider=decider_component, mouseover = data_description) 
		#"Able to attack in water. Wields a three-pronged weapon.")


	elif name == 'faerie':
		#create a faerie that floats around the dugeon!
		fighter_component = Fighter(hp=1, defense=0, power=1, death_function=monster_death, attack_color = color_faerie, faded_attack_color = color_faerie)
		ai_component = Faerie_AI(weapon = Weapon_Unarmed(), guard_duty = False)	#faeries are ill-suited for guard duty and always wander
		decider_component = Decider(ai_component)
		# faeries don't block, right?
		monster = Object(x, y, 379, 'faerie', PLAYER_COLOR, blocks=False, fighter=fighter_component, decider=decider_component, mouseover = "Catch it before it gets away!", phantasmal = True)


	elif name == 'rogue':
		#create a guy with an axe!
		fighter_component = Fighter(hp=2, defense=0, power=1, death_function=monster_death, attack_color = color_rogue, faded_attack_color = color_rogue)
		ai_component = Rogue_AI(weapon = Weapon_Sai(), guard_duty = guard_duty)
		decider_component = Decider(ai_component)
		monster = Object(x, y, 'K', 'rogue', color_rogue, blocks=True, fighter=fighter_component, decider=decider_component, mouseover = "Ah man, I can't remember how the AI for this one worked. Did they like to attack everywhere except where you are? I guess you're about to find out.")



	elif name == 'hammerer':
		#create a lady with a hammer!
		fighter_component = Fighter(hp=3, defense=0, power=1, death_function=monster_death, attack_color = color_boman, faded_attack_color = color_boman)
		ai_component =  BasicMonster(weapon = Weapon_Hammer())
		decider_component = Decider(ai_component)
		monster = Object(x, y, data_symbol, data_name, color_white, blocks=True, fighter=fighter_component, decider=decider_component, mouseover = data_description) 
		#monster = Object(x, y, 'H', 'hammerer', color_boman, blocks=True, fighter=fighter_component, decider=decider_component, mouseover = "The secret long lost character.")


	elif name == 'ninja':
		#create a sneaky ninja!
		fighter_component = Fighter(hp=2, defense=0, power=1, death_function=monster_death, attack_color = data_color, faded_attack_color = data_color)
		ai_component = Ninja_AI(weapon = Weapon_Dagger())
		decider_component = Decider(ai_component)
		monster = Object(x, y, data_symbol, data_name, color_white, blocks=True, fighter=fighter_component, decider=decider_component, mouseover = data_description) 
		#"Cautious and sneaky. Doesn't like a fair fight.")


	elif name == 'wizard':
		#create a wizard!
		fighter_component = Fighter(hp=10, defense=0, power=1, death_function=monster_death, attack_color = data_color, faded_attack_color = data_color)
		ai_component = Wizard_AI(weapon = Weapon_Ring_Of_Power())
		decider_component = Decider(ai_component)
		monster = Object(x, y, data_symbol, data_name, color_white, blocks=True, fighter=fighter_component, decider=decider_component, mouseover = data_description) 
		#"Your nemesis, in the flesh at last!")



	elif name == 'security drone':
		# let's make a security drone! It stays where it is and doesn't attack! In fact it's basically a strawman with more health.
		strawman_component = Fighter(hp=1, defense=0, power=1, death_function=monster_death,  attack_color =color_swordsman, faded_attack_color = color_swordsman, bleeds = False)
		ai_component = Strawman_AI(weapon = None)
		decider_component = Decider(ai_component)
		temp_alarm_time = lev_set.security_timer
		if dungeon_level < 2:	# make security drones a bit easier on the tutorial and level 1
			temp_alarm_time +=  + 2
			if  dungeon_level == 0:
				temp_alarm_time += 1
		alarmer_component = Alarmer(alarm_time = temp_alarm_time, pre_alarm_time = 0, assoc_fighter = strawman_component)
		monster = Object(x, y, 320, 'security drone', color_white, blocks=True, fighter=strawman_component, decider=decider_component, alarmer = alarmer_component, always_visible = True, mouseover = "Raises the alarm level by 2 if it can see you for too many turns. Killing it after it has sounded the alarm reduces the alarm level by 1. Destroy it for keys and favour.")
		alarmer_component.owner = monster



	else:
		monster = None
	
	if monster.alarmer is not None:
		number_alarmers += 1

	return monster



def create_strawman(x,y, weapon, command):
	global enemyArtHandler
	(data_name, data_symbol, data_color, data_description) = enemyArtHandler.getEnemyArtData('flailing strawman')
	# let's create a strawman that can theoretically do damage!
	strawman_component = Fighter(hp=1, defense=0, power=1, death_function=monster_death,  attack_color = data_color, faded_attack_color = data_color, bleeds = False)
	ai_component = Strawman_AI(get_weapon_from_name(weapon), command)		
	decider_component = Decider(ai_component)
	monster = Object(x, y, data_symbol, data_name, color_white, blocks=True, fighter=strawman_component, decider=decider_component, mouseover = data_description)
	#"A training dummy, blindly attacking with a real weapon. What could go wrong?")
	return monster





def create_projectile(x,y,name,direction, attacker):

	if name == 'bullet':
		projectile = Bullet(x,y, direction = direction, shooter = attacker)
	#def __init__(self, x, y, tags = set(), shooter = None, direction = 'right', damage = 1) : 
	# Note that for our current purposes, damage done by projectile is not affected by things like player strength etc...	
	return projectile






#todo probably add objectsarray as a global here? and then find the place to initialise it
def make_map(start_ele_direction = None, start_ele_spawn = None, test_level = False):
	global map, background_map, stairs, game_level_settings, dungeon_level, spawn_points, elevators, center_points, nearest_points_array, room_adjacencies, MAP_HEIGHT, MAP_WIDTH, number_alarmers, camera, alarm_level, key_count, currency_count, lev_set, decoration_count, TEMP_player_previous_center, objectsArray, bgColorArray, worldAttackList, worldEntitiesList, worldArrowsList, total_monsters, shrine_list
	global pathname

	lev_gen = Level_Generator(pathname)
	lev_set = game_level_settings.get_setting(dungeon_level)
	# update level settings with what sort of elevator situation we want the player to start in
	lev_set.start_ele_direction = start_ele_direction
	lev_set.start_ele_spawn = start_ele_spawn
	level_data = lev_gen.make_level(dungeon_level, lev_set, test_level)

	number_alarmers = 0		# how many things in the level do stuff with the alarm? If this becomes 0, all alarms stuff
	total_monsters = 0

	map = level_data.map
	background_map = level_data.background_map
	camera_x_offset = camera.x - player.x
	camera_y_offset = camera.y - player.y
	player.x = level_data.player_start_x
	player.y = level_data.player_start_y
	camera.x = player.x + camera_x_offset
	camera.y = player.y + camera_y_offset
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
	shrine_list = []	# This is gonna be a list of all the shrines
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
	worldArrowsList = []	## list of exit arrows that will light up when the level is complete

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

	# TODO actually make starting alarm level depend on what floor you're on.
	if dungeon_level > 1:
		alarm_level = 1
	else:
		alarm_level = 0
	key_count = 0
	decoration_count = 0

	# now create objects from object_data! This code resorting thing is actually getting kind of fun now
	for od in object_data:
		if od.name == 'stairs':
			stairs = Object(od.x, od.y, '<', 'stairs', PLAYER_COLOR, always_visible=True, mouseover = "We took these out of the game")
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
				if od.info == 'security drone':
					monster.drops_key = True
			total_monsters += 1
		elif od.name == 'strawman':
			strawman = create_strawman(od.x,od.y,od.info, od.more_info)
			objectsArray[od.x][od.y].append(strawman)
			worldEntitiesList.append(strawman)
		elif od.name == 'shrine':
			#get altar color - gonna make it depend on the background of the tile it's on.
			altar_color = 	default_altar_color	#color_light_ground_alt
			if background_map[od.x][od.y] == 2:
				altar_color = alt_altar_color #color_light_ground
		#	num = randint( 0, 2) 
		#	if num == 0:
				#shrine = Object(od.x, od.y, '&', 'shrine to ' + god_healer.name, altar_color, blocks=False, shrine= Shrine(god_healer), always_visible=True) 	
			shrine = Object(od.x, od.y, 353, 'shrine', altar_color, blocks=False, shrine= Shrine(god_healer), always_visible=True, mouseover = "Home to a small god. Favour can be exchanged here for a possibly useful upgrade.") 	
		#	elif num == 1:
		#		shrine = Object(od.x, od.y, '&', 'shrine2', altar_color, blocks=False, shrine= Shrine(god_destroyer), always_visible=True) 
				#shrine = Object(od.x, od.y, '&', 'shrine to ' + god_destroyer.name, altar_color, blocks=False, shrine= Shrine(god_destroyer), always_visible=True) 
		#	else: 
		#		shrine = Object(od.x, od.y, '&', 'shrine3', altar_color, blocks=False, shrine= Shrine(god_deliverer), always_visible=True) 
				#shrine = Object(od.x, od.y, '&', 'shrine to ' + god_deliverer.name, altar_color, blocks=False, shrine= Shrine(god_deliverer), always_visible=True) 
			shrine.shrine.cost += dungeon_level - 2
			objectsArray[od.x][od.y].append(shrine)
			shrine.send_to_back()
			shrine_list.append(shrine.shrine)
			if od.info == 'rejuvenation':
				shrine.shrine.upgrade = Rejuvenation()
			elif od.info == 'instantaneous-strength':
				shrine.shrine.upgrade = InstantaneousStrength()
			if dungeon_level == 0:		# hack for making tutorial shrines cost more than like, 1 or 0.
				shrine.shrine.cost = 2				

		elif  od.name == 'security drone':
			monster = create_monster(od.x,od.y, 'security drone', guard_duty = True)
			if od.info == 'drops-key':
				monster.drops_key = True
			objectsArray[od.x][od.y].append(monster)
			worldEntitiesList.append(monster)


			#number_alarmers += 1			#Now doing this elsewhere..
		#elif  od.name == 'door'or od.name == 'easydoor':
		#	if od.info == 'horizontal':
		#		door = Object(od.x, od.y, 301, 'door', default_door_color, blocks=True, door = Door(horizontal = True), always_visible=True) 
		#		map[od.x][od.y].block_sight = True
		#		objectsArray[od.x][od.y].append(door)
		#		worldEntitiesList.append(door)
		#	elif od.info == 'vertical':
		#		door = Object(od.x, od.y, 301, 'door', default_door_color, blocks=True, door = Door(horizontal = False), always_visible=True) 	
		#		map[od.x][od.y].block_sight = True
		#		objectsArray[od.x][od.y].append(door)
		#		worldEntitiesList.append(door)
		#	door.mouseover = "Walk into this door or attack it to open. (Doors have a chance of sticking.)"
		#	if od.name == 'easydoor':		# a door that doesn't stick!!
		#		door.door.easy_open = True
		#	# TODO MAKE PATHFINDING TAKE DOORS INTO ACCOUNT AT SOME POINT


		elif  od.name == 'enemy dispenser':
			dispenser = EnemyDispenser(od.x,od.y)
			objectsArray[od.x][od.y].append(dispenser)
			worldEntitiesList.append(dispenser)

		elif od.name == 'door':
			new_door = Door(od.x,od.y)
			objectsArray[od.x][od.y].append(new_door)
			worldEntitiesList.append(new_door)
		elif od.name == 'easydoor':
			new_door = Door(od.x,od.y, easy_open= True)
			objectsArray[od.x][od.y].append(new_door)
			worldEntitiesList.append(new_door)

		elif od.name == 'key':
			new_key = Object(od.x, od.y, 400, 'key', PLAYER_COLOR, blocks = False, weapon = False, always_visible=True, mouseover = "Gain enough of these to get access to the next floor.")
			objectsArray[od.x][od.y].append(new_key)
		elif od.name == 'water':
			new_water = Object(od.x, od.y, 352, 'water', water_foreground_color, blocks = False, weapon = False, always_visible=True, mouseover = "A pool of water. Most people can't attack while swimming.")
			objectsArray[od.x][od.y].append(new_water)
		elif od.name == 'fire':
			#new_fire = Object(od.x, od.y, 317 + randint(0,1), 'fire', fire_color, blocks = False, weapon = False, always_visible=False, mouseover = "Uh oh.")
			new_fire = Fire(od.x,od.y)
			objectsArray[od.x][od.y].append(new_fire)
			worldEntitiesList.append(new_fire)
		elif od.name == 'grenade':
			#new_fire = Object(od.x, od.y, 317 + randint(0,1), 'fire', fire_color, blocks = False, weapon = False, always_visible=False, mouseover = "Uh oh.")
			new_grenade = Grenade(od.x,od.y)
			objectsArray[od.x][od.y].append(new_grenade)
			worldEntitiesList.append(new_grenade)
		elif od.name == 'infinifire':
			new_fire = Fire(od.x,od.y, infinite = True)
			objectsArray[od.x][od.y].append(new_fire)
			worldEntitiesList.append(new_fire)
		elif od.name == 'firepit':
			#new_firepit = Object(od.x, od.y, 333 + randint(0,1), 'firepit', fire_color, blocks = True, weapon = False, always_visible=False, mouseover = "Mmmm, burny.")
			new_firepit = Firepit(od.x,od.y)
			objectsArray[od.x][od.y].append(new_firepit)
		elif od.name == 'plant':
			flower_part = Flower(flower_type = od.info, state = 'blooming')
			new_plant = Object(od.x, od.y, 402, flower_part.name, default_flower_color, blocks = False, plant = flower_part,  always_visible=True, mouseover = "Nutritious and delicious. Heals 1 wound when you pick it up, thereby restoring your max energy.")
			objectsArray[od.x][od.y].append(new_plant)
			worldEntitiesList.append(new_plant)
		elif od.name == 'tree':
			new_tree = Object(od.x, od.y, 369, 'tree', default_door_color, blocks = True,  always_visible=True, mouseover = "Sturdy and wooden.")
			objectsArray[od.x][od.y].append(new_tree)
			worldEntitiesList.append(new_tree)
		elif od.name == 'grass':
			new_grass = Object(od.x, od.y, 345 + randint(0,2), 'grass', default_flower_color, blocks = False,  always_visible=False, mouseover = "It sways as if in an outdoor breeze.")
			objectsArray[od.x][od.y].append(new_grass)
			worldEntitiesList.append(new_grass)
		elif od.name == 'message':
			message_color = color_light_ground_alt
			if background_map[od.x][od.y] == 2:
				message_color = color_light_ground
			floor_message = Object(od.x, od.y, 354, 'message', message_color, blocks=False, floor_message = Floor_Message(od.info), mouseover = "A helpful message. The writing is too small to read from this distance.")
			objectsArray[od.x][od.y].append(floor_message)
			floor_message.send_to_back()
		elif od.name == 'decoration':
			floor_message = Object(od.x, od.y, od.info, 'decoration', default_decoration_color, blocks=False, always_visible=True, mouseover = "Nothing to see here.")
			objectsArray[od.x][od.y].append(floor_message)
			floor_message.send_to_back()
			decoration_count += 1
		elif od.name == 'exit-arrow':
	#		symbol = 24
	#		if od.info == 'up':
	#			symbol = 24
	#		elif od.info == 'down':
	#			symbol = 25
	#		elif od.info == 'right':
	#			symbol = 26
	#		elif od.info == 'left':
	#			symbol = 27
	#		exit_arrow = Object(od.x, od.y, symbol, 'exit arrow', color_boman, blocks=False, always_visible=True, mouseover = "Go here to win!")
			exit_arrow = ExitArrow(od.x,od.y,od.info)
			objectsArray[od.x][od.y].append(exit_arrow)
			exit_arrow.send_to_back()
			worldArrowsList.append(exit_arrow)
			

	# elevator data because elevators are complicated! Do you know how to build an elevator? I sure don't!
	for ele in elevators:
		ele.special_door_list = []
		for ele_door in ele.doors:
			#door = Object(ele_door.x, ele_door.y, '+', 'elevator door', color_axe_maniac, blocks=True, door = Door(horizontal = ele_door.door.horizontal), always_visible=True, mouseover = "Opens for you if you have enough keys. But mainly opens for your enemies.") 
			door = ElevatorDoor(ele_door.x, ele_door.y, owner = ele)
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
	
	
def is_blocked(x, y, care_about_doors = False, generally_ignore_doors = True, care_about_fighters = False, generally_ignore_fighters = False, avoid_water = False):
	#first test the map tile
	if map[x][y].blocked:
		return True


	#now check for any blocking objects
	for object in objectsArray[x][y]:
		if object.blocks:
			#if object.door is not None:
			if object.name == 'door':
				if care_about_doors == True:
					return 'closed-door'
				if generally_ignore_doors == False:
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
		elif avoid_water:
			if object.name == "water":
				return True

	return False




#def player_move_or_attack(dx, dy):
#	global fov_recompute
# 
#	#the coordinates the player is moving to/attacking
#	x = player.x + dx
#	y = player.y + dy
# 
#	#try to find an attackable object there
#	target = None
#	for object in objectsArray[x][y]:
#		if object.fighter:
#			target = object
#			break
# 
#	#attack if target found, move otherwise
#	if target is not None:
#		player.fighter.attack(target)
#	else:
#		player.move(dx, dy)
#		fov_recompute = True



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
	if player_weapon.combat_type == 'melee':
		for (com, data, usage) in player_weapon.command_items:
			if com == actionCommand:
				command_recognised = True
	elif player_weapon.combat_type == 'projectile':
		for (com, data, usage) in player_weapon.projectile_command_items:
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


			if player_weapon.combat_type == 'melee':
				abstract_attack_data = player_weapon.do_energy_attack(actionCommand)
				temp_attack_list = process_abstract_attack_data(player.x,player.y, abstract_attack_data, player, bonus_strength)	
				player.decider.set_decision(Decision(attack_decision = Attack_Decision(attack_list=temp_attack_list, force=player_weapon.force)))
			elif player_weapon.combat_type == 'projectile':
				# todo make this be projetiley
				abstract_projectile_data = player_weapon.do_energy_projectile_attack(actionCommand)
				temp_projectile_list = process_abstract_projectile_data(player.x,player.y, abstract_projectile_data, player, bonus_strength)	
				player.decider.set_decision(Decision(projectile_decision = Projectile_Decision(projectile_list=temp_projectile_list)))
				# Also the weapon loses durability! Right now. Because the durability is really 'ammo'.
				player_weapon.durability -= 1
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
		(abstract_array, direction) = abstract_attack_data
		#for (i,j,val) in abstract_attack_data:
		for (i,j,val) in abstract_array:
			# adjust attack for position, and also extra strength from the fighter.
			temp_attack = Object(x+i, y+j, '#', 'attack', temp_color, blocks=False, attack= BasicAttack(val + attacker.fighter.extra_strength + bonus_strength, attacker=attacker, direction = direction), mouseover = "A space where " + attacker.name + " just attacked.")
			temp_attack_list.append(temp_attack)
	return temp_attack_list

# like process_abstract_attack_data, but for projectile weapons!
def process_abstract_projectile_data(x,y,abstract_projectile_data, attacker=None, bonus_strength = 0):
	# given data (i,j, val) from an abstract attack, produce an attack at co-ordinates x_i, y_j with damage val.
	# this function mainly exists because I am a bad programmer and can't figure out how to get the weapons file to recognise Attacks...
	temp_projectile_list = []
	temp_color = color_swordsman  # libtcod.dark_red
	if attacker is not None:
		if attacker.fighter:
			temp_color = attacker.fighter.attack_color
	# not having this condition leads to the wierd event handling issues leaf to game-crashing bugs.
	# Let's add this condition so we can investigate the wierd handling issues a bit, and/or find another game-crashing bug
	if abstract_projectile_data is not None:	
		#for (i,j,projectile_name, direction) in abstract_projectile_data:
		for (i,j,projectile_name, direction) in abstract_projectile_data:
			# create projectile of the type, location and direction that the data says (damage unaffected by strength etc)
			temp_projectile = create_projectile(x,y,projectile_name,direction, attacker)	
			temp_projectile_list.append(temp_projectile)
	return temp_projectile_list

	

def player_death(player):
	#the game ended!
	global game_state
	message('You collapse to the floor...', Color_Dangerous_Combat)
	message('Press R to restart, Q to quit', Color_Menu_Choice)
	game_state = 'dead'
 
	#for added effect, transform the player into a corpse!
	player.char = 257
	#player.color = libtcod.dark_red
 
def monster_death(monster):
	global garbage_list, favoured_by_healer, tested_by_destroyer, favoured_by_destroyer, tested_by_deliverer, favoured_by_deliverer, destroyer_test_count, deliverer_test_count, number_alarmers, alarm_level, total_monsters
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
					elif item.name != 'unarmed':	# don't drop 'unarmed', the game crashes when you pick it up
						num = randint(0, 100)
						if num <= CHANCE_OF_ENEMY_DROP:
							drop_weapon(item)
							reorder_objects(item.x,item.y)
	

	#transform it into a nasty corpse! it doesn't block, can't be
	#attacked and doesn't move
	#if monster.name == 'security drone':
	if monster.alarmer is not None:
		number_alarmers -= 1
		message(monster.name.capitalize() + ' is destroyed!', color_warning)
		if monster.alarmer.status != 'alarm-raised':
			message("Success! Defeated a " + monster.name.capitalize() + ' without triggering an alarm.', Color_Stat_Info)
		#decrease the alarm level alittle bit! Unless that was the last one, in which case set it to 0
		if number_alarmers > 0:
			if alarm_level > 0 and monster.alarmer.status == 'alarm-raised':
				#alarm_level += (-monster.alarmer.alarm_value + monster.alarmer.dead_alarm_value)
				message('The alarms get a little quieter.', Color_Interesting_In_World)
		else:
			alarm_level = 0
			message('A sudden silence descends as the alarms stop.', Color_Interesting_In_World)

		# Temp hack, probably: if thismonster is an alarmer (i.e. a security drone), make it drop currency?

		favour_object = Object(monster.x, monster.y, '$', 'favour token', color_tridentor, blocks = False,  always_visible=True, mouseover = "Gives you favour, which can be exchanged at shrines to get upgrades.")
		objectsArray[monster.x][monster.y].append(favour_object) 
		reorder_objects(monster.x, monster.y)

	# faeires drop favour? that's what we're doing at the mo.
	# actually for now no. I'll figure out what to do with faeries later
	if monster.name == 'faerie': 
		message('Oh no!', color_warning)
		#favour_object = Object(monster.x, monster.y, '$', 'favour token', color_tridentor, blocks = False,  always_visible=True, mouseover = "Gives you favour, which can be exchanged at shrines to get upgrades.")
		#objectsArray[monster.x][monster.y].append(favour_object) 
		reorder_objects(monster.x, monster.y)



	else:	
		message(monster.name.capitalize() + ' is dead!', Color_Interesting_Combat)
	monster.char = '%'
	monster.color = default_weapon_color
	monster.blocks = False
	monster.fighter = None
	monster.decider = None
	monster.name = 'dying ' + monster.name
#	monster.send_to_back()
	garbage_list.append(monster)

	#monster may drop a key?
	if monster.drops_key == True:
		new_key = Object(monster.x,monster.y, 400, 'key', PLAYER_COLOR, blocks = False, weapon = False, always_visible=True)
		objectsArray[monster.x][monster.y].append(new_key)
		# trigger a draw order cleanup, because otherwise you get enemies hiding under keys
#		reorder_objects(monster.x, monster.y)

	#killing a monster affects some test stuff for the god of destruction
	if tested_by_destroyer:
		if destroyer_test_count > 0:
			destroyer_test_count -= 1
		if destroyer_test_count <= 0:
			tested_by_destroyer = False
			favoured_by_destroyer = True
			favoured_by_healer = False


	# update the monster count
	total_monsters -= 1



def load_test_level():

	#objects = []
	make_map(test_level = True)
	objectsArray[player.x][player.y].append(player)
	worldEntitiesList.append(player)
	#print( 'heyo (' + str(player.x) + ',' + str(player.y))	


	# display some stuff about level effects maybe?
	#print ('word' + str(lev_set.effects))
	if 'waterlogged' in lev_set.effects:
		message('There must be a leak somewhere. This floor is waterlogged!', Color_Stat_Info)
	if 'cold' in lev_set.effects:
		message('Brrrr! It\'s so cold! You gain energy slowly', Color_Stat_Info)
		



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


	initialize_fov()


	enemy_spawn_rate = lev_set.enemy_spawn_rate
	spawn_timer = decide_spawn_time(enemy_spawn_rate,alarm_level)

	# Final thing... reset all the different event phases because otherwise you get some game-crashing bugs, especially involving things trying to remove themselves from lists they are no longer part of
	
	PreliminaryEvents = []
	MovementPhaseEvents = []
	AttackPhaseEvents = []
	DamagePhaseEvents = []
	MiscPhaseEvents = []
	FinalPreDrawEvents = []
	FinalPostDrawEvents = []


def next_level():
	global colorHandler
	global dungeon_level, objectsArray, game_state, current_big_message, lev_set, favoured_by_healer, favoured_by_destroyer, favoured_by_deliverer, tested_by_deliverer, enemy_spawn_rate, deliverer_test_count, time_level_started, elevators, alarm_level, key_count, currency_count, spawn_timer,  already_healed_this_level, player, player_weapon, upgrade_array, color_handler
	global SHOW_WEAPON_NAME, SHOW_ATTACK_COMMANDS, SHOW_WEAPON_WEIGHT, SHOW_WEAPON_DURABILITY, SHOW_ENERGY, SHOW_MOVE_COMMANDS, SHOW_JUMP_COMMAND, SHOW_TIME_ELAPSED, SHOW_CURRENT_FLOOR, SHOW_ALARM_LEVEL, SHOW_KEYS, SHOW_FAVOUR, SHOW_REINFORCEMENTS, SHOW_TOTAL_MONSTERS, SHOW_UPGRADES
	global 	PreliminaryEvents, MovementPhaseEvents, AttackPhaseEvents, DamagePhaseEvents, MiscPhaseEvents, FinalPreDrawEvents, FinalPostDrawEvents

	# doing some test saving
	save_game()


	#Go to the end screen if you just beat the final level woo!
	if lev_set.final_level is True:
		beat_game()	

	#moving to next level has affects for Taylor the Deliverer!
	if tested_by_deliverer and deliverer_test_count >= 0:
		favoured_by_deliverer = True




	# make a note of what elevator situation the player is in,
	# save a starting direction and position with elevator, if we can find such values
	start_ele_direction = None
	start_ele_spawn = None
	print ("player leaving level at" + str(player.x) + ", " + str(player.y))
	for ele in elevators:
		for i in range (len(ele.spawn_points)):
			(spawn_x, spawn_y) = ele.spawn_points[i]
			if spawn_x == player.x and spawn_y == player.y:
				#print("that's a bingo!")
				start_ele_direction = ele.direction
				start_ele_spawn = i


	#message("New ability: " + new_upgrade.name + ". " + new_upgrade.verbose_description, color_energy)


	# if leaving the tutorial, reset the players health + energy, and give them a fresh sword
	if dungeon_level == 0:
		print ("leaving tutorial, resetting player stats")
		player.fighter.hp = STARTING_ENERGY
		player.fighter.wounds = 0
		player_weapon = Weapon_Shiv()
		#player_weapon = Weapon_Hammer()
		#player_weapon = Weapon_Broom()
		#player_weapon = Weapon_Gun()
		#player_weapon = Weapon_Sai()
		#player_weapon = Weapon_Nunchuck()
		currency_count = STARTING_CURRENCY
		upgrade_array = []
	
		# Also reveal a bunch of UI stuff
		SHOW_WEAPON_NAME = True 
		SHOW_ATTACK_COMMANDS = True 
		SHOW_WEAPON_WEIGHT = True 
		SHOW_WEAPON_DURABILITY = True 
		SHOW_ENERGY = True 
		SHOW_MOVE_COMMANDS = True 
		SHOW_JUMP_COMMAND = True 
		SHOW_TIME_ELAPSED = True 
		SHOW_CURRENT_FLOOR = True 
		SHOW_ALARM_LEVEL = False 
		SHOW_KEYS = False 
		SHOW_FAVOUR = False 
		SHOW_REINFORCEMENTS = False 
		SHOW_TOTAL_MONSTERS = True
		SHOW_UPGRADES = False
		# give player a test upgrade?
		#new_upgrade = Get_Test_Upgrade()
		#upgrade_array.append(new_upgrade)



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



	lev_set = game_level_settings.get_setting(dungeon_level)

	# Update color scheme
	colorHandler = ColorHandler(lev_set.color_scheme)  #('adjustedOriginal')
	#print ('setting color scheme yO ' + lev_set.color_scheme)
	#colorHandler = ColorHandler(game_level)
	setColorScheme()


	#objects = []
	make_map(start_ele_direction, start_ele_spawn)
	objectsArray[player.x][player.y].append(player)
	worldEntitiesList.append(player)
	#print( 'heyo (' + str(player.x) + ',' + str(player.y))	


	# display some stuff about level effects maybe?
	#print ('word' + str(lev_set.effects))
	if 'waterlogged' in lev_set.effects:
		message('There must be a leak somewhere. This floor is waterlogged!', Color_Stat_Info)
	if 'cold' in lev_set.effects:
		message('Brrrr! It\'s so cold! You gain energy slowly', Color_Stat_Info)
		



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


	initialize_fov()


	enemy_spawn_rate = lev_set.enemy_spawn_rate
	spawn_timer = decide_spawn_time(enemy_spawn_rate,alarm_level)

	# Final thing... reset all the different event phases because otherwise you get some game-crashing bugs, especially involving things trying to remove themselves from lists they are no longer part of
	
	PreliminaryEvents = []
	MovementPhaseEvents = []
	AttackPhaseEvents = []
	DamagePhaseEvents = []
	MiscPhaseEvents = []
	FinalPreDrawEvents = []
	FinalPostDrawEvents = []

	# TODO: I bet there is a memory leak here and we should take pains to patch it up by maybe getting rid deleting all the things in the world except the player and maybe a special enely or two.

	




	#for ele in elevators:			#open the doors when the level starts?
	#	ele.set_doors_open(True)
	#DOESN'T WORK, SO YOU HAVE TO WAIT A TURN BEFORE THE DOORS OPEN. WHICH IS ANNOYING

	#current_big_message = "As you ascend the stairs, you inwardly breathe a sigh of relief. The trials of the floor below you are now in the past, but what dangers lie up ahead? Your enemies only seem to be getting more deadly the closer you get to your nemesis. You think back to the wise words of your mentor: \"Stick 'em with the pointy end.\""

	#game_state  = 'big message'


# Figure out how often enemies should spawn, based on overall rate for this floor, and the alarm level.
# Originally was just one divided by the other; now it's going to be something a bit more tierd, hopefully?
# Update: might have been my fault for not making it visible to the player, but I  wasn't really feeling the tiered drone.
# Going back to 'faster with higher alarm'; 
# I have some ideas about how to make it more exicitng to avoid alarms so am going to make alarm level more of a threat?
def decide_spawn_time(enemy_spawn_rate,alarm_level):
	temp_alarm_level = max(alarm_level, 1)
	return int(4*enemy_spawn_rate/temp_alarm_level)

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
	global upgrade_array
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
	elif name == 'scythe':
		new_weapon =  Weapon_Axe()
	elif name == 'katana':
		new_weapon =  Weapon_Katana()
	elif name == 'hammer':
		new_weapon =  Weapon_Hammer()
	elif name == 'trident':
		new_weapon =  Weapon_Trident()
	elif name == 'broom':
		new_weapon =  Weapon_Broom()
	elif name == 'pike':
		new_weapon =  Weapon_Pike()
	elif name == 'halberd':
		new_weapon =  Weapon_Halberd()
	elif name == 'shiv':
		new_weapon =  Weapon_Shiv()
	elif name == 'gun':
		new_weapon =  Weapon_Gun()
	elif name == 'ring of power':
		new_weapon =  Weapon_Ring_Of_Power()
	else:
		new_weapon = None

	if new_weapon is not None:
		new_weapon.max_charge = new_weapon.max_charge + bonus_max_charge

		# upgrades might affect weapon stats
		for power_up in upgrade_array:
			if getattr(power_up, "affect_weapon_on_creation", None) is not None:
				power_up.affect_weapon_on_creation(player, new_weapon)
	
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
	mouseover_text = '...'
	object = None
	if name == 'sword':
		char = 280#302
		mouseover_text = "A lightweight, short range, versatile weapon. Stabby stabby."
	elif name == 'dagger':
		char = 300
		mouseover_text = "Like a sword, if a sword was heavier and did more damage. Yes, this is the opposite of how things actually work."
	elif name == 'bo staff':
		char = 302
		mouseover_text = "Surprisingly good for what looks like a giant stick."		
	elif name == 'spear':
		char = 296
		mouseover_text = "A weapon with great reach but only in cardinal directions."	
	elif name == 'sai':
		char = 298
		mouseover_text = "Great for attacking two enemies at once, as long as they're not standing next to each other."	
	elif name == 'nunchaku':
		char = 313
		mouseover_text = "Easy to learn. Impossible to master."	
	elif name == 'scythe':
		char = 316
		mouseover_text = "Slow and destructive, like an overfilled shopping trolley."	
	elif name == 'katana':
		char = 'k'
		mouseover_text = "Flexibility. Precision. Rotational symmetry."
	elif name == 'hammer':
		char = 312
		mouseover_text = "I can't remember what the hammer does."
	elif name == 'trident':
		char = 283
		mouseover_text = "Everyone's favourite undersea weapon with three pointy bits."
	elif name == 'broom':
		char = 297
		mouseover_text = "Attacks three adjacent spaces in a cardinal direction. Great in crowds."
	elif name == 'pike':
		char = 299
		mouseover_text = "Great for attacking diagonally and nothing else."
	elif name == 'halberd':
		char = 301
		mouseover_text = "Long range only weapon. Equally terrifying for you and your opponent."
	elif name == 'shiv':
		char = 's'
		mouseover_text = "A lightweight, short range, versatile weapon."
	elif name == 'gun':
		char = 314
		mouseover_text = "A weapon of terrifying range."
	elif name == 'ring of power':
		char = 333
		mouseover_text = "Ancient weapon of mass destruction. Currently seeking new collaborators."
	object = Object(x, y, char, name, color_white, blocks=False, weapon = True, always_visible = True, mouseover = mouseover_text)
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
		#weapon_item.send_to_back()
		reorder_objects(weapon_x, weapon_y)


def drop_item(item):
	item_x = item.x
	item_y= item.y
	objectsArray[item_x][item_y].append(item)
	reorder_objects(item_x, item_y)

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


# display a message! but only if the player can see it
def localMessage(new_msg, x,y, color = default_text_color):		
	if fov_map.fov[x, y]:
		message(new_msg, color)

def message(new_msg, color = default_text_color):
	global game_time

	#print(str(color))

	msg_time = game_time

	# Turn hashtag shortcuts into actual key commands
	new_msg = translateCommands(new_msg)

	#split the message if necessary, among multiple lines
	new_msg_lines = textwrap.wrap(new_msg, MSG_WIDTH)

	for line in new_msg_lines:
		#if the buffer is full, remove the first line to make room for the new one
		if len(game_msgs) == MSG_HEIGHT:
			del game_msgs[0]

		#add the new line as a tuple, with the text and the color
		game_msgs.append( (line, color, msg_time) )


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
			#print ("Found hashtag " + command_substring)
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
	global game_level_settings
	global enemyArtHandler

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
	#translated_console_print_ex_center(pause_menu, SCREEN_WIDTH/2, 6, libtcod_BKGND_NONE, libtcod_CENTER,
	#"This is play number " + str(play_count))
	translated_console_print_ex_center(pause_menu, SCREEN_WIDTH/2, 6, libtcod_BKGND_NONE, libtcod_CENTER,
	VERSION_STRING)
	
	# add some stuff about the level effects here, for now
	translated_console_print_ex_center(pause_menu, SCREEN_WIDTH/2, 8, libtcod_BKGND_NONE, libtcod_CENTER, "Levels: ")
	temp_lev_num = 0
	current_line = 10		
	for temp_lev_num in range (1, len(game_level_settings.bigArray)-1):
		temp_lev_set = game_level_settings.bigArray[temp_lev_num]
		translated_console_print_ex_center(pause_menu, SCREEN_WIDTH/2, current_line, libtcod_BKGND_NONE, libtcod_CENTER, str(temp_lev_num) + " " + str(temp_lev_set.effects))
		current_line += 1


		# Display sprites of the enemies that will be in this level
		enemy_count = 0
		for (enemy_name, enemy_prob) in temp_lev_set.enemy_probabilities:
			(data_name, data_symbol, data_color, data_description) = enemyArtHandler.getEnemyArtData(enemy_name)


			#con.draw_char(self.x - x_offset, self.y - y_offset, self.char, bg=bg_color, fg = self.color)
			pause_menu.draw_char(int(SCREEN_WIDTH/2) + enemy_count, current_line, data_symbol, bg=None, fg = color_white) #, bg = libtcod_BKGND_NONE, fg = color_white)
			enemy_count += 2
			#translated_console_print_ex_center(pause_menu, SCREEN_WIDTH/2, current_line, libtcod_BKGND_NONE, libtcod_CENTER, str(enemy_name) + " ")
			
		current_line += 1


		current_line += 1


	#	translated_console_print_ex_center(pause_menu, SCREEN_WIDTH/2, current_line, libtcod_BKGND_NONE, libtcod_CENTER, str(temp_lev_num) + " " + str(temp_lev_set.enemy_probabilities))
	#	current_line += 1
	
		

	current_line += 1
	translated_console_print_ex_center(pause_menu, SCREEN_WIDTH/2, current_line, libtcod_BKGND_NONE, libtcod_CENTER,
	'-------------------------------------------------------')
	current_line += 2
	# Add a list of what upgrades the player has
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





def report_objects_here(args):  #FINALPREDRAW i think

		
		(x,y) = args
		# do some messages saying what you see here!
		#names = [obj.name for obj in objects
		#	if obj.x == player.x and obj.y == player.y and obj is not player]
		objects_here = [obj for obj in objectsArray[x][y]
			if obj is not player]
		names = [obj.name for obj in objects_here if obj.floor_message is None and obj.name is not 'water' and obj.name is not 'decoration'  and obj.name is not 'blood' and obj.name is not 'attack']  #todo: get a better way of not including certain objects in this list
		possible_commands = []

		weapon_found = False
		key_found = False
		favour_found = False
		plant_found = False
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
			if plant_found == False and obj.plant is not None:
				plant_found = True
			if stairs_found == False and obj.name == 'stairs':
				stairs_found = True
				possible_commands.append('< to ascend')
			if shrine_found == False and obj.shrine is not None:
				shrine_found = True
			if floor_message_found == False and obj.floor_message is not None:
				floor_message_text = obj.floor_message.string
				floor_message_found = True


		if weapon_found or key_found or favour_found or plant_found:	
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




def do_weapon_degradation():
	global player_hit_something, player_clashed_something
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
		


def render_all(render_mode = None):

	global fov_map, color_dark_wall, color_light_wall
	global color_dark_ground, color_light_ground, color_light_ground_alt
	global fov_recompute, bgColorArray
	global fontpath, spritepath



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
			con.draw_char(x + ACTION_SCREEN_X, y, ' ', fg=None, bg=color_fog_of_war)

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
						#if True: 	#temp making walls and such visible to check enemy behaviour/ navigation
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
						#if True:		#temp hack to test enemy navigation
							if object.name == 'water':
								#libtcod.console_set_char_background(con, object.x - x_offset, object.y - y_offset, water_background_color, libtcod_BKGND_SET )
								con.draw_char(object.x - x_offset, object.y - y_offset, None, fg = None, bg = water_background_color)
							if object.name == 'blood':
								# libtcod.console_set_char_background(con, object.x - x_offset, object.y - 	y_offset, blood_background_color, libtcod_BKGND_SET )
								con.draw_char(object.x - x_offset, object.y - y_offset, None, fg = None, bg = water_background_color)
							# ok but if there's attacks draw those instead
							for other_object in objectsArray[x][y]:
								if object is not other_object:
									if (object.attack is not None or ('attack' in object.tags and not object.deflected)) and other_object.fighter is not None:
										# libtcod.console_set_char_background(con, object.x - x_offset, object.y - y_offset, object.attack.faded_color, libtcod_BKGND_SET )
										#con.draw_char(object.x - x_offset, object.y - y_offset, None, fg = None, bg = object.attack.faded_color)
										con.draw_char(object.x - x_offset, object.y - y_offset, None, fg = None, bg = object.color)
							#Draw fire for things on fire
							if object.getting_burned or object.aflame:
								con.draw_char(object.x - x_offset, object.y - y_offset, None, fg = None, bg = fire_color)
				


						# DRAW ALL THE THINGS
						object.draw(render_mode = render_mode)
	
					# trying to add a pattern on empty space. This is buggy.
					#if len(objectsArray[x][y]) == 0:
					#	if fov_map.fov[x, y] == True and not map[x][y].blocked:
					#		con.draw_char(x - x_offset, y - y_offset, 305, bg=None, fg = default_decoration_color)

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
	#root_console.blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)
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
	global spawn_timer, total_monsters
	global SHOW_WEAPON_NAME, SHOW_ATTACK_COMMANDS, SHOW_WEAPON_WEIGHT, SHOW_WEAPON_DURABILITY, SHOW_ENERGY, SHOW_MOVE_COMMANDS, SHOW_JUMP_COMMAND, SHOW_TIME_ELAPSED, SHOW_CURRENT_FLOOR, SHOW_ALARM_LEVEL, SHOW_KEYS, SHOW_FAVOUR, SHOW_REINFORCEMENTS, SHOW_UPGRADES, SHOW_TOTAL_MONSTERS

	lev_set = game_level_settings.get_setting(dungeon_level)

	## Update color scheme
	#colorHandler = ColorHandler(lev_set.color_scheme)  #('adjustedOriginal')
	#setColorScheme()

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


	if SHOW_WEAPON_NAME:
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
	if SHOW_ATTACK_COMMANDS	:
		#attack_list = str(player_weapon.command_list)
		#libtcod.console_print_ex(panel, attack_panel_x, 3, libtcod_BKGND_NONE, libtcod_LEFT, "Attacks:")
		panel.draw_str(attack_panel_x, 3, "Attacks:", fg=attack_panel_default_color, bg=None)

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


	# Display weapon charge details.
	if SHOW_WEAPON_WEIGHT:
		#libtcod.console_print_ex(panel, attack_panel_x, 6, libtcod_BKGND_NONE, libtcod_LEFT,	'Weight: ' + str(player_weapon.get_default_usage_cost() + 1))
		panel.draw_str(int(attack_panel_x) , 6, 'Weight: ' + str(player_weapon.get_default_usage_cost() + 1), bg=None, fg=attack_panel_default_color)



	current_text_color = default_text_color
	if player_weapon.durability <= WEAPON_FAILURE_WARNING_PERIOD and player_weapon.durability > 0:
		#libtcod.console_set_default_foreground(panel, color_warning)
		current_text_color = color_warning
	elif player_weapon.durability <= 0:
		#libtcod.console_set_default_foreground(panel, color_big_alert)
		current_text_color = color_big_alert
	#libtcod.console_print_ex(panel, attack_panel_x, 7, libtcod_BKGND_NONE, libtcod_LEFT,
	#'Durability: ' + str(player_weapon.durability))
	if SHOW_WEAPON_DURABILITY:
		if player_weapon.combat_type != 'projectile':
			panel.draw_str(int(attack_panel_x) , 7, 'Durability: ' + str(player_weapon.durability), bg=None, fg=current_text_color)
		else:
			panel.draw_str(int(attack_panel_x) , 7, 'Ammo: ' + str(player_weapon.durability), bg=None, fg=current_text_color)

	#PLAYER PANEL STUFF

	#show the player's energy stats
	energy_color = color_energy
	non_energy_color = color_faded_energy
	wound_color = color_big_alert	
#	adrenaline_color = libtcod.green
#	non_adrenaline_color = libtcod.darker_green
#	if player.fighter.adrenaline_mode == False:
	#libtcod.console_print_ex(panel, player_panel_x, 1, libtcod_BKGND_NONE, libtcod_LEFT, "Energy:")

	if SHOW_ENERGY:
		panel.draw_str(player_panel_x, 1, "Energy:", bg=None, fg=default_text_color)
		for i in range(player.fighter.max_hp):

			if i <  player.fighter.hp:			
				translated_console_set_default_foreground(panel, energy_color)
				translated_console_print_ex(panel, player_panel_x + 7 + i, 1, libtcod_BKGND_NONE, libtcod_LEFT, '*')
			elif i < player.fighter.max_hp - player.fighter.wounds:
				translated_console_set_default_foreground(panel, non_energy_color)
				translated_console_print_ex(panel, player_panel_x + 7 + i, 1, libtcod_BKGND_NONE, libtcod_LEFT, '.')
			else:
				translated_console_set_default_foreground(panel, wound_color)
				translated_console_print_ex(panel, player_panel_x + 7 + i, 1, libtcod_BKGND_NONE, libtcod_LEFT, '\\')


			

	#render_bar(player_panel_x, 1, BAR_WIDTH, 'HP', player.fighter.hp, player.fighter.max_hp - player.fighter.wounds,
	#libtcod.light_red, libtcod.darker_red)

	#display some sweet moves!
	if SHOW_MOVE_COMMANDS:
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

	if SHOW_JUMP_COMMAND:
		translated_console_print_ex(panel, player_panel_x, 7, libtcod_BKGND_NONE, libtcod_CENTER, "Jump:   " + controlHandler.controlLookup["JUMP"])



	#LEVEL PANEL STUFF
	translated_console_set_default_foreground(panel, default_text_color)
	if SHOW_TIME_ELAPSED:
		translated_console_print_ex(panel, level_panel_x, 1, libtcod_BKGND_NONE, libtcod_LEFT,
		'Time:   ' + str(game_time))
	if SHOW_CURRENT_FLOOR:
		translated_console_print_ex(panel, level_panel_x, 2, libtcod_BKGND_NONE, libtcod_LEFT,
		'Floor:  ' + str(dungeon_level))
	if SHOW_ALARM_LEVEL:
		translated_console_print_ex(panel, level_panel_x, 3, libtcod_BKGND_NONE, libtcod_LEFT,
		'Alarm:  ' + str(alarm_level))
	if SHOW_KEYS:
		translated_console_print_ex(panel, level_panel_x, 4, libtcod_BKGND_NONE, libtcod_LEFT,
		'Keys:   ' + str(key_count) + '/' + str(lev_set.keys_required))
	if SHOW_FAVOUR:
		translated_console_print_ex(panel, level_panel_x, 5, libtcod_BKGND_NONE, libtcod_LEFT,
		'Favour: ' + str(currency_count))


	#testing testing
	#translated_console_print_ex(panel, level_panel_x, 7, libtcod_BKGND_NONE, libtcod_LEFT,
	#'Player action ' + str(player_action))
	if SHOW_REINFORCEMENTS:
		translated_console_print_ex(panel, level_panel_x, 7, libtcod_BKGND_NONE, libtcod_LEFT,
		'Reinforcements in ' + str(spawn_timer))



	if SHOW_TOTAL_MONSTERS == True:
		translated_console_print_ex(panel, level_panel_x, 8, libtcod_BKGND_NONE, libtcod_LEFT,
		'Enemies: ' + str(total_monsters))

#	if favoured_by_healer:
#		translated_console_print_ex(panel, level_panel_x + BAR_WIDTH/2, 8, libtcod_BKGND_NONE, libtcod_CENTER,
#		'Favoured by ' + god_healer.name)
#
#	elif favoured_by_destroyer:
#		translated_console_print_ex(panel, level_panel_x + BAR_WIDTH/2, 8, libtcod_BKGND_NONE, libtcod_CENTER,
#		'Favoured by ' + god_destroyer.name)
#
#	elif tested_by_destroyer:
#		translated_console_print_ex(panel, level_panel_x + BAR_WIDTH/2, 8, libtcod_BKGND_NONE, libtcod_CENTER,
#		'Tested by ' + god_destroyer.name + '(' + str(destroyer_test_count) + ')')
#
#	elif favoured_by_deliverer:	# actually for the deliverer you probably never get this message, right? If the mission is to complete level quickly?
#		translated_console_print_ex(panel, level_panel_x + BAR_WIDTH/2, 8, libtcod_BKGND_NONE, libtcod_CENTER,
#		'Favoured by ' + god_deliverer.name)
#
#	elif tested_by_deliverer:
#		translated_console_print_ex(panel, level_panel_x + BAR_WIDTH/2, 8, libtcod_BKGND_NONE, libtcod_CENTER,
#		'Tested by ' + god_deliverer.name + '(' + str(deliverer_test_count) + ')')

	#display names of objects under the mouse  #commenting out for now!
	#libtcod.console_set_default_foreground(panel, libtcod.light_gray)
	#libtcod.console_print_ex(panel, 1, 0, libtcod_BKGND_NONE, libtcod_LEFT, get_names_under_mouse())
	#translated_console_print_ex(panel, 1, 0, libtcod_BKGND_NONE, libtcod_LEFT, get_mouseover_text())





	# Surprise upgrade panel stuff!
	if SHOW_UPGRADES:
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
	
						translated_console_print_ex(panel, upgrade_panel_x + i*4, 3+j+upg_offset, libtcod_BKGND_NONE, 							libtcod_CENTER,	temp_upgrade.code)
	
	translated_console_set_default_foreground(panel, default_text_color)
	translated_console_set_default_background(panel, default_background_color)
				




	#blit the contents of "panel" to the root console
	#libtcod.console_blit(panel, 0, 0, SCREEN_WIDTH, PANEL_HEIGHT, 0, 0, PANEL_Y)
	root_console.blit(panel, 0, PANEL_Y, SCREEN_WIDTH, PANEL_HEIGHT, 0, 0)


# Here is where all the messages go
def create_message_panel():
	global game_time

	#GUI STUFF
	#prepare to render the GUI panel
	translated_console_set_default_background(message_panel, default_background_color)
	translated_console_clear(message_panel)	
	
	#print the game messages, one line at a time
	y = 0
	for (line, color, msg_time) in game_msgs:
		translated_console_set_default_foreground(message_panel, color)
		
		# highlight recent messages
		if msg_time >= game_time:
			translated_console_set_default_background(message_panel, color)
			translated_console_set_default_foreground(message_panel, default_background_color)
			

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
	global color_dark_wall, color_light_wall, color_dark_ground, color_light_ground, color_light_ground_alt, color_fog_of_war, default_altar_color, alt_altar_color, default_door_color, default_message_color, default_decoration_color, water_background_color, water_foreground_color, blood_background_color, blood_foreground_color, default_flower_color, default_weapon_color, fire_color
	global PLAYER_COLOR, color_swordsman, color_boman, color_rook, color_axe_maniac, color_tridentor, color_rogue, color_ninja, color_faerie, color_wizard, color_alarmer_idle, color_alarmer_suspicious, color_alarmer_alarmed
	global default_background_color, default_text_color, color_energy, color_faded_energy, color_warning, color_big_alert
	global 	Color_Message_In_World,	Color_Menu_Choice, Color_Not_Allowed, Color_Dangerous_Combat, Color_Interesting_Combat, Color_Boring_Combat, Color_Interesting_In_World, Color_Boring_In_World,	Color_Stat_Info, Color_Personal_Action, Color_Route_Guidance
	
	#print("i think it's " + colorHandler.colorScheme)

	levelColors = colorHandler.levelColors

	#print("i think walls are " + str(levelColors['color_light_wall']))
	
	color_dark_wall = levelColors['color_dark_wall']
	color_light_wall = levelColors['color_light_wall']
	color_dark_ground = levelColors['color_dark_ground']
	color_light_ground = levelColors['color_light_ground']
	color_light_ground_alt = levelColors['color_light_ground_alt']
	color_fog_of_war = levelColors['color_fog_of_war']
	default_altar_color = levelColors['default_altar_color']
	alt_altar_color = levelColors['alt_altar_color']
	default_door_color = levelColors['default_door_color']
	default_message_color = levelColors['default_message_color']
	default_decoration_color = levelColors['default_decoration_color']
	water_background_color = levelColors['water_background_color']
	water_foreground_color = levelColors['water_foreground_color']
	blood_background_color = levelColors['blood_background_color']
	blood_foreground_color = levelColors['blood_foreground_color']


	#print("now i think walls are " + str(color_light_wall))

	# collectiable e.g. weapons and plants and keys
	default_flower_color = levelColors['default_flower_color']
	default_weapon_color = levelColors['default_weapon_color']


	fire_color = levelColors['fire_color']


	# enemies, including player
	PLAYER_COLOR = levelColors['PLAYER_COLOR']
	color_swordsman = levelColors['color_swordsman']
	color_boman = levelColors['color_boman']
	color_rook = levelColors['color_rook']
	color_axe_maniac = levelColors['color_axe_maniac']
	color_tridentor = levelColors['color_tridentor']
	color_rogue = levelColors['color_rogue']
	color_ninja = levelColors['color_ninja']
	color_faerie = levelColors['color_faerie']
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
	Color_Route_Guidance = menuColors['Route_Guidance']		# Telling the player where to go, in particular when exits open


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
	global current_big_message, game_msgs, game_level_settings, dungeon_level, game_time, spawn_timer, player, player_weapon, objectsArray, game_state, player_action, con, enemy_spawn_rate, favoured_by_healer, favoured_by_destroyer, tested_by_destroyer,  favoured_by_deliverer, tested_by_deliverer,  god_healer, god_destroyer, god_deliverer, camera, alarm_level, already_healed_this_level, something_changed, upgrade_array, currency_count, controlHandler, colorHandler, control_scheme, enemyArtHandler
	global SHOW_WEAPON_NAME, SHOW_ATTACK_COMMANDS, SHOW_WEAPON_WEIGHT, SHOW_WEAPON_DURABILITY, SHOW_ENERGY, SHOW_MOVE_COMMANDS, SHOW_JUMP_COMMAND, SHOW_TIME_ELAPSED, SHOW_CURRENT_FLOOR, SHOW_ALARM_LEVEL, SHOW_KEYS, SHOW_FAVOUR, SHOW_REINFORCEMENTS, SHOW_TOTAL_MONSTERS, SHOW_UPGRADES
	global pathname
	current_big_message = 'You weren\'t supposed to see this'

	spawn_timer = 0

	# load stuff. yay, I'm testing loading and saving
	load_game()

	#Initialise controls
	controlHandler = ControlHandler(control_scheme)


	colorHandler = ColorHandler('lobbyTest')  #('adjustedOriginal')
	#colorHandler = ColorHandler('coldTest')  #('adjustedOriginal')
	#colorHandler = ColorHandler(game_level)


	# set up enemy graphics
	enemyArtHandler = EnemyArtHandler(pathname)

	# do a test ofEnemyArtHandmer
	#print("testing csv loading")
	#enemyArtHandler.getEnemyArtData("greenhorn")

	#create the list of game messages and their colors, starts empty
	game_msgs = []
	something_changed = True
	
	game_level_settings = Level_Settings()
	dungeon_level = 0	#SO HEY currently there is a game-crashing flaw on the first level because room_adjacencies is not properly initialised, that's great


	setColorScheme()

	alarm_level = 0 #1
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
	player = Object(0, 0, 256, 'player', PLAYER_COLOR, blocks=True, fighter=fighter_component, decider=decider_component, mouseover = "It's you! Our protagonist, engaged on a quest of dubious honor.")
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
	#player_weapon = Weapon_Gun()
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
	#print('howdy (' + str(player.x) + ',' + str(player.y))
	#for object in objectsArray[player.x][player.y]:
		#print(object.name)

	#the list of objects starting with the player
#	objects = [player]				#TODO/NOTE: When changing to 'objectsArray', this might cause problems?
							# Think it's enough to move this to after make_map(), and then use player's x and y
	
	initialize_fov()
	
	game_state = 'playing'
	player_action = None
	player_action_before_pause = None
	
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
		#print (str(Color_Interesting_In_World))





	# Decide which bits of GUI to show mouseover for


	SHOW_WEAPON_NAME = False
	SHOW_ATTACK_COMMANDS = False
	SHOW_WEAPON_WEIGHT = False
	SHOW_WEAPON_DURABILITY = False
	SHOW_ENERGY = False
	SHOW_MOVE_COMMANDS = True
	SHOW_JUMP_COMMAND = False
	SHOW_TIME_ELAPSED = True
	SHOW_CURRENT_FLOOR = False
	SHOW_ALARM_LEVEL = False 
	SHOW_KEYS = False
	SHOW_FAVOUR = False
	SHOW_REINFORCEMENTS = False
	SHOW_TOTAL_MONSTERS = False
	SHOW_UPGRADES = False




	#temporarily commenting out, WHICH IS AN EXTRA BAD IDEA
	#libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE,key,mouse)
	#print('6')
	render_all()
	translated_console_flush()




def get_info_panel_mouseover_text(x,y):

	global SHOW_WEAPON_NAME, SHOW_ATTACK_COMMANDS, SHOW_WEAPON_WEIGHT, SHOW_WEAPON_DURABILITY, SHOW_ENERGY, SHOW_MOVE_COMMANDS, SHOW_JUMP_COMMAND, SHOW_TIME_ELAPSED, SHOW_CURRENT_FLOOR, SHOW_ALARM_LEVEL, SHOW_KEYS, SHOW_FAVOUR, SHOW_REINFORCEMENTS, SHOW_TOTAL_MONSTERS, SHOW_UPGRADES
	global PANEL_HEIGHT, PANEL_WIDTH
	#global bottom_panel_mouseover_array
	#return_string = "Information Panel"
	#try :
	#	return_string = bottom_panel_mouseover_array[x][y]
	
	#except IndexError:
	#	return_string = "Information Panel, Out of Bounds Exception"
	#return return_string
#	return  "Information Panel (" + str(x) + "," + str(y) + ")"


	if x in range(SCREEN_WIDTH) and y in range(PANEL_HEIGHT):

# Produce an array describing the mouseover text for each part of the bottom "GUI" panel
#def initialise_panel_mouseover():
#	global bottom_panel_mouseover_array
#	global PANEL_HEIGHT, PANEL_WIDTH
	# First set default "Information Panel" text
#	bottom_panel_mouseover_array = [[ "Information Panel ("  + str(x) + "," + str(y) + ") YO"
#		for y in range(PANEL_HEIGHT) ]
#			for x in range(SCREEN_WIDTH)]
#
#	# Now modify speci
#	for y in range(PANEL_HEIGHT):
#		for x in range(SCREEN_WIDTH):
		mouseover_text = "Information Panel"

		if y > 0:
			# Weapon Subpanel
			if x <= 21:
				# -- Weapon Name --
				if y <= 2 and SHOW_WEAPON_NAME:
					mouseover_text = "Your weapon: " + player_weapon.name + " [Uses " + str(player_weapon.default_usage +1) + " energy, does " + str(player_weapon.default_attack_strength) + " damage]. "	#Ideally a pithy summary goes here...

				# -- Attack Commands --
				elif y <= 5 and SHOW_ATTACK_COMMANDS:
					mouseover_text = "Attack Commands: Press these keys to attack. (Attacking uses " + str(player_weapon.default_usage + 1) + " energy)"

				# -- Weapon Weight --
				elif y <= 6 and SHOW_WEAPON_WEIGHT:
					mouseover_text = "Weapon Weight: Attacking with " + player_weapon.name + " costs this much energy. (You can always attack when at max energy.)"

				# -- Weapon Durability --
				elif y <= 7 and SHOW_WEAPON_DURABILITY:
					mouseover_text = "Weapon Durability: Reduces by 1 when you hit something, and by 2 when your attack clashes off another attack. When it reaches 0, your weapon breaks."
		

			# Player Subpanel
			elif x <= 41:
				# -- Health and Energy--	
				if y <= 2 and SHOW_ENERGY:
					mouseover_text = "Energy: Attacking, jumping and getting hit uses up energy. Otherwise, energy recharges by 1 each turn. Getting hit also reduces max energy. When your max energy reaches 0, you die."
					# -- Energy Bar (which is its own thing) --
					if y == 1 and x >= 29 and x <= 38:
						mouseover_text = "Energy Bar"
						energy_index = x - 29
						if energy_index < player.fighter.hp:
							mouseover_text = "Available Energy: This is spent when you attack (" + str(player_weapon.default_usage + 1) +" energy) or jump (" + str(player.fighter.jump_recharge_time) + " energy). Recharges by 1 each turn."
						elif energy_index < player.fighter.max_hp - player.fighter.wounds:
							mouseover_text = "Consumed Energy: This will recharge by 1 each turn."
						else: 
							mouseover_text = "Wound: You take wounds whenever you get hit. Each wound reduces your maximum energy by 1. When your maximum energy reaches 0, you die. Wounds can be healed by picking up fruit."




				# -- Movement Commands -- 
				elif y <= 5 and SHOW_MOVE_COMMANDS:
					mouseover_text =  translateCommands("Movement Commands: Press these keys to move, or #STANDSTILL# to stand still.")

				# -- Jump Command --
				elif y == 7 and SHOW_JUMP_COMMAND:
					mouseover_text = "Jump Command: Press this key to jump 2 spaces in any direction (uses " + str(player.fighter.jump_recharge_time) + " energy)."
							


			# Level info subpanel
			elif x <= 55:
				
				# -- Time Elapsed --
				if y == 1 and SHOW_TIME_ELAPSED:
					mouseover_text = "Time Elapsed"

				# -- Current Floor --
				elif y == 2 and SHOW_CURRENT_FLOOR:
					mouseover_text = "Current Floor"

				# -- Alarm Level --
				elif y == 3 and SHOW_ALARM_LEVEL:
					mouseover_text = "Alarm Level: Higher level means more enemies. Increases by 2 when a security drone becomes alert. Destroying an alert security drone reduces alarm level by 1. Destroying all drones reduces it to 0."

				# -- Keys Gathered / Required --
				elif y == 4 and SHOW_KEYS:
					mouseover_text = "Keys Gathered / Required: Collect enough keys on this floor to gain access to the next floor. Keys are often held or guarded by security drones. "

				# -- Favour --
				elif y == 5 and SHOW_FAVOUR:
					mouseover_text = "Favour: Can be exchanged at shrines for powerful upgrades. Get favour tokens by destroying security drones."



				# -- Reinforcements timer   (split across this and the upgrades panel, for reasons) --
				elif y == 7 and SHOW_REINFORCEMENTS:
					mouseover_text = "Reinforcements Timer: More enemies will arrive when this reaches 0. Enemies are also summoned whenever the alarm level is raised."

				elif y == 8 and SHOW_TOTAL_MONSTERS:
					mouseover_text = "Enemies: The total number of enemies currently in the level."


			# Upgrades subpanel  (to fix up properly later)
			else:
				if y >= 1 and y <= 6 and SHOW_UPGRADES:
					mouseover_text = "Upgrades Panel: Powerful upgrades to help you in your quest. Upgrades can be purchased at shrines in exchange for Favour."
					# Figure out which index of upgrade the mouse is hovering over
					# First figure out the index valu mod 3.
					upgrade_number = 0
					if x > 60 and x <= 63:
						upgrade_number = 1
					elif x > 63:
						upgrade_number = 2
					# Then add the requisite multiple of 3, based on y value and also number of upgrades (because upgrades get moved around a bit based on how many there are)	
					upgrade_count = len(upgrade_array)	
					upg_offset = 0
					if upgrade_count > 15 and upgrade_count < 22:
						upg_offset = 1
					elif upgrade_count >= 22:
						upg_offset = 2
					upgrade_number += (3*(y-3 + upg_offset))
			
					# Get details of the upgrade with specified index, if it exists.
					if upgrade_number >= 0 and upgrade_number < len(upgrade_array):
						mouseover_text = upgrade_array[upgrade_number].name.capitalize() + ": " + upgrade_array[upgrade_number].tech_description








				# -- Reinforcements timer   (split across this and the level info panel, for reasons) --
				elif y == 7 and SHOW_REINFORCEMENTS:
					mouseover_text = "Reinforcements Timer: More enemies will arrive when this reaches 0. Enemies are also summoned whenever the alarm level is raised."
						

		#bottom_panel_mouseover_array[x][y] = mouseover_text
		return mouseover_text

	else:
		return "Information Panel, Out of Bounds Exception"





# See if all  player attakcs hit something (and update upgrades that care about that, if they exist)
def checkForPlayerAttackAccuracy():
	global all_player_attacks_on_target, worldAttackList, upgrade_array

	# check how many enemies the player has hit, and 
	# check if the player is getting 'hit' (whether or not the attack gets deflected)

	all_player_attacks_on_target = True		# thing to test whether all player attacks hit
	#print("'fied' CHECKING IF PLAYER GOT HIT")
	for attack in worldAttackList:	# just do checks on player attacks
		if attack.attacker == player:
			this_attack_on_target = False
			for object in objectsArray[attack.x][attack.y]:
				if object.blocks or object.fighter:	# check if this attack hit a blocky thing (like a door) or a fighter
					this_attack_on_target = True
			if not this_attack_on_target:
				all_player_attacks_on_target = False
	#	attackee = object.find_attackee()
	#	if attackee == player:
	#		player_got_hit = True
	#	elif object.attack.attacker == player:
	#		if attackee is not None:
	#			number_hit_by_player += 1
	#		else:
	#			all_player_attacks_on_target = False

	#if all_player_attacks_on_target:
	#	message("attacks on target")
	#else:
	#	message("whiff")


	# Update relevant upgrades
	for power_up in upgrade_array:
		if getattr(power_up, "update_based_on_player_accuracy", None) is not None:
			power_up.update_based_on_player_accuracy(all_player_attacks_on_target)
								




def doGlobalPreliminaryEvents():
	global 	game_time, spawn_timer,	player_hit_something, player_clashed_something, player_got_hit,	player_just_jumped, player_just_attacked, number_hit_by_player, sloMoAttack
	global player, nearest_points_array, worldEntitiesList, nearest_center_to_player


	game_time += 1
	spawn_timer -= 1
	update_nav_data()
	player_hit_something = False
	player_clashed_something = False
	player_got_hit = False
	player_just_jumped = False
	number_hit_by_player = 0
	player_just_attacked = False
	sloMoAttack = False

	if nearest_points_array[player.x][player.y] is not None:
		nearest_center_to_player =  nearest_points_array[player.x][player.y]




	# LET'S PROCES SOME DECISIONS, WHICH BASICALLY ARE THE STARTING POINTS FOR ALL EVENTS 
	#player stuff comes first
	player.createActionEventDetails()
	player.decider.processDecisions()
	for ob in worldEntitiesList:
		if ob is not player:
			ob.createActionEventDetails()
			if ob.decider:
				ob.decider.processDecisions()



	return





def doGlobalPreDrawPhaseEvents():
	global SHOW_WEAPON_NAME, SHOW_ATTACK_COMMANDS, SHOW_WEAPON_WEIGHT, SHOW_WEAPON_DURABILITY, SHOW_ENERGY, SHOW_MOVE_COMMANDS, SHOW_JUMP_COMMAND, SHOW_TIME_ELAPSED, SHOW_CURRENT_FLOOR, SHOW_ALARM_LEVEL, SHOW_KEYS, SHOW_FAVOUR, SHOW_REINFORCEMENTS, SHOW_TOTAL_MONSTERS, SHOW_UPGRADES
	global  level_complete, ready_for_next_level
	global player_just_attacked, player_got_hit, player_just_jumped, cold_energy_parity, upgrade_array, number_hit_by_player
	global time_since_last_elevator_message
	global alarm_level, worldArrowsList

	#FINALPREDRAW
	# Reveal parts of the UI based on some early-game triggers. Another part where I don't know where it goes.
	if (not SHOW_WEAPON_NAME or not SHOW_ATTACK_COMMANDS) and player_weapon.name is not 'unarmed':
		SHOW_WEAPON_NAME = True
		SHOW_ATTACK_COMMANDS = True
	if (not SHOW_ENERGY or not SHOW_WEAPON_WEIGHT) and (player.fighter.hp < STARTING_ENERGY - 4  or player.fighter.wounds > 0 or player.y <= 45):
		SHOW_WEAPON_WEIGHT= True
		SHOW_ENERGY = True
	if not SHOW_WEAPON_DURABILITY and (player_weapon.durability <= 30):
		SHOW_WEAPON_DURABILITY = True
	# TODO Don't know how to handle showing JUmp commands yet!
	if not SHOW_JUMP_COMMAND and player.y <= 24:
		SHOW_JUMP_COMMAND = True
	if not SHOW_CURRENT_FLOOR and dungeon_level > 0:
		SHOW_CURRENT_FLOOR = True
	if not SHOW_ALARM_LEVEL and alarm_level > 0:
		SHOW_ALARM_LEVEL = True
	if not SHOW_KEYS and key_count > 0:
		SHOW_KEYS = True
	if not SHOW_FAVOUR and currency_count > 0:
		SHOW_FAVOUR = True
	if not SHOW_REINFORCEMENTS and alarm_level > 0:
		SHOW_REINFORCEMENTS = True
	if not SHOW_TOTAL_MONSTERS and alarm_level > 0:
		SHOW_TOTAL_MONSTERS = True
	if not SHOW_UPGRADES and len(upgrade_array) > 0:
		SHOW_UPGRADES = True


	#UPDATE THE UPGRADES THAT AFFECT PLAYER STATS ONCE AND THEN STOP; I'M NOT SURE WHERE ELSE TO PUT THIS	
	for power_up in upgrade_array:
		if getattr(power_up, "upgrade_player_stats_once", None) is not None:
			power_up.upgrade_player_stats_once(player)
		if getattr(power_up, "upgrade_player_weapon_once", None) is not None:
			power_up.upgrade_player_weapon_once(player, player_weapon)
		if getattr(power_up, "update_based_on_level", None) is not None:
			power_up.update_based_on_level(dungeon_level)


	# refresh the player's energy
	# design question: when should this refresh? maybe it's only if you haven't done an attack? if you haven't been hurt?
	if (player_just_attacked == False and player_got_hit == False and player_just_jumped == False):


		recharge_rate = 1  			#by default

		# if it's cold, recharging happens at half usual speed.
		if 'cold' in lev_set.effects:	
			if cold_energy_parity == 0:
				cold_energy_parity = 1
			else:
				cold_energy_parity = 0
			recharge_rate = cold_energy_parity

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
	


	# FINALPREDRAW
	do_weapon_degradation()






	# finalpredraw?
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
		# update elevators with whether the player is authorized - for now this is just based on whether there are security drones around.
	# later this process will become a bit more complicated (and might be folded into Elevator.update)
	level_complete = False
	if lev_set.boss is not None:
		level_complete = True
		#check for bosses?
		#print ("CHECKING FOR BOSSES")
		for object in worldEntitiesList:
			#for object in objects:
			if object.name == lev_set.boss:
				level_complete = False



	#finalpostdraw?
	#elif number_security_drones <= 0:
	#	level_complete = True
	elif lev_set.keys_required <= key_count:
		level_complete = True
	if level_complete is True:
		for ele in elevators:
			if not ele.player_authorised:
				ele.set_player_authorisation(True)

	for ea in worldArrowsList:
		ea.update(level_complete)




	spotted = False

	# FINALPOSTDRAW? AND ALSO FINALPREDRAW? Kind of split up via some decision mecahnism
	#UPDATE THE ALARMERS AND OTHER THINGS
#	print ("'fixed' UPDATING ALARMERS AND OTHER THINGS")
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
		# alaso update the dispensers???
		elif 'listener' in ob.tags:
			ob.update()

	if temp_alarm_countdown < large_count_down_val:
		message(str(temp_alarm_countdown) + " seconds from being recognized.", Color_Stat_Info)



	#UPDATE THE PLANTS
	#	if ob.plant is not None:
	#		ob.plant.update()
	#		ob.name = ob.plant.name	#hey this is probably not the most efficient way to do this
	#		ob.char = ob.plant.symbol



	# FINALPREDRAW

	# Now do alarm soundings! and other alarmer-based stuff
#	for ob in objects:
#	print ("'fixed' UPDATING ALARMERS")	
	for ob in worldEntitiesList:
		if ob.alarmer is not None:
		#prev_suspicious = (ob.alarmer.status == 'suspicious')	# ugh what horrible code
			# first, update the alarmer
	
			#ob.alarmer.update(libtcod.map_is_in_fov(fov_map, ob.x, ob.y))
			# next, do things depending on the alarmer's state
			if ob.alarmer.status == 'idle' or  ob.alarmer.status == 'pre-suspicious':
				#ob.color = ob.alarmer.idle_color
				ob.char = ob.alarmer.idle_char
			elif ob.alarmer.status == 'suspicious':
				if ob.alarmer.prev_suspicious == False:
					message('The ' + ob.name + ' is suspicious!', Color_Interesting_In_World)	
					#ob.color = ob.alarmer.suspicious_color
					ob.char = ob.alarmer.suspicious_char
			elif ob.alarmer.status == 'raising-alarm':
				#alarm_level += ob.alarmer.alarm_value
				spawn_timer = 1		#run the  spawn clock forwards so new enemies appear
				message('The ' + ob.name + ' sounds a loud alarm!', Color_Interesting_In_World)
				#ob.color = ob.alarmer.alarmed_color
				ob.char = ob.alarmer.alarmed_char
			elif ob.alarmer.status == 'alarm-raised':
				#ob.color =  color_alarmer_alarmed #ob.alarmer.alarmed_color	
				ob.char = ob.alarmer.alarmed_char




def doGlobalPostDrawPhaseEvents():
	global garbage_list
	global  ready_for_next_level
	global spawn_timer


	# reset upgrade statuses to 'dormant' ? this is probably not where this goes...
	for upgrade in upgrade_array:
		upgrade.status = 'dormant'


	#FINALPOSTDRAW
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

	#PROB GOES IN FINALPOSTDRAW SINCE IT'S TO DO WITH LEVEL SPAWNING?
	# oh let's start creating enemies at random intervals? 
	#if alarm_level > 0 and spawn_timer % (enemy_spawn_rate/alarm_level) == 0: #and number_security_drones > 0:
	if alarm_level > 0 and spawn_timer <= 0:
		#reset timer
		spawn_timer = decide_spawn_time(enemy_spawn_rate,alarm_level)
	#	reorder_objects() #temp test
	#	print('tick')
	#	print('enemy spawn rate = ' + str(enemy_spawn_rate))
	#	print('total enemy prob = ' + str(lev_set.total_enemy_prob))
	#	print('enemy probabilites = ' + str( lev_set.enemy_probabilities))
#		for (x,y) in spawn_points:

		# check if level is complete
		level_complete = False
		if lev_set.boss is not None:
			level_complete = True
			#check for bosses?
#			for object in objects:
#			print ("'fixed' CHECKING FOR BOSS AGAIN")
			for object in worldEntitiesList:
				if object.name == lev_set.boss:
					level_complete = False
		#elif number_security_drones <= 0:
		#	level_complete = True
		elif lev_set.keys_required <= key_count:
			level_complete = True



		

		# are there too many monsters?
		total_monsters = 0
#				for object in objects:
#				print ("'fixed' COUNTING MONSTERS")
		for object in worldEntitiesList:
			if object.fighter is not None and object.name != 'strawman' and object.name != 'flailing strawman' and object.name != 'strawman on wheels':
				total_monsters = total_monsters + 1

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
#							print('tick' + str(x) + ',' + str(y) + ' ' + name)
							monster = create_monster(x,y, name)
							objectsArray[x][y].append(monster)
							worldEntitiesList.append(monster)
							break
						else:
							num -= prob



	# do decisions??? at this point??? or after garbage collection???????
	for ob in worldEntitiesList:
		#if ob.name == 'fire':
		#ob.createActionEventDetails()
		if ob.decider:
			ob.decider.decide()


	# Also do garbage collection stuff because the previous phase mostly probably involved deleting stuff
	for object in garbage_list:
		#print ('deleting ' + object.name + '...')
		if object in objectsArray[object.x][object.y]:
			objectsArray[object.x][object.y].remove(object)				#TODO NOTE: Think this should work the usual way? i.e objectarray[x][y].remove...
		if object in worldEntitiesList:
			worldEntitiesList.remove(object)
		if object in worldAttackList:
			worldAttackList.remove(object)
		if object.progenitor is not None:
			object.progenitor.progency.remove(object)
	#reset garbage list
	garbage_list = []




	#FINALPREDRAW
	# finally... go to the next level maybe?
	if ready_for_next_level == True:
		ready_for_next_level = False
		next_level()
		# also we do a special one-off drawing of everything
		nav_data_changed = True
		initialize_fov()		# this is ok, right? update the field of view stuff
		fov_recompute = True
		render_all()
		translated_console_flush()
		print("hey i just drew everything on level change")

###############################################

#		MAIN METHOD FOLLOWS	

###############################################




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
#sprite_choice = 'terminal16x16plusSprites.png'
sprite_choice = 'terminal16x16Current.png'

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
spritepath = os.path.join(pathname,  sprite_choice)
print ('font file = ' + fontpath)
libtcod.set_font(spritepath, greyscale=True, altLayout=False)



#libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)
#tdl version
root_console = libtcod.init(SCREEN_WIDTH, SCREEN_HEIGHT, title='Sword Dancer')

# tdl version
con = libtcod.Console(MAP_WIDTH, MAP_HEIGHT)
panel = libtcod.Console(SCREEN_WIDTH, PANEL_HEIGHT)
message_panel = libtcod.Console(SCREEN_WIDTH, MESSAGE_PANEL_HEIGHT)
pause_menu = libtcod.Console(SCREEN_WIDTH, SCREEN_HEIGHT)
mouse_panel = libtcod.Console(SCREEN_WIDTH, 3)
#con = libtcod.console_new(MAP_WIDTH, MAP_HEIGHT)
#panel = libtcod.console_new(SCREEN_WIDTH, PANEL_HEIGHT)
#message_panel = libtcod.console_new(SCREEN_WIDTH, MESSAGE_PANEL_HEIGHT)
#pause_menu = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

translated_console_set_default_background(mouse_panel, Color_Mouseover_Background)
translated_console_set_default_foreground(mouse_panel, Color_Mouseover_Foreground)


# cutting out mouse stuff for now, because it hasn't worked in a while.
# may come back to it once i have everything working with tdl. but for now, it's not worth porting faulty code
# mouse = libtcod.Mouse()
mouse = None
global mouse_coord_x
global mouse_coord_y
mouse_coord_x = 5
mouse_coord_y = 0
#TEMP COMMENTING OUT OH GOD
#key = libtcod.Key()
key = None



PreliminaryEvents = []
MovementPhaseEvents = []
AttackPhaseEvents = []
DamagePhaseEvents = []
MiscPhaseEvents = []
FinalPreDrawEvents = []
FinalPostDrawEvents = []


#TEMP COMMENTING OUT OH GOD
# libtcod.sys_set_fps(LIMIT_FPS) 

initialise_game()

# initialise_panel_mouseover()

lev_set = game_level_settings.get_setting(dungeon_level)

# Update color scheme
colorHandler = ColorHandler(lev_set.color_scheme)  #('adjustedOriginal')
setColorScheme()

enemy_spawn_rate = lev_set.enemy_spawn_rate
spawn_timer = decide_spawn_time(enemy_spawn_rate,alarm_level)

time_since_last_elevator_message = 0

ready_for_next_level = False

libtcod.set_fps(LIMIT_FPS)

# So for future reference, this code prints the numbers 1 to 9:
#for num in range(1,10):
#	print str(num)

internal_loop_count = 0


# hear is a thing to keep track of yay
cold_energy_parity = 0










garbage_list = []




# Main loop!
while not translated_console_is_window_closed():


#	garbage_list = []	#list of things (e.g. dead bodies) to delete from objects list at the end of the loop

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
			elif event.type == 'MOUSEMOTION' and game_state == 'playing':			
				(temp_x, temp_y) = event.cell
				mouse_coord_x =temp_x
				mouse_coord_y =temp_y
				#print(mouse_coord)
				#currency_count = currency_count  + 1

				# print mouseover text for this part of the screen
				mouse_panel.clear()
				mouseover_text = get_mouseover_text()
				translated_console_print_ex(mouse_panel, 1, 0, libtcod_BKGND_NONE, libtcod_LEFT, mouseover_text)



				#blit the contents of "message_panel" to the root console
				#libtcod.console_blit(message_panel, 0, 0, SCREEN_WIDTH, MESSAGE_PANEL_HEIGHT, 0, 0, 0)
				# libtcod.console_blit(message_panel, 0, 0, MESSAGE_PANEL_WIDTH, MESSAGE_PANEL_HEIGHT, 0, 0, 0)
				root_console.blit(mouse_panel, 0, 0, SCREEN_WIDTH, 3, 0, 0)


				translated_console_flush()
		
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
		if game_state == 'playing':
			game_state = 'paused'
		elif game_state == 'control screen':
			game_state = 'paused'	
		elif game_state == 'paused' or game_state == 'big message':
			game_state = 'playing'
			player_action = player_action_before_pause
	#	break


	# Game things happen woo!
	elif game_state == 'playing' and player_action != 'didnt-take-turn' and  player_action != 'invalid-move' and player_action != 'pickup_dialog' and player_action != 'upgrade-shop-dialog-sales-pitch' and player_action != 'upgrade-shop-dialog-catalog'  and player_action != 'upgrade-shop-dialog-confirm' and player_action != 'jump_dialog' :
		
		

		#PREILIMINARYPHASE

	#	print(str(mouse_coord_x))






	#	potential_open_list = []





		#MOVEMENTPHASE ALSO

		# actually before movement happens, let's have things picking up things
		# todo: integrate the player pickup stuff into this 
	#	mover_list = []
	#	for object in worldEntitiesList:
	#		if object.decider and object is not player:
	#			if object.decider.decision is not None:
	#				if object.decider.decision.pickup_decision:
	#					# for now, all we're doing is checking for plants to pickup
	#					for other_object in objectsArray[object.x][object.y]:	
	#						if other_object.plant is not None:
	#							other_object.plant.tread()
	#							garbage_list.append(other_object)
	#							# also I guess get health maybe???
	#							if object.fighter and object is not player:
	#								message('The ' + object.name + ' picks up the ' + other_object.name + ' and eats it.', Color_Personal_Action)
	#								other_object.plant.harvest(object)



		#MOVEMENTPHASE

		# firstly movement happens
		# player always moves first
	#	if player.decider:
	#		if player.decider.decision is not None:
	#			if player.decider.decision.move_decision is not None:
	#				md = player.decider.decision.move_decision
	#				if map[player.x + md.dx][player.y + md.dy].blocked:
	#					message ("You walk into a wall.", Color_Personal_Action)
	#	# TEMP COMMENT		player.move(md.dx, md.dy)
	#			elif player.decider.decision.jump_decision is not None:
	#				jd = player.decider.decision.jump_decision
	#				# Check for things between the player and where they want to be,
	#				# and see if they are things that block the player or can be jumped over.
	#				# For now, assumes all jumps are of length 2;
	#				# Will need to be changed if different jumps come in.
	#				tempx = 0
	#				if jd.dx == -2:
	#					tempx = -1
	#				elif jd.dx == 2:
	#					tempx = 1
	#				tempy = 0
	#				if jd.dy == -2:
	#					tempy = -1
	#				elif jd.dy == 2:
	#					tempy = 1
	#				somethingInWay = False
	#				jumpee = None		#The thing you're jumping over...
	#				if player.fighter.jump_available() == False:
	#					message("Your legs are too tired to jump!", Color_Not_Allowed )
	#				elif map[player.x + tempx][player.y + tempy].blocked:
	#					somethingInWay = True
	#					message("There's a wall in the way!!!", Color_Not_Allowed )
	#				else: 
	#					#check for doors, and/or find the thing the player is jumping over.
	#					for ob in objectsArray[player.x + tempx][player.y + tempy]:
	#						if ob.door:
	#							somethingInWay = True
	#						if ob.fighter:
	#							jumpee = ob	
	#						if ob.name == 'fire' and jumpee is None:
	#							jumpee = ob
	#					if somethingInWay == True:
	#						message("There's a door in the way!", Color_Not_Allowed )
	#				if somethingInWay == False:
	#					if map[player.x + jd.dx][player.y + jd.dy].blocked:
	#						message ("You leap gracefully into a wall.", Color_Personal_Action)
	#		# TEMP COMMENT			player.move(tempx, tempy)
	#					else:
	#						if jumpee is not None:
	#							if ob.name == 'fire':
	#								message ("You leap through the flames!", Color_Personal_Action)
	#							else:
	#								message ("You leap over the " + jumpee.name + "\'s head!", Color_Personal_Action)
	#					player.fighter.make_jump()
	#		# TEMP COMMENT		player.move(jd.dx, jd.dy)
	#					player_just_jumped = True
	



			#	# check for player trampling plants. This is not where it should go...
			#	for other_object in objectsArray[player.x][player.y]:	
			#		if other_object.plant is not None:
			#			other_object.plant.tread()
			#			# also I guess get health maybe???
			#			other_object.plant.harvest(player)
			#			garbage_list.append(other_object)



		#MOVEMENTPHASE


	 	# move other objects.
		# first, make a list of objects to move (because naively going through objectsArray and moving everything at each grid reference can lead to objects getting moved multiple times
		
#		print ("'FIXED'  GETTING LIST OF MOVERS")
#		mover_list = []
#		for object in worldEntitiesList:
#			if object.decider and object is not player:
#				if object.decider.decision is not None:
#					if object.decider.decision.move_decision is not None:
#						mover_list.append(object)
#
#
#
#		currentMovementPhaseEvents = list(MovementPhaseEvents)
#		MovementPhaseEvents = []		#clear these events so new things can be added
#		for (function, argset) in currentMovementPhaseEvents:
#			if function is not None:
#				function(argset)
#		render_all()
#		translated_console_flush()


				



		




#		# MOVEPHASE i guess?
#		# draw things in their new places
#		if player.decider.decision:
#			if player.decider.decision.move_decision or player.decider.decision.jump_decision:			
#				fov_recompute = True


#		clear_onscreen_objects()


#		translated_console_set_default_foreground(con, default_text_color)
#		#temporarily commenting out, WHICH IS AN EXTRA BAD IDEA
#		#libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE,key,mouse)
#		#print('1')
#		render_all()
#		translated_console_flush()
#
#		#put in a pause before drawing the other stuff?
#		time.sleep(0.05)







	# Thinks this should be redundant now
	#	#MOVEMENTPHASE! I have decreed it
	#	# now do door openings!
	#	for (opener, victim) in potential_open_list:
	#		if victim.door is not None:
	#			#print "opening door"
	# TEMP COMMENT		victim.door.open()
	#			# Here is another terrible hack, to make it so an alarmer actually spots you when you open a door on it
	#			# libtcod.map_compute_fov(fov_map, player.x, player.y, TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)
	#			fov_map.compute_fov(player.x, player.y, fov=FOV_ALGO, radius=TORCH_RADIUS, light_walls=FOV_LIGHT_WALLS)






		#if spotted == True:
		#	print "Alarmage status: spotted"
		#else: 
		#	print "Alarmage status: NOT spotted"

		# now create attacks!
		# MOVING : REDOING THIS STUFF, SHOULD BE DONE ON A PER-FIGHTER BASIS IN THE makeAttacks method of decider object

		#deletionList = []
##		print ("'fixed'  CREATING ATTAKS")
#		for object in worldEntitiesList:
#			if object.decider:
#				if object.decider.decision is not None:
#					if object.decider.decision.attack_decision is not None:
#						attack_list = object.decider.decision.attack_decision.attack_list
#						for attack_object in attack_list:
#						#for attack in attack_list:
#							try:
#								attack_data = attack_object.attack
#								attack = ModernAttack(x = attack_object.x, y = attack_object.y, color = attack_object.color, attacker = attack_data.attacker, damage = attack_data.damage)		#very tempt hack hopefully
#								objectsArray[attack.x][attack.y].append(attack)	
#								worldAttackList.append(attack)
#								attack.send_to_front()
#							except IndexError:		#todo: check that this is the right thing to catch...
#								print('')










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



# TODO this is commented out for maybe being the cause of 'double hitting'. 
# We'll see if it causes something else to break. I'm not really sure that this 'player_just_attacked' thing is going to be necessary ultimately
#		player_just_attacked = False
#		if player.decider.decision is not None:
#			if player.decider.decision.attack_decision is not None:
#				player_attack_list = player.decider.decision.attack_decision.attack_list
#				if len(attack_list) > 0:
#					player_just_attacked = True






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
		render_all(render_mode = 'attack-step')
		translated_console_flush()
		#put in a pause before drawing the other stuff?
		#time.sleep(0.05)

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

		











		# temp terrible hack
		#player_clashed_something = True


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



		#a COmbination of Phase types I think?  ATTACKPHASE / DAMAGEPHASE at the least?
		## regular old attacks just happening
		#deletionList = []
#		for object in objects:
#		print ("'fixed'  YMAKING ATTACKS HAPPEN")

		# ANOTHER THING I AM COMMENTING OUT BECAUSE I THINK IT'S REDUNDANT, BUT WHOOO KNOWS
#		for object in worldAttackList:
#			x = object.x
#			y = object.y
#			if object.attack:
#				# Increase attack strengths from upgrades. whoof; this is a bit cycle hungry
#				for power_up in upgrade_array:
#					if getattr(power_up, "affect_strength_of_individual_attack", None) is not None:
#						power_up.affect_strength_of_individual_attack(player, object)
#				object.attack.inflict_damage()
#				object.attack.fade()
#				# todo fix??? to make attack highlighting work properly. I commented out these lines and added a reorder. I am scared that this is secretly going to break something
##				if object.attack.existing == False:
##					deletionList.append(object)






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



		# MiscPhase? or actually this probably doesn't need to be the game any more?

		#recharge player attack charge. this probably shouldn't go here ultimately
		#if player_recharge_time > 0:
		#	player_recharge_time = player_recharge_time - 1
		player_weapon.recharge(player.fighter.recharge_rate)
	





			


		




		# FINALPOSTDRAW?? I thinnk garbage collection should mostly happen once at end of all the other stuff,
		# Attack deletion might have to happen in between? But hopefully it can mostly be handled by attacks themselves?

		# clean up stuff
		for object in garbage_list:
			#print ('deleting ' + object.name + '...')
			if object in objectsArray[object.x][object.y]:
				objectsArray[object.x][object.y].remove(object)				#TODO NOTE: Think this should work the usual way? i.e objectarray[x][y].remove...
			if object in worldEntitiesList:
				worldEntitiesList.remove(object)
			if object in worldAttackList:
				worldAttackList.remove(object)
			if object.progenitor is not None:
				object.progenitor.progency.remove(object)
		#reset garbage list
		garbage_list = []
		







		










	




		# How we expect object types to go:
		# PreliminaryEvents
		# 	MovementPhaseEvents
		# 		AttackPhaseEvents
		#		 DamgePhaseEvents
		# 		MiscPhaseEvents
		# FinalPreDrawEvents
		# FinalPostDrawEvents



		#PreliminaryEvents = []
		#MovementPhaseEvents = []
		#AttackPhaseEvents = []
		#DamgePhaseEvents = []
		#MiscPhaseEvents = []
		#FinalPreDrawEvents = []
		#FinalPostDrawEvents = []

		#super_cool_action_event_list = []

		# Do some  fire spreading maybe? This is mainly just as a test.
		#spreading_fire_list = []





		#for fire in spreading_fire_list: 
		#	fire.spread()

		# MOre events queue stuff






		#print("Phase: prelim")
		#print(str(objectsArray[13][61]))

		# Do preliminary phase stuff
		doGlobalPreliminaryEvents()
		# Do (non-global) preliminary events
		currentPreliminaryEvents = list(PreliminaryEvents)
		PreliminaryEvents = []
		for (function, argset) in currentPreliminaryEvents:
			if function is not None:
				function(argset)







		loop_count_sanity_check = 0

		# Loop through movement phase and attack phase (and damage phase and 'misc' phase) until they are all processed
		while(len(MovementPhaseEvents) + len(AttackPhaseEvents) + len(AttackPhaseEvents) + len(DamagePhaseEvents)  + len(MiscPhaseEvents) > 0 and loop_count_sanity_check < 500):

			# Movement phase stuff is treated separately from the other events, and goes first
			while (len(MovementPhaseEvents) > 0  and loop_count_sanity_check < 500):
				loop_count_sanity_check += 1

		
				#print("Phase: movement")
				#print(str(objectsArray[13][61]))
				# Clear out the current list of movement phase events and process them
				# Movement events can trigger other movements, which will be processed on the next go through the loop
				currentMovementPhaseEvents = list(MovementPhaseEvents)
				MovementPhaseEvents = []		#clear these events so new things can be added
				for (function, argset) in currentMovementPhaseEvents:
					if function is not None:
						function(argset)
	
				render_all()
				translated_console_flush()	
		#		if len(currentMovementPhaseEvents) > 0:				
					#put in a pause before drawing the other stuff?
					#time.sleep(frame_pause)
				if sloMoAttack:				
					#put in a pause before drawing the other stuff?
					print("TIMATTAKCPAUS")
					time.sleep(frame_attack_pause)
		
		
			


			# After the movement phase is cleared we handle the other events. Once they are done, more movement events may have been triggered, in which case we start the loop over
			while(len(AttackPhaseEvents) + len(DamagePhaseEvents)  + len(MiscPhaseEvents) > 0 and loop_count_sanity_check < 500):
	
				loop_count_sanity_check += 1
	

				#print("Phase: attack")
				#print(str(objectsArray[13][61]))
				# Process Attack phase events		(things hitting/attacking)
				currentAttackPhaseEvents = list(AttackPhaseEvents)
				#print(str(currentAttackPhaseEvents))
				AttackPhaseEvents = []		#clear these events so new things can be added
				for (function, argset) in currentAttackPhaseEvents:
					if function is not None:
						#print("Phase: mid-attack")
						#print(str(objectsArray[13][61]))
						function(argset)
	
				render_all()
				translated_console_flush()
		#		if len(currentAttackPhaseEvents) > 0:	
		#			if len(DamagePhaseEvents) > 0:			
						# do a longer pause if attacks are doing damage???
						#time.sleep(frame_attack_pause)
		#			else:
						#time.sleep(frame_pause)
	
					
				#print("Phase: damage")	
				#print(str(objectsArray[13][61]))	

				# Process Damage Phase Events		(things getting damaged by attacks)
				currentDamagePhaseEvents = list(DamagePhaseEvents)
				DamagePhaseEvents = []
				for (function, argset) in currentDamagePhaseEvents:
					if function is not None:
						function(argset)
	
				render_all()
				translated_console_flush()
		#		if len(currentDamagePhaseEvents) > 0:				
					#put in a pause before drawing the other stuff?
					#time.sleep(frame_pause)
	

				#print("Phase: misc")
				#print(str(objectsArray[13][61]))
	
				# Process Misc Phase events		(other stuff in response to damage e.g. chain reactions)
				currentMiscPhaseEvents = list(MiscPhaseEvents)
				MiscPhaseEvents = []
				for (function, argset) in currentMiscPhaseEvents:
					if function is not None:
						function(argset)
	
				render_all()
				translated_console_flush()	
		#		if len(currentMiscPhaseEvents) > 0:				
					#put in a pause before drawing the other stuff?
					#time.sleep(frame_pause)

		if loop_count_sanity_check >= 500:
			print("warning! Attack Phase/ Misc Phase looped over 500 times")




		#print("Phase: predraw")
		# Final pre-draw phase
		currentFinalPreDrawEvents = list(FinalPreDrawEvents)
		FinalPreDrawEvents = []
		for (function, argset) in currentFinalPreDrawEvents:
			if function is not None:
				function(argset)
		# Also do a few things I didn't want to fit into this framework really
		doGlobalPreDrawPhaseEvents()





		# Do the final draw of this turn
		render_all()
		translated_console_flush()


		#print("Phase: postdraw")
		#print(str(objectsArray[13][61]))
		# Final post-draw phase
		currentFinalPostDrawEvents = list(FinalPostDrawEvents)
		FinalPostDrawEvents = []
		for (function, argset) in currentFinalPostDrawEvents:
			if function is not None:
				function(argset)
		# Also do a few things I didn't want to fit into this framework really
		doGlobalPostDrawPhaseEvents()





	elif game_state == 'playing' and player_action == 'pickup_dialog' or player_action == 'upgrade-shop-dialog-sales-pitch' or player_action == 'upgrade-shop-dialog-catalog' or player_action == 'upgrade-shop-dialog-confirm':
		render_all()
		translated_console_flush()


	elif game_state == 'playing' and player_action == 'jump_dialog':
		render_all()
		translated_console_flush()


	# I think this goes here: want to draw stuff if there's a "you can't do that" message
	elif game_state == 'playing' and player_action == 'invalid-move':
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















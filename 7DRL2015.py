import libtcodpy as libtcod
import math
import textwrap
from weapons import Weapon_Sword, Weapon_Staff, Weapon_Spear, Weapon_Dagger, Weapon_Strawhands, Weapon_Sai, Weapon_Sai_Alt, Weapon_Nunchuck, Weapon_Axe, Weapon_Katana, Weapon_Hammer, Weapon_Wierd_Sword, Weapon_Wierd_Staff, Weapon_Ring_Of_Power
from levelSettings import Level_Settings
from levelGenerator import Level_Generator
from gods import God, God_Healer, God_Destroyer, God_Deliverer

SCREEN_WIDTH = 70
SCREEN_HEIGHT = 39
CAMERA_FOCUS_WIDTH = 8
CAMERA_FOCUS_HEIGHT = 8

LIMIT_FPS = 20

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
elif ControlMode == 'Crypsis':
	ATTCKUPLEFT	 = 'a'
	ATTCKUP		 = 'z'
	ATTCKUPRIGHT	 = 'e'
	ATTCKRIGHT	 = 'd'
	ATTCKDOWNRIGHT	 = 'c'
	ATTCKDOWN	 = 'x'
	ATTCKDOWNLEFT	 = 'w'
	ATTCKLEFT	 = 'q'


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

JUMP = 'r'


# and now here are some  3-character forms of these string names, to make AI code more readable.
# it's gonna use QWERTY-specific terms (like aQa for ATTCKUPLEFT), just because that makes 
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

DEFAULT_JUMP_RECHARGE_TIME = 5		#40


#color_dark_wall = libtcod.Color(0, 0, 100)
#color_dark_ground = libtcod.Color(50, 50, 150)
color_dark_wall = libtcod.Color(100, 100, 100)
color_dark_ground = libtcod.Color(150, 150, 150)

# FOV algorithm stuff
FOV_ALGO = 0  #default FOV algorithm
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 50 #20

max_nav_data_loops = 1


color_dark_wall = libtcod.Color(100,100,100)		#(0, 0, 100)
color_light_wall = libtcod.Color(130, 110, 50)
color_dark_ground = libtcod.Color(150,150,150)		#(50, 50, 150)
color_light_ground = libtcod.Color(200, 180, 50)
color_fog_of_war = libtcod.black
default_weapon_color = libtcod.grey
default_altar_color = color_light_wall
default_message_color = color_light_wall
default_decoration_color = libtcod.Color(250,230,50)		#(165,145,50)

#sizes and coordinates relevant for the GUI
BAR_WIDTH = 20
PANEL_HEIGHT = 9
#MESSAGE_PANEL_HEIGHT = 4
MESSAGE_PANEL_HEIGHT = 30
MESSAGE_PANEL_WIDTH = 25
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT

MSG_X = BAR_WIDTH + 2
#MSG_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
#MSG_WIDTH = SCREEN_WIDTH-2
#MSG_HEIGHT = MESSAGE_PANEL_HEIGHT
MSG_WIDTH = MESSAGE_PANEL_WIDTH-2
MSG_HEIGHT = MESSAGE_PANEL_HEIGHT-1

class Object:
	#this is a generic object: the player, a monster, an item, the stairs...
	#it's always represented by a character on screen.
	def __init__(self, x, y, char, name, color, blocks=False, always_visible=False, fighter=None, decider=None, attack=None, weapon = False, shrine = None, floor_message = None, door = None, currently_invisible = False, alarmer = None, drops_key = False):  #raising_alarm = False):
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
		self.currently_invisible = currently_invisible	# I am introducing this as a hack 
								#to make elevator doors go away. Instead of actually going away, 									#they'll be made invisible, not blocking and not blocking light
								# (different from being invisible). Video games!
		#self.raising_alarm = raising_alarm
		self.alarmer = alarmer
		self.drops_key = drops_key

	def move(self, dx, dy):
		if not is_blocked(self.x + dx, self.y + dy):
			#move by the given amount
		        self.x += dx
		        self.y += dy


	def draw(self):
		global camera

		#x_offset = camera.x-SCREEN_WIDTH/2
		x_offset = camera.x-(SCREEN_WIDTH + MESSAGE_PANEL_WIDTH)/2
		#y_offset = camera.y-SCREEN_HEIGHT/2
		y_offset = camera.y-(SCREEN_HEIGHT-PANEL_HEIGHT)/2
		#only show if it's visible to the player; or it's set to "always visible" and on an explored tile
		# also don't draw it if it's set to 'currently invisible'

		#if True:	# temporary hack to test enemy naviation
		if (libtcod.map_is_in_fov(fov_map, self.x, self.y) or (self.always_visible and map[self.x][self.y].explored)) and not self.currently_invisible:
			#set the color and then draw the character that represents this object at its position
			libtcod.console_set_default_foreground(con, self.color)
			libtcod.console_put_char(con, self.x - x_offset, self.y - y_offset, self.char, libtcod.BKGND_NONE)

	def clear(self):
		global camera

		x_offset = camera.x-(SCREEN_WIDTH + MESSAGE_PANEL_WIDTH)/2
		#y_offset = camera.y-SCREEN_HEIGHT/2
		y_offset = camera.y-(SCREEN_HEIGHT-PANEL_HEIGHT)/2
		#erase the character that represents this object
		libtcod.console_put_char(con, self.x-x_offset, self.y - y_offset, ' ', libtcod.BKGND_NONE)

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

	def send_to_almost_back(self):
		#make this object be drawn just above the decorations but below all other objects.
		global objects, decoration_count
		objects.remove(self)
		objects.insert(decoration_count, self)

	def send_to_front(self):
		#make this object be drawn last, so all others appear below it if they're in the same tile.
		global objects
		objects.remove(self)
		objects.append(self)



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
	def __init__(self, god):
		self.god = god
		self.visited = False
	
	def visit(self):
		self.visited = True


class Floor_Message:
	def __init__(self, string):
		self.string = string


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

	def open(self):		#normal doors can't be closed after opening, Just one of those things
		message('The door opens', libtcod.white)

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


class Fighter:
	#combat-related properties and methods (monster, player, NPC).
	def __init__(self, hp, defense, power, death_function=None, attack_color = libtcod.white, faded_attack_color = libtcod.white, extra_strength = 0, recharge_rate = 1, bonus_max_charge = 0, jump_array = [], jump_recharge_time = DEFAULT_JUMP_RECHARGE_TIME):
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
		


class Energy_Fighter:
	# combat-related properties and methods (player).
	# trying out an exciting new 'energy system'. Use energy to attack and to jump, energy gradually recharges, but getting hit reduces your energy semi-permanently, and you die if you lose more energy than you have.
	def __init__(self, hp, defense, power, death_function=None, attack_color = libtcod.white, faded_attack_color = libtcod.white, extra_strength = 0, recharge_rate = 1, bonus_max_charge = 0, jump_array = [], jump_recharge_time = DEFAULT_JUMP_RECHARGE_TIME):
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

	def take_damage(self, damage):
		#apply damage if possible
		if damage > 0:
			self.hp -= damage
			#check for death. if there's a death function, call it
			if self.hp <= 0:
				function = self.death_function
				if function is not None:
					function(self.owner)
			#add wounds!
			self.wounds += damage
			if self.wounds > self.max_hp:
				self.wounds = self.max_hp

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

	#check if the energy fighter has enough energy to make an attack
	def can_attack(self, energy_cost):
		if self.hp >= energy_cost:
			return True
		else:
			return False

	#lose the required amount of energy, down to a minimum of 0
	def lose_energy(self, energy_cost):
		if energy_cost > 0:
			self.hp -= energy_cost
			if self.hp <= 0:
				self.hp = 0

	#lose the required amount of energy, down to a minimum of 0
	def gain_energy(self, energy_amount):
		if energy_amount > 0:
			self.hp += energy_amount
			if self.hp > self.max_hp - self.wounds:
				self.hp = self.max_hp - self.wounds
	
	# check if any of the jumps in the array are at 0. If so, they are available.
	def jump_available(self):
		if self.hp >= self.jump_recharge_time:
			return True
		else:
			return False
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
	def __init__(self, alarm_time = 3, pre_alarm_time = 1, alarm_value = 2, dead_alarm_value = 1, idle_color = libtcod.dark_blue, suspicious_color = libtcod.white, alarmed_color = libtcod.dark_red):
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
				self.status = 'alarm-raised'
			# if self.status = 'alarm-raised', don't do anything

		else:
			#if self.status =='idle', keep doing what you're doing
			if self.status == 'suspicious' or self.status == 'pre-suspicious':
				self.status = 'idle'	# false alarm, go back to sleep
			elif self.status ==  'raising-alarm':
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
	def __init__(self, weapon, guard_duty  = False, attack_dist = 1):
		self.recharge_time = 0
		self.stunned_time = 0
		self.weapon = weapon
		if self.weapon is not None:
			self.weapon.owner = self
		self.guard_duty = guard_duty		# monsters on 'guard duty' don't come looking for you
		self.attack_dist = attack_dist

	def decide(self):
		#a basic monster takes its turn. If you can see it, it can see you
		decider = self.owner
		monster = decider.owner #yaaay
		# only do thing (including weapon recharge? maybe not) if not stunned
		if self.stunned_time <= 0:
			
			# if you can't see the player, go where you think the player is
			if not libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

				# but only go looking if you're not on guard duty!
				if self.guard_duty == False:
					(dx,dy) = Head_Towards_Players_Room(monster.x, monster.y)
					if is_blocked(monster.x+dx, monster.y+dy) == False:
						decider.decision = Decision(move_decision=Move_Decision(dx,dy))

			else:	
				#As we've now spotted the player, stop being on guard duty
				self.guard_duty = False
				# ok first question. where is the player and how do we get to them?
				dx = 0
				dy = 0



				#move towards player if far away
				if monster.distance_to(player) >= self.attack_dist + 1:

					(dx,dy) = Move_Towards_Visible_Player(monster.x, monster.y)
					decider.decision = Decision(move_decision=Move_Decision(dx,dy))

				

				#close enough, attack! (if the player is still alive.)
				elif player.fighter.hp > 0 and self.weapon.current_charge >= self.weapon.default_usage:#   recharge_time <= 0:
					attackList = []

					(dx,dy) = next_step_towards(monster.x, monster.y, player.x, player.y)
					
					# and now we manually code what keys the monster would press based on where they want to attack.
					# yes, this isn't great code design. It's a 7drl, deal with it.
					if dx == 0 and dy == -1:
						abstract_attack_data = self.weapon.do_attack(ATTCKUP)
					elif dx == 1 and dy == -1:
						abstract_attack_data = self.weapon.do_attack(ATTCKUPRIGHT)
					elif dx == 1 and dy == 0:
						abstract_attack_data = self.weapon.do_attack(ATTCKRIGHT)
					elif dx == 1 and dy == 1:
						abstract_attack_data = self.weapon.do_attack(ATTCKDOWNRIGHT)
					elif dx == 0 and dy == 1:
						abstract_attack_data = self.weapon.do_attack(ATTCKDOWN)
					elif dx == -1 and dy == 1:
						abstract_attack_data = self.weapon.do_attack(ATTCKDOWNLEFT)
					elif dx == -1 and dy == 0:
						abstract_attack_data = self.weapon.do_attack(ATTCKLEFT)
					elif dx == -1 and dy == -1:
						abstract_attack_data = self.weapon.do_attack(ATTCKUPLEFT)
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
			if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
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
			if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):


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
							num  = libtcod.random_get_int(0, 0, 2)
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
							num  = libtcod.random_get_int(0, 0, 2)
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
#						num  = libtcod.random_get_int(0, 0, 2)
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
			if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

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
							num  = libtcod.random_get_int(0, 0, 2)
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
			if not libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

				# but only if you're not on guard duty!
				if self.guard_duty == False:
					(dx,dy) = Head_Towards_Players_Room(monster.x, monster.y, rook_moves = True)
					if is_blocked(monster.x+dx, monster.y+dy) == False:
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
				elif player.fighter.hp > 0 and self.weapon.current_charge >= self.weapon.default_usage:#   recharge_time <= 0:
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




class Strawman_on_wheels_AI:
	def __init__(self, weapon):
		self.recharge_time = 0
		self.stunned_time = 0
		self.weapon = weapon
		if self.weapon is not None:
			self.weapon.owner = self
		num  = libtcod.random_get_int(0, 0, 4)
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
				num =  libtcod.random_get_int(0, 0, 2) 
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
			num =  libtcod.random_get_int(0, 0, 2) 
			if num == 0:
				return (dx,0)
			else:
				return(0,dy)
		else:
			return (0,0)

	elif dy!= 0 and dx == 0:
		# if trying to move vertically, try going left or right instead
		num =  libtcod.random_get_int(0, 0, 2) 
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
		num =  libtcod.random_get_int(0, 0, 2) 
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
			choice =  libtcod.random_get_int(0, 0, len(movement_options)-1)
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
			for target in objects:
				if target.x == self.owner.x and target.y == self.owner.y:
					if target.fighter is not None:
						if self.attacker is not None:
							if target is player:
								message('The ' + self.attacker.name.capitalize() + ' hits!', libtcod.red)	
							elif self.attacker is player:
								message('You hit the ' + target.name.capitalize() + '!')
								player_hit_something = True	
							else:
								message('The ' + self.attacker.name.capitalize() + ' hits the ' + target.name.capitalize() + '!')
				
						libtcod.console_set_char_background(con, target.x, target.y, self.faded_color, libtcod.BKGND_SET)
						target.fighter.take_damage(self.damage)
#					if target.name == 'security system':
#						if target.raising_alarm is False:
#							target.raising_alarm = True
#							alarm_level += 2
#							message('The security system sounds a loud alarm!')
#							# Let's also run the spawn clock forwards so a fresh wave of enemies arrives
#							spawn_timer = 1	#This is not always working as I'd like???
					elif target.door is not None and target.name != 'elevator door':
						libtcod.console_set_char_background(con, target.x, target.y, self.faded_color, libtcod.BKGND_SET)
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
			for target in objects:
				if target.fighter and target.x == self.owner.x and target.y == self.owner.y:
					return target




def process_nearest_center_points():
	global center_points, nearest_points_array
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
	if current_x > 0 and nav_data[current_x-1][current_y][center_number] ==  nav_data[current_x][current_y][center_number] and not is_blocked(current_x-1, current_y) and rook_moves == True:
		temp_array.append((-1,0))
	if current_x < MAP_WIDTH-1 and nav_data[current_x+1][current_y][center_number] ==  nav_data[current_x][current_y][center_number]and not is_blocked(current_x+1, current_y)and rook_moves == True:
		temp_array.append((1,0))
	if current_y > 0 and nav_data[current_x][current_y-1][center_number] ==  nav_data[current_x][current_y][center_number]and not is_blocked(current_x, current_y-1) and rook_moves == True:
		temp_array.append((0, -1))
	if current_y < MAP_HEIGHT-1 and nav_data[current_x][current_y+1][center_number] ==  nav_data[current_x][current_y][center_number]and not is_blocked(current_x, current_y+1) and rook_moves == True:
		temp_array.append((0,1))

	# if multiple options, pick one at random. If no options, stay where we are
	if len(temp_array) > 0:
		num =  libtcod.random_get_int(0, 0, len(temp_array)-1)
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
				num =  libtcod.random_get_int(0, 0, 1)
				if num == 0:
					dx = 0
				elif num == 1:
					dy = 0
			
	return(dx, dy)


		


def get_names_under_mouse():
	global mouse
	#return a string with the names of all objects under the mouse
	(x, y) = (mouse.cx, mouse.cy)

	#create a list with the names of all objects at the mouse's coordinates and in FOV
	names = [obj.name for obj in objects
		if obj.x == x and obj.y == y 
		and libtcod.map_is_in_fov(fov_map, obj.x, obj.y)]			#temporarily forgetting this bit for bugfixing
		#]
	names = ', '.join(names)  #join the names, separated by commas
	return names.capitalize()



# MAIN CONTROL HANDLING METHOD WOO

def handle_keys():
	global fov_recompute, keys, stairs, player_weapon, game_state, player_action, player_just_attacked, favoured_by_healer, favoured_by_destroyer, tested_by_destroyer,  favoured_by_deliverer, tested_by_deliverer,  destroyer_test_count, deliverer_test_count, time_level_started, key_count, already_healed_this_level

	# key = libtcod.console_wait_for_keypress(True)
	if key.vk == libtcod.KEY_ENTER and key.lalt:
	#Alt+Enter: toggle fullscreen
		libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

	elif key.vk == libtcod.KEY_ESCAPE:
		return 'pause' #exit game

	if game_state == 'big message':
		if key.vk != 0:
			game_state = 'playing'

	elif game_state == 'end message':
		if key.vk != 0:
			game_state = 'end data'


	elif game_state == 'end data':
		if key.vk != 0:
			game_state = 'restartynscreen'

	elif game_state == 'restartynscreen':
		key_char = chr(key.c) 
		if key_char == 'n':
			game_state='exit'
		elif key_char == 'y':
			restart_game()

		

	elif game_state == 'paused':
		key_char = chr(key.c) 
		if key_char == 'q':
			game_state='exit'

	elif game_state == 'dead':
		key_char = chr(key.c)
		if key_char == 'r':
			restart_game()
		elif key_char == 'q':
			game_state='exit'

	
	elif player_action == 'pickup_dialog':
		key_char = chr(key.c)
		#print str(key.vk)
		keynum = key.vk - 34	#yay magic number:
		weapons_found = []
		for object in objects:
			if object.x == player.x and object.y == player.y and object.weapon == True: 
				weapons_found.append(object)		
		if keynum >= 1 and keynum <= len(weapons_found):
			new_weapon = get_weapon_from_item(weapons_found[keynum-1], player.fighter.bonus_max_charge)
			old_weapon = get_item_from_weapon(player_weapon)
			player_weapon = new_weapon
			objects.remove(weapons_found[keynum-1])
			# let's try that you don't drop your weapon, you throw it away entirely so you can't pick it up later.
			#drop_weapon(old_weapon)
			weapon_found = True
			message('You throw away your ' + old_weapon.name + ' and pick up the ' + new_weapon.name) 
		elif key.vk != 0:
			game_state = 'playing'
			message('Never mind.')
			#keynum = key
			#print str(libtcod.KEY_KP7)		# hang on... 41 is 7. So... 35 is 1, right? blah - 34
			return 'didnt-take-turn'

		else:
			return 'pickup_dialog'

	elif player_action == 'jump_dialog':
		key_char = chr(key.c)
		# jump direction options
		if key.vk == libtcod.KEY_KP7 or key.vk == libtcod.KEY_HOME or key_char == 't':
			player.decider.set_decision(Decision(jump_decision=Jump_Decision(-2,-2)))
		elif key.vk == libtcod.KEY_KP8 or key.vk == libtcod.KEY_UP or key_char == 'y':
			player.decider.set_decision(Decision(jump_decision=Jump_Decision(0,-2)))
		elif key.vk == libtcod.KEY_KP9 or key.vk == libtcod.KEY_PAGEUP or key_char == 'u':
			player.decider.set_decision(Decision(jump_decision=Jump_Decision(2,-2)))
		elif key.vk == libtcod.KEY_KP2 or key.vk == libtcod.KEY_DOWN or key_char == 'n':
			player.decider.set_decision(Decision(jump_decision=Jump_Decision(0,2)))
		elif key.vk == libtcod.KEY_KP1 or key.vk == libtcod.KEY_END or key_char == 'b':
			player.decider.set_decision(Decision(jump_decision=Jump_Decision(-2,2)))
		elif key.vk == libtcod.KEY_KP4 or key.vk == libtcod.KEY_LEFT or key_char == 'g':
			player.decider.set_decision(Decision(jump_decision=Jump_Decision(-2,0)))
		elif key.vk == libtcod.KEY_KP3 or key.vk == libtcod.KEY_PAGEDOWN or key_char == 'm':
			player.decider.set_decision(Decision(jump_decision=Jump_Decision(2,2)))
		elif key.vk == libtcod.KEY_KP6 or key.vk == libtcod.KEY_RIGHT or key_char == 'j':
			player.decider.set_decision(Decision(jump_decision=Jump_Decision(2,0)))
		#elif key.vk == libtcod.KEY_KP5 or chr(key.c) == '.' or key_char == 'h':	
		#	message('You  perfectly still.')
		#game_state = 'playing'
		elif key.vk != 0:
			game_state = 'playing'
			message('You stand paralyzed by indecision or maybe bad programming!.')	#TODO probably change this message
		else: 
			return 'jump_dialog'

	elif game_state == 'playing':
		key_char = chr(key.c)
		#print "walk!"
		#movement keys
		if key.vk == libtcod.KEY_KP7 or key.vk == libtcod.KEY_HOME or key_char == 't':
			player.decider.set_decision(Decision(move_decision=Move_Decision(-1,-1)))
		elif key.vk == libtcod.KEY_KP8 or key.vk == libtcod.KEY_UP or key_char == 'y':
			player.decider.set_decision(Decision(move_decision=Move_Decision(0,-1)))
		elif key.vk == libtcod.KEY_KP9 or key.vk == libtcod.KEY_PAGEUP or key_char == 'u':
			player.decider.set_decision(Decision(move_decision=Move_Decision(1,-1)))
		elif key.vk == libtcod.KEY_KP2 or key.vk == libtcod.KEY_DOWN or key_char == 'n':
			player.decider.set_decision(Decision(move_decision=Move_Decision(0,1)))
		elif key.vk == libtcod.KEY_KP1 or key.vk == libtcod.KEY_END or key_char == 'b':
			player.decider.set_decision(Decision(move_decision=Move_Decision(-1,1)))
		elif key.vk == libtcod.KEY_KP4 or key.vk == libtcod.KEY_LEFT or key_char == 'g':
			player.decider.set_decision(Decision(move_decision=Move_Decision(-1,0)))
		elif key.vk == libtcod.KEY_KP3 or key.vk == libtcod.KEY_PAGEDOWN or key_char == 'm':
			player.decider.set_decision(Decision(move_decision=Move_Decision(1,1)))
		elif key.vk == libtcod.KEY_KP6 or key.vk == libtcod.KEY_RIGHT or key_char == 'j':
			player.decider.set_decision(Decision(move_decision=Move_Decision(1,0)))
		elif key.vk == libtcod.KEY_KP5 or chr(key.c) == '.' or key_char == 'h':	
			message('You stand perfectly still.')
			pass

		else:
			#test for other keys
			key_char = chr(key.c)

			# picking up a new weapon
			if key_char == 'p':
				weapons_found = []
				weapon_found = False
				keys_found = []
				for object in objects:
					if object.x == player.x and object.y == player.y and object.weapon == True: 
						weapons_found.append(object)
					if object.x == player.x and object.y == player.y and object.name == 'key': 
						keys_found.append(object)
				#keys take priority over weapons. I'm just calling it. Would rather not make the submenu happen.
				if len(keys_found) > 0:
					message('You snatch up the key.')
					key_count = key_count + len(keys_found)
					for ki in keys_found:
						objects.remove(ki)	
			#STILL TODO KEEP A KEY COUNT AND MAKE IT AFFECT ELEVATOR OPENING
				elif len(weapons_found) == 1:
					new_weapon = get_weapon_from_item(weapons_found[0], player.fighter.bonus_max_charge)
					old_weapon = get_item_from_weapon(player_weapon)
					player_weapon = new_weapon
					objects.remove(weapons_found[0])
					# let's try that you don't drop your weapon, you throw it away entirely so you can't pick it up later.
					#drop_weapon(old_weapon)
					weapon_found = True
					message('You throw away your ' + old_weapon.name + ' and pick up the ' + new_weapon.name) 
				elif len(weapons_found) == 0:
				#if weapon_found == False:
					message('Nothing to pick up')
					return 'didnt-take-turn'	
				else:	
					message_string = ('Pick up what? (')
					count = 1
					for weapon_item in weapons_found:
						message_string = message_string + ( str(count) + '. ' + weapon_item.name + ' ')
						count += 1
					message_string = message_string + ')'
					message(message_string, libtcod.orange)
					return 'pickup_dialog'
					#handle_keys()	# why do I get the feeling I am going to regret this


			#elif key_char == JUMP:
			elif key.vk == libtcod.KEY_SPACE:		#todo make this mappable somehow
				canJump = player.fighter.jump_available()
				if canJump:
					message_string = 'Jump in which direction?'
					message(message_string, libtcod.orange)
					return 'jump_dialog'
				else:
					message_string = 'Your legs are too tired to jump.'
					message(message_string, libtcod.orange)
					return 'didnt-take-turn'

			#attacky keys!
			else :			
	

				if key_char in player_weapon.command_list:
					return process_player_attack(key_char)

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
					for obj in objects:
						if obj.x == player.x and obj.y == player.y and obj is not player and obj.shrine is not None:
							shrine_here = True
							current_shrine = obj.shrine
							break
					if shrine_here == True:
						current_god = current_shrine.god
						message('You close your eyes and focus your mind.')
						current_shrine.visit()
						message('You here the voice of ' + current_god.name + ' whisper to you...')
						message(current_god.first_prayer_message, current_god.color)
						#message('\"Be at peace, my child. I watch over all who come to me with faith in their hearts.\"', libtcod.orange)

						favoured_by_healer = False
						favoured_by_destroyer = False
						tested_by_destroyer = False
						favoured_by_deliverer = False
						tested_by_deliverer = False
						if current_god.god_type.type == 'healer':
							if already_healed_this_level == False:
								if player.fighter.hp < player.fighter.max_hp:
									already_healed_this_level = True
									#player.fighter.heal(3)
									player.fighter.cure_wounds(1)
									message("You feel a little better")
									player.fighter.fully_heal()
							else:
								message('\"Sadly I can do no more for you at this moment. But hold on to your faith, and it shall be well rewarded.\"', libtcod.orange)
							favoured_by_healer = True
						elif current_god.god_type.type == 'destroyer':
							tested_by_destroyer = True
							#destroyer_test_count = 10
							destroyer_test_count = lev_set.max_monsters
						elif current_god.god_type.type == 'deliverer':
							# do a test: did we get to the shrine quickly enough?
							if (time - time_level_started) > 190:
								message('\"Hang on a sec, actually you already took too long to get here. Sorry!\"', libtcod.orange)
							else:
								tested_by_deliverer = True
								deliverer_test_count = 200 - (time-time_level_started)		#TODO put these kind of values in gods.py
					else:
						message('There is no shrine here.')
						return 'didnt-take-turn'

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
	num_monsters = libtcod.random_get_int(0, 0, max_room_monsters)


	for i in range(num_monsters):
	#for i in range(50):
		#choose random spot for this monster
		x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
		y = libtcod.random_get_int(0, room.y1+1, room.y2-1)

		#only place it if the tile is not blocked
		if not is_blocked(x, y):


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
					

			monster = create_monster(x,y,name)
			objects.append(monster)

	# on first level, in in 2 chance of a weapon appearing in a room I guess
	if dungeon_level == 0:
		num = libtcod.random_get_int(0, 0, 2)
		if num == 0:
			x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
			y = libtcod.random_get_int(0, room.y1+1, room.y2-1)
			new_weapon = Object(x,y, 's', 'sword', default_weapon_color, blocks = False, weapon = True)
			drop_weapon(new_weapon)
			#objects.append(new_weapon)
			#new_weapon.send_to_back()
		elif num == 1:
			x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
			y = libtcod.random_get_int(0, room.y1+1, room.y2-1)
			new_weapon = Object(x,y, 'f', 'sai', default_weapon_color, blocks = False, weapon = True)
			drop_weapon(new_weapon)
			#objects.append(new_weapon)
			#new_weapon.send_to_back()

	# on higher levels, maybe there are shrines? Maybe??
	else:
		num = libtcod.random_get_int(0,0,18)
		if num == 0:
			(shrine_x, shrine_y) = room.center()
			new_shrine = Object(shrine_x, shrine_y, '&', 'shrine to ' + god_healer.name, default_altar_color, blocks=False, shrine= Shrine(god_healer), always_visible=True) 		
			objects.append(new_shrine)
			new_shrine.send_to_back()
		elif num == 1:
			(shrine_x, shrine_y) = room.center()
			new_shrine = Object(shrine_x, shrine_y, '&', 'shrine to ' + god_destroyer.name, default_altar_color, blocks=False, shrine= Shrine(god_destroyer), always_visible=True) 		
			objects.append(new_shrine)
			new_shrine.send_to_back()
		elif num == 2:
			(shrine_x, shrine_y) = room.center()
			new_shrine = Object(shrine_x, shrine_y, '&', 'shrine to ' + god_deliverer.name, default_altar_color, blocks=False, shrine= Shrine(god_deliverer), always_visible=True) 		
			objects.append(new_shrine)
			new_shrine.send_to_back()





def create_monster(x,y, name, guard_duty = False):
	global number_alarmers
	if name == 'strawman':
		# let's make a strawman!
		strawman_component = Fighter(hp=1, defense=0, power=1, death_function=monster_death,  attack_color = libtcod.dark_blue, faded_attack_color = libtcod.darker_blue)
		ai_component = Strawman_AI(weapon = None)
		decider_component = Decider(ai_component)
		monster = Object(x, y, 'A', 'strawman', libtcod.dark_blue, blocks=True, fighter=strawman_component, decider=decider_component)

	elif name == 'flailing strawman':
		# let's create a strawman that can theoretically do damage!
		strawman_component = Fighter(hp=1, defense=0, power=1, death_function=monster_death,  attack_color = libtcod.dark_red, faded_attack_color = libtcod.darker_red)
		ai_component = Strawman_AI(weapon = Weapon_Sai())
		decider_component = Decider(ai_component)
		monster = Object(x, y, 'A', 'strawman', libtcod.dark_red, blocks=True, fighter=strawman_component, decider=decider_component)	

	elif name == 'strawman on wheels':
		# let's create a strawman that can move around!
		strawman_component = Fighter(hp=1, defense=0, power=1, death_function=monster_death,  attack_color = libtcod.dark_green, faded_attack_color = libtcod.darker_green)
		ai_component = Strawman_on_wheels_AI(weapon = None)
		decider_component = Decider(ai_component)
		monster = Object(x, y, 'A', 'strawman on wheels', libtcod.darker_green, blocks=True, fighter=strawman_component, decider=decider_component)
				
	elif name == 'swordsman':
		#create an orc
		fighter_component = Fighter(hp=1, defense=0, power=1, death_function=monster_death, attack_color = libtcod.dark_blue, faded_attack_color = libtcod.darker_blue)
		ai_component = BasicMonster(weapon = Weapon_Sword(), guard_duty= guard_duty)
		decider_component = Decider(ai_component)
		monster = Object(x, y, 'S', 'swordsman', libtcod.dark_blue, blocks=True, fighter=fighter_component, decider=decider_component)

	elif name == 'boman':
		#create a troll
		fighter_component = Fighter(hp=3, defense=0, power=1, death_function=monster_death, attack_color = libtcod.dark_green, faded_attack_color = libtcod.darker_green)
		ai_component = BasicMonster(weapon = Weapon_Staff(), guard_duty= guard_duty)
		decider_component = Decider(ai_component)
		monster = Object(x, y, 'B', 'boman', libtcod.darker_green, blocks=True, fighter=fighter_component, decider=decider_component)


	elif name == 'rook':
		#create a rook! That's a guy with a spear who only moves in four directions
		fighter_component = Fighter(hp=3, defense=0, power=1, death_function=monster_death, attack_color = libtcod.dark_blue, faded_attack_color = libtcod.darker_blue)
		ai_component = Rook_AI(weapon = Weapon_Spear(), guard_duty = guard_duty)
		decider_component = Decider(ai_component)
		monster = Object(x, y, 'R', 'rook', libtcod.darker_blue, blocks=True, fighter=fighter_component, decider=decider_component)


	elif name == 'nunchuck fanatic':
		#create a troll
		fighter_component = Fighter(hp=2, defense=0, power=1, death_function=monster_death, attack_color = libtcod.dark_green, faded_attack_color = libtcod.darker_green)
		ai_component = BasicMonster(weapon = Weapon_Nunchuck(), guard_duty= guard_duty, attack_dist = 2)
		decider_component = Decider(ai_component)
		monster = Object(x, y, 'F', 'nunchuck fanatic', libtcod.darker_green, blocks=True, fighter=fighter_component, decider=decider_component)


	elif name == 'axe maniac':
		#create a guy with an axe!
		fighter_component = Fighter(hp=3, defense=0, power=1, death_function=monster_death, attack_color = libtcod.dark_red, faded_attack_color = libtcod.darker_red)
		ai_component = BasicMonster(weapon = Weapon_Axe(), guard_duty = guard_duty)
		decider_component = Decider(ai_component)
		monster = Object(x, y, 'M', 'axe maniac', libtcod.darker_red, blocks=True, fighter=fighter_component, decider=decider_component)

	elif name == 'samurai':
		#create a guy with an axe!
		fighter_component = Fighter(hp=5, defense=0, power=1, death_function=monster_death, attack_color = libtcod.dark_red, faded_attack_color = libtcod.darker_red)
		ai_component = Samurai_AI(weapon = Weapon_Katana())
		decider_component = Decider(ai_component)
		monster = Object(x, y, 'Z', 'samurai', libtcod.darker_red, blocks=True, fighter=fighter_component, decider=decider_component)

	elif name == 'hammer sister':
		#create a lady with a hammer!
		fighter_component = Fighter(hp=3, defense=0, power=1, death_function=monster_death, attack_color = libtcod.dark_green, faded_attack_color = libtcod.darker_green)
		ai_component =  Ninja_AI(weapon = Weapon_Hammer())
		decider_component = Decider(ai_component)
		monster = Object(x, y, 'H', 'hammer sister', libtcod.darker_green, blocks=True, fighter=fighter_component, decider=decider_component)


	elif name == 'ninja':
		#create a sneaky ninja!
		fighter_component = Fighter(hp=2, defense=0, power=1, death_function=monster_death, attack_color = libtcod.black, faded_attack_color = libtcod.black)
		ai_component = Ninja_AI(weapon = Weapon_Dagger())
		decider_component = Decider(ai_component)
		monster = Object(x, y, 'N', 'ninja', libtcod.black, blocks=True, fighter=fighter_component, decider=decider_component)


	elif name == 'wizard':
		#create a wizard!
		fighter_component = Fighter(hp=10, defense=0, power=1, death_function=monster_death, attack_color = libtcod.dark_purple, faded_attack_color = libtcod.darker_purple)
		ai_component = Wizard_AI(weapon = Weapon_Ring_Of_Power())
		decider_component = Decider(ai_component)
		monster = Object(x, y, 'W', 'wizard', libtcod.darker_purple, blocks=True, fighter=fighter_component, decider=decider_component)



	elif name == 'security system':
		# let's make a security system! It stays where it is and doesn't attack! In fact it's basically a strawman with more health.
		strawman_component = Fighter(hp=5, defense=0, power=1, death_function=monster_death,  attack_color = libtcod.dark_blue, faded_attack_color = libtcod.darker_blue)
		ai_component = Strawman_AI(weapon = None)
		decider_component = Decider(ai_component)
		alarmer_component = Alarmer()
		monster = Object(x, y, 'O', 'security system', libtcod.dark_blue, blocks=True, fighter=strawman_component, decider=decider_component, alarmer = alarmer_component, always_visible = True)



	else:
		monster = None
	
	if monster.alarmer is not None:
		number_alarmers += 1

	return monster



def create_strawman(x,y, weapon, command):
	# let's create a strawman that can theoretically do damage!
	strawman_component = Fighter(hp=1, defense=0, power=1, death_function=monster_death,  attack_color = libtcod.dark_red, faded_attack_color = libtcod.darker_red)
	ai_component = Strawman_AI(get_weapon_from_name(weapon), command)		
	decider_component = Decider(ai_component)
	monster = Object(x, y, 'A', 'strawman', libtcod.dark_red, blocks=True, fighter=strawman_component, decider=decider_component)
	return monster

def make_map():
	global map, stairs, game_level_settings, dungeon_level, spawn_points, elevators, center_points, nearest_points_array, MAP_HEIGHT, MAP_WIDTH, number_alarmers, camera, alarm_level, key_count, lev_set, decoration_count

	lev_gen = Level_Generator()

	lev_set = game_level_settings.get_setting(dungeon_level)
	level_data = lev_gen.make_level(dungeon_level, lev_set)

	number_alarmers = 0		# how many things in the level do stuff with the alarm? If this becomes 0, all alarms stuff

	map = level_data.map
	player.x = level_data.player_start_x
	player.y = level_data.player_start_y
	camera.x = player.x
	camera.y = player.y
	nearest_points_array = level_data.nearest_points_array
	center_points = level_data.center_points
	spawn_points = level_data.spawn_points
	object_data = level_data.object_data
	elevators = level_data.elevators
	MAP_WIDTH = len(map)
	MAP_HEIGHT = len(map[0])

	process_nearest_center_points()
	initialize_nav_data()
	#calculate_nav_data()

	alarm_level = 1
	key_count = 0
	decoration_count = 0

	# now create objects from object_data! This code resorting thing is actually getting kind of fun now
	for od in object_data:
		if od.name == 'stairs':
			stairs = Object(od.x, od.y, '<', 'stairs', libtcod.white, always_visible=True)
			objects.append(stairs)
			stairs.send_to_back()  #so it's drawn below the monsters
		elif od.name == 'weapon':
			weapon = get_item_from_name(od.x,od.y, od.info)
			objects.append(weapon)
			weapon.send_to_back()
		elif od.name == 'monster' or od.name == 'boss':		# maybe these cases will be treated differently in future
			monster = create_monster(od.x,od.y, od.info, guard_duty = True)
			objects.append(monster)	
			# Hackiest of all hacks - make the tutorial rook drop a key
			if dungeon_level == 0:
				if od.info == 'rook':
					monster.drops_key = True
		elif od.name == 'strawman':
			strawman = create_strawman(od.x,od.y,od.info, od.more_info)
			objects.append(strawman)
		elif od.name == 'shrine':
			num = libtcod.random_get_int(0, 0, 2) 
			if num == 0:
				shrine = Object(od.x, od.y, '&', 'shrine to ' + god_healer.name, default_altar_color, blocks=False, shrine= Shrine(god_healer), always_visible=True) 	
			elif num == 1:
				shrine = Object(od.x, od.y, '&', 'shrine to ' + god_destroyer.name, default_altar_color, blocks=False, shrine= Shrine(god_destroyer), always_visible=True) 
			else: 
				shrine = Object(od.x, od.y, '&', 'shrine to ' + god_deliverer.name, default_altar_color, blocks=False, shrine= Shrine(god_deliverer), always_visible=True) 
			objects.append(shrine)
			shrine.send_to_back()
		elif  od.name == 'security system':
			monster = create_monster(od.x,od.y, 'security system', guard_duty = True)
			if od.info == 'drops-key':
				monster.drops_key = True
			objects.append(monster)	
			#number_alarmers += 1			#Now doing this elsewhere..
		elif  od.name == 'door':
			if od.info == 'horizontal':
				door = Object(od.x, od.y, '+', 'door', default_altar_color, blocks=True, door = Door(horizontal = True), always_visible=True) 
				map[od.x][od.y].block_sight = True
				objects.append(door)
			elif od.info == 'vertical':
				door = Object(od.x, od.y, '+', 'door', default_altar_color, blocks=True, door = Door(horizontal = False), always_visible=True) 	
				map[od.x][od.y].block_sight = True
				objects.append(door)
			# TODO MAKE PATHFINDING TAKE DOORS INTO ACCOUNT AT SOME POINT
		elif od.name == 'key':
			new_key = Object(od.x, od.y, '*', 'key', libtcod.white, blocks = False, weapon = False, always_visible=True)
			objects.append(new_key)
		elif od.name == 'message':
			floor_message = Object(od.x, od.y, '~', 'message', default_message_color, blocks=False, floor_message = Floor_Message(od.info))
			objects.append(floor_message)
			floor_message.send_to_back()
		elif od.name == 'decoration':
			floor_message = Object(od.x, od.y, od.info, 'decoration', default_decoration_color, blocks=False, always_visible=True)
			objects.append(floor_message)
			floor_message.send_to_back()
			decoration_count += 1
			

	# elevator data because elevators are complicated! Do you know how to build an elevator? I sure don't!
	for ele in elevators:
		ele.special_door_list = []
		for ele_door in ele.doors:
			door = Object(ele_door.x, ele_door.y, '+', 'elevator door', libtcod.red, blocks=True, door = Door(horizontal = ele_door.door.horizontal), always_visible=True) 
			map[ele_door.x][ele_door.y].block_sight = True			
			objects.append(door)
			ele.special_door_list.append(door)

			
		#for (x,y) in ele.door_points:
		#	door = Object(x, y, '+', 'elevator door', libtcod.red, blocks=True, door = Door(horizontal = False), always_visible=True) 
		#	map[od.x][od.y].block_sight = True
		#	objects.append(door)



#	#fill map with "blocked" tiles
#	map = [[ Tile(True)
#		for y in range(MAP_HEIGHT) ]
#			for x in range(MAP_WIDTH) ]
#
#	nearest_points_array  = [[ None
#		for y in range(MAP_HEIGHT) ]
#			for x in range(MAP_WIDTH) ]
#
#	
#
#	rooms = []
#	num_rooms = 0
#
#	spawn_points = []
#	center_points = []
#
#
#
#	lev_set = game_level_settings.get_setting(dungeon_level)
#
#
#	room_range = lev_set.max_rooms
#	map_width = lev_set.max_map_width
#	map_height = lev_set.max_map_height
#	room_min_size = lev_set.room_min_size
#	room_max_size = lev_set.room_max_size
#
#	if lev_set.level_type == 'modern':
#		# okay, maybe let's get some larger rooms going that can overlap?
#
#		# so for now, this is the code for classic mode, with the code for checking room overlaps removed
#		for r in range(room_range):
#			#random width and height
#			w = libtcod.random_get_int(0, room_min_size, room_max_size)
#			h = libtcod.random_get_int(0, room_min_size, room_max_size)
#			#random position without going out of the boundaries of the map
#			x = libtcod.random_get_int(0, 0, map_width - w - 1)
#			y = libtcod.random_get_int(0, 0, map_height - h - 1)
#	
#			#"Rect" class makes rectangles easier to work with
#			new_room = Rect(x, y, w, h)
#	 
#
#	
#			if True:
#				#this means there are no intersections, so this room is valid
#	
#				#"paint" it to the map's tiles
#				create_room(new_room)
#				#add some contents to this room, such as monsters
#				place_objects(new_room)
#	
#				#center coordinates of new room, will be useful later
#				(new_x, new_y) = new_room.center()
#				if num_rooms == 0:
#					#this is the first room, where the player starts at
#					player.x = new_x
#					player.y = new_y
#				else:
#					#all rooms after the first:
#					#connect it to the previous room with a tunnel
#	
#					#center coordinates of previous room
#					(prev_x, prev_y) = rooms[num_rooms-1].center()
#	
#					#draw a coin (random number that is either 0 or 1)
#					if libtcod.random_get_int(0, 0, 1) == 1:
#						#first move horizontally, then vertically
#						create_h_tunnel(prev_x, new_x, prev_y)
#						create_v_tunnel(new_y, prev_y, new_x)
#					else:
#						#first move vertically, then horizontally
#						create_v_tunnel(prev_y, new_y, prev_x)
#						create_h_tunnel(new_x, prev_x, new_y)
#	
#				#finally, append the new room to the list
#				rooms.append(new_room)
#				num_rooms += 1
#
#		
#		#create stairs at the center of the last room
#		stairs = Object(new_x, new_y, '<', 'stairs', libtcod.white, always_visible=True)
#		objects.append(stairs)
#		stairs.send_to_back()  #so it's drawn below the monsters
#	
#		if lev_set.boss is not None:
#			boss_monster = create_monster(new_x,new_y,lev_set.boss)
#			objects.append(boss_monster)
#
#
#
#		# now, append some elevators?
#		num_norm_rooms = num_rooms
#		elev1 = Rect(5, 5, 4, 4)
#		elev2 = Rect(MAP_WIDTH-5, 5, 4, 4)
#		elev3 = Rect(MAP_WIDTH-5, MAP_HEIGHT -5, 4, 4)
#		elev4 = Rect(5, MAP_HEIGHT - 5, 4, 4)
#		create_elevator(elev1)
#		create_elevator(elev2)
#		create_elevator(elev3)
#		create_elevator(elev4)
#		(new_x, new_y) = elev1.center()
#		num = libtcod.random_get_int(0, 0, num_norm_rooms-1)
#		(prev_x, prev_y) = rooms[num].center()
#			#draw a coin (random number that is either 0 or 1)
#		if libtcod.random_get_int(0, 0, 1) == 1:
#			#first move horizontally, then vertically
#			create_h_tunnel(prev_x, new_x, prev_y)
#			create_v_tunnel(new_y, prev_y, new_x)
#		else:
#			#first move vertically, then horizontally
#			create_v_tunnel(prev_y, new_y, prev_x)
#			create_h_tunnel(new_x, prev_x, new_y)
#		(new_x, new_y) = elev2.center()
#		num = libtcod.random_get_int(0, 0, num_norm_rooms-1)
#		(prev_x, prev_y) = rooms[num].center()
#			#draw a coin (random number that is either 0 or 1)
#		if libtcod.random_get_int(0, 0, 1) == 1:
#			#first move horizontally, then vertically
#			create_h_tunnel(prev_x, new_x, prev_y)
#			create_v_tunnel(new_y, prev_y, new_x)
#		else:
#			#first move vertically, then horizontally
#			create_v_tunnel(prev_y, new_y, prev_x)
#			create_h_tunnel(new_x, prev_x, new_y)
#		(new_x, new_y) = elev3.center()
#		num = libtcod.random_get_int(0, 0, num_norm_rooms-1)
#		(prev_x, prev_y) = rooms[num].center()
#			#draw a coin (random number that is either 0 or 1)
#		if libtcod.random_get_int(0, 0, 1) == 1:
#			#first move horizontally, then vertically
#			create_h_tunnel(prev_x, new_x, prev_y)
#			create_v_tunnel(prev_y, new_y, new_x)
#		else:
#			#first move vertically, then horizontally
#			create_v_tunnel(prev_y, new_y, prev_x)
#			create_h_tunnel(new_x, prev_x, new_y)
#		(new_x, new_y) = elev4.center()
#		num = libtcod.random_get_int(0, 0, num_norm_rooms-1)
#		(prev_x, prev_y) = rooms[num].center()
#			#draw a coin (random number that is either 0 or 1)
#		if libtcod.random_get_int(0, 0, 1) == 1:
#			#first move horizontally, then vertically
#			create_h_tunnel(prev_x, new_x, prev_y)
#			create_v_tunnel(new_y, prev_y, new_x)
#		else:
#			#first move vertically, then horizontally
#			create_v_tunnel(prev_y, new_y, prev_x)
#			create_h_tunnel(new_x, prev_x, new_y)
#			# ok that was a bunch of code to appenx some elevators! Let's see how it goes
#
#
#
#	else:		# 'classic' mode
#
#		for r in range(room_range):
#			#random width and height
#			w = libtcod.random_get_int(0, room_min_size, room_max_size)
#			h = libtcod.random_get_int(0, room_min_size, room_max_size)
#			#random position without going out of the boundaries of the map
#			x = libtcod.random_get_int(0, 0, map_width - w - 1)
#			y = libtcod.random_get_int(0, 0, map_height - h - 1)
#	
#			#"Rect" class makes rectangles easier to work with
#			new_room = Rect(x, y, w, h)
#	 
#			#run through the other rooms and see if they intersect with this one
#			failed = False
#			for other_room in rooms:
#				if new_room.intersect(other_room):
#					failed = True
#					break
#	
#			if not failed:
#				#this means there are no intersections, so this room is valid
#	
#				#"paint" it to the map's tiles
#				create_room(new_room)
#				#add some contents to this room, such as monsters
#				place_objects(new_room)
#	
#				#center coordinates of new room, will be useful later
#				(new_x, new_y) = new_room.center()
#				if num_rooms == 0:
#					#this is the first room, where the player starts at
#					player.x = new_x
#					player.y = new_y
#				else:
#					#all rooms after the first:
#					#connect it to the previous room with a tunnel
#	
#					#center coordinates of previous room
#					(prev_x, prev_y) = rooms[num_rooms-1].center()
#	
#					#draw a coin (random number that is either 0 or 1)
#					if libtcod.random_get_int(0, 0, 1) == 1:
#						#first move horizontally, then vertically
#						create_h_tunnel(prev_x, new_x, prev_y)
#						create_v_tunnel(new_y, prev_y, new_x)
#					else:
#						#first move vertically, then horizontally
#						create_v_tunnel(prev_y, new_y, prev_x)
#						create_h_tunnel(new_x, prev_x, new_y)
#	
#				#finally, append the new room to the list
#				rooms.append(new_room)
#				num_rooms += 1
#	
#		#create stairs at the center of the last room
#		stairs = Object(new_x, new_y, '<', 'stairs', libtcod.white, always_visible=True)
#		objects.append(stairs)
#		stairs.send_to_back()  #so it's drawn below the monsters
#	
#		if lev_set.boss is not None:
#			boss_monster = create_monster(new_x,new_y,lev_set.boss)
#			objects.append(boss_monster)
#		
#	process_nearest_center_points()
#
#	calculate_nav_data()



def initialize_nav_data():
	global map, center_points, nav_data, nav_data_changed


	big_M = MAP_HEIGHT * MAP_WIDTH
	NUMBER_POINTS = len(center_points)
	nav_data = [[[ big_M
		for p  in range(NUMBER_POINTS)]
			for y in range(MAP_HEIGHT) ]
				for x in range(MAP_WIDTH)]

	for n in range(NUMBER_POINTS):
		(x,y) = center_points[n]
		nav_data[x][y][n] = 0

	nav_data_changed = True

	update_nav_data()


def update_nav_data():

#def calculate_nav_data():
	# come up with a nav data thing that calculates the distances to a bunch of checkpoints!
	global map, center_points, nav_data, nav_data_changed

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
		anything_changed = False
		#for r in range(MAP_HEIGHT*MAP_WIDTH*NUMBER_POINTS):
		for r in range(max_nav_data_loops):#horse
			for p  in range(len(center_points)):
				for y in range(MAP_HEIGHT):
					for x in range(MAP_WIDTH):
						if map[x][y].blocked == False:
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
			if anything_changed:
				anything_changed = False		#check it again!
			else: 
				# if actually nothing changed, we can mark the nav data as done.
				nav_data_changed = False		
				#print 'nav data finished after ' + str(r) + ' iterations'
				break
	
	# okay, I think that concludes calculating the distance to things? Let's see.
	
	
def is_blocked(x, y):
	#first test the map tile
	if map[x][y].blocked:
		return True

	#now check for any blocking objects
	for object in objects:
		if object.blocks and object.x == x and object.y == y:
			return True
	return False




def player_move_or_attack(dx, dy):
	global fov_recompute
 
	#the coordinates the player is moving to/attacking
	x = player.x + dx
	y = player.y + dy
 
	#try to find an attackable object there
	target = None
	for object in objects:
		if object.fighter and object.x == x and object.y == y:
			target = object
			break
 
	#attack if target found, move otherwise
	if target is not None:
		player.fighter.attack(target)
	else:
		player.move(dx, dy)
		fov_recompute = True



#Processing player attack, woop woo! we want the decision for whether an attack is possible to belong to the player's Fighter class rather than the weapon itself; we're putting the wrapper for all that stuff around here.
def process_player_attack(key_char):

	if player_weapon.durability <= 0:
		message('Your ' +  str(player_weapon.name) + ' is broken!')
		return 'didnt-take-turn'
	else:
		energy_cost = player_weapon.get_usage_cost(key_char) + 1   #let's try and make weapons a bit harder to use...
		if player.fighter.can_attack(energy_cost):
			abstract_attack_data = player_weapon.do_energy_attack(key_char)
			temp_attack_list = process_abstract_attack_data(player.x,player.y, abstract_attack_data, player)	
			player.decider.set_decision(Decision(attack_decision = Attack_Decision(attack_list=temp_attack_list)))
			player.fighter.lose_energy(energy_cost)
		
		#Note: this code might need to change in future if we decide to have other reasons for not being able to attack
		else:
			#message('Attack used up; can attack again in ' + str(player_weapon.default_usage - player_weapon.current_charge) + ' seconds.', libtcod.orange)
			message('You are too tired to attack', libtcod.orange)
			return 'didnt-take-turn'

def process_abstract_attack_data(x,y,abstract_attack_data, attacker=None):
	# given data (i,j, val) from an abstract attack, produce an attack at co-ordinates x_i, y_j with damage val.
	# this function mainly exists because I am a bad programmer and can't figure out how to get the weapons file to recognise Attacks...
	temp_attack_list = []
	temp_color = libtcod.dark_red
	if attacker is not None:
		if attacker.fighter:
			temp_color = attacker.fighter.attack_color
	for (i,j,val) in abstract_attack_data:
		# adjust attack for position, and also extra strength from the fighter.
		temp_attack = Object(x+i, y+j, '#', 'attack', temp_color, blocks=False, attack= BasicAttack(val + attacker.fighter.extra_strength, attacker=attacker))
		temp_attack_list.append(temp_attack)
	return temp_attack_list

	

def player_death(player):
	#the game ended!
	global game_state
	message('You died!', libtcod.red)
	message('Press R to restart, Q to quit')
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
						reorder_objects()
					else:
						num = libtcod.random_get_int(0,0, 100)
						if num <= CHANCE_OF_ENEMY_DROP:
							drop_weapon(item)
							reorder_objects()
	

	#transform it into a nasty corpse! it doesn't block, can't be
	#attacked and doesn't move
	#if monster.name == 'security system':
	if monster.alarmer is not None:
		number_alarmers -= 1
		message(monster.name.capitalize() + ' is destroyed!', libtcod.orange)		
		#decrease the alarm level alittle bit! Unless that was the last one, in which case set it to 0
		if number_alarmers > 0:
			if alarm_level > 0:
				alarm_level += (-monster.alarmer.alarm_value + monster.alarmer.dead_alarm_value)
				message('The alarms get a little quieter.')
		else:
			alarm_level = 0
			message('A sudden silence descends as the alarms stop.')


	else:	
		message(monster.name.capitalize() + ' is dead!', libtcod.orange)
	monster.char = '%'
	monster.color = libtcod.gray
	monster.blocks = False
	monster.fighter = None
	monster.decider = None
	monster.name = 'remains of ' + monster.name
	monster.send_to_back()
	garbage_list.append(monster)

	#monster may drop a key?
	if monster.drops_key == True:
		new_key = Object(monster.x,monster.y, '*', 'key', libtcod.white, blocks = False, weapon = False, always_visible=True)
		objects.append(new_key)
		# trigger a draw order cleanup, because otherwise you get enemies hiding under keys
		reorder_objects()

	#killing a monster affects some test stuff for the god of destruction
	if tested_by_destroyer:
		if destroyer_test_count > 0:
			destroyer_test_count -= 1
		if destroyer_test_count <= 0:
			tested_by_destroyer = False
			favoured_by_destroyer = True
			favoured_by_healer = False






def next_level():
	global dungeon_level, objects, game_state, current_big_message, lev_set, favoured_by_healer, favoured_by_destroyer, favoured_by_deliverer, tested_by_deliverer, enemy_spawn_rate, deliverer_test_count, time_level_started, elevators, alarm_level, key_count, spawn_timer,  already_healed_this_level

	#Go to the end screen if you just beat the final level woo!
	if lev_set.final_level is True:
		beat_game()	

	#moving to next level has affects for Taylor the Deliverer!
	if tested_by_deliverer and deliverer_test_count >= 0:
		favoured_by_deliverer = True


	dungeon_level += 1
	alarm_level = dungeon_level + 1
	key_count = 0
	time_level_started = time
	message('You ascend to the next level!', libtcod.red)
	if favoured_by_healer == True:
		message('You hear the voice of ' + god_healer.name)
		message('\"Behold my child! Faith in me shall always be rewarded.\"', libtcod.orange)
		player.fighter.max_hp = player.fighter.max_hp + 1
		player.fighter.heal_wounds(3)
		player.fighter.fully_heal()
		#player.fighter.heal(5)
		message('You feel rejuvenated!')
		favoured_by_healer = False

	if favoured_by_destroyer == True:
		message('You hear the voice of ' + god_destroyer.name)
		message('\"Your destruction pleases me. I shall grant you a boon!\"', libtcod.orange)
		#player.fighter.fully_heal()
		player.fighter.increase_strength(1)
		message('You feel stronger!')
		favoured_by_destroyer = False

	if favoured_by_deliverer == True:
		message('You hear the voice of ' + god_deliverer.name)
		message('\"Good job! Here\'s your reward. Have fun with it!\"', libtcod.orange)
		#player.fighter.increase_recharge_rate(1)
		# make the player always have an increased max charge on their weapon
		player.fighter.increase_max_charge(1)
		player_weapon.max_charge = player_weapon.max_charge + 1
		message('You feel faster!')
		favoured_by_deliverer = False
		tested_by_deliverer = False

	already_healed_this_level = False

	objects = [player]

#color_fog_of_war
	#delete all the old stuff. Hope this works...
#	for y in range(SCREEN_HEIGHT):
#		for x in range(SCREEN_WIDTH):
#			libtcod.console_set_char_background(con, x, y, libtcod.red, libtcod.red)
#			print "blah (" + str(x) + "," + str(y) + ")" 
   	make_map()  #create a fresh new level!
#	for y in range(MAP_HEIGHT):
#		for x in range(MAP_WIDTH):
	for y in range(SCREEN_HEIGHT):
		for x in range(SCREEN_WIDTH):
			if (y >= MAP_HEIGHT or x>= MAP_WIDTH):
				#map[x][y].explored = False
				libtcod.console_set_char_background(con, x, y, libtcod.red, libtcod.red)
				#print "blah (" + str(x) + "," + str(y) + ")" 
			else:
				map[x][y].explored = False
				libtcod.console_set_char_background(con, x, y, color_fog_of_war, libtcod.BKGND_SET)
				#print "bloo (" + str(x) + "," + str(y) + ")" 
    	initialize_fov()


	lev_set = game_level_settings.get_setting(dungeon_level)
	enemy_spawn_rate = lev_set.enemy_spawn_rate
	spawn_timer = int(enemy_spawn_rate/alarm_level)

	#for ele in elevators:			#open the doors when the level starts?
	#	ele.set_doors_open(True)
	#DOESN'T WORK, SO YOU HAVE TO WAIT A TURN BEFORE THE DOORS OPEN. WHICH IS ANNOYING

	#current_big_message = "As you ascend the stairs, you inwardly breathe a sigh of relief. The trials of the floor below you are now in the past, but what dangers lie up ahead? Your enemies only seem to be getting more deadly the closer you get to your nemesis. You think back to the wise words of your mentor: \"Stick 'em with the pointy end.\""

	#game_state  = 'big message'

def beat_game():
	global dungeon_level, objects, game_state, current_big_message
	#current_big_message = "As you ascend the stairs, the air around you crackles with electricity. Reaching the rooftop of the building, you stare into the sunrise of a beautiful new day. With the wizard defeated and the ring of power in your hands, there is no one to stand in your way. This city will be yours!"
	game_state  = 'end message'


def initialize_fov():
	global fov_recompute, fov_map
	fov_recompute = True

	#create the FOV map, according to the generated map
	fov_map = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
	for y in range(MAP_HEIGHT):
		for x in range(MAP_WIDTH):
			libtcod.map_set_properties(fov_map, x, y, not map[x][y].block_sight, not map[x][y].blocked)

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
		new_weapon =  Weapon_Sai_Alt()
	elif name == 'nunchaku':
		new_weapon =  Weapon_Nunchuck()
	elif name == 'axe':
		new_weapon =  Weapon_Axe()
	elif name == 'katana':
		new_weapon =  Weapon_Katana()
	elif name == 'hammer':
		new_weapon =  Weapon_Hammer()
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
	elif name == 'ring of power':
		char = 'o'
	object = Object(x, y, char, name, default_weapon_color, blocks=False, weapon = True)
	return object



def drop_weapon(weapon_item):
	weapon_name = weapon_item.name
	weapon_x = weapon_item.x
	weapon_y = weapon_item.y
	# check to see if there's already an item with the same name in this location
	copy_found = False
	for object in objects:
		if object.x == weapon_x and object.y == weapon_y and object.name == weapon_name:
			copy_found = True

	# only drop the item if there isn't an item with the same name in this location.
	if copy_found == False:
		objects.append(weapon_item)
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
		objects.append(new_shrine)
		new_shrine.send_to_back()



def restart_game(): 	#TODO OKAY SO THERE IS A WIERD BUG WHERE WHEN YOU RESTART THE GAME IT DOESN'T KNOW THAT THE FINAL LEVEL IS THE FINAL LEVEL??? OK GOOD NEWS THOUGH IT ONLY SEEMS TO BE IF THE FINAL LEVEL IS THE FIRST LEVEL? MAYBE? SO HOPEFULLY WE CAN JUST LEAVE IT
	global dungeon_level

	dungeon_level = 0
	alarm_level = 1
	key_count = 0
    	make_map()  #create a fresh new level!
	for y in range(MAP_HEIGHT):
		for x in range(MAP_WIDTH):
			map[x][y].explored = False
			libtcod.console_set_char_background(con, x, y, color_fog_of_war, libtcod.BKGND_SET)
    	initialize_fov()
	initialise_game()






def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color):
	#render a bar (HP, experience, etc). first calculate the width of the bar
	bar_width = int(float(value) / maximum * total_width)

	#render the background first
	libtcod.console_set_default_background(panel, back_color)
	libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

	#now render the bar on top
	libtcod.console_set_default_background(panel, bar_color)
	if bar_width > 0:
		libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

	#finally, some centered text with the values
	libtcod.console_set_default_foreground(panel, libtcod.white)
	libtcod.console_print_ex(panel, x + total_width / 2, y, libtcod.BKGND_NONE, libtcod.CENTER,
	name + ': ' + str(value) + '/' + str(maximum))
		


def message(new_msg, color = libtcod.white):
	#split the message if necessary, among multiple lines
	new_msg_lines = textwrap.wrap(new_msg, MSG_WIDTH)

	for line in new_msg_lines:
		#if the buffer is full, remove the first line to make room for the new one
		if len(game_msgs) == MSG_HEIGHT:
			del game_msgs[0]

		#add the new line as a tuple, with the text and the color
		game_msgs.append( (line, color) )

def pause_screen():


	# print the pause screen I guess 
	libtcod.console_set_default_background(pause_menu, libtcod.black)
	libtcod.console_clear(pause_menu)
	libtcod.console_set_default_foreground(pause_menu, libtcod.white)
	libtcod.console_print_ex(pause_menu, SCREEN_WIDTH/2, 2, libtcod.BKGND_NONE, libtcod.CENTER,
	'The game is paused (press Esc to unpause or Q to quit)')

	#blit the contents of "pause_menu" to the root console
	libtcod.console_blit(pause_menu, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

def big_message(string):	

	#split the message if necessary, among multiple lines
	new_msg_lines = textwrap.wrap(string, MSG_WIDTH)


	# print the big message
	libtcod.console_set_default_background(pause_menu, libtcod.black)
	libtcod.console_clear(pause_menu)
	libtcod.console_set_default_foreground(pause_menu, libtcod.white)
	y = 2
	for line in new_msg_lines:
		libtcod.console_print_ex(pause_menu, SCREEN_WIDTH/2, y, libtcod.BKGND_NONE, libtcod.CENTER, line)
		y = y + 1

	#blit the contents of "pause_menu" to the root console
	libtcod.console_blit(pause_menu, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)


def end_message():
	global current_big_message
	
	current_big_message = "As you ascend the stairs, THE MIGHTY MIGHTY STAIRS, the air around you crackles with electricity. Reaching the rooftop of the building, you stare into the sunrise of a beautiful new day. With the wizard defeated and the ring of power in your hands, there is no one to stand in your way. \n This city will be yours!"
	string = current_big_message

	#split the message if necessary, among multiple lines
	new_msg_lines = textwrap.wrap(string, MSG_WIDTH)


	# print the big message
	libtcod.console_set_default_background(pause_menu, libtcod.black)
	libtcod.console_clear(pause_menu)
	libtcod.console_set_default_foreground(pause_menu, libtcod.white)
	y = 2
	for line in new_msg_lines:
		libtcod.console_print_ex(pause_menu, SCREEN_WIDTH/2, y, libtcod.BKGND_NONE, libtcod.CENTER, line)
		y = y + 1

	#blit the contents of "pause_menu" to the root console
	libtcod.console_blit(pause_menu, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

	

def end_data_message():
	global current_big_message, player_weapon, time

	string = current_big_message
	data_string = "You ascended the tower with the " + player_weapon.name + " in " + str(time) + " seconds."

#split the message if necessary, among multiple lines
	new_msg_lines = textwrap.wrap(string, MSG_WIDTH)
	new_data_msg_lines = textwrap.wrap(data_string, MSG_WIDTH)

	# print the big message
	libtcod.console_set_default_background(pause_menu, libtcod.black)
	libtcod.console_clear(pause_menu)
	libtcod.console_set_default_foreground(pause_menu, libtcod.white)
	y = 2
	for line in new_msg_lines:
		libtcod.console_print_ex(pause_menu, SCREEN_WIDTH/2, y, libtcod.BKGND_NONE, libtcod.CENTER, line)
		y = y + 1
	y = y + 2

	for line in new_data_msg_lines:
		libtcod.console_print_ex(pause_menu, SCREEN_WIDTH/2, y, libtcod.BKGND_NONE, libtcod.CENTER, line)
		y = y + 1

	#blit the contents of "pause_menu" to the root console
	libtcod.console_blit(pause_menu, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

def restartynscreen():
	global current_big_message, player_weapon, time

	string = current_big_message
	data_string = "You ascended the tower with the " + player_weapon.name + " in " + str(time) + " seconds."
	query_string = "Would you like to play again? (y/n)"	

#split the message if necessary, among multiple lines
	new_msg_lines = textwrap.wrap(string, MSG_WIDTH)
	new_data_msg_lines = textwrap.wrap(data_string, MSG_WIDTH)
	new_query_msg_lines = textwrap.wrap(query_string, MSG_WIDTH)


	# print the big message
	libtcod.console_set_default_background(pause_menu, libtcod.black)
	libtcod.console_clear(pause_menu)
	libtcod.console_set_default_foreground(pause_menu, libtcod.white)
	y = 2
	for line in new_msg_lines:
		libtcod.console_print_ex(pause_menu, SCREEN_WIDTH/2, y, libtcod.BKGND_NONE, libtcod.CENTER, line)
		y = y + 1
	y = y + 2
	for line in new_data_msg_lines:
		libtcod.console_print_ex(pause_menu, SCREEN_WIDTH/2, y, libtcod.BKGND_NONE, libtcod.CENTER, line)
		y = y + 1
	y = y+2
	for line in new_query_msg_lines:
		libtcod.console_print_ex(pause_menu, SCREEN_WIDTH/2, y, libtcod.BKGND_NONE, libtcod.CENTER, line)
		y = y + 1

	#blit the contents of "pause_menu" to the root console
	libtcod.console_blit(pause_menu, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

def render_all():

	global fov_map, color_dark_wall, color_light_wall
	global color_dark_ground, color_light_ground
	global fov_recompute

	if fov_recompute:
		#recompute FOV if needed (the player moved or something)
		fov_recompute = False
		libtcod.map_compute_fov(fov_map, player.x, player.y, TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)

	update_camera()
	#x_offset = camera.x-SCREEN_WIDTH/2
	x_offset = camera.x-(SCREEN_WIDTH + MESSAGE_PANEL_WIDTH)/2
	#y_offset = camera.y-SCREEN_HEIGHT/2
	y_offset = camera.y-(SCREEN_HEIGHT-PANEL_HEIGHT)/2

	for y in range(SCREEN_HEIGHT):
		for x in range(SCREEN_WIDTH):
			libtcod.console_set_char_background(con, x, y, color_fog_of_war, libtcod.BKGND_SET)


	#go through all tiles, and set their background color according to the FOV
	for y in range(MAP_HEIGHT):
		for x in range(MAP_WIDTH):
			#visible = True # temporary hack to test enemy navigation
			visible = libtcod.map_is_in_fov(fov_map, x, y)
			wall = map[x][y].blocked 	#block_sight
			
			#if False:
			if not visible:
				#if it's not visible right now, the player can only see it if it's explored	
				if map[x][y].explored:
					#it's out of the player's FOV
					if wall:
						libtcod.console_set_char_background(con, x - x_offset, y - y_offset, color_dark_wall, libtcod.BKGND_SET)
					else:
						libtcod.console_set_char_background(con, x - x_offset, y - y_offset, color_dark_ground, libtcod.BKGND_SET)
				else: 
					libtcod.console_set_char_background(con, x - x_offset, y - y_offset, color_fog_of_war, libtcod.BKGND_SET)
			else:
				if wall:
					libtcod.console_set_char_background(con, x - x_offset, y - y_offset, color_light_wall, libtcod.BKGND_SET  )
				#	libtcod.console_put_char_ex(con, x, y, '#', libtcod.white, libtcod.dark_blue)
				else:
					libtcod.console_set_char_background(con, x - x_offset, y - y_offset, color_light_ground, libtcod.BKGND_SET )
				#	libtcod.console_put_char_ex(con, x, y, '.', libtcod.white,  color_dark_ground)
				
				map[x][y].explored = True


	# do some background type stuff based, on whether someone has just been attacked.
	for object in objects:
		if libtcod.map_is_in_fov(fov_map, object.x, object.y) == True:
			for other_object in objects:
				if object is not other_object and object.x == other_object.x and object.y == other_object.y:
					if object.attack is not None and other_object.fighter is not None:
						libtcod.console_set_char_background(con, object.x - x_offset, object.y - y_offset, object.attack.faded_color, libtcod.BKGND_SET )
					


	for object in objects:
		#if object != player:
		object.draw()
	#player.draw()
	
	player.send_to_front()
	

#	libtcod.console_blit(con, 0, 0, MAP_WIDTH, MAP_HEIGHT, 0, 0, 0)
	libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

	
	# write GUI stuff to "panel"
	create_GUI_panel()
	create_message_panel()


def create_GUI_panel():
	global fov_map, color_dark_wall, color_light_wall
	global color_dark_ground, color_light_ground
	global fov_recompute
	global game_level_settings, dungeon_level


	lev_set = game_level_settings.get_setting(dungeon_level)

	#GUI STUFF
	#prepare to render the GUI panel
	libtcod.console_set_default_background(panel, libtcod.black)
	libtcod.console_clear(panel)

	#Three subpanels within this panel. From left to right: attack panel, player panel, level panel
	attack_panel_width = 20
	player_panel_width = 20
	level_panel_width = 20
	attack_panel_x = 1
	player_panel_x = attack_panel_x + attack_panel_width + 1
	level_panel_x = player_panel_x + player_panel_width + 1


	#ATTACK PANEL STUFF
	#change color based on weapon status
	attack_panel_default_color = libtcod.white
	if player_weapon.durability <= 0:
		attack_panel_default_color = libtcod.red
	elif player_weapon.durability <= WEAPON_FAILURE_WARNING_PERIOD:
		attack_panel_default_color = libtcod.orange
	elif player_weapon.current_charge < player_weapon.default_usage:
		attack_panel_default_color = libtcod.blue


	libtcod.console_set_default_foreground(panel, attack_panel_default_color)
	if len(player_weapon.name) <= attack_panel_width - 10:
		libtcod.console_print_ex(panel, attack_panel_x, 1, libtcod.BKGND_NONE, libtcod.LEFT,
	'Weapon: ' + str(player_weapon.name).upper())
	else:
		libtcod.console_print_ex(panel, attack_panel_x, 1, libtcod.BKGND_NONE, libtcod.LEFT,
	str(player_weapon.name).upper())

	# list some attacks out.
	attack_list = str(player_weapon.command_list)
	libtcod.console_print_ex(panel, attack_panel_x, 3, libtcod.BKGND_NONE, libtcod.LEFT, "Attacks:")
	## set colors based on weapon durability
	#if player_weapon.durability <= 0:
	#		libtcod.console_set_default_foreground(panel, libtcod.orange)
	#elif player_weapon.durability <= WEAPON_FAILURE_WARNING_PERIOD:
	#		libtcod.console_set_default_foreground(panel, libtcod.orange)
	#else: 
	#		libtcod.console_set_default_foreground(panel, libtcod.white)
		
	if ATTCKUPLEFT in attack_list:
			libtcod.console_print_ex(panel, attack_panel_x + attack_panel_width/2 - 2, 3, libtcod.BKGND_NONE, libtcod.CENTER,
		ATTCKUPLEFT)

	if ATTCKUP in attack_list:
			libtcod.console_print_ex(panel, attack_panel_x + attack_panel_width/2, 3, libtcod.BKGND_NONE, libtcod.CENTER,
		ATTCKUP)

	if ATTCKUPRIGHT in attack_list:
			libtcod.console_print_ex(panel, attack_panel_x + attack_panel_width/2 + 2, 3, libtcod.BKGND_NONE, libtcod.CENTER,
		ATTCKUPRIGHT)

	if ATTCKLEFT in attack_list:
			libtcod.console_print_ex(panel, attack_panel_x + attack_panel_width/2 - 2, 4, libtcod.BKGND_NONE, libtcod.CENTER,
		ATTCKLEFT)


	if ATTCKRIGHT in attack_list:
			libtcod.console_print_ex(panel, attack_panel_x + attack_panel_width/2 + 2, 4, libtcod.BKGND_NONE, libtcod.CENTER,
		ATTCKRIGHT)

		
	if ATTCKDOWNLEFT in attack_list:
			libtcod.console_print_ex(panel, attack_panel_x + attack_panel_width/2 - 2, 5, libtcod.BKGND_NONE, libtcod.CENTER,
		ATTCKDOWNLEFT)

	if ATTCKDOWN in attack_list:
			libtcod.console_print_ex(panel, attack_panel_x + attack_panel_width/2, 5, libtcod.BKGND_NONE, libtcod.CENTER,
		ATTCKDOWN)

	if ATTCKDOWNRIGHT in attack_list:
			libtcod.console_print_ex(panel, attack_panel_x + attack_panel_width/2 + 2, 5, libtcod.BKGND_NONE, libtcod.CENTER,
		ATTCKDOWNRIGHT)
	libtcod.console_set_default_foreground(panel, attack_panel_default_color)

	# Display weapon charge details.
	uncharged_color = libtcod.blue
	insufficient_charge_color = libtcod.red
	charge_color = libtcod.green
	bonus_charge_color = libtcod.darker_green
	libtcod.console_print_ex(panel, attack_panel_x, 6, libtcod.BKGND_NONE, libtcod.LEFT,	'Charge:')
	if player_weapon.current_charge < player_weapon.default_usage:
		libtcod.console_set_default_foreground(panel, insufficient_charge_color)
		for i in range(player_weapon.current_charge):
			libtcod.console_print_ex(panel, attack_panel_x + 7 + i, 6, libtcod.BKGND_NONE, libtcod.LEFT, '*')
	else:
		libtcod.console_set_default_foreground(panel, bonus_charge_color)
		for i in range(player_weapon.current_charge - player_weapon.default_usage):
			libtcod.console_print_ex(panel, attack_panel_x + 7 + i, 6, libtcod.BKGND_NONE, libtcod.LEFT, '*')
		libtcod.console_set_default_foreground(panel, charge_color)
		for i in range(player_weapon.current_charge - player_weapon.default_usage, player_weapon.current_charge):
			libtcod.console_print_ex(panel, attack_panel_x + 7 + i, 6, libtcod.BKGND_NONE, libtcod.LEFT, '*')

	libtcod.console_set_default_foreground(panel, uncharged_color)
	for i in range(player_weapon.current_charge, player_weapon.max_charge):
		libtcod.console_print_ex(panel, attack_panel_x + 7 + i, 6, libtcod.BKGND_NONE, libtcod.LEFT,
	'*')


	
	libtcod.console_set_default_foreground(panel, attack_panel_default_color)

#	if player_weapon.current_charge < player_weapon.default_usage:
#	else:
#	libtcod.console_print_ex(panel, attack_panel_x, 6, libtcod.BKGND_NONE, libtcod.LEFT,
#	'Charge:** ' + str(player_weapon.current_charge) + '/' + str(player_weapon.max_charge) + ' (req:' + str(player_weapon.default_usage) + ')')
	if player_weapon.durability <= WEAPON_FAILURE_WARNING_PERIOD and player_weapon.durability > 0:
		libtcod.console_set_default_foreground(panel, libtcod.orange)
	elif player_weapon.durability <= 0:
		libtcod.console_set_default_foreground(panel, libtcod.red)
	libtcod.console_print_ex(panel, attack_panel_x, 7, libtcod.BKGND_NONE, libtcod.LEFT,
	'Durability: ' + str(player_weapon.durability))

	#PLAYER PANEL STUFF

	#show the player's stats
	render_bar(player_panel_x, 1, BAR_WIDTH, 'HP', player.fighter.hp, player.fighter.max_hp - player.fighter.wounds,
	libtcod.light_red, libtcod.darker_red)

	#display some sweet moves!
	libtcod.console_set_default_foreground(panel, libtcod.white)
	libtcod.console_print_ex(panel, player_panel_x, 3, libtcod.BKGND_NONE, libtcod.LEFT, "Moves:")
	libtcod.console_print_ex(panel, player_panel_x + player_panel_width/2 - 2, 3, libtcod.BKGND_NONE, libtcod.CENTER, '7')
	libtcod.console_print_ex(panel, player_panel_x + player_panel_width/2, 3, libtcod.BKGND_NONE, libtcod.CENTER, '8')
	libtcod.console_print_ex(panel, player_panel_x + player_panel_width/2 + 2, 3, libtcod.BKGND_NONE, libtcod.CENTER, '9')
	libtcod.console_print_ex(panel, player_panel_x + player_panel_width/2 - 2, 4, libtcod.BKGND_NONE, libtcod.CENTER, '4')
	libtcod.console_print_ex(panel, player_panel_x + player_panel_width/2, 4, libtcod.BKGND_NONE, libtcod.CENTER, '.')
	libtcod.console_print_ex(panel, player_panel_x + player_panel_width/2 + 2, 4, libtcod.BKGND_NONE, libtcod.CENTER, '6')
	libtcod.console_print_ex(panel, player_panel_x + player_panel_width/2 - 2, 5, libtcod.BKGND_NONE, libtcod.CENTER, '1')
	libtcod.console_print_ex(panel, player_panel_x + player_panel_width/2, 5, libtcod.BKGND_NONE, libtcod.CENTER, '2')
	libtcod.console_print_ex(panel, player_panel_x + player_panel_width/2 + 2, 5, libtcod.BKGND_NONE, libtcod.CENTER, '3')


	#Display some stuff about jumps, woo!
	jump_charged_color = libtcod.orange
	jump_uncharged_color = libtcod.red
	if  len(player.fighter.jump_array) > 0:
		libtcod.console_print_ex(panel, player_panel_x, 7, libtcod.BKGND_NONE, libtcod.LEFT, "Jumps:")
		for i in range(len(player.fighter.jump_array)):
			if player.fighter.jump_array[i] == 0:
				libtcod.console_set_default_foreground(panel, jump_charged_color)
				libtcod.console_print_ex(panel, player_panel_x + 6 + i, 7, libtcod.BKGND_NONE, libtcod.LEFT, '*')
			else:
				libtcod.console_set_default_foreground(panel, jump_uncharged_color)
				libtcod.console_print_ex(panel, player_panel_x + 6 + i, 7, libtcod.BKGND_NONE, libtcod.LEFT, '*')


	#LEVEL PANEL STUFF
	libtcod.console_set_default_foreground(panel, libtcod.white)
	libtcod.console_print_ex(panel, level_panel_x, 1, libtcod.BKGND_NONE, libtcod.LEFT,
	'Level:  ' + str(dungeon_level))
	libtcod.console_print_ex(panel, level_panel_x, 2, libtcod.BKGND_NONE, libtcod.LEFT,
	'Time:   ' + str(time))
	libtcod.console_print_ex(panel, level_panel_x, 3, libtcod.BKGND_NONE, libtcod.LEFT,
	'Alarm:  ' + str(alarm_level))
	libtcod.console_print_ex(panel, level_panel_x, 4, libtcod.BKGND_NONE, libtcod.LEFT,
	'Keys:   ' + str(key_count) + '/' + str(lev_set.keys_required))


	if favoured_by_healer:
		libtcod.console_print_ex(panel, level_panel_x + BAR_WIDTH/2, 8, libtcod.BKGND_NONE, libtcod.CENTER,
		'Favoured by ' + god_healer.name)

	elif favoured_by_destroyer:
		libtcod.console_print_ex(panel, level_panel_x + BAR_WIDTH/2, 8, libtcod.BKGND_NONE, libtcod.CENTER,
		'Favoured by ' + god_destroyer.name)

	elif tested_by_destroyer:
		libtcod.console_print_ex(panel, level_panel_x + BAR_WIDTH/2, 8, libtcod.BKGND_NONE, libtcod.CENTER,
		'Tested by ' + god_destroyer.name + '(' + str(destroyer_test_count) + ')')

	elif favoured_by_deliverer:	# actually for the deliverer you probably never get this message, right? If the mission is to complete level quickly?
		libtcod.console_print_ex(panel, level_panel_x + BAR_WIDTH/2, 8, libtcod.BKGND_NONE, libtcod.CENTER,
		'Favoured by ' + god_deliverer.name)

	elif tested_by_deliverer:
		libtcod.console_print_ex(panel, level_panel_x + BAR_WIDTH/2, 8, libtcod.BKGND_NONE, libtcod.CENTER,
		'Tested by ' + god_deliverer.name + '(' + str(deliverer_test_count) + ')')

	#display names of objects under the mouse
	libtcod.console_set_default_foreground(panel, libtcod.light_gray)
	libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT, get_names_under_mouse())

	#blit the contents of "panel" to the root console
	libtcod.console_blit(panel, 0, 0, SCREEN_WIDTH, PANEL_HEIGHT, 0, 0, PANEL_Y)


# Here is where all the messages go
def create_message_panel():

	#GUI STUFF
	#prepare to render the GUI panel
	libtcod.console_set_default_background(message_panel, libtcod.black)
	libtcod.console_clear(message_panel)	
	
	#print the game messages, one line at a time
	y = 0
	for (line, color) in game_msgs:
		libtcod.console_set_default_foreground(message_panel, color)
		libtcod.console_print_ex(message_panel, 1, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
		#libtcod.console_print_ex(message_panel, MSG_X, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
		y += 1 


	#blit the contents of "message_panel" to the root console
	#libtcod.console_blit(message_panel, 0, 0, SCREEN_WIDTH, MESSAGE_PANEL_HEIGHT, 0, 0, 0)
	libtcod.console_blit(message_panel, 0, 0, MESSAGE_PANEL_WIDTH, MESSAGE_PANEL_HEIGHT, 0, 0, 0)


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


def reorder_objects():
	#rearrange the world objects so they appear in the correct order.
	#for now that order is: moving objects like the player and enemies drawn last, then 'keys', then weapons, then static objects like shrines and messages. Ummmm how do I do this
	global objects		
	# Rough plan: move all the keys to the back. then, move all the weapons to the back. then, move all the non-movey things to do the back.
	# Identifying elements to move is currently done in a very janky object-specific way, and is likely to break when I add new objects.
	total = len(objects)
	#index = total -1
	#step 1: move all keys to back
	index = 0
	while index < total: 				# >= 0:	
		#print str(objects[index].name)
		ob = objects[index]
		if ob.name == 'key':
			ob.send_to_back()
		index = index + 1 
	#step 2: move all weapons to back
	index = 0
	while index < total: 				# >= 0:	
		#print str(objects[index].name)
		ob = objects[index]
		if ob.weapon == True:
			ob.send_to_back()
		index = index + 1 

	#step 3: move all non-movey backroundy stuff (non-key, non-weapon, non-obstructey), except for decorations and attacks, to back
	index = 0
	while index < total: 				# >= 0:	
		#print str(objects[index].name)
		ob = objects[index]
		if ob.blocks == False and ob.weapon == False and ob.name != 'key' and ob.name != 'decoration' and not ob.attack:
			ob.send_to_back()
		index = index + 1 	

	#step 3.5: move all attacks to back
	index = 0
	while index < total: 				# >= 0:	
		#print str(objects[index].name)
		ob = objects[index]
		if ob.attack:
			ob.send_to_back()
		index = index + 1 

	#step 4: finally, decorations, the lowest of the low.
	index = 0
	while index < total: 				# >= 0:	
		#print str(objects[index].name)
		ob = objects[index]
		if ob.name == 'decoration':
			ob.send_to_back()
		index = index + 1 
	# Well; let's see if this works..


def initialise_game():
	global current_big_message, game_msgs, game_level_settings, dungeon_level, time, spawn_timer, player, player_weapon, objects, game_state, player_action, con, enemy_spawn_rate, favoured_by_healer, favoured_by_destroyer, tested_by_destroyer,  favoured_by_deliverer, tested_by_deliverer,  god_healer, god_destroyer, god_deliverer, camera, alarm_level, already_healed_this_level
	current_big_message = 'You weren\'t supposed to see this'


	#Initialise controls

	#create the list of game messages and their colors, starts empty
	game_msgs = []
	
	game_level_settings = Level_Settings()
	dungeon_level = 0
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
	time = 1
	
	#create object representing the player
	fighter_component = Energy_Fighter(hp=6, defense=2, power=5, death_function=player_death, jump_array = [0,0,0,0])
	#fighter_component = Fighter(hp=10, defense=2, power=5, death_function=player_death, jump_array = [0,0,0,0])
	decider_component = Decider()
	player = Object(0, 0, '@', 'player', libtcod.white, blocks=True, fighter=fighter_component, decider=decider_component)
	camera = Location(player.x, player.y)
	
	#WEAPON SELECT
	player_weapon = Weapon_Sword()
	#player_weapon = Weapon_Wierd_Staff()
	#player_weapon = Weapon_Katana()
	#player_weapon = Weapon_Dagger()
	
	#the list of objects starting with the player
	objects = [player]
	
	make_map()
	
	initialize_fov()
	
	game_state = 'playing'
	player_action = None
	
	#a warm welcoming message!
	message('Welcome! Use arrows or 1-9 to move, qweasdzxc to attack, p to pick up a new weapon. Go right for a tutorial, or step into the elevator on your left to go to Level 1.', libtcod.cyan)


	libtcod.console_set_default_foreground(con, libtcod.white)
	libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE,key,mouse)
	render_all()
	libtcod.console_flush()




#libtcod.console_set_custom_font('arial12x12.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

libtcod.console_set_custom_font('arial14test2.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)


libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)

con = libtcod.console_new(MAP_WIDTH, MAP_HEIGHT)
panel = libtcod.console_new(SCREEN_WIDTH, PANEL_HEIGHT)
message_panel = libtcod.console_new(SCREEN_WIDTH, MESSAGE_PANEL_HEIGHT)
pause_menu = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

mouse = libtcod.Mouse()
key = libtcod.Key()

libtcod.sys_set_fps(LIMIT_FPS) 

initialise_game()


lev_set = game_level_settings.get_setting(dungeon_level)

enemy_spawn_rate = lev_set.enemy_spawn_rate
spawn_timer = int(enemy_spawn_rate/alarm_level)

time_since_last_elevator_message = 0

ready_for_next_level = False

# So for future reference, this code prints the numbers 1 to 9:
#for num in range(1,10):
#	print str(num)


# Main loop!
while not libtcod.console_is_window_closed():


	garbage_list = []	#list of things (e.g. dead bodies) to delete from objects list at the end of the loop

#	libtcod.console_put_char(con, playerx, playery, ' ', libtcod.BKGND_NONE)
	for object in objects:
		object.clear()

	#get player decisions and handle keys and exit game if needed
	player_action = handle_keys()
	if player_action == 'pause':
		if game_state == 'playing':
			game_state = 'paused'
		elif game_state == 'paused' or game_state == 'big message':
			game_state = 'playing'
	#	break

	# Game things happen woo!
	elif game_state == 'playing' and player_action != 'didnt-take-turn' and player_action != 'pickup_dialog' and player_action != 'jump_dialog' :
		
		
		time += 1
		spawn_timer -= 1
		update_nav_data()

		player_hit_something = False
		player_clashed_something = False
		player_got_hit = False
		player_just_jumped = False

		if nearest_points_array[player.x][player.y] is not None:
			nearest_center_to_player =  nearest_points_array[player.x][player.y]


		# delete attacks from the past?! This is a fix because attacks seem to be hanging around longer than I'd like, may cause problems further down the line...
		deletionList = []
		for object in objects:
			if object.attack:
				object.attack.fade()
				if object.attack.existing == False:
					deletionList.append(object)
		# deleting attacks that have happened
		for object in objects:
			object.clear()
		for object in deletionList:
			objects.remove(object)

		#let monsters take their decisions
		for object in objects:
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
		for object in objects:
			if object.decider:
				if object.decider.decision is not None:
					if object.decider.decision.move_decision is not None:
						md = object.decider.decision.move_decision
						if md.dx != 0 or md.dy != 0:	# let's not have people punch themselves just by standing still.
							target_x = object.x + md.dx
							target_y = object.y + md.dy	
							for victim in objects:
								# try to punch if there's a fighter in this square
								if victim.fighter and victim.x == target_x and victim.y == target_y:
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
									print str(victim.name)
								

		# firstly movement happens
		# player always moves first
		if player.decider:
			if player.decider.decision is not None:
				if player.decider.decision.move_decision is not None:
					md = player.decider.decision.move_decision
					if map[player.x + md.dx][player.y + md.dy].blocked:
						message ("You walk into a wall.")
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
						message("Your legs are too tired to jump!")
					elif map[player.x + tempx][player.y + tempy].blocked:
						somethingInWay = True
						message("There's a wall in the way!")
					else: 
						#check for doors, and/or find the thing the player is jumping over.
						for ob in objects:
							if ob.door and ob.x == player.x + tempx and ob.y == player.y + tempy:
								somethingInWay = True
							if ob.fighter and ob.x == player.x + tempx and ob.y == player.y + tempy:
								jumpee = ob	
						if somethingInWay == True:
							message("There's a door in the way!")
					if somethingInWay == False:
						if map[player.x + jd.dx][player.y + jd.dy].blocked:
							message ("You leap gracefully into a wall.")
							player.move(tempx, tempy)
						else:
							if jumpee is not None:
								message ("You leap over the " + jumpee.name + "\'s head!")
						player.fighter.make_jump()
						player.move(jd.dx, jd.dy)
						player_just_jumped = True

		for object in objects:
			if object.decider and object is not player:
				if object.decider.decision is not None:
					if object.decider.decision.move_decision is not None:
						md = object.decider.decision.move_decision
						object.move(md.dx, md.dy)	

		


		# do some messages saying what you see here!
		#names = [obj.name for obj in objects
		#	if obj.x == player.x and obj.y == player.y and obj is not player]
		objects_here = [obj for obj in objects
			if obj.x == player.x and obj.y == player.y and obj is not player]
		names = [obj.name for obj in objects_here if obj.floor_message is None]
		possible_commands = []

		weapon_found = False
		key_found = False
		stairs_found = False
		shrine_found = False
		floor_message_found = False
	
		floor_message_text = ''
		for obj in objects_here:
			if weapon_found == False and obj.weapon == True:
				weapon_found = True
				if key_found == False:
					possible_commands.append('p to pick up')
			if key_found == False and obj.name == 'key':
				key_found = True
				if weapon_found== False:
					possible_commands.append('p to pick up')
			if stairs_found == False and obj.name == 'stairs':
				stairs_found = True
				possible_commands.append('< to ascend')
			if shrine_found == False and obj.shrine is not None:
				shrine_found = True
				possible_commands.append('o to meditate')
			if floor_message_found == False and obj.floor_message is not None:
				floor_message_text = obj.floor_message.string
				floor_message_found = True
			
		if floor_message_found == True:
			message('You see a message on the floor:')
			message('\"' + floor_message_text + '\"', libtcod.cyan)

		if len(names) > 0:
			names = ', '.join(names)
			possible_commands = ', '.join(possible_commands)
			temp_message = 'You see a ' + names + ' here (' + possible_commands + ').'
			message(temp_message)





		# draw things in their new places
		if player.decider.decision:
			if player.decider.decision.move_decision or player.decider.decision.jump_decision:			
				fov_recompute = True

		for object in objects:
			object.clear()
		libtcod.console_set_default_foreground(con, libtcod.white)
		libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE,key,mouse)
		render_all()
		libtcod.console_flush()

		
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
						message("\"Access to the next floor is restricted by security. " + str(lev_set.keys_required) + " keys required.\"")
						time_since_last_elevator_message = 0
			for (x,y) in ele.door_points:
				if player.x == x and player.y == y:
					player_in_doorway = True				
			ele.update(elevator_occupied, player_in_elevator, player_near_elevator, player_in_doorway)
			if ele.doors_opening == True:
				#play a 'ding' noise if the player can see the doors opening
				for door in ele.special_door_list:
					if libtcod.map_is_in_fov(fov_map, door.x, door.y):
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
			message("Ding!")

		# update elevators with whether the player is authorized - for now this is just based on whether there are security systems around.
		# later this process will become a bit more complicated (and might be folded into Elevator.update)
		level_complete = False
		if lev_set.boss is not None:
			level_complete = True
			#check for bosses?
			for object in objects:
				if object.name == lev_set.boss:
					level_complete = False
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
			#print "opening door"
			victim.door.open()
			# Here is another terrible hack, to make it so an alarmer actually spots you when you open a door on it
			libtcod.map_compute_fov(fov_map, player.x, player.y, TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)
		


		spotted = False

		#UPDATE THE ALARMERS
		for ob in objects:
			if ob.alarmer is not None:
				if libtcod.map_is_in_fov(fov_map, ob.x, ob.y):
					ob.alarmer.update(True)
					spotted = True
				else: 
					ob.alarmer.update(False)

		#if spotted == True:
		#	print "Alarmage status: spotted"
		#else: 
		#	print "Alarmage status: NOT spotted"

		# now create attacks!
		deletionList = []
		for object in objects:
			if object.decider:
				if object.decider.decision is not None:
					if object.decider.decision.attack_decision is not None:
						attack_list = object.decider.decision.attack_decision.attack_list
						for attack in attack_list:
							objects.append(attack)	
							attack.send_to_front()

		player_just_attacked = False
		if player.decider.decision is not None:
			if player.decider.decision.attack_decision is not None:
				player_attack_list = player.decider.decision.attack_decision.attack_list
				if len(attack_list) > 0:
					player_just_attacked = True

		#if player_just_attacked:
		#	print 'the player just attacked!'

		# draw things with the attacks!
		for object in objects:
			object.clear()
		libtcod.console_set_default_foreground(con, libtcod.white)
		libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE,key,mouse)
		render_all()
		libtcod.console_flush()

		# process attacks!

		#check if the player is getting 'hit' (whether or not the attack gets deflected)

		for object in objects:
			if object.attack:
				attackee = object.attack.find_attackee()
				if attackee == player:
					player_got_hit = True

		# attacks 'bouncing' off each other (when an attack from A hits B and vice versa, neither attack damages)
		clashing_pairs_list = []
		deletionList = []
		for object in objects:
			if object.attack:
				attackee = object.attack.find_attackee()
				for other_object in objects:
					# perform a check to ensure each unordered pair only gets processed once
					if object.x < other_object.x or (object.x == other_object.x and object.y <= other_object.y):
						if other_object.attack and other_object.attack.attacker == attackee:
							other_attackee = other_object.attack.find_attackee()
							if other_attackee == object.attack.attacker:
								# so now we have two fighters attacking each other
								clashing_pairs_list.append((object, other_object))
								# deletion happens, because the attacks "cancel each other out"
								deletionList.append(object)
								deletionList.append(other_object)
								message('Clash! The ' + attackee.name + ' and ' + other_attackee.name + '\'s attacks bounce off each other!')
								if attackee is player or other_attackee is player:
									player_clashed_something = True
		for object in objects:
			object.clear()
		for object in deletionList:
			objects.remove(object)

		## regular old attacks just happening
		deletionList = []
		for object in objects:
			if object.attack:
				object.attack.inflict_damage()
				object.attack.fade()
				if object.attack.existing == False:
					deletionList.append(object)
		# deleting attacks that have happened
		for object in objects:
			object.clear()
		for object in deletionList:
			objects.remove(object)
	

		#recharge player attack charge. this probably shouldn't go here ultimately
		#if player_recharge_time > 0:
		#	player_recharge_time = player_recharge_time - 1
		player_weapon.recharge(player.fighter.recharge_rate)
	




		# refresh the player's energy
		# design question: when should this refresh? maybe it's only if you haven't done an attack? if you haven't been hurt?
		if player_just_attacked == False and player_got_hit == False and player_just_jumped == False:
			player.fighter.gain_energy(1)


		##recharge player jump? TODO well, how should jumping work...
		#player.fighter.recharge_jumps()

		
		#weapon degradation time!
		if( player_hit_something == True or player_clashed_something == True) and player_weapon.durability > 0:
			degredation = 0
			if player_clashed_something:
				degredation = 2
			else:
				degredation = 1
			if player_weapon.durability - degredation  <= WEAPON_FAILURE_WARNING_PERIOD and player_weapon.durability > WEAPON_FAILURE_WARNING_PERIOD:
				message("Your "  + player_weapon.name + " is close to breaking!", libtcod.orange)
			player_weapon.durability -= degredation
			if player_weapon.durability <= 0:
				message("Your " + player_weapon.name + " breaks!", libtcod.red)
		

		# clean up stuff
		for object in garbage_list:
			objects.remove(object)
		
		#refresh decisions!
		for object in objects:
			if object.decider:	
				object.decider.refresh()



		# Now do alarm soundings! and other alarmer-based stuff
		for ob in objects:
			if ob.alarmer is not None:
				#prev_suspicious = (ob.alarmer.status == 'suspicious')	# ugh what horrible code

				# first, update the alarmer
				
				#ob.alarmer.update(libtcod.map_is_in_fov(fov_map, ob.x, ob.y))

				# next, do things depending on the alarmer's state
				if ob.alarmer.status == 'idle' or  ob.alarmer.status == 'pre-suspicious':
					ob.color = ob.alarmer.idle_color
				elif ob.alarmer.status == 'suspicious':
					if ob.alarmer.prev_suspicious == False:
						message('The ' + ob.name + ' is suspicious!', libtcod.orange)		
						ob.color = ob.alarmer.suspicious_color

				elif ob.alarmer.status == 'raising-alarm':
					alarm_level += ob.alarmer.alarm_value
					spawn_timer = 1		#run the  spawn clock forwards so new enemies appear
					message('The ' + ob.name + ' sounds a loud alarm!', libtcod.red)
					ob.color = ob.alarmer.alarmed_color
				elif ob.alarmer.status == 'alarm-raised':
					ob.color = ob.alarmer.alarmed_color	


		# oh let's start creating enemies at random intervals? 
		#if alarm_level > 0 and spawn_timer % (enemy_spawn_rate/alarm_level) == 0: #and number_security_systems > 0:
		if alarm_level > 0 and spawn_timer <= 0:
			#reset timer
			spawn_timer = int(enemy_spawn_rate/alarm_level)

		#	reorder_objects() #temp test
		#	print 'tick'
		#	print 'enemy spawn rate = ' + str(enemy_spawn_rate)
		#	print 'total enemy prob = ' + str(lev_set.total_enemy_prob)
		#	print 'enemy probabilites = ' + str( lev_set.enemy_probabilities)
#			for (x,y) in spawn_points:

			# check if level is complete
			level_complete = False
			if lev_set.boss is not None:
				level_complete = True
				#check for bosses?
				for object in objects:
					if object.name == lev_set.boss:
						level_complete = False
			#elif number_security_systems <= 0:
			#	level_complete = True
			elif lev_set.keys_required <= key_count:
				level_complete = True

			# are there too many monsters?
			total_monsters = 0
			for object in objects:
				if object.fighter is not None:
					total_monsters = total_monsters + 1

			# if level_complete == False and    #currently commented out because it stops spawning when you have enough keys
			# probably the 'level_complete' stuff should be looked at and possibly taken out altogether
			if total_monsters < lev_set.max_monsters:		#otherwise, stop the spawning
				elevator_shortlist = []
				if lev_set.level_type == 'arena':	#pick one elvator at random
					choice =  libtcod.random_get_int(0, 0, len(elevators)-1)
					elevator_shortlist.append(elevators[choice])
				else:					# do all elevators at once
					elevator_shortlist = elevators
				for ele in elevator_shortlist:
					#pick a random spawn point from those available
	
					num =  libtcod.random_get_int(0, 0, len(ele.spawn_points)-1)
					(x,y) = ele.spawn_points[num] 
					#for (x,y) in ele.spawn_points:
					if not is_blocked(x, y):
						#print 'ding'
	#ELEVATOR SPAWNING MONKEY HORSESHOE
						total_enemy_prob = lev_set.total_enemy_prob
						enemy_probabilities = lev_set.enemy_probabilities
						enemy_name = 'none'
						num = libtcod.random_get_int(0,0, total_enemy_prob)
						for (name, prob) in enemy_probabilities:
						#	print 'hi'
							#print '(' + name + ',' + str(prob) + ')'
							if num <= prob:
								enemy_name = name
#								print 'tick' + str(x) + ',' + str(y) + ' ' + name
								monster = create_monster(x,y, name)
								objects.append(monster)
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
	

	#num_monsters = libtcod.random_get_int(0, 0, max_room_monsters)
#


	elif game_state == 'playing' and player_action == 'pickup_dialog':
		render_all()


	elif game_state == 'playing' and player_action == 'jump_dialog':
		render_all()



	# I guess let's draw things once more?	
	for object in objects:
		object.clear()
	libtcod.console_set_default_foreground(con, libtcod.white)
	
	

	libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE,key,mouse)

	if game_state == 'paused':
		pause_screen()
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

	libtcod.console_flush()

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




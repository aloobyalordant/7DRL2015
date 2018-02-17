import tdl as libtcod
#import libtcodpy as libtcod
import random
from random import randint

#Controls
#ControlMode = 'Crypsis' 	# 'Wheatley'   'Glados'
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


# A generic class for weapons, that hopefully I can make everything an extension of
class Generic_Weapon:
	def __init__(self, name, max_charge, current_charge, default_usage, durability = 50):
		self.name = name
		self.max_charge = max_charge
		self.current_charge = current_charge
		self.default_usage = default_usage
		self.durability = durability
		self.just_attacked = False
		self.command_items = []
		#self.command_list = 'acdeqswxz'

	# Look up the attack corresponding to a command, use up the required charge and return the attach data
	def do_attack(self, command):
		for (com, data, usage) in self.command_items:
			if com == command and usage <= self.current_charge and self.durability > 0:
				self.current_charge = self.current_charge - usage
				self.just_attacked = True
				return data


	#get attack data without using up charge (for 'energy_fighter' types who use their own energy to wield a weapon)
	def do_energy_attack(self, command):
		for (com, data, usage) in self.command_items:
			if com == command and self.durability > 0:
				self.just_attacked = True
				return data

	# return the how much charge / energy a given attack will use.
	def get_usage_cost(self, command):
		for (com, data, usage) in self.command_items:
			if com == command:
				return usage
		print('attack not found, returning cost 0')
		return 0

	# return the how much charge / energy a given attack will use.
	def get_default_usage_cost(self):
		(com, data, usage) = self.command_items[0]
		return usage


	# recharge the weapon (for non-'energy_fighter' types)
	def recharge(self, recharge_val = 1):
		if self.just_attacked == False:
			self.current_charge = self.current_charge + recharge_val
		if self.current_charge > self.max_charge:
			self.current_charge = self.max_charge
		self.just_attacked = False






def create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos):
	return_array = []
	#changed 'xrange' to 'range' for python3
	for j in range(len(temp_array)):
		for i in range(len(temp_array[j])):
			#print ('(' +str(j) + ',' + str(i) + '), (' + str(j-y_start_offset) + ',' + str(i-x_start_offset) + ')')
			if (temp_array[j][i] > 0):
				return_array.append((i-ava_x_pos,j-ava_y_pos,temp_array[j][i]))
	return return_array











class Weapon_Staff(Generic_Weapon):

	def __init__(self):
		Generic_Weapon.__init__(self, 'bo staff', 1, 1, 1)
		default_usage = self.default_usage

		command = ATTCKUP
		temp_array =	 [[0,0,0,0,0],
				  [0,1,1,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKUPRIGHT
		temp_array =	 [[0,0,0,0,1],
				  [0,0,0,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,1,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKDOWNRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,1]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKDOWN
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,1,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = ATTCKDOWNALT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,1,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKDOWNLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,0,0],
				  [1,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,1,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKUPLEFT
		temp_array =	 [[1,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



	######################



class Weapon_Wierd_Staff(Generic_Weapon):
	def __init__(self):
		Generic_Weapon.__init__(self, 'wierd bo staff', 10, 10, 3)
		default_usage = self.default_usage

	def __init__(self):
		
		command = ATTCKUP
		temp_array =	 [[0,0,0,0,0],
				  [0,1,1,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKUPRIGHT
		temp_array =	 [[0,0,0,0,1],
				  [0,0,0,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,1,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKDOWNRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,1]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKDOWN
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,1,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = ATTCKDOWNALT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,1,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKDOWNLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,0,0],
				  [1,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,1,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKUPLEFT
		temp_array =	 [[1,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


	######################



class Weapon_Spear(Generic_Weapon):

	def __init__(self):
		Generic_Weapon.__init__(self, 'spear', 1, 1, 1)
		default_usage = self.default_usage
		#self.command_list = []
		#self.command_items = []
		
		command = ATTCKUP
		temp_array =	 [[0,0,1,0,0],
				  [0,0,1,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))




		command = ATTCKRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,1,1],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKDOWN
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,0,1,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = ATTCKDOWNALT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,0,1,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))




		command = ATTCKLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [1,1,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


	#	for (command, data,usage) in self.command_items:
	#		self.command_list.append(command)

	######################



class Weapon_Sword(Generic_Weapon):

	def __init__(self):
		Generic_Weapon.__init__(self, 'sword', 2, 2, 1)
		default_usage = self.default_usage
		
		command = ATTCKUP
		temp_array =	 [[0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKUPRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKDOWNRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKDOWN
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = ATTCKDOWNALT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKDOWNLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKUPLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


#############


# ok, bear with me, trying a thing. What if you hadlots more charge but your  weapons used more energy / recharged slower
class Weapon_Wierd_Sword(Generic_Weapon):

	def __init__(self):
		Generic_Weapon.__init__(self, 'wierd sword', 10, 10, 2)
		default_usage = self.default_usage
		
		command = ATTCKUP
		temp_array =	 [[0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKUPRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKDOWNRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKDOWN
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = ATTCKDOWNALT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKDOWNLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKUPLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


#############



class Weapon_Dagger(Generic_Weapon):
	# like a sword, but does more damage and is a bit slower? Used by ninjas? Who knows



	def __init__(self):
		Generic_Weapon.__init__(self, 'dagger', 1, 1, 1)
		default_usage = self.default_usage

		
		command = ATTCKUP
		temp_array =	 [[0,0,0,0,0],
				  [0,0,2,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKUPRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,2,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,2,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKDOWNRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,2,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKDOWN
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,2,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = ATTCKDOWNALT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,2,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKDOWNLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,2,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,2,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKUPLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,2,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))





class Weapon_Unarmed(Generic_Weapon):



	def __init__(self):
		Generic_Weapon.__init__(self, 'unarmed', 0, 0, 0)
		default_usage = self.default_usage


		# NO WEAPON ATTACKS GO HERE BECAUSE IT IS UNARMED!

	# return the how much charge / energy a given attack will use.
	def get_default_usage_cost(self):
		return 0


##############



class Weapon_Sai(Generic_Weapon):

	def __init__(self):
		Generic_Weapon.__init__(self, 'sai', 1, 1, 1)
		default_usage = self.default_usage
		
		command = ATTCKUP
		temp_array =	 [[0,0,0,0,0],
				  [0,1,0,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))




		command = ATTCKRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))




		command = ATTCKUPRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKDOWNRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,1,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = ATTCKDOWN
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = ATTCKDOWNALT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))





		command = ATTCKLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))

		command = ATTCKUPLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))

		command = ATTCKDOWNLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,1,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))





class Weapon_Sai_Alt(Generic_Weapon):

	def __init__(self):
		Generic_Weapon.__init__(self, 'sai', 10, 1, 1)
		default_usage = self.default_usage
		
		command = ATTCKUP
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [1,1,0,1,1],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))




		command = ATTCKRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,1,1],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))




		command = ATTCKUPRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKDOWNRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = ATTCKDOWN
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [1,1,0,1,1],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = ATTCKDOWNALT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [1,1,0,1,1],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))





		command = ATTCKLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [1,1,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))

		command = ATTCKUPLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))

		command = ATTCKDOWNLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKUPLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



#############

#############

class Weapon_Sai_Alt_Alt(Generic_Weapon):

	def __init__(self):
		Generic_Weapon.__init__(self, 'sai', 1, 1, 1)
		default_usage = self.default_usage
		
		command = ATTCKUP
		temp_array =	 [[0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))




		command = ATTCKRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))




		command = ATTCKUPRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKDOWNRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = ATTCKDOWN
		temp_array =	 [[0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = ATTCKDOWNALT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))





		command = ATTCKLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))

		command = ATTCKUPLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))

		command = ATTCKDOWNLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKUPLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



##############


# ok, hear me out. Nunchucks... have infinite charge essentially, but do a random attack?
# this is based on my own very poor understanding of what's going on when I see nunchucks in action
class Weapon_Nunchuck(Generic_Weapon):

	def __init__(self):
		Generic_Weapon.__init__(self, 'nunchaku', 1, 1, 0)
		default_usage = self.default_usage
		
		command = ATTCKUPLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,1,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKUP
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = ATTCKUPRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = ATTCKLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,1,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKDOWNLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,1,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))





		command = ATTCKDOWN
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))




		command = ATTCKDOWNRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = ATTCKRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,1,1,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = 'g'
		temp_array =	 [[0,0,0,0,0],
				  [1,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = 'h'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,0,0],
				  [1,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = 'i'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,1,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = 'j'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,0,0,1,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))




		command = 'm'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,1],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = 'n'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,1],
				  [0,0,0,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = 'q'
		temp_array =	 [[0,0,0,1,0],
				  [0,0,1,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = 'r'
		temp_array =	 [[0,1,0,0,0],
				  [0,0,1,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = 's'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = 't'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = 'u'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,1,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = 'v'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,1,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = 'w'
		temp_array =	 [[0,0,1,0,0],
				  [0,0,1,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = 'x'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,0,1,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = 'y'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,1,1],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = 'z'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [1,1,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))







	# random attack! This is not how weapons normally work
	def do_attack(self, command):
		for (com, data, usage) in self.command_items:
			if com == command:
				#for (com, data, usage) in self.command_items:
				#choice = libtcod.random_get_int(0, 0, len(self.command_items)-1)
				choice = randint(0, len(self.command_items)-1)
				(com, data, usage) = self.command_items[choice]
				if usage <= self.current_charge and self.durability > 0:
					self.current_charge = self.current_charge - usage
					self.just_attacked = True
					return data
#		return generic_do_attack(choice, self.command_items, self.current_charge, self.durability)

	#get attack data without using up charge (for 'energy_fighter' types who use their own energy to wield a weapon)
	def do_energy_attack(self, command):
		for (com, data, usage) in self.command_items:
			if com == command:
				#choice = libtcod.random_get_int(0, 0, len(self.command_items)-1)
				choice = randint(0, len(self.command_items)-1)
				(com, data, usage) = self.command_items[choice]
				if self.durability > 0:
					self.just_attacked = True
					return data

#############

class Weapon_Axe(Generic_Weapon):
	# A different version of the axe. Wider circles! Probably a nightmare to fight against in narrow corridors
	def __init__(self):
		Generic_Weapon.__init__(self, 'axe', 2, 2, 2)
		default_usage = self.default_usage
	
		self.command_items = []
		
		command = ATTCKUP
		temp_array =	 [[1,1,1,1,1],
				  [1,0,1,0,1],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))




		command = ATTCKRIGHT
		temp_array =	 [[0,0,0,1,1],
				  [0,0,0,0,1],
				  [0,0,0,1,1],
				  [0,0,0,0,1],
				  [0,0,0,1,1]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))




		command = ATTCKUPRIGHT
		temp_array =	 [[0,1,1,1,1],
				  [0,0,0,1,1],
				  [0,0,0,0,1],
				  [0,0,0,0,1],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKDOWNRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,1],
				  [0,0,0,0,1],
				  [0,0,0,1,1],
				  [0,1,1,1,1]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = ATTCKDOWN
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [1,0,1,0,1],
				  [1,1,1,1,1]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = ATTCKDOWNALT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [1,0,1,0,1],
				  [1,1,1,1,1]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))





		command = ATTCKLEFT
		temp_array =	 [[1,1,0,0,0],
				  [1,0,0,0,0],
				  [1,1,0,0,0],
				  [1,0,0,0,0],
				  [1,1,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))

		command = ATTCKUPLEFT
		temp_array =	 [[1,1,1,1,0],
				  [1,1,0,0,0],
				  [1,0,0,0,0],
				  [1,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))

		command = ATTCKDOWNLEFT
		temp_array =	 [[0,0,0,0,0],
				  [1,0,0,0,0],
				  [1,0,0,0,0],
				  [1,1,0,0,0],
				  [1,1,1,1,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))

#############



class Weapon_Hammer(Generic_Weapon):
	# swing it around! Originally a first draft of the axe, I'm going to try and bring it back.
	# intended to be good when you're surrounded?
	# Enemy will have ninja ai or something similar, because if they just attack when next to you, you can treat them just like swordsmen.
	# also increasing the charge usage, in hopes of reinforcing the 'wait till a lot of people surround you' play style.

	def __init__(self):
		Generic_Weapon.__init__(self, 'hammer', 2, 2, 2)
		default_usage = self.default_usage
		
		command = ATTCKUP
		temp_array =	 [[0,0,0,0,0],
				  [0,1,1,1,0],
				  [0,1,0,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))




		command = ATTCKRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,1,1,0],
				  [0,0,0,1,0],
				  [0,0,1,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))




		command = ATTCKUPRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,1,1,1,0],
				  [0,0,0,1,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKDOWNRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,1,0],
				  [0,1,1,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = ATTCKDOWN
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,1,0],
				  [0,1,1,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = ATTCKDOWNALT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,1,0],
				  [0,1,1,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))





		command = ATTCKLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,1,1,0,0],
				  [0,1,0,0,0],
				  [0,1,1,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))

		command = ATTCKUPLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,1,1,1,0],
				  [0,1,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))

		command = ATTCKDOWNLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,1,0,0,0],
				  [0,1,1,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



#############


class Weapon_Katana(Generic_Weapon):
	# Basically a bigger sword?
	def __init__(self):
		Generic_Weapon.__init__(self,  'katana', 1, 1, 1)
		default_usage = self.default_usage
	
		self.command_items = []
		
		command = ATTCKUPLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,1,1,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))




		command = ATTCKUPRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))




		command = ATTCKUP
		temp_array =	 [[0,0,1,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,1],
				  [0,0,0,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = ATTCKDOWNRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,1,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = ATTCKDOWNLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))

		command = ATTCKLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,1,0,0,0],
				  [1,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))

		command = ATTCKDOWN
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,1,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))

		command = ATTCKDOWNALT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,1,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



#############


class Weapon_Trident(Generic_Weapon):
	# Absolutely not a trident, but I have no idea what real-world weapon it would correspond to.
	# Basically makes close-range attakcs in 3 directions.
	# Should I make it slower than a sword? Or is it ok to be a strict upgrade that just appears later?
	def __init__(self):
		Generic_Weapon.__init__(self,  'trident', 1, 1, 1)
		default_usage = self.default_usage

		
		command = ATTCKUPLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,1,0],
				  [0,0,1,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))




		command = ATTCKUPRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,1,0,0,0],
				  [0,0,1,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))




		command = ATTCKUP
		temp_array =	 [[0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,0,0,0,0],
				  [0,1,0,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,1,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = ATTCKDOWNRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,1,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = ATTCKDOWNLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,0,0,1,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))

		command = ATTCKLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,1,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))

		command = ATTCKDOWN
		temp_array =	 [[0,0,0,0,0],
				  [0,1,0,1,0],
				  [0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))

		command = ATTCKDOWNALT
		temp_array =	 [[0,0,0,0,0],
				  [0,1,0,1,0],
				  [0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


#############


class Weapon_Ring_Of_Power(Generic_Weapon):
	# Ooooh, a big scary one! Yeah!
	def __init__(self):
		self.name = 'ring of power'
		self.command_list =  'acdeqswxz'
		self.max_charge = 8
		self.current_charge = 8
		self.default_usage = 2
		self.durability = 1000
		self.just_attacked = False
		default_usage = self.default_usage
	
		self.command_items = []
		
		command = ATTCKUP
		temp_array =	 [[0,0,1,0,0,1,0,0,1,0,0],
				  [0,0,1,0,0,1,0,0,1,0,0],
				  [0,0,0,1,0,1,0,1,0,0,0],
				  [0,0,0,1,0,1,0,1,0,0,0],
				  [0,0,0,0,1,1,1,0,0,0,0],
				  [0,0,0,0,1,0,1,0,0,0,0],
				  [0,0,0,0,0,1,0,0,0,0,0],
				  [0,0,0,0,0,0,0,0,0,0,0],
				  [0,0,0,0,0,0,0,0,0,0,0],
				  [0,0,0,0,0,0,0,0,0,0,0],
				  [0,0,0,0,0,0,0,0,0,0,0]]
		ava_x_pos = 5
		ava_y_pos = 5
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = ATTCKDOWNALT
		temp_array =	 [[0,0,0,0,0,0,0,0,0,0,0],
				  [0,0,0,0,0,0,0,0,0,0,0],
				  [0,0,0,0,0,0,0,0,0,0,0],
				  [0,0,0,0,0,0,0,0,0,0,0],
				  [0,0,0,0,0,1,0,0,0,0,0],
				  [0,0,0,0,1,0,1,0,0,0,0],
				  [0,0,0,0,1,1,1,0,0,0,0],
				  [0,0,0,1,0,1,0,1,0,0,0],
				  [0,0,0,1,0,1,0,1,0,0,0],
				  [0,0,1,0,0,1,0,0,1,0,0],
				  [0,0,1,0,0,1,0,0,1,0,0]]
		ava_x_pos = 5
		ava_y_pos = 5
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = ATTCKDOWN
		temp_array =	 [[0,0,0,0,0,0,0,0,0,0,0],
				  [0,0,0,0,0,0,0,0,0,0,0],
				  [0,0,0,0,0,0,0,0,0,0,0],
				  [0,0,0,0,0,0,0,0,0,0,0],
				  [0,0,0,0,0,1,0,0,0,0,0],
				  [0,0,0,0,1,0,1,0,0,0,0],
				  [0,0,0,0,1,1,1,0,0,0,0],
				  [0,0,0,1,0,1,0,1,0,0,0],
				  [0,0,0,1,0,1,0,1,0,0,0],
				  [0,0,1,0,0,1,0,0,1,0,0],
				  [0,0,1,0,0,1,0,0,1,0,0]]
		ava_x_pos = 5
		ava_y_pos = 5
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = ATTCKLEFT
		temp_array =	 [[0,0,0,0,0,0,0,0,0,0,0],
				  [0,0,0,0,0,0,0,0,0,0,0],
				  [1,1,0,0,0,0,0,0,0,0,0],
				  [0,0,1,1,0,0,0,0,0,0,0],
				  [0,0,0,0,1,1,0,0,0,0,0],
				  [1,1,1,1,1,0,1,0,0,0,0],
				  [0,0,0,0,1,1,0,0,0,0,0],
				  [0,0,1,1,0,0,0,0,0,0,0],
				  [1,1,0,0,0,0,0,0,0,0,0],
				  [0,0,0,0,0,0,0,0,0,0,0],
				  [0,0,0,0,0,0,0,0,0,0,0]]
		ava_x_pos = 5
		ava_y_pos = 5
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKRIGHT
		temp_array =	 [[0,0,0,0,0,0,0,0,0,0,0],
				  [0,0,0,0,0,0,0,0,0,0,0],
				  [0,0,0,0,0,0,0,0,0,1,1],
				  [0,0,0,0,0,0,0,1,1,0,0],
				  [0,0,0,0,0,1,1,0,0,0,0],
				  [0,0,0,0,1,0,1,1,1,1,1],
				  [0,0,0,0,0,1,1,0,0,0,0],
				  [0,0,0,0,0,0,0,1,1,0,0],
				  [0,0,0,0,0,0,0,0,0,1,1],
				  [0,0,0,0,0,0,0,0,0,0,0],
				  [0,0,0,0,0,0,0,0,0,0,0]]
		ava_x_pos = 5
		ava_y_pos = 5
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKUPLEFT
		temp_array =	 [[1,0,0,0,0,0,0,0,0,0,0],
				  [1,1,0,0,0,0,0,0,0,0,0],
				  [0,1,1,0,0,0,0,0,0,0,0],
				  [0,0,1,1,0,0,0,0,0,0,0],
				  [0,0,0,1,1,1,1,0,0,0,0],
				  [0,0,0,0,1,0,0,0,0,0,0],
				  [0,0,0,0,1,0,1,0,0,0,0],
				  [0,0,0,0,0,0,0,0,0,0,0],
				  [0,0,0,0,0,0,0,0,0,0,0],
				  [0,0,0,0,0,0,0,0,0,0,0],
				  [0,0,0,0,0,0,0,0,0,0,0]]
		ava_x_pos = 5
		ava_y_pos = 5
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))

		command = ATTCKUPRIGHT
		temp_array =	 [[0,0,0,0,0,0,0,0,0,1,1],
				  [0,0,0,0,0,0,0,0,1,1,0],
				  [0,0,0,0,0,0,0,1,1,0,0],
				  [0,0,0,0,0,0,1,1,0,0,0],
				  [0,0,0,0,1,1,1,0,0,0,0],
				  [0,0,0,0,0,0,1,0,0,0,0],
				  [0,0,0,0,1,0,1,0,0,0,0],
				  [0,0,0,0,0,0,0,0,0,0,0],
				  [0,0,0,0,0,0,0,0,0,0,0],
				  [0,0,0,0,0,0,0,0,0,0,0],
				  [0,0,0,0,0,0,0,0,0,0,0]]
		ava_x_pos = 5
		ava_y_pos = 5
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = ATTCKDOWNRIGHT
		temp_array =	 [[0,0,0,0,0,0,0,0,0,0,0],
				  [0,0,0,0,0,0,0,0,0,0,0],
				  [0,0,0,0,0,0,0,0,0,0,0],
				  [0,0,0,0,0,0,0,0,0,0,0],
				  [0,0,0,0,1,0,1,0,0,0,0],
				  [0,0,0,0,0,0,1,0,0,0,0],
				  [0,0,0,0,1,1,1,1,0,0,0],
				  [0,0,0,0,0,0,0,1,1,0,0],
				  [0,0,0,0,0,0,0,0,1,1,0],
				  [0,0,0,0,0,0,0,0,0,1,1],
				  [0,0,0,0,0,0,0,0,0,0,1]]
		ava_x_pos = 5
		ava_y_pos = 5
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = ATTCKDOWNLEFT
		temp_array =	 [[0,0,0,0,0,0,0,0,0,0,0],
				  [0,0,0,0,0,0,0,0,0,0,0],
				  [0,0,0,0,0,0,0,0,0,0,0],
				  [0,0,0,0,0,0,0,0,0,0,0],
				  [0,0,0,0,1,0,1,0,0,0,0],
				  [0,0,0,0,1,0,0,0,0,0,0],
				  [0,0,0,1,1,1,1,0,0,0,0],
				  [0,0,1,1,0,0,0,0,0,0,0],
				  [0,1,1,0,0,0,0,0,0,0,0],
				  [1,1,0,0,0,0,0,0,0,0,0],
				  [1,0,0,0,0,0,0,0,0,0,0]]
		ava_x_pos = 5
		ava_y_pos = 5
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))







#############


class Weapon_Strawhands(Generic_Weapon):
	# a bad weapon. Do not use it.
	def __init__(self):
		self.name = 'straw hand'
		self.command_list = ATTCKUP
		self.max_charge = 1
		self.current_charge = 1
		self.default_usage = 1
		self.durability = 1000
		self.just_attacked = False
		default_usage = self.default_usage
	
		self.command_items = []
		
		command = ATTCKUP
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))
	






class Weapon_Shiv(Generic_Weapon):
	# New thing: like a sword, but lighter
	def __init__(self):
		Generic_Weapon.__init__(self,  'shiv', 1, 1, 0)
		default_usage = self.default_usage

		
		command = ATTCKUPLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))




		command = ATTCKUPRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))




		command = ATTCKUP
		temp_array =	 [[0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = ATTCKDOWNRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = ATTCKDOWNLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))

		command = ATTCKLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))

		command = ATTCKDOWN
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))

		command = ATTCKDOWNALT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))





class Weapon_Broom(Generic_Weapon):
	# New thing: basically the cardinal directions of the bo staff

	def __init__(self):
		Generic_Weapon.__init__(self, 'broom', 1, 1, 1)
		default_usage = self.default_usage

		command = ATTCKUP
		temp_array =	 [[0,0,0,0,0],
				  [0,1,1,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = ATTCKRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,1,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKDOWN
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,1,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = ATTCKDOWNALT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,1,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,1,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))





# new thing: basically the diagonal directions of the bo staff
class Weapon_Pike(Generic_Weapon):

	def __init__(self):
		Generic_Weapon.__init__(self, 'pike', 1, 1, 1)
		default_usage = self.default_usage


		command = ATTCKUPRIGHT
		temp_array =	 [[0,0,0,0,1],
				  [0,0,0,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKDOWNRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,1]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKDOWNLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,0,0],
				  [1,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKUPLEFT
		temp_array =	 [[1,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



	######################



class Weapon_Halberd(Generic_Weapon):
	# A long range weapon, like a lighter but less flexible axe? can attack 3 spaces at distance but can't do anything up close
	def __init__(self):
		Generic_Weapon.__init__(self, 'halberd', 1, 1, 1)
		default_usage = self.default_usage
	
		self.command_items = []
		
		command = ATTCKUP
		temp_array =	 [[0,1,1,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))




		command = ATTCKRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,1],
				  [0,0,0,0,1],
				  [0,0,0,0,1],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))




		command = ATTCKUPRIGHT
		temp_array =	 [[0,0,0,1,1],
				  [0,0,0,0,1],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = ATTCKDOWNRIGHT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,1],
				  [0,0,0,1,1]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = ATTCKDOWN
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,1,1,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = ATTCKDOWNALT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,1,1,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))





		command = ATTCKLEFT
		temp_array =	 [[0,0,0,0,0],
				  [1,0,0,0,0],
				  [1,0,0,0,0],
				  [1,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))

		command = ATTCKUPLEFT
		temp_array =	 [[1,1,0,0,0],
				  [1,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))

		command = ATTCKDOWNLEFT
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [1,0,0,0,0],
				  [1,1,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))

#############




#return generic_do_attack(command, self.command_items, self.current_charge, self.durability)
#def generic_do_attack(command, command_items, current_charge, durability):
#	for (com, data, usage) in command_items:
#		if com == command and usage <= current_charge and durability > 0:
#			current_charge = current_charge - usage
#			return data

#(recharge_val, self.current_charge, self.max_charge)
#def generic_recharge(current_charge, max_charge, recharge_val = 1,):
#		current_charge = current_charge + recharge_val
#		if current_charge > max_charge:
#			current_charge = max_charge


import libtcodpy as libtcod

class Weapon_Staff:

	def __init__(self):
		self.name = 'bo staff'
		self.command_list = 'acdeqswxz'
		self.max_charge = 2
		self.current_charge = 2
		self.default_usage = 2
		self.durability = 50
		default_usage = self.default_usage
	
		self.command_items = []
		
		command = 'w'
		temp_array =	 [[0,0,0,0,0],
				  [0,1,1,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = 'e'
		temp_array =	 [[0,0,0,0,1],
				  [0,0,0,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = 'd'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,1,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = 'c'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,1]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = 'x'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,1,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = 's'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,1,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = 'z'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,0,0],
				  [1,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = 'a'
		temp_array =	 [[0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,1,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = 'q'
		temp_array =	 [[1,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


	
	def do_attack(self, command):
		for (com, data, usage) in self.command_items:
			if com == command and usage <= self.current_charge and self.durability > 0:
				self.current_charge = self.current_charge - usage
				return data


	def recharge(self, recharge_val = 1):
		self.current_charge = self.current_charge + recharge_val
		if self.current_charge > self.max_charge:
			self.current_charge = self.max_charge

	######################


class Weapon_Spear:

	def __init__(self):
		self.name = 'spear'
		self.command_list = 'adswx'
		self.max_charge = 2
		self.current_charge = 2
		self.default_usage = 2
		self.durability = 50
		default_usage = self.default_usage
	
		self.command_items = []
		
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




		command = 'd'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,1,1],
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


		command = 's'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,0,1,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))




		command = 'a'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [1,1,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



	
	def do_attack(self, command):
		for (com, data, usage) in self.command_items:
			if com == command and usage <= self.current_charge and self.durability > 0:
				self.current_charge = self.current_charge - usage
				return data


	def recharge(self, recharge_val = 1):
		self.current_charge = self.current_charge + recharge_val
		if self.current_charge > self.max_charge:
			self.current_charge = self.max_charge

	######################



class Weapon_Sword:

	def __init__(self):
		self.name = 'sword'
		self.command_list = 'acdeqswxz'
		self.max_charge = 3
		self.current_charge = 3
		self.default_usage = 2
		self.durability = 50
		default_usage = self.default_usage
	
		self.command_items = []
		
		command = 'w'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = 'e'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = 'd'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = 'c'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,1,0],
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
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = 's'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = 'z'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = 'a'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = 'q'
		temp_array =	 [[0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


	
	def do_attack(self, command):
		for (com, data, usage) in self.command_items:
			if com == command and usage <= self.current_charge and self.durability > 0:
				self.current_charge = self.current_charge - usage
				return data


	def recharge(self, recharge_val = 1):
		self.current_charge = self.current_charge + recharge_val
		if self.current_charge > self.max_charge:
			self.current_charge = self.max_charge


#############




class Weapon_Dagger:
	# like a sword, but does more damage and is a bit slower? Used by ninjas? Who knows
	def __init__(self):
		self.name = 'dagger'
		self.command_list = 'acdeqswxz'
		self.max_charge = 2
		self.current_charge = 2
		self.default_usage = 2
		self.durability = 50
		default_usage = self.default_usage
	
		self.command_items = []
		
		command = 'w'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,2,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = 'e'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,2,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = 'd'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,2,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = 'c'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,2,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = 'x'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,2,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = 's'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,2,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = 'z'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,2,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = 'a'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,2,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = 'q'
		temp_array =	 [[0,0,0,0,0],
				  [0,2,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


	
	def do_attack(self, command):
		for (com, data, usage) in self.command_items:
			if com == command and usage <= self.current_charge and self.durability > 0:
				self.current_charge = self.current_charge - usage
				return data


	def recharge(self, recharge_val = 1):
		self.current_charge = self.current_charge + recharge_val
		if self.current_charge > self.max_charge:
			self.current_charge = self.max_charge







##############



class Weapon_Sai:

	def __init__(self):
		self.name = 'sai'
		self.command_list = 'acdeqswxz'
		self.max_charge = 1
		self.current_charge = 1
		self.default_usage = 1
		self.durability = 50
		default_usage = self.default_usage
	
		self.command_items = []
		
		command = 'w'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [1,1,0,1,1],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))




		command = 'd'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,1,1],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))




		command = 'e'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = 'c'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = 'x'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [1,1,0,1,1],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = 's'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [1,1,0,1,1],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))





		command = 'a'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [1,1,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))

		command = 'q'
		temp_array =	 [[0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))

		command = 'z'
		temp_array =	 [[0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = 'q'
		temp_array =	 [[0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


	
	def do_attack(self, command):
		for (com, data, usage) in self.command_items:
			if com == command and usage <= self.current_charge and self.durability > 0:
				self.current_charge = self.current_charge - usage
				return data


	def recharge(self, recharge_val = 1):
		self.current_charge = self.current_charge + recharge_val
		if self.current_charge > self.max_charge:
			self.current_charge = self.max_charge


#############

class Weapon_Sai_Alt:

	def __init__(self):
		self.name = 'sai'
		self.command_list = 'acdeqswxz'
		self.max_charge = 2
		self.current_charge = 2
		self.default_usage = 2
		self.durability = 50
		default_usage = self.default_usage
	
		self.command_items = []
		
		command = 'w'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))




		command = 'd'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))




		command = 'e'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = 'c'
		temp_array =	 [[0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = 'x'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = 's'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,0,0,0,0],
				  [0,0,1,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))





		command = 'a'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))

		command = 'q'
		temp_array =	 [[0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))

		command = 'z'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = 'q'
		temp_array =	 [[0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


	
	def do_attack(self, command):
		for (com, data, usage) in self.command_items:
			if com == command and usage <= self.current_charge and self.durability > 0:
				self.current_charge = self.current_charge - usage
				return data


	def recharge(self, recharge_val = 1):
		self.current_charge = self.current_charge + recharge_val
		if self.current_charge > self.max_charge:
			self.current_charge = self.max_charge


##############


# ok, hear me out. Nunchucks... have infinite charge essentially, but do a random attack?
# this is based on my own very poor understanding of what's going on when I see nunchucks in action
class Weapon_Nunchuck:

	def __init__(self):
		self.name = 'nunchaku'
		self.command_list = 'abcdefghijkmnqrstuvwxyz'
		self.max_charge = 1
		self.current_charge = 1
		self.default_usage = 1
		self.durability = 50
		default_usage = self.default_usage
	
		self.command_items = []
		
		command = 'a'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,1,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = 'b'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = 'c'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = 'd'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,1,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = 'e'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,1,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))





		command = 'f'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))




		command = 'g'
		temp_array =	 [[0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = 'h'
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
				choice = libtcod.random_get_int(0, 0, len(self.command_items)-1)
				(com, data, usage) = self.command_items[choice]
				if usage <= self.current_charge and self.durability > 0:
					self.current_charge = self.current_charge - usage
					return data

#	def do_attack(self, command):
#		for (com, data, usage) in self.command_items:
#			if com == command and usage <= self.current_charge and self.durability > 0:
#				self.current_charge = self.current_charge - usage
#				return data


	def recharge(self, recharge_val = 1):
		self.current_charge = self.current_charge + recharge_val
		if self.current_charge > self.max_charge:
			self.current_charge = self.max_charge





#############

class Weapon_Axe:
	# A different version of the axe. Wider circles! Probably a nightmare to fight against in narrow corridors
	def __init__(self):
		self.name = 'axe'
		self.command_list = 'acdeqswxz'
		self.max_charge = 2
		self.current_charge = 2
		self.default_usage = 2
		self.durability = 50
		default_usage = self.default_usage
	
		self.command_items = []
		
		command = 'w'
		temp_array =	 [[1,1,1,1,1],
				  [1,0,1,0,1],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))




		command = 'd'
		temp_array =	 [[0,0,0,1,1],
				  [0,0,0,0,1],
				  [0,0,0,1,1],
				  [0,0,0,0,1],
				  [0,0,0,1,1]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))




		command = 'e'
		temp_array =	 [[0,1,1,1,1],
				  [0,0,0,1,1],
				  [0,0,0,0,1],
				  [0,0,0,0,1],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = 'c'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,1],
				  [0,0,0,0,1],
				  [0,0,0,1,1],
				  [0,1,1,1,1]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = 'x'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [1,0,1,0,1],
				  [1,1,1,1,1]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = 's'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [1,0,1,0,1],
				  [1,1,1,1,1]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))





		command = 'a'
		temp_array =	 [[1,1,0,0,0],
				  [1,0,0,0,0],
				  [1,1,0,0,0],
				  [1,0,0,0,0],
				  [1,1,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))

		command = 'q'
		temp_array =	 [[1,1,1,1,0],
				  [1,1,0,0,0],
				  [1,0,0,0,0],
				  [1,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))

		command = 'z'
		temp_array =	 [[0,0,0,0,0],
				  [1,0,0,0,0],
				  [1,0,0,0,0],
				  [1,1,0,0,0],
				  [1,1,1,1,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


	
	def do_attack(self, command):
		for (com, data, usage) in self.command_items:
			if com == command and usage <= self.current_charge and self.durability > 0:
				self.current_charge = self.current_charge - usage
				return data


	def recharge(self, recharge_val = 1):
		self.current_charge = self.current_charge + recharge_val
		if self.current_charge > self.max_charge:
			self.current_charge = self.max_charge


#############



class Weapon_Hammer:
	# swing it around! Originally a first draft of the axe, I'm going to try and bring it back.
	# intended to be good when you're surrounded?
	# Enemy will have ninja ai or something similar, because if they just attack when next to you, you can treat them just like swordsmen.
	# also increasing the charge usage, in hopes of reinforcing the 'wait till a lot of people surround you' play style.

	def __init__(self):
		self.name = 'hammer'
		self.command_list = 'acdeqswxz'
		self.max_charge = 3
		self.current_charge = 3
		self.default_usage = 3
		self.durability = 50
		default_usage = self.default_usage
	
		self.command_items = []
		
		command = 'w'
		temp_array =	 [[0,0,0,0,0],
				  [0,1,1,1,0],
				  [0,1,0,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))




		command = 'd'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,1,1,0],
				  [0,0,0,1,0],
				  [0,0,1,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))




		command = 'e'
		temp_array =	 [[0,0,0,0,0],
				  [0,1,1,1,0],
				  [0,0,0,1,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = 'c'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,1,0],
				  [0,1,1,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = 'x'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,1,0],
				  [0,1,1,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = 's'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,1,0],
				  [0,1,1,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))





		command = 'a'
		temp_array =	 [[0,0,0,0,0],
				  [0,1,1,0,0],
				  [0,1,0,0,0],
				  [0,1,1,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))

		command = 'q'
		temp_array =	 [[0,0,0,0,0],
				  [0,1,1,1,0],
				  [0,1,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))

		command = 'z'
		temp_array =	 [[0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,1,0,0,0],
				  [0,1,1,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


	
	def do_attack(self, command):
		for (com, data, usage) in self.command_items:
			if com == command and usage <= self.current_charge and self.durability > 0:
				self.current_charge = self.current_charge - usage
				return data


	def recharge(self, recharge_val = 1):
		self.current_charge = self.current_charge + recharge_val
		if self.current_charge > self.max_charge:
			self.current_charge = self.max_charge


#############


class Weapon_Katana:
	# Basically a bigger sword?
	def __init__(self):
		self.name = 'katana'
		self.command_list = 'acdeqswxz'
		self.max_charge = 2
		self.current_charge = 2
		self.default_usage = 2
		self.durability = 50
		default_usage = self.default_usage
	
		self.command_items = []
		
		command = 'q'
		temp_array =	 [[0,0,0,0,0],
				  [0,1,1,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))




		command = 'e'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,1,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))




		command = 'w'
		temp_array =	 [[0,0,1,0,0],
				  [0,0,0,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))



		command = 'd'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,1],
				  [0,0,0,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = 'c'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,1,1,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


		command = 'z'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,1,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))

		command = 'a'
		temp_array =	 [[0,0,0,0,0],
				  [0,1,0,0,0],
				  [1,0,0,0,0],
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
				  [0,1,0,0,0],
				  [0,0,1,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))

		command = 's'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,0,0],
				  [0,0,1,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))


	
	def do_attack(self, command):
		for (com, data, usage) in self.command_items:
			if com == command and usage <= self.current_charge and self.durability > 0:
				self.current_charge = self.current_charge - usage
				return data


	def recharge(self, recharge_val = 1):
		self.current_charge = self.current_charge + recharge_val
		if self.current_charge > self.max_charge:
			self.current_charge = self.max_charge


#############


class Weapon_Ring_Of_Power:
	# Ooooh, a big scary one! Yeah!
	def __init__(self):
		self.name = 'ring of power'
		self.command_list =  'acdeqswxz'
		self.max_charge = 9
		self.current_charge = 9
		self.default_usage = 3
		self.durability = 1000
		default_usage = self.default_usage
	
		self.command_items = []
		
		command = 'w'
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


		command = 's'
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


		command = 'x'
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


		command = 'a'
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



		command = 'd'
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



		command = 'q'
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

		command = 'e'
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


		command = 'c'
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


		command = 'z'
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


	
	def do_attack(self, command):
		for (com, data, usage) in self.command_items:
			if com == command and usage <= self.current_charge and self.durability > 0:
				self.current_charge = self.current_charge - usage
				return data


	def recharge(self, recharge_val = 1):
		self.current_charge = self.current_charge + recharge_val
		if self.current_charge > self.max_charge:
			self.current_charge = self.max_charge





#############


class Weapon_Strawhands:
	# a bad weapon. Do not use it.
	def __init__(self):
		self.name = 'straw hand'
		self.command_list = 'w'
		self.max_charge = 2
		self.current_charge = 2
		self.default_usage = 2
		self.durability = 1000
		default_usage = self.default_usage
	
		self.command_items = []
		
		command = 'w'
		temp_array =	 [[0,0,0,0,0],
				  [0,0,0,0,0],
				  [0,1,0,1,0],
				  [0,0,0,0,0],
				  [0,0,0,0,0]]

		ava_x_pos = 2
		ava_y_pos = 2
		abstract_attack_data = create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos)
		self.command_items.append((command, abstract_attack_data, default_usage))
	
	def do_attack(self, command):
		for (com, data, usage) in self.command_items:
			if com == command and usage <= self.current_charge and self.durability > 0:
				self.current_charge = self.current_charge - usage
				return data


	def recharge(self, recharge_val = 1):
		self.current_charge = self.current_charge + recharge_val
		if self.current_charge > self.max_charge:
			self.current_charge = self.max_charge



def create_abstract_attack_data(temp_array, ava_x_pos, ava_y_pos):
	return_array = []
	for j in xrange(len(temp_array)):
		for i in xrange(len(temp_array[j])):
			#print ('(' +str(j) + ',' + str(i) + '), (' + str(j-y_start_offset) + ',' + str(i-x_start_offset) + ')')
			if (temp_array[j][i] > 0):
				return_array.append((i-ava_x_pos,j-ava_y_pos,temp_array[j][i]))
	return return_array



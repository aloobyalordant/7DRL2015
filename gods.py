import libtcodpy as libtcod

class God:

	def __init__(self, god_type):
		self.god_type = god_type
		if self.god_type is not None:
			self.god_type.owner = self
		self.favours_player = False
		
		# i am certainly not doing components properly...
		
		# default values first.
		self.name = 'Unnamed'
		self.color = libtcod.white
		self.first_prayer_message = '\"Commandments: 1. Worship me. 2. Do no harm. 3. Kill the non-believers.\"'


		# now update values based on those set by the god type.
		if god_type.name is not None:
			self.name = god_type.name

		if god_type.color is not None:
			self.color = god_type.color

		if god_type.first_prayer_message is not None:
			self.first_prayer_message = god_type.first_prayer_message


class God_Healer:
	
	def __init__(self):
		self.name = "Sydney"
		self.type = 'healer'
		self.color = libtcod.orange
		self.first_prayer_message = '\"Be at peace, my child. I watch over all who come to me with faith in their hearts.\"'


class God_Destroyer:

	def __init__(self):
		self.name = "Lindsey"
		self.type = 'destroyer'
		self.color = libtcod.orange
		self.first_prayer_message = '\"Destroy my enemies, wretched minion!\"'


class God_Deliverer:

	def __init__(self):
		self.name = "Taylor"
		self.type = 'deliverer'
		self.color = libtcod.orange
		self.first_prayer_message = '\"Hey there! Get through this floor quickly for a reward!\"'



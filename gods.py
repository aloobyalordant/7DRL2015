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


class God:

	def __init__(self, god_type):
		self.god_type = god_type
		if self.god_type is not None:
			self.god_type.owner = self
		self.favours_player = False
		
		# i am certainly not doing components properly...
		
		# default values first.
		self.name = 'Unnamed'
		self.color = default_text_color
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
		self.color = color_warning
		self.first_prayer_message = '\"Be at peace, my child. I watch over all who come to me with faith in their hearts.\"'


class God_Destroyer:

	def __init__(self):
		self.name = "Lindsey"
		self.type = 'destroyer'
		self.color = color_warning
		self.first_prayer_message = '\"Destroy my enemies, wretched minion!\"'


class God_Deliverer:

	def __init__(self):
		self.name = "Taylor"
		self.type = 'deliverer'
		self.color = color_warning
		self.first_prayer_message = '\"Hey there! Get through this floor quickly for a reward!\"'



import tdl as libtcod



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


# A class that is hopefully like ControlHandler, but simpler and for colors.
# Yes, colors. I have completely lost the fight against american english on this one. Blame graph theory.
class ColorHandler:


	def __init__(self,colorScheme = "default", customDictionary = None):
		print("Setting colors with type " + colorScheme)
		self.colorScheme = colorScheme	# options: "QWERTY-numpad"  "QWERTY-nopad" "AZERTY-numpad" "AZERTY-nopad" "custom"


		self.levelColors = self.getLevelColors(self.colorScheme) # For stuff in the level (Player, enemies, walls, floors, weapons etc)
		
		self.menuColors = self.getMenuColors(self.colorScheme) #For stuff in the menu / gui

		print("Done setting colors.")






	def getLevelColors(self, colorScheme):	
		newDictionary = {}
		



		newDictionary = dict([	
		# Environment colors (walls +floors, altars, visible or not)
			('color_dark_wall',(100,100,100)),	#	(100,100,100)		#(0, 0, 100)
			('color_light_wall', (130, 110, 50)),	# ((vsw,vsw,vsw), vsw)),	#	(130, 110, 50)
			('color_dark_ground', (150,150,150)),	#	(150,150,150)		#(50, 50, 150)
			('color_light_ground', (200, 180, 100)),	#	(200, 180, 50)
			('color_light_ground_alt', (250, 100, 100)),	#	(200, 180, 50)
			('color_fog_of_war', (0,0,0)),	#	(0,0,0)			#libtcod.black
			('default_altar_color', (130, 110, 50)),
			('default_door_color', (130, 110, 50)),
			('default_message_color', (130, 110, 50)),
			('default_decoration_color',(130, 110, 50)),	#	(250,230,50)		#(165,145,50)
			('water_background_color',(100,100,250)),	#	(100,100,250)
			('water_foreground_color', (25,25,250)),	#	(25,25,250)
			('blood_background_color',(200,0,0)),	#	(200,0,0)
			('blood_foreground_color',(150,0,0)),	#	(150,0,0)
			# collectiable e.g. weapons and plants and keys
			('default_flower_color',(50,150,0)),	#(50,150,0)
			('default_weapon_color',(50,50,50)),	#(50,50,50) #libtcod.grey
			# enemies, including player
			('PLAYER_COLOR',(255, 255, 255)),	#(255, 255, 255)
			#color_sneaky_enemy
			#color_shortrange_enemy
			#color_midrange_enemy
			#color_longrange_enemy
			#color_big_boss
			('color_swordsman',(0,0,191)),	#	(0,0,191)		#libtcod.dark_blue
			('color_boman',(0,128,0)),	#	(0,128,0)		#libtcod.darker_green
			('color_rook',(0,0,128)),	#	(0,0,128)		#libtcod.darker_blue
			('color_axe_maniac',(128,0,0)),	#	 (128,0,0)		#libtcod.darker_red
			('color_tridentor',(0,0, 255)),	#	(0,0, 255)		#libtcod.blue
			('color_rogue',(0,64, 64)),	
			('color_ninja',(0,0,0)),	#	(0,0,0)		#libtcod.black
			('color_wizard',(95, 0, 128)),	#	(95, 0, 128)			#libtcod.darker_purple
			('color_alarmer_idle',(0,0,191)),
			('color_alarmer_suspicious',(255, 255, 255)),
			('color_alarmer_alarmed',(128,0,0))
		])

		if colorScheme == 'lobbyTest':
			newDictionary['color_dark_wall'] = (100,100,100)	#	(100,100,100)		#(0, 0, 100)
			newDictionary['color_light_wall'] = (102, 28, 25)	# ((vsw,vsw,vsw), vsw)),	#	(130, 110, 50)
			newDictionary['color_dark_ground'] = (150,150,150)	#	(150,150,150)		#(50, 50, 150)
			newDictionary['color_light_ground'] = (243, 195, 134)	#	(200, 180, 50)
			newDictionary['color_light_ground_alt'] = (219, 126, 61)	#	(200, 180, 50)
			newDictionary['default_altar_color'] = (230, 00, 230)
			newDictionary['default_door_color'] = (102, 28, 25)
			newDictionary['default_message_color'] = (230, 00, 230)
			newDictionary['default_decoration_color'] =(200, 106, 41)
			newDictionary['color_alarmer_alarmed'] =(250,0,0)	#	(2




		# 'grand budapest hotel lobby palette apparently'
		#  219, 126, 61    orangey
		#  102, 28, 25		dark red?
		# 253, 112, 114   pinky / light red?
		#  243, 195, 134  some very neutral orangey beige
	
		# Commenting out a bunch of stuff:
		# For now,not going to do the 'adjust for Value' stuff, because it's clear that Saturation is also important 
		# and I should probably just be doing it by hand + checking with filters now I know a bit more about this stuff.
		# Also, gona make it so a bunch of the fields we expect to stay  the same are pre-loaded, so the 
		# sections for different color schemes don't get unnecessarily long.

#		if colorScheme == 'default':
#			# start with 4 values - the unadjusted rgb, then the desired capital V Value.
#			# later we'll come back and turn this into adjust RGB values
#			newDictionary = dict([	
#			# Environment colors (walls +floors, altars, visible or not)
#				('color_dark_wall',((vuw,vuw,vuw),vuw)),	#	(100,100,100)		#(0, 0, 100)
#				('color_light_wall', ((vsw,vsw,vsw), vsw)),	# ((vsw,vsw,vsw), vsw)),	#	(130, 110, 50)
#				('color_dark_ground', ((vuf,vuf,vuf),vuf)),	#	(150,150,150)		#(50, 50, 150)
#				('color_light_ground', ((vsf,vsf,vsf),vsf)),	#	(200, 180, 50)
#				('color_fog_of_war', ((vfw,vfw,vfw),vfw)),	#	(0,0,0)			#libtcod.black
#				('default_altar_color', ((vsw,vsw,vsw), vsw)),
#				('default_message_color', ((vsw,vsw,vsw), vsw)),
#				('default_decoration_color',((vuw,vuw,vuw), vuw)),	#	(250,230,50)		#(165,145,50)
#				('water_background_color',((vuf,vuf,vuf), vuf)),	#	(100,100,250)
#				('water_foreground_color', ((vsw,vsw,vsw),vsw)),	#	(25,25,250)
#				('blood_background_color',((vuf,vuf,vuf),vuf)),	#	(200,0,0)
#				('blood_foreground_color',((vsw,vsw,vsw),vsw)),	#	(150,0,0)
#				# collectiable e.g. weapons and plants and keys
#				('default_flower_color',((vsw,vsw,vsw),vsw)),	#(50,150,0)
#				('default_weapon_color',((vsw,vsw,vsw),vsw)),	#(50,50,50) #libtcod.grey
#				# enemies, including player
#				('PLAYER_COLOR',((v_p,v_p,v_p),v_p)),	#(255, 255, 255)
#				#color_sneaky_enemy
#				#color_shortrange_enemy
#				#color_midrange_enemy
#				#color_longrange_enemy
#				#color_big_boss
#				('color_swordsman',((v_e,v_e,v_e),v_e)),	#	(0,0,191)		#libtcod.dark_blue
#				('color_boman',((v_e,v_e,v_e),v_e)),	#	(0,128,0)		#libtcod.darker_green
#				('color_rook',((v_e,v_e,v_e),v_e)),	#	(0,0,128)		#libtcod.darker_blue
#				('color_axe_maniac',((v_e,v_e,v_e),v_e)),	#	 (128,0,0)		#libtcod.darker_red
#				('color_tridentor',((v_e,v_e,v_e),v_e)),	#	(0,0, 255)		#libtcod.blue
#				('color_ninja',((v_e,v_e,v_e),v_e)),	#	(0,0,0)		#libtcod.black
#				('color_wizard',((v_e,v_e,v_e),v_e)),	#	(95, 0, 128)			#libtcod.darker_purple
#				('color_alarmer_idle',((vsw,vsw,vsw),vsw)),
#				('color_alarmer_suspicious',((v_p,v_p,v_p),v_p)),
#				('color_alarmer_alarmed',((v_e,v_e,v_e),v_e))
#			])
#
#		elif colorScheme == 'adjustedOriginal':
#			# start with 4 values - the unadjusted rgb, then the desired capital V Value.
#			# later we'll come back and turn this into adjust RGB values
#			newDictionary = dict([	
#			# Environment colors (walls +floors, altars, visible or not)
#				('color_dark_wall',((100,100,100),vuw)),	#	(100,100,100)		#(0, 0, 100)
#				('color_light_wall', ((130, 110, 50), vsw)),	# ((vsw,vsw,vsw), vsw)),	#	(130, 110, 50)
#				('color_dark_ground', ((150,150,150),vuf)),	#	(150,150,150)		#(50, 50, 150)
#				('color_light_ground', ((200, 180, 100),vsf)),	#	(200, 180, 50)
#				('color_fog_of_war', ((0,0,0),vfw)),	#	(0,0,0)			#libtcod.black
#				('default_altar_color', ((130, 110, 50), vsw)),
#				('default_message_color', ((130, 110, 50), vsw)),
#				('default_decoration_color',((130, 110, 50), vuw+10)),	#	(250,230,50)		#(165,145,50)
#				('water_background_color',((100,100,250), vuf+3)),	#	(100,100,250)
#				('water_foreground_color', ((25,25,250),vsw+3)),	#	(25,25,250)
#				('blood_background_color',((200,0,0),vuf-5)),	#	(200,0,0)
#				('blood_foreground_color',((150,0,0),vsw-5)),	#	(150,0,0)
#				# collectiable e.g. weapons and plants and keys
#				('default_flower_color',((50,150,0),vsw)),	#(50,150,0)
#				('default_weapon_color',((50,50,50),vsw)),	#(50,50,50) #libtcod.grey
#				# enemies, including player
#				('PLAYER_COLOR',((255, 255, 255),v_p)),	#(255, 255, 255)
#				#color_sneaky_enemy
#				#color_shortrange_enemy
#				#color_midrange_enemy
#				#color_longrange_enemy
#				#color_big_boss
#				('color_swordsman',((0,0,191),v_e)),	#	(0,0,191)		#libtcod.dark_blue
##				('color_boman',((0,128,0),v_e)),	#	(0,128,0)		#libtcod.darker_green
#				('color_rook',((0,0,128),v_e)),	#	(0,0,128)		#libtcod.darker_blue
#				('color_axe_maniac',((128,0,0),v_e)),	#	 (128,0,0)		#libtcod.darker_red
#				('color_tridentor',((0,0, 255),v_e)),	#	(0,0, 255)		#libtcod.blue
#				('color_ninja',((0,0,0),v_e)),	#	(0,0,0)		#libtcod.black
#				('color_wizard',((95, 0, 128),v_e)),	#	(95, 0, 128)			#libtcod.darker_purple
#				('color_alarmer_idle',((0,0,191),vsw)),
#				('color_alarmer_suspicious',((255, 255, 255),v_p)),
#				('color_alarmer_alarmed',((128,0,0),v_e))
#			])
#
#
#		# Update colors to be value-adjusted
#		for name in newDictionary:
#			colorInfo = newDictionary[name]
#			(oldRGB,val) = colorInfo
#			newRGB = self.adjustForValue(oldRGB,val)
#			newDictionary[name] = newRGB
#
		return newDictionary



	def getMenuColors(self, colorScheme):
		
		#if colorScheme = 'default':
			# start with 4 values - the unadjusted rgb, then the desired capital V Value.
			# later we'll come back and turn this into adjust RGB values

		print("color scheme is" + colorScheme)

		# default (black and white?) values
		newDictionary = dict([	
			# text colors
			('default_background_color',(vfw,vfw,vfw)),	#(0,0,0)
			('default_text_color',(vsf,vsf,vsf)),	#(255,255,255)
			('color_energy',(v_p,v_p,v_p)),	#(0,255,255)
			('color_faded_energy',(vsf,vsf,vsf)),	#	(0,0,255)
			('color_warning',(v_p,v_p,v_p)),	#	(255,127,0)
			('color_big_alert',(v_p,v_p,v_p)),	#(255,0,0)
			('Message_In_World',(v_p,0,v_p)),		# e.g. messages on floor, deities or elevators talking to you
			('Menu_Choice',(v_p,v_p,v_p)),			# when the player has to input an option from mutliple choices
			('Not_Allowed',(v_p,v_p,v_p)),			# when a player action is invalid or prevented
			('Dangerous_Combat',(v_p,v_p,v_p)),		# when bad things happen in combat, like dying or getting hit
			('Interesting_Combat',(v_p,v_p,v_p)),		# notable combat stuff like enemies dying
			('Boring_Combat',(v_p,v_p,v_p)),		# Run of the mill combat stuff. you hit an enemy. yawn
			('Interesting_In_World',(v_p,v_p,v_p)),		# Events of note happening in the world. Like alarms going off
			('Boring_In_World',(v_p,v_p,v_p)),		# everyday occurences like doors opening
			('Stat_Info',(v_p,v_p,v_p)),			# info about not-in-the-world stuff like gaining energy
			('Personal_Action',(v_p,v_p,v_p))		# Things the player does that aren't combat "you pick up the sword" etc
		])


		# trying colors taken from Solarized  http://ethanschoonover.com/solarized
		if colorScheme == 'lobbyTest':
			print("yoooooo")
			newDictionary['default_background_color']=(0,0,15)
			newDictionary['color_energy']=(38,139,210)	
			newDictionary['Message_In_World']=(38,139,210)		# e.g. messages on floor, deities or elevators talking to you
			newDictionary['Menu_Choice']=(211,54,130)		# when the player has to input an option from mutliple choices
			newDictionary['Not_Allowed']=(108,113,196)		# when a player action is invalid or prevented
			newDictionary['Dangerous_Combat']=(220,50,47)		# when bad things happen in combat, like dying or getting hit
			newDictionary['Interesting_Combat']=(203,75,22)		# notable combat stuff like enemies dying
			newDictionary['Boring_Combat']=(253,246,227)		# Run of the mill combat stuff. you hit an enemy. yawn
			newDictionary['Interesting_In_World']=(203,75,22)	# Events of note happening in the world. Like alarms going off
			newDictionary['Boring_In_World']=(238,232,213)		# everyday occurences like doors opening
			newDictionary['Stat_Info']=(42,161,152)		# info about not-in-the-world stuff like gaining energy
			newDictionary['Personal_Action']=(191, 147, 10)		# (181,137,0)Things the player does that aren't combat "you pick up the sword" etc

			
		# Commenting out a bunch of stuff:
		# For now,not going to do the 'adjust for Value' stuff, because it's clear that Saturation is also important 
		# and I should probably just be doing it by hand + checking with filters now I know a bit more about this stuff.
		# Also, gona make it so a bunch of the fields we expect to stay  the same are pre-loaded, so the 
		# sections for different color schemes don't get unnecessarily long.

	#	newDictionary = dict([	
	#		# text colors
	#		('default_background_color',((vfw,vfw,vfw),vfw)),	#(0,0,0)
	#		('default_text_color',((vsf,vsf,vsf),vsf)),	#(255,255,255)
	#		('color_energy',((v_p,v_p,v_p),v_p)),	#(0,255,255)
	#		('color_faded_energy',((vsf,vsf,vsf),vsf)),	#	(0,0,255)
	#		('color_warning',((v_p,v_p,v_p),vsf)),	#	(255,127,0)
	#		('color_big_alert',((v_p,v_p,v_p), v_p))	#(255,0,0)
	#	])

	#	# Update colors to be value-adjusted
	#	for name in newDictionary:
	#		colorInfo = newDictionary[name]
	#		(oldRGB,val) = colorInfo
	#		newRGB = self.adjustForValue(oldRGB,val)
	#		newDictionary[name] = newRGB

		return newDictionary



	# A function that takes a color in RGB and a desired value, 
	# and produces a color such that the RGB values avaerage out to the specified value.
	# theoretically, that means that when converted to grayscale, 
	# it should like the shade of grey with the specified value.
	# I should check that though.
	# Even more theoretically, that shade of grey is hopefully what it looks like to people who see in black and white?
	# I  check that though.
	#
	# NOTE TO SELF: I've got some approximate values that I want to keep types of object in (e.g. all enemies have approx the same value),
	# but I should probably make sure to vary that value a bit. Otherwise in black+white tit's hard to distinguish between things.
	# (This especially holds for floors + walls, that migjthave no distinguishing features except color)
	# varying to within +/- 5 seems probably fine, maybe even more?
	def adjustForValue(self, rgbColor, value):
		(r,g,b) = rgbColor
		total = r+g+b
		if total > 0:
			adjustment = (value*3)/total
			r = int(r*adjustment)
			g = int(g*adjustment)
			b = int(b*adjustment)
		else:	# if initial color was just black, update to the desired shade of gray.
			r = value
			g = value
			b = value

		# sanity check: if r,g,b end up outside the accepted range for RGB colors (i.e. 0 to 255), nring them back in line.
		if r < 0:
			r = 0
		elif r > 255:
			r = 255
		if g < 0:
			g = 0
		elif g > 255:
			g = 255
		if b < 0:
			b = 0
		elif b > 255:
			b = 255

		# return adjusted color
		return (r,g,b)

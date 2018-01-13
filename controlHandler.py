import tdl as libtcod

class ControlHandler:

	def __init__(self, controlType = "QWERTY-numpad", customDictionary = None):
		self.controlType = controlType	# options: "QWERTY-numpad"  "QWERTY-nopad" "AZERTY-numpad" "AZERTY-nopad" "custom"
		if self.controlType == "custom":
			self.controlDictionary = customDictionary	# maps keynames (and/or characters?) to command names
		else:
			self.controlDictionary = self.getDefaultDictionary(self.controlType)

		self.menuDictionary = self.getMenuDictionary()		# for 'menu' commands (e.g. y/n, q for quit, r for restart)
		
		self.controlLookup = self.getControlLookup()
		self.singleCharacterControlLookup = self.getSingleCharacterLookup()


	
	def getDefaultDictionary(self, controlType = "QWERTY-numpad"):

		newDictionary = {}

		if controlType == "AZERTY-numpad":
			# customisable controls	
			newDictionary = dict([('a', "ATTCKUPLEFT"),('z', "ATTCKUP"),('e', "ATTCKUPRIGHT"),('d', "ATTCKRIGHT"),('c',"ATTCKDOWNRIGHT"),('x',"ATTCKDOWN"),('w',	"ATTCKDOWNLEFT"), ('q', "ATTCKLEFT"), ('s',"ATTCKDOWNALT"),
			('KP7', "MOVEUPLEFT"), ('HOME', "MOVEUPLEFT"), ('KP8', "MOVEUP"), ('UP',"MOVEUP"),('KP9', "MOVEUPRIGHT"), ('PAGEUP', "MOVEUPRIGHT"), ('KP6', "MOVERIGHT"), ('RIGHT',"MOVERIGHT"), ('KP3', "MOVEDOWNRIGHT"), ('PAGEDOWN', "MOVEDOWNRIGHT"), ('KP2', "MOVEDOWN"), ('DOWN', "MOVEDOWN"), ('KP1', "MOVEDOWNLEFT"), ('KP4', "MOVELEFT"), ('LEFT', "MOVELEFT"),
			('KP5', "STANDSTILL"), ('.', "STANDSTILL"),
			('p', "PICKUP"), ('o', "MEDIDATE"), ('SPACE', "JUMP")])

		elif controlType == "QWERTY-numpad":
			# customisable controls	
			newDictionary = dict([('q', "ATTCKUPLEFT"),('w', "ATTCKUP"),('e', "ATTCKUPRIGHT"),('d', "ATTCKRIGHT"),('c',"ATTCKDOWNRIGHT"),('x',"ATTCKDOWN"),('z',	"ATTCKDOWNLEFT"), ('a', "ATTCKLEFT"), ('s',"ATTCKDOWNALT"),
			('KP7', "MOVEUPLEFT"), ('HOME', "MOVEUPLEFT"), ('KP8', "MOVEUP"), ('UP',"MOVEUP"),('KP9', "MOVEUPRIGHT"), ('PAGEUP', "MOVEUPRIGHT"), ('KP6', "MOVERIGHT"), ('RIGHT',"MOVERIGHT"), ('KP3', "MOVEDOWNRIGHT"), ('PAGEDOWN', "MOVEDOWNRIGHT"), ('KP2', "MOVEDOWN"), ('DOWN', "MOVEDOWN"), ('KP1', "MOVEDOWNLEFT"), ('KP4', "MOVELEFT"), ('LEFT', "MOVELEFT"),
			('KP5', "STANDSTILL"), ('.', "STANDSTILL"),
			('p', "PICKUP"), ('o', "MEDIDATE"), ('SPACE', "JUMP")])
		

		#TODO nopad versions
		
		# controls that are nae fixed.
		newDictionary['ESCAPE'] = "PAUSE"
		newDictionary['ENTER'] = "FULLSCREEN"


		return newDictionary


	def getMenuDictionary(self):
		newDictionary = dict([('y', "MENUYES"), ('n', "MENUNO"), ('q', "MENUQUIT"), ('r', "MENURESTART")])
		return newDictionary



	def getGameplayCommand(self, veekay, key_char):
		if veekay in self.controlDictionary:
			return self.controlDictionary[veekay]
		# check upper case and lower case versions of key_char
		elif key_char.upper() in self.controlDictionary:
			return self.controlDictionary[key_char.upper()]
		elif key_char.lower() in self.controlDictionary:
			return self.controlDictionary[key_char.lower()]
		else:
			return "NO_COMMAND" 


	# reverse dictionary for controlDictionary
	def getControlLookup(self):
		newDictionary = {}
		# obvs only going to have one result, even if multiple keys do the same command. That's fine.
		for k,v in self.controlDictionary.items():
			newDictionary[v] = k
		return newDictionary

	# reverse dictionary for controlDictionary, but finds a single character key if one is available, 
	# and if not returns the first character 
	# of an available command
	def getSingleCharacterLookup(self):
		newDictionary = {}
		# obvs only going to have one result, even if multiple keys do the same command. That's fine.
		for k,v in self.controlDictionary.items():
			#add sensible single character option if possible, otherwise add first character
			if len(k) == 1:
				print('BANHD')
				newDictionary[v] = k
			elif len(k) == 3 and k[0:2] == 'KP':
				print('wooop')
				newDictionary[v] =  k[2]
			elif v not in newDictionary:
			#else:
				newDictionary[v] =  k[0]

		# a bad hack that is dishonest to the player: if '.' is an option for "STANDSTILL" then use that because it looks better
		if self.controlDictionary['.'] == "STANDSTILL":
			newDictionary["STANDSTILL"] = '.'


		return newDictionary


# if key in array:
  # do somethin

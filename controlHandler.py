import tdl as libtcod

class ControlHandler:

	def __init__(self, controlType = "QWERTY-numpad", customDictionary = None):
		print("Setting controls with type " + controlType)
		self.controlType = str(controlType)	# options: "QWERTY-numpad"  "QWERTY-nopad" "AZERTY-numpad" "AZERTY-nopad" "custom"
		if self.controlType == "custom":
			self.controlDictionary = customDictionary	# maps keynames (and/or characters?) to command names
		else:
			self.controlDictionary = self.getDefaultDictionary(self.controlType)

		self.menuDictionary = self.getMenuDictionary()		# for 'menu' commands (e.g. y/n, q for quit, r for restart)
		
		self.controlLookup = self.getControlLookup()
		self.singleCharacterControlLookup = self.getSingleCharacterLookup()

		self.intFromLetter = self.getIntFromLetterLookup()
		self.letterFromInt = self.getLetterFromIntLookup()

		self.controlOptionsArray = self.getControlOptionsArray()
		print("Done setting controls.")


	
	def getDefaultDictionary(self, controlType = "QWERTY-numpad"):

		newDictionary = {}

		if controlType == "AZERTY-numpad":
			print("Setting AZERTY-numpad...")
			# customisable controls	
			newDictionary = dict([('a', "ATTCKUPLEFT"),('z', "ATTCKUP"),('e', "ATTCKUPRIGHT"),('d', "ATTCKRIGHT"),('c',"ATTCKDOWNRIGHT"),('x',"ATTCKDOWN"),('w',	"ATTCKDOWNLEFT"), ('q', "ATTCKLEFT"), ('s',"ATTCKDOWNALT"),
			('KP7', "MOVEUPLEFT"), ('HOME', "MOVEUPLEFT"), ('KP8', "MOVEUP"), ('UP',"MOVEUP"),('KP9', "MOVEUPRIGHT"), ('PAGEUP', "MOVEUPRIGHT"), ('KP6', "MOVERIGHT"), ('RIGHT',"MOVERIGHT"), ('KP3', "MOVEDOWNRIGHT"), ('PAGEDOWN', "MOVEDOWNRIGHT"), ('KP2', "MOVEDOWN"), ('DOWN', "MOVEDOWN"), ('KP1', "MOVEDOWNLEFT"), ('KP4', "MOVELEFT"), ('LEFT', "MOVELEFT"),
			('KP5', "STANDSTILL"), ('.', "STANDSTILL"),
			('p', "PICKUP"), ('o', "MEDITATE"), ('SPACE', "JUMP")])

		elif controlType == "QWERTY-numpad":
			print("Setting QWERTY-numpad...")
			# customisable controls	
			newDictionary = dict([('q', "ATTCKUPLEFT"),('w', "ATTCKUP"),('e', "ATTCKUPRIGHT"),('d', "ATTCKRIGHT"),('c',"ATTCKDOWNRIGHT"),('x',"ATTCKDOWN"),('z',	"ATTCKDOWNLEFT"), ('a', "ATTCKLEFT"), ('s',"ATTCKDOWNALT"),
			('KP7', "MOVEUPLEFT"), ('HOME', "MOVEUPLEFT"), ('KP8', "MOVEUP"), ('UP',"MOVEUP"),('KP9', "MOVEUPRIGHT"), ('PAGEUP', "MOVEUPRIGHT"), ('KP6', "MOVERIGHT"), ('RIGHT',"MOVERIGHT"), ('KP3', "MOVEDOWNRIGHT"), ('PAGEDOWN', "MOVEDOWNRIGHT"), ('KP2', "MOVEDOWN"), ('DOWN', "MOVEDOWN"), ('KP1', "MOVEDOWNLEFT"), ('KP4', "MOVELEFT"), ('LEFT', "MOVELEFT"),
			('KP5', "STANDSTILL"), ('.', "STANDSTILL"),
			('p', "PICKUP"), ('o', "MEDITATE"), ('SPACE', "JUMP")])


		elif controlType == "QWERTY-nopad":
			print("Setting QWERTY-nopad...")
			# customisable controls	
			newDictionary = dict([('q', "ATTCKUPLEFT"),('w', "ATTCKUP"),('e', "ATTCKUPRIGHT"),('d', "ATTCKRIGHT"),('c',"ATTCKDOWNRIGHT"),('x',"ATTCKDOWN"),('z',	"ATTCKDOWNLEFT"), ('a', "ATTCKLEFT"), ('s',"ATTCKDOWNALT"),
			('t', "MOVEUPLEFT"), ('y', "MOVEUP"), ('UP',"MOVEUP"),('u', "MOVEUPRIGHT"), ('j', "MOVERIGHT"), ('RIGHT',"MOVERIGHT"), ('m', "MOVEDOWNRIGHT"), ('n', "MOVEDOWN"), ('DOWN', "MOVEDOWN"), ('b', "MOVEDOWNLEFT"), ('g', "MOVELEFT"), ('LEFT', "MOVELEFT"),
			('h', "STANDSTILL"), ('.', "STANDSTILL"),
			('p', "PICKUP"), ('o', "MEDITATE"), ('SPACE', "JUMP")])
		
		elif controlType == "AZERTY-nopad":
			print("Setting AZERTY-nopad...")
			# customisable controls	
			newDictionary = dict([('a', "ATTCKUPLEFT"),('z', "ATTCKUP"),('e', "ATTCKUPRIGHT"),('d', "ATTCKRIGHT"),('c',"ATTCKDOWNRIGHT"),('x',"ATTCKDOWN"),('w',	"ATTCKDOWNLEFT"), ('q', "ATTCKLEFT"), ('s',"ATTCKDOWNALT"),
			('t', "MOVEUPLEFT"), ('y', "MOVEUP"), ('UP',"MOVEUP"),('u', "MOVEUPRIGHT"), ('j', "MOVERIGHT"), ('RIGHT',"MOVERIGHT"), (',', "MOVEDOWNRIGHT"), ('n', "MOVEDOWN"), ('DOWN', "MOVEDOWN"), ('b', "MOVEDOWNLEFT"), ('g', "MOVELEFT"), ('LEFT', "MOVELEFT"),
			('h', "STANDSTILL"), ('.', "STANDSTILL"),
			('p', "PICKUP"), ('o', "MEDITATE"), ('SPACE', "JUMP")])

		else:
			print("Control scheme not recognised, setting QWERTY-numpad by default...")
			# customisable controls	
			newDictionary = dict([('q', "ATTCKUPLEFT"),('w', "ATTCKUP"),('e', "ATTCKUPRIGHT"),('d', "ATTCKRIGHT"),('c',"ATTCKDOWNRIGHT"),('x',"ATTCKDOWN"),('z',	"ATTCKDOWNLEFT"), ('a', "ATTCKLEFT"), ('s',"ATTCKDOWNALT"),
			('KP7', "MOVEUPLEFT"), ('HOME', "MOVEUPLEFT"), ('KP8', "MOVEUP"), ('UP',"MOVEUP"),('KP9', "MOVEUPRIGHT"), ('PAGEUP', "MOVEUPRIGHT"), ('KP6', "MOVERIGHT"), ('RIGHT',"MOVERIGHT"), ('KP3', "MOVEDOWNRIGHT"), ('PAGEDOWN', "MOVEDOWNRIGHT"), ('KP2', "MOVEDOWN"), ('DOWN', "MOVEDOWN"), ('KP1', "MOVEDOWNLEFT"), ('KP4', "MOVELEFT"), ('LEFT', "MOVELEFT"),
			('KP5', "STANDSTILL"), ('.', "STANDSTILL"),
			('p', "PICKUP"), ('o', "MEDITATE"), ('SPACE', "JUMP")])
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

			# if k begins with 'KP', replace it with the bit after
			if len(k) == 3 and k[0:2] == 'KP':
				newDictionary[v] =  k[2]
			# actually try and make it so shorter keys get used where possible? ugh
			elif v in newDictionary:
				if len(k) < len(newDictionary[v]):
					newDictionary[v] = k
			else:
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
				newDictionary[v] = k
			elif len(k) == 3 and k[0:2] == 'KP':
				newDictionary[v] =  k[2]
			elif v not in newDictionary:
			#else:
				newDictionary[v] =  k[0]

		# a bad hack that is dishonest to the player: if '.' is an option for "STANDSTILL" then use that because it looks better
		if '.' in self.controlDictionary:
			if self.controlDictionary['.'] == "STANDSTILL":
				newDictionary["STANDSTILL"] = '.'

		return newDictionary


	def getIntFromLetterLookup(self):
		newDictionary = dict ([('a',1),('b',2),('c',3),('d',4),('e',5),('f',6),('g',7),('h',8),('i',9),('j',10),('k',11),('l',12),('m',13),('n',14),('o',15),('p',16),('q',17),('r',18),('s',19),('t',20),('u',21),('v',22),('w',23),('x',24),('y',25),('z',26),
		('A',1),('B',2),('C',3),('D',4),('E',5),('F',6),('G',7),('H',8),('I',9),('J',10),('K',11),('L',12),('M',13),('N',14),('O',15),('P',16),('Q',17),('R',18),('S',19),('T',20),('U',21),('V',22),('W',23),('X',24),('Y',25),('Z',26)])
		return newDictionary

	def getLetterFromIntLookup(self):
		newDictionary = dict ([(1,'a'),(2,'b'),(3,'c'),(4,'d'),(5,'e'),(6,'f'),(7,'g'),(8,'h'),(9,'i'),(10,'j'),(11,'k'),(12,'l'),(13,'m'),(14,'n'),(15,'o'),(16,'p'),(17,'q'),(18,'r'),(19,'s'),(20,'t'),(21,'u'),(22,'v'),(23,'w'),(24,'x'),(25,'y'),(26,'z')])
		return newDictionary


	def getControlOptionsArray(self):		
		control_option_list = []
		control_option_list.append(("QWERTY-numpad", "QWERTY with numpad"))
		control_option_list.append(("QWERTY-nopad", "QWERTY, no numpad"))
		control_option_list.append(("AZERTY-numpad", "AZERTY with numpad"))
		control_option_list.append(("AZERTY-nopad", "AZERTY, no numpad"))
		return control_option_list
# if key in array:
  # do somethin

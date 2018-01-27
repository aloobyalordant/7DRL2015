import tdl as libtcod

# For default values, see the functions headed "# DEFAULT VALUES GO HERE"

# This class does all the reading save data and loading save data and all that business.
# Stored in a separate file so I hopefully don't have to look at it too often.
class SaveDataHandler:

	def __init__(self):
		# file path for save files depends on where
		import sys, os
		pathname = os.path.dirname(sys.argv[0])       

		self.testFileName = os.path.join(pathname, "testfile.txt")
		print("Getting test data from " + self.testFileName)

		self.controlsFileName = os.path.join(pathname, "controls.dat")
		print("Getting control data from " + self.controlsFileName)

		self.colorsFileName = os.path.join(pathname, "colors.dat")
		print("Getting color data from " + self.colorsFileName)


	def loadData(self):
		self.testFileData =  self.loadTestFileData()
		self.controlData =  self.loadControlData()
		


	# Stuff to do with Test File data

	# DEFAULT VALUES GO HERE
	def getDefaultTestFileData(self):
		returnDictionary = {}
		returnDictionary["FLD_TEST_1"] = "Hello this is a test string"
		returnDictionary["FLD_TEST_2"] = "Hi! This is another test string"
		returnDictionary["FLD_PLAY_COUNT"] = 0
		return returnDictionary

	# Load data from save file, 
	def loadTestFileData(self):
		tempDictionary = {}
		# first populate dictionary with default values
		# Make a shallow copy of the default dictionary
		for k,v in self.getDefaultTestFileData().items():
			tempDictionary[k] = v

		# try to update dictionary with values from save data
		try:
			file = open(self.testFileName, "r") 	
			for line in file: 
				colonLocation = line.find(":")
				if colonLocation > -1:
					fieldString = line[:colonLocation]
					valueString = line[(colonLocation + 1):]
					tempDictionary[fieldString] = valueString
			file.close()
		except:
			print("No Test file found")
		return tempDictionary


	def getTestFileData(self):
		return self.testFileData

	# Use this file to update individual fields before saving
	def updateTestFileDataValue(self, key, value):
		self.testFileData[key] = value

	# save all current data to file
	def saveTestFileData(self):
		file = open(self.testFileName,"w") 
 
		# Only write fields that we care about here.
		print("saving...")

		for k,v in self.testFileData.items():
			desiredFieldName = "FLD_TEST_1"
			if(k == desiredFieldName):
				file.write(str(k) + ":" + str(v) + "\n")
			desiredFieldName = "FLD_TEST_2"
			if(k == desiredFieldName):
				file.write(str(k) + ":" + str(v) + "\n")
			desiredFieldName = "FLD_PLAY_COUNT"
			if(k == desiredFieldName):
				file.write(str(k) + ":" + str(v) + "\n")
		file.close() 





	# Stuff to do with Control data

	# DEFAULT VALUES GO HERE
	def getDefaultControlData(self):
		returnDictionary = {}
		returnDictionary["CONTROL_SCHEME"] = "QWERTY-numpad"
		return returnDictionary

	# Load data from save file, 
	def loadControlData(self):
		tempDictionary = {}
		# first populate dictionary with default values
		# Make a shallow copy of the default dictionary
		for k,v in self.getDefaultControlData().items():
			tempDictionary[k] = v

		# try to update dictionary with values from save data
		try:
			file = open(self.controlsFileName, "r") 	
			for line in file: 
				colonLocation = line.find(":")
				if colonLocation > -1:
					fieldString = line[:colonLocation]
					newlineLocation = line.find("\n")
					if newlineLocation > colonLocation:
						valueString = line[(colonLocation + 1):newlineLocation]
					else: 
						valueString = line[(colonLocation + 1):]
					tempDictionary[fieldString] = valueString
			file.close()
		except:
			print("No Control file found")
		return tempDictionary


	def getControlData(self):
		return self.controlData

	# Use this file to update individual fields before saving
	def updateControlDataValue(self, key, value):
		self.controlData[key] = value

	# save all current data to file
	def saveControlData(self):
		file = open(self.controlsFileName,"w") 
 
		# Only write fields that we care about here.
		print("saving...")

		for k,v in self.controlData.items():
			desiredFieldName = "CONTROL_SCHEME"
			if(k == desiredFieldName):
				file.write(str(k) + ":" + str(v))
			#desiredFieldName = "FLD_TEST_1"
			#if(k == desiredFieldName):
			#	file.write(str(k) + ":" + str(v) + "\n")
			#desiredFieldName = "FLD_TEST_2"
			#if(k == desiredFieldName):
			#	file.write(str(k) + ":" + str(v) + "\n")
			#desiredFieldName = "FLD_PLAY_COUNT"
			#if(k == desiredFieldName):
			#	file.write(str(k) + ":" + str(v) + "\n")
		file.close() 





## The basic unit of save data. We have the name of the field, and its value. Good stuff.
#class SaveDatum:
#	def __init__(self, fieldName, value):
#		self.fieldName = fieldName
#		self.value = value

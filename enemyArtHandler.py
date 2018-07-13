import csv
import os
# A class that loads non-mechanical enemy data stuff (names, sprite location, colors, description) from a csv file,
# and then returns that data to the game when requested
class EnemyArtHandler:
	def __init__(self,pathname, dataFile = "enemyArtData.csv"):

		datapath = os.path.join(pathname,  dataFile)
		print("Loading enemy art data from " + datapath)

		# create a dictionary for storing all the enemy data.
		self.enemyArtDict = {}

		with open(datapath) as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				self.enemyArtDict[row['game_name']]=(row['Name'], row['Symbol'], (int(row['colorR']), int(row['colorG']), int(row['colorB'])), row['Description'] )

	def getEnemyArtData(self, enemy_name):
		returnData = None
		#print ("testing...")
		if ( enemy_name in self.enemyArtDict):
			returnData = self.enemyArtDict[enemy_name]
		else:
			returnData = (None, None, (0,0,0), None)
		return returnData
			#print(row['game_name'])
			#if row['game_name'] == enemy_name:
			#	# populate data from this row
			#	print("Found data!")
			#	break
#print(row['first_name'], row['last_name'])

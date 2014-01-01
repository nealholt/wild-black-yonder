import random as rd
import globalvars
import sys
sys.path.append('code/cython')
import cygeometry
import ship


def printNodeLocations(nodelist):
	for n in nodelist:
		print n.loc


class Node():
	def __init__(self, myid, x, y):
		''' '''
		self.id = myid
		self.x = x
		self.y = y
		self.loc = (x,y)
		#list of id,location pairs this node is connected to
		self.connections = []

		#Parameters for the faction (if any) that owns this node:
		self.owner = -1 #Id of the faction that owns this node.
		self.flag = ''
		#The following arrays determine how many items of the given tech level 
		#are produced at this node per turn.
		#For example, if self.ship_production[4] = 2 then 2 class 4 ships will be produced.
		self.ship_production = [0 for _ in range(len(ship.ship_class_names))]
		self.engine_production = [0 for _ in range(len(ship.engine.engine_class_names))]
		self.weapon_production = [0 for _ in range(len(ship.weapon.weapon_class_names))]
		self.missile_production = [0 for _ in range(len(ship.missile.missile_class_names))]
		self.mine_production = [0 for _ in range(len(ship.mine.mine_class_names))]
		#How many of these tech items are at this node.
		#Production values are added into this array each turn.
		self.ship_tech = [0 for _ in range(len(ship.ship_class_names))]
		self.engine_tech = [0 for _ in range(len(ship.engine.engine_class_names))]
		self.weapon_tech = [0 for _ in range(len(ship.weapon.weapon_class_names))]
		self.missile_tech = [0 for _ in range(len(ship.missile.missile_class_names))]
		self.mine_tech = [0 for _ in range(len(ship.mine.mine_class_names))]

		#Parameters to distinguish nodes by parameterizing the infinite space generator.
		#Randomly initialize these for now:
		rd.seed(self.id)
		self.description = 'Unknown'
		self.piracy = rd.uniform(0.0, 4.0) #chance to generate pirate ships
		self.pirate_caps = rd.uniform(0.0, 1.2) #chance of generating pirate capital ships
		self.amt_debris = rd.uniform(3.0, 15.0) #chance of asteroids
		self.amt_wealth = rd.uniform(0.5, 3.0) #chance of gems, health, and rich asteroids
		#The class of pirate ships generated at this node.
		self.pirate_weapon_tech = rd.randint(0, len(ship.weapon.weapon_class_names) / 2)
		self.pirate_missile_tech = rd.randint(0, len(ship.missile.missile_class_names) / 2)
		self.pirate_mine_tech = rd.randint(0, len(ship.mine.mine_class_names) / 2)
		self.pirate_ship_tech = rd.randint(0, len(ship.ship_class_names) / 2)
		self.pirate_engine_tech = rd.randint(0, len(ship.engine.engine_class_names) / 2)

		#Nodes will store the references to the following objects at their location
        #TODO LEFT OFF HERE
		self.warps=[]
		self.planets=[]
		self.fuel_depots=[]

		#Now initialize the values to be used to populate space based on the above values.
		self.initialize()


	def initialize(self):
		self.enemy_min = 0.0
		self.enemy_max = self.piracy
		self.crystal_min = 0.0
		self.crystal_max = self.amt_wealth / 2.0
		self.large_asteroid_min = 0.0
		self.large_asteroid_max = self.amt_debris / 3.0
		self.medium_asteroid_min = 0.0
		self.medium_asteroid_max = self.amt_debris / 2.0
		self.small_asteroid_min = 0.0
		self.small_asteroid_max = self.amt_debris
		self.gold_metal_min = 0.0
		self.gold_metal_max = self.amt_wealth
		self.silver_metal_min = 0.0
		self.silver_metal_max = self.amt_wealth
		self.health_min = 0.0
		self.health_max = 1.5
		self.capital_ship_min = 0.0
		self.capital_ship_max = self.pirate_caps
		self.fuel_min = 0.0
		self.fuel_max = self.amt_wealth/2
		self.planet_min = 0.0
		self.planet_max = self.amt_wealth/2


	def getTextArray(self):
		return [
		'Id: '+str(self.id)+'.',
		'Description: '+self.description+'.',
		'Piracy: '+"{0:.2f}".format(self.piracy)+'. Chance to generate opposing ships.',
		'Pirate Capital Ships: '+"{0:.2f}".format(self.pirate_caps)+'. Chance of hostile capital ships.',
		'Debris: '+"{0:.2f}".format(self.amt_debris)+'. Chance of asteroids.',
		'Wealth: '+"{0:.2f}".format(self.amt_wealth)+'. Chance of gems, health, and rich asteroids.',
		'Pirate weapon tech: '+str(self.pirate_weapon_tech),
		'Pirate missile tech: '+str(self.pirate_missile_tech),
		'Pirate mine tech: '+str(self.pirate_mine_tech),
		'Pirate ship tech: '+str(self.pirate_ship_tech),
		'Pirate engine tech: '+str(self.pirate_engine_tech),
		'Owner weapon production: '+str(self.weapon_production),
		'Owner missile production: '+str(self.missile_production),
		'Owner mine production: '+str(self.mine_production),
		'Owner ship production: '+str(self.ship_production),
		'Owner engine production: '+str(self.engine_production)
		]


	def changeAttribute(self, attribute_index, amount):
		if attribute_index == globalvars.node_debris_index:
			self.amt_debris += amount
		elif attribute_index == globalvars.node_wealth_index:
			self.amt_wealth += amount
		elif attribute_index == globalvars.node_production_index:
			#Select a random production
			rand_production = rd.randint(0,4)
			production_to_alter = None
			if rand_production == 0:
				production_to_alter = self.ship_production
			elif rand_production == 1:
				production_to_alter = self.engine_production
			elif rand_production == 2:
				production_to_alter = self.weapon_production
			elif rand_production == 3:
				production_to_alter = self.missile_production
			elif rand_production == 4:
				production_to_alter = self.mine_production
			#Get index to alter.
			#and alter production by amount with a minimum of zero and max of 10
			if amount > 0:
				for i in range(len(production_to_alter)):
					if production_to_alter[i] < 10:
						production_to_alter[i] = min(10, production_to_alter[i]+amount)
						break
			else:
				for i in range(len(production_to_alter)):
					if production_to_alter[i] > 0:
						production_to_alter[i] = max(0, production_to_alter[i]+amount)
						break
		else:
			print 'Error: attribute_index, '+str(attribute_index)+' out of bounds in nodeManager.changeAttribute'; exit()


	def boostProduction(self, production_attribute, tech_level, amount):
		production_to_alter = None
		if production_attribute == 0:
			production_to_alter = self.ship_production
		elif production_attribute == 1:
			production_to_alter = self.engine_production
		elif production_attributen == 2:
			production_to_alter = self.weapon_production
		elif production_attribute == 3:
			production_to_alter = self.missile_production
		elif production_attribute == 4:
			production_to_alter = self.mine_production
		else:
			print 'ERROR production_attribute == '+str(production_attribute)+' is invalid in nodeManager.boostProduction.'; exit()
		#Alter production by amount with a minimum of zero
		production_to_alter[i] = max(0, production_to_alter[i]+amount)


	def getStrength(self):
		#Just return the number of ships at this node for now.
		return sum(self.ship_tech)


	def addConnection(self, connectid, location):
		self.connections.append((connectid,location))


	def removeConnection(self, connectid):
		for c in self.connections:
			if c[0] == connectid:
				self.connections.remove(c)
				break

	def alreadyConnected(self, connectid):
		for c in self.connections:
			if c[0] == connectid:
				return True
		return False

	def setPiracyStrength(self, min_percent, max_percent):
		#The class of pirate ships generated at this node.
		maximum = len(ship.weapon.weapon_class_names)
		low = int(min_percent * maximum)
		high = int(max_percent * maximum)
		self.pirate_weapon_tech = rd.randint(low,high)

		maximum = len(ship.missile.missile_class_names)
		low = int(min_percent * maximum)
		high = int(max_percent * maximum)
		self.pirate_missile_tech = rd.randint(low,high)

		maximum = len(ship.mine.mine_class_names)
		low = int(min_percent * maximum)
		high = int(max_percent * maximum)
		self.pirate_mine_tech = rd.randint(low,high)

		maximum = len(ship.ship_class_names)
		low = int(min_percent * maximum)
		high = int(max_percent * maximum)
		self.pirate_ship_tech = rd.randint(low,high)

		maximum = len(ship.engine.engine_class_names)
		low = int(min_percent * maximum)
		high = int(max_percent * maximum)
		self.pirate_engine_tech = rd.randint(low,high)




class NodeManager():
	def __init__(self):
		self.nodes = []
		#a list of x,y pairs representing connections without duplicates.
		self.connections = []

	def getNode(self, nodeid):
		for n in self.nodes:
			if n.id == nodeid:
				return n
		return None

	def generateGalaxy(self, seed=0, nodecount=10, minimumNodeDist=40):
		'''Post: randomly populates self.nodes.'''
		maxNeighbors = 6
		#Reset nodes
		self.nodes = []
		rd.seed(seed)
		#Randomly create locations for each node.
		for i in range(nodecount):
			x = rd.randint(globalvars.MENU_PADDING+globalvars.MENU_BORDER_PADDING,
				globalvars.WIDTH-globalvars.MENU_PADDING-globalvars.MENU_BORDER_PADDING)
			y = rd.randint(globalvars.MENU_PADDING+globalvars.MENU_BORDER_PADDING,
				globalvars.HEIGHT-globalvars.MENU_PADDING-globalvars.MENU_BORDER_PADDING)
			self.nodes.append(Node(i, x, y))
		#Sort the nodes by x
		sortednodes = sorted(self.nodes, key=lambda n: n.x, reverse=True)
		#Remove nodes that are too close
		anyTooClose = True
		while anyTooClose:
			anyTooClose = False
			#Check for pairs of nodes that are too close together and remove one of them.
			for i in xrange(nodecount-1):
				for j in xrange(i+1, nodecount):
					if cygeometry.distance(sortednodes[i].loc, sortednodes[j].loc) < minimumNodeDist:
						anyTooClose = True
						sortednodes.pop(j)
						nodecount -= 1
						break
				if anyTooClose: break
		#print 'Final node count is '+str(nodecount) #TESTING
		#Re-id the nodes to ensure that a node with id 0 exists.
		#This must be done before connecting the nodes.
		for i in xrange(len(sortednodes)):
			sortednodes[i].id = i
		#Connect each node only to its closest maxNeighbors neighbors.
		closestsNeighbors = [] #Store pairs of neighbor ids and distances
		for i in xrange(len(sortednodes)):
			#Populate closestsNeighbors with
			#maxNeighbors - len(sortednodes[i].connections) connections
			closestNeighbors = []
			for j in xrange(len(sortednodes)):
				#Get the distance between the nodes
				dist = cygeometry.distance(sortednodes[i].loc, sortednodes[j].loc)
				#Determine how full of connections the current node is
				vacancies = maxNeighbors - len(sortednodes[i].connections)
				if vacancies == 0: break
				#If node i is not the same as node j and
				#node i is not already connected to node j and
				#(closestsNeighbors is not yet full or 
				#node j is closer to node i than any other node in closetsNeighbors)
				#Then replace the furthest node in closestNeighbors with node j
				#and sort closestsNeighbors.
				if i != j and\
				not sortednodes[i].alreadyConnected(sortednodes[i].id) and\
				((len(closestNeighbors) < vacancies) or\
				(dist < closestNeighbors[0][1])):
					#If closestNeighbors is not yet full
					if len(closestNeighbors) < vacancies:
						closestNeighbors.append((j, dist))
					else:
						#Then replace the furthest node in closestNeighbors with node j
						closestNeighbors[0] = (j, dist)
					#and sort closestsNeighbors by distance.
					closestNeighbors = sorted(closestNeighbors, reverse=True,
							key=lambda neighbor: neighbor[1])
			#Connect all the closest neighbors
			for cn in closestNeighbors:
				sortednodes[i].addConnection(sortednodes[cn[0]].id,
					sortednodes[cn[0]].loc)
				sortednodes[cn[0]].addConnection(sortednodes[i].id,
					sortednodes[i].loc)
		#Copy all the final nodes to the self.nodes
		self.nodes = sortednodes
		#Randomly remove between 0 and (the number of connections -2) connections
		for sn in self.nodes:
			toRemove = rd.randint(0, len(sn.connections)-2)
			for _ in range(toRemove):
				removeIndex = rd.randint(0, len(sn.connections)-1)
				removed = sn.connections.pop(removeIndex)
				otherEndOfConnection = self.getNode(removed[0])
				otherEndOfConnection.removeConnection(sn.id)
		#Create list of connections without duplicates.
		self.connections = []
		for n in self.nodes:
			for c in n.connections:
				#Only add connections in one direction to prevent duplicates.
				if c[0] > n.id:
					otherend = self.getNode(c[0])
					self.connections.append([n.x, n.y, otherend.x, otherend.y])
		#Scale pirate difficulty with distance from node 0 where the player starts.
		#Go through all nodes and get their distance from node 0 where the player will start
		#Set the pirate strength of the node based on its distance from the player's start node.
		#Treat globalvars.WIDTH as roughly the maximum distance from node 0.
		for n in self.nodes:
			d = cygeometry.distance(n.loc, self.nodes[0].loc)
			percent = d / float(globalvars.WIDTH)
			n.setPiracyStrength(percent/2.0, min(1.0, percent))


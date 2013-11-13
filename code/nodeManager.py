import random as rd
import globalvars
from geometry import distance

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
		#Parameters to distinguish nodes by parameterizing the infinite space generator.
		self.hostility = 0.0 #chance to generate opposing ships
		self.strength = 0.0 #strength of opposing ships (initially just capital ship chance)
		self.amt_debris = 0.0 #chance of asteroids
		self.amt_wealth = 0.0 #chance of gems, health, and rich asteroids
		self.owner = -1 #Id of the faction that owns this node.
		self.flag = ''

		#For now, deterministically set the profile of the node based on its index:
		self.description = ''
		if self.id % 4 == 0:
			self.description = 'Hostile'
			self.hostility = 4.0
			self.strength = 0.0
			self.amt_debris = 6.0
			self.amt_wealth = 1.1
		elif self.id % 3 == 0:
			self.description = 'Capital ships'
			self.hostility = 2.5
			self.strength = 2.0
			self.amt_debris = 6.0
			self.amt_wealth = 1.1
		elif self.id % 2 == 0:
			self.description = 'Wealthy'
			self.hostility = 0.0
			self.strength = 0.0
			self.amt_debris = 6.0
			self.amt_wealth = 3.0
		else:
			self.description = 'Asteroids'
			self.hostility = 1.5
			self.strength = 0.0
			self.amt_debris = 15.0
			self.amt_wealth = 1.5

		self.enemy_min = 0.0
		self.enemy_max = self.hostility
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
		self.capital_ship_max = self.strength
		self.fuel_min = 0.0
		self.fuel_max = self.amt_wealth/2


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
					if distance(sortednodes[i].loc, sortednodes[j].loc) < minimumNodeDist:
						anyTooClose = True
						sortednodes.pop(j)
						nodecount -= 1
						break
				if anyTooClose: break
		print 'Final node count is '+str(nodecount)
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
				dist = distance(sortednodes[i].loc, sortednodes[j].loc)
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


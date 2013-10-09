import random as rd
import globalvars
from geometry import distance
import menus

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


	def addConnection(self, connectid, location):
		self.connections.append((connectid,location))


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
		'''Post: randomly populates self.nodes.
		chanceNoConnect is the probability that a connection will be skipped if at 
		least one connection already exists at both endpoints.'''
		padding = 20
		#Reset nodes
		self.nodes = []
		rd.seed(seed)
		#Randomly create locations for each node.
		for i in range(nodecount):
			x = rd.randint(padding+menus.border_padding,
				globalvars.WIDTH-padding-menus.border_padding)
			y = rd.randint(padding+menus.border_padding,
				globalvars.HEIGHT-padding-menus.border_padding)
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
		#Calculate the largest distance between nearest nodes for each node
		largestNeighborDist = 0.0
		for i in xrange(1, len(sortednodes)-1):
			largestNeighborDist = max(largestNeighborDist,\
					distance(sortednodes[i-1].loc, sortednodes[i].loc),
					distance(sortednodes[i].loc, sortednodes[i+1].loc))
		#Connect each node only to its closest neighbor
		for i in xrange(len(sortednodes)-1):
			closestIndex = 0
			smallestDistance = largestNeighborDist
			for j in xrange(i+1, len(sortednodes)):
				dist = distance(sortednodes[i].loc, sortednodes[j].loc)
				if dist < smallestDistance:
					closestIndex = j
					smallestDistance = dist
			#Connect the closest node
			sortednodes[i].addConnection(sortednodes[closestIndex].id,
							sortednodes[closestIndex].loc)
			sortednodes[closestIndex].addConnection(sortednodes[i].id,
								sortednodes[i].loc)


		#Copy all the final nodes to the self.nodes
		self.nodes = sortednodes
		#Create list of connections without duplicates.
		self.connections = []
		for n in self.nodes:
			for c in n.connections:
				#Only add connections in one direction to prevent duplicates.
				if c[0] > n.id:
					otherend = self.getNode(c[0])
					self.connections.append([n.x, n.y, otherend.x, otherend.y])


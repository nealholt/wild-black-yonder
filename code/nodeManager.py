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

	def generateGalaxy(self, seed=0):
		'''Post randomly populates self.nodes'''
		padding = 20
		minimumNodeDist = 40
		#Reset nodes
		self.nodes = []
		rd.seed(seed)
		#Select a random number of nodes.
		nodecount = rd.randint(5,10)
		#Randomly create locations for each node.
		for i in range(nodecount):
			x = rd.randint(0, globalvars.WIDTH-padding-menus.border_padding)
			y = rd.randint(0, globalvars.HEIGHT-padding-menus.border_padding)
			self.nodes.append(Node(i, x, y))
		#Sort the nodes by x
		sortednodes = sorted(self.nodes, key=lambda n: n.x, reverse=True)
		#Remove nodes that are too close
		finalNodeList = []
		for i in xrange(nodecount-1):
			keep = True
			for j in xrange(i+1, nodecount):
				if distance(sortednodes[i].loc, sortednodes[j].loc) < minimumNodeDist:
					keep = False
					break
			if keep:
				finalNodeList.append(sortednodes[i])
		#Re-id the nodes to ensure that a node with id 0 exists. This must be done before connecting the nodes.
		for i in xrange(len(finalNodeList)):
			finalNodeList[i].id = i
		#Calculate the largest distance between nearest nodes for each node
		largestNeighborDist = 0.0
		for i in xrange(1, len(finalNodeList)-1):
			largestNeighborDist = max(largestNeighborDist,\
					distance(finalNodeList[i-1].loc, finalNodeList[i].loc),
					distance(finalNodeList[i].loc, finalNodeList[i+1].loc))
		#Connect all nodes that are within the largest distance from each other.
		for i in xrange(len(finalNodeList)-1):
			for j in xrange(i+1, len(finalNodeList)):
				dist = distance(finalNodeList[i].loc, finalNodeList[j].loc)
				if dist < largestNeighborDist:
					#Add a chance to not add connections if at least one connection 
					#already exists at both endpoints
					if len(finalNodeList[i].connections) == 0 or \
					len(finalNodeList[j].connections) == 0 or \
					rd.random() > 0.5:
						finalNodeList[i].addConnection(finalNodeList[j].id, finalNodeList[j].loc)
						finalNodeList[j].addConnection(finalNodeList[i].id, finalNodeList[i].loc)
				else:
					break
		#Copy all the final nodes to the self.nodes
		self.nodes = finalNodeList
		#Create list of connections without duplicates.
		self.connections = []
		for n in self.nodes:
			for c in n.connections:
				#Only add connections in one direction to prevent duplicates.
				if c[0] > n.id:
					otherend = self.getNode(c[0])
					self.connections.append([n.x, n.y, otherend.x, otherend.y])


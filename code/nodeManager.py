import random as rd
import globalvars
from geometry import distance
import menus

class Node():
	def __init__(self, myid, x, y):
		''' '''
		self.id = myid
		self.x = x
		self.y = y
		self.loc = (x,y)
		#list of ids this node is connected to
		self.connections = []

	def addConnection(self, connectid):
		self.connections.append(connectid)


class NodeManager():
	def __init__(self):
		self.nodes = []
		#a list of x,y pairs representing connections without duplicates.
		self.connections = []

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
			x = rd.randint(padding+menus.left, globalvars.WIDTH-padding-menus.border_padding)
			y = rd.randint(padding+menus.top, globalvars.HEIGHT-padding-menus.border_padding)
			self.nodes.append(Node(i, x, y))
		#Sort the nodes by x as a secondary key and y as a primary key.
		sortednodes = sorted(self.nodes, key=lambda n: n.x, reverse=True)
		sortednodes = sorted(sortednodes, key=lambda n: n.y, reverse=True)
		#Remove nodes that are too close
		finalNodeList = []
		for i in xrange(nodecount-1):
			if distance(sortednodes[i].loc, sortednodes[i+1].loc) > minimumNodeDist:
				finalNodeList.append(sortednodes[i])
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
					finalNodeList[i].addConnection(finalNodeList[j].id)
					finalNodeList[j].addConnection(finalNodeList[i].id)
				else:
					break
		#Create list of connections without duplicates.
		self.connections = []
		#TODO LEFT OFF HERE



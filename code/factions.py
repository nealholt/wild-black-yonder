import globalvars
import colors
import random as rd

class Faction():
	def __init__(self, name, myid, color, flag=None):
		''' '''
		self.name = name
		self.id = myid
		self.color = color
		self.flag = flag #Later this should be a small square image
		self.allies = []
		self.enemies = []
		self.nodes = []
		#Zero is neutral. Positive is a good relationship. Negative is a bad relationship.
		self.relationToPlayer = 0

	def captureNode(self, nodeid):
		'''Do this very carefully.'''
		#Make sure that the node has no current owner.
		node = globalvars.galaxy.getNode(nodeid)
		if node.owner != -1: print 'ERROR: node is already owned by '+str(node.owner)+'.'; exit()
		if nodeid in self.nodes: print 'ERROR: node is already owned by self.'; exit()
		self.nodes.append(nodeid)
		node.owner = self.id
		node.flag = self.flag


class FactionManager():
	def __init__(self):
		self.factions = []
		#initialize a short list of factions
		self.factions.append(Faction('Federation', 0, colors.blue, flag='flag00'))
		self.factions.append(Faction('Cephalopods', 1, colors.red, flag='flag01'))
		self.factions.append(Faction('Pirates', 2, colors.black, flag='flag02'))
		#Assign each faction a random node
		for f in self.factions:
			#Get a node that is not yet owned:
			nodeid = rd.randint(0, len(globalvars.galaxy.nodes))
			node = globalvars.galaxy.getNode(nodeid)
			while node.owner != -1:
				nodeid = rd.randint(0, len(globalvars.galaxy.nodes))
				node = globalvars.galaxy.getNode(nodeid)
			#Give this node to the current faction
			f.captureNode(nodeid)

	def getFactionById(self, factionid):
		for f in self.factions:
			if f.id == factionid:
				return f
		return None


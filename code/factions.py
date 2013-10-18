import colors

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


class FactionManager():
	def __init__(self):
		self.factions = []
		#initialize a short list of factions
		self.factions.append(Faction('Federation', 0, colors.blue))
		self.factions.append(Faction('Cephalopods', 1, colors.red))
		self.factions.append(Faction('Pirates', 0, colors.black))

	def example(self):
		pass


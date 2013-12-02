import colors
from objInstances import Mine
import globalvars
import random as rd

class MineLayer():
	def __init__(self, shooter, name='default'):
		self.name=name
		self.refire_rate=10 #Fires once every refire_rate frames
		self.cooldown=0 #How long until next shot
		self.shooter = shooter
		self.attack_angle = 10 #if within this angle to target, can shoot at target
		self.is_a = 'mine'

	def cool(self):
		if self.cooldown > 0:
			self.cooldown -= 1

	def shoot(self):
		tempmine = Mine(self.shooter)
		#Add mine to the sprite groups
		globalvars.tangibles.add(tempmine)
		#Add it to whiskerables so enemy ships will avoid it.
		globalvars.whiskerables.add(tempmine)
		self.cooldown=self.refire_rate

	def toStringArray(self):
		str_array = [self.name,
			'Refire rate: '+str(self.refire_rate)]
		return str_array

import ship
import profiles

class Player(ship.Ship):
	def __init__(self, image_name):

		ship.Ship.__init__(self,image_name=image_name)

		profiles.shipProfile(self, profile='mk1')
		self.setProfile()

		self.is_player=True

		self.health = 100.0
		self.maxhealth = 100.0

		self.parkAtDestination = False


	def parkingBrake(self):
		'''Change the truth value of park.'''
		self.parkAtDestination = not self.parkAtDestination


	def update(self, offset=(0,0)):
		if not self.destination is None:
			#Turn towards target
			self.turnTowards()

			if self.parkAtDestination:
				self.park()
			else:
				#Approach target speed
				self.approachSpeed()
		else:
			#Approach target speed
			self.approachSpeed()

		self.move()


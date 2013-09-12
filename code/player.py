import ship
import profiles

class Player(ship.Ship):
	def __init__(self, image_name):

		ship.Ship.__init__(self,image_name=image_name)

		profiles.shipProfile(self, profile='mk2')
		self.setProfile()

		self.rect.topleft = (-100,-100)

		self.parkAtDestination = False


	def parkingBrake(self):
		'''Change the truth value of park.'''
		self.parkAtDestination = not self.parkAtDestination


	def update(self, offset=(0,0)):
		'''The player's update function does nothing.
		The player uses the special playerUpdate function
		which is needed for when the screen follows or 
		centers on the player.'''
		pass


	def playerUpdate(self, offset=(0,0)):
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


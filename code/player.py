import ship
import profiles
import weapon #TODO TESTING SPREAD SHOT


class Player(ship.Ship):
	def __init__(self, image_name):

		ship.Ship.__init__(self,image_name=image_name)

		profiles.shipProfile(self, profile='mk2')
		self.setProfile()

		#TODO TESTING SPREAD SHOT
		w = weapon.Weapon()
		weapon.setProfile('spread_mk3', w)
		w.shooter = self
		self.weapons = [w]


		self.health=500
		self.maxhealth=500

		self.rect.centerx = -100.
		self.rect.centery = -100.

		self.parkAtDestination = False

		self.destination = None

		print self.speed


	def parkingBrake(self):
		'''Change the truth value of park.'''
		self.parkAtDestination = not self.parkAtDestination


	def update(self, offset=(0,0)):
		'''The player's update function does very little.
		The player uses the special playerUpdate function
		which is needed for when the screen follows or 
		centers on the player.'''
		self.cooldown() #cooldown all the weapons
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


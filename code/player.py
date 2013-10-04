import ship
import profiles
import globalvars #TODO TESTING
from geometry import translate

class Player(ship.Ship):
	def __init__(self, image_name):

		ship.Ship.__init__(self,image_name=image_name)

		profiles.shipProfile(self, profile='mk3')
		self.setProfile()

		#Initialize the player with just one weapon. Make it a spread shot.
		self.weapons = None
		self.setWeapon('spread_mk3')

		self.health=300
		self.maxhealth=300

		self.rect.centerx = -100.
		self.rect.centery = -100.

		self.parkAtDestination = False

		self.destination = None

		self.isPlayer = True

		#Node location of the player.
		self.nodeid = 0
		self.destinationNode = 0


	def parkingBrake(self):
		'''Change the truth value of park.'''
		self.parkAtDestination = not self.parkAtDestination


	def update(self):
		'''The player's update function does very little.
		The player uses the special playerUpdate function
		which is needed for when the screen follows or 
		centers on the player.'''
		self.cooldown() #cooldown all the weapons
		#Update my health bar
		self.updateHealthBar()


	def getLeadIndicator(self):
		'''Return the point in space that enemies should shoot 
		at to hit the player when the player is moving.'''
		#return self.rect.center
		return translate(self.rect.center, self.theta, self.speed*50.0) #The amount to translate depends on player speed, distance from enemy, and bullet speed. There might be a better way to do this.
		#Why when self.rect.center is used does this still not work for the capital ship? Specifically there is a problem when I perch over the upper left corner of the capital ship. It creates a kind-of cool blind spot though. Maybe this is not a problem.


	def playerUpdate(self):
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


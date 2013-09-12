import ship
import profiles
import weapon

class Player(ship.Ship):
	def __init__(self, image_name):

		ship.Ship.__init__(self,image_name=image_name)

		profiles.shipProfile(self, profile='mk3')
		self.setProfile()

		#Initialize the player with just one weapon. Make it a spread shot.
		self.weapons = [weapon.Weapon()]
		self.setWeapon('spread_mk3')

		self.health=300
		self.maxhealth=300

		self.rect.centerx = -100.
		self.rect.centery = -100.

		self.parkAtDestination = False

		self.destination = None

		self.isPlayer = True

		#print 'TESTING player speed in player.py: '+str(self.speed)


	def setWeapon(self, weaponId):
		'''Pre: weaponId is a string such as 'spread_mk3'.
		Assumes the player only has one weapon equipped.
		Post: Changes the player's weapon.
		This is called by the weapons panel in menus.py.'''
		weapon.setProfile(weaponId, self.weapons[0])
		self.weapons[0].shooter = self


	def parkingBrake(self):
		'''Change the truth value of park.'''
		self.parkAtDestination = not self.parkAtDestination


	def update(self):
		'''The player's update function does very little.
		The player uses the special playerUpdate function
		which is needed for when the screen follows or 
		centers on the player.'''
		self.cooldown() #cooldown all the weapons
		pass


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


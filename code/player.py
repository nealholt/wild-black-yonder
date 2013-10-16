import ship
import profiles
from geometry import translate
import weapon
import globalvars
from displayUtilities import TemporaryText
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

		#Track the most recent fuel alert level to avoid giving multiple warnings.
		self.fuelAlertLevel = 4

		#Node location of the player.
		self.nodeid = 0
		self.destinationNode = 0

		#For testing purposes, load all the weapons except the initially equipped 
		#weapon into the player's cargo hold.
		weaponsList = ['mk0', 'mk1', 'mk2', 'spread_mk2', 'missile_mk1', 'mine', 'hit_box_test']
		for w in weaponsList:
			self.cargo.append(weapon.getWeapon(w, self))


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
		self.fuel -= self.engine.fuel_consumption
		if self.fuel < 10*globalvars.FPS*self.engine.fuel_consumption and \
		self.fuelAlertLevel > 1:  #10 seconds of fuel remain
			announcement = TemporaryText(x=globalvars.CENTERX, y=globalvars.CENTERY+52,
				text='Empty fuel tank imminent! 10 seconds!',
				timeOff=0, timeOn=1, ttl=3.5, fontSize=52)
			globalvars.intangibles_top.add(announcement)
			self.fuelAlertLevel = 1
		elif self.fuel < 30*globalvars.FPS*self.engine.fuel_consumption and \
		self.fuelAlertLevel > 2: #30 seconds of fuel remain
			announcement = TemporaryText(x=globalvars.CENTERX, y=globalvars.CENTERY+52,
				text='Fuel critical! 30 seconds of fuel remain.',
				timeOff=0, timeOn=1, ttl=3.5, fontSize=52)
			globalvars.intangibles_top.add(announcement)
			self.fuelAlertLevel = 2
		elif self.fuel < 60*globalvars.FPS*self.engine.fuel_consumption and \
		self.fuelAlertLevel > 3: #60 seconds of fuel remain
			announcement = TemporaryText(x=globalvars.CENTERX, y=globalvars.CENTERY+52,
				text='Fuel low! 60 seconds of fuel remain.',
				timeOff=0, timeOn=1, ttl=3.5, fontSize=52)
			globalvars.intangibles_top.add(announcement)
			self.fuelAlertLevel = 3

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


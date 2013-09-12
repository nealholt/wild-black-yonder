import colors
import game
import objInstances


class Weapon():
	def __init__(self):
		self.name='default'
		self.refire_rate=10 #Fires once every refire_rate frames
		self.cooldown=0 #How long until next shot
		self.bullet_speed=10
		self.bullet_lifespan=50 #How long the bullet lasts before expiring
		self.bullet_num=1 #number of bullets fired at a time
		self.bullet_color=colors.pink
		self.spread=0 #spread of bullets fired
		self.attack_angle = 1 #if within this angle to target, can shoot at target
		#1.2 is a fudge factor used so that the ship shoots slightly before 
		#its target moves into range, in case the two ships are closing
		self.weapon_range = self.bullet_speed*self.bullet_lifespan*1.2
		self.shooter = None

	def cool(self):
		if self.cooldown > 0:
			self.cooldown -= 1

	def shoot(self):
		#If we are firing spread shot, do things differently
		if self.spread > 0 and self.bullet_num > 1:
			#I calculate half beforehand because for some reason in python
			#rounding works differently when the numbers are negative. 
			#For example:
			# 3/2 = 1
			# -3/2 = -2
			half = self.bullet_num/2
			if self.bullet_num%2 == 0:
				range_of_spread = range(-half/2, half+1)
				#There will be one too many bullets if the number is even so 
				#remove the middle one
				range_of_spread.pop(len(range_of_spread)/2)
			else:
				range_of_spread = range(-half, half+1)
			#Adjust the angle for each bullet in the spread
			for adj in range_of_spread:
				angle = self.shooter.theta + self.spread*adj
				self.makeBullet(angle)
		else:
			self.makeBullet(self.shooter.theta)
		#reset cooldown
		self.cooldown = self.refire_rate


	def makeBullet(self, angle):
		tempbullet = objInstances.Bullet(angle, self.shooter.rect.centerx,\
			self.shooter.rect.centery, self.shooter)
		#Set bullet attributes
		tempbullet.speed = self.bullet_speed
		tempbullet.setColor(self.bullet_color)
		tempbullet.timeToLive = self.bullet_lifespan
		#Add bullet to the sprite groups
		game.tangibles.add(tempbullet)


def setProfile(profile, weapon):
	if profile == 'mk0':
		weapon.name='Laser Mk0'
		weapon.refire_rate=1000 #Fires once every refire_rate frames
		weapon.cooldown=0 #How long until next shot
		weapon.bullet_speed=0
		weapon.bullet_lifespan=0 #How long the bullet lasts before expiring
		weapon.bullet_num=0 #number of bullets fired at a time
		weapon.spread=0 #spread of bullets fired
		weapon.attack_angle = 0
		weapon.bullet_color=colors.pink
	elif profile == 'mk1':
		weapon.name='Laser Mk1'
		weapon.refire_rate=10 #Fires once every refire_rate frames
		weapon.cooldown=0 #How long until next shot
		weapon.bullet_speed=15
		weapon.bullet_lifespan=50 #How long the bullet lasts before expiring
		weapon.bullet_num=1 #number of bullets fired at a time
		weapon.spread=0 #spread of bullets fired
		weapon.attack_angle = 3
		weapon.bullet_color=colors.pink
	elif profile == 'mk2':
		weapon.name='Laser Mk2'
		weapon.refire_rate=5 #Fires once every refire_rate frames
		weapon.cooldown=0 #How long until next shot
		weapon.bullet_speed=25
		weapon.bullet_lifespan=50 #How long the bullet lasts before expiring
		weapon.bullet_num=1 #number of bullets fired at a time
		weapon.spread=0 #spread of bullets fired
		weapon.attack_angle = 3
		weapon.bullet_color=colors.pink
	elif profile == 'spread_mk2':
		weapon.name='Spread Shot Laser Mk2'
		weapon.refire_rate=10 #Fires once every refire_rate frames
		weapon.cooldown=0 #How long until next shot
		weapon.bullet_speed=25
		weapon.bullet_lifespan=50 #How long the bullet lasts before expiring
		weapon.bullet_num=2 #number of bullets fired at a time
		weapon.spread=10 #spread of bullets fired
		weapon.attack_angle = 3
		weapon.bullet_color=colors.pink
	elif profile == 'spread_mk3':
		weapon.name='Spread Shot Laser Mk3'
		weapon.refire_rate=10 #Fires once every refire_rate frames
		weapon.cooldown=0 #How long until next shot
		weapon.bullet_speed=25
		weapon.bullet_lifespan=50 #How long the bullet lasts before expiring
		weapon.bullet_num=3 #number of bullets fired at a time
		weapon.spread=10 #spread of bullets fired
		weapon.attack_angle = 3
		weapon.bullet_color=colors.pink


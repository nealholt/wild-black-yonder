import colors
from objInstances import Bullet, Missile, Mine
import globalvars
from testFunctions import HitBoxTestBullet

class Weapon():
	def __init__(self, shooter, name='default'):
		self.name=name
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
		self.shooter = shooter
		#Use the following for ships like the capital ship that have guns offset from their center
		self.offset = (0,0)

	def cool(self):
		if self.cooldown > 0:
			self.cooldown -= 1

	def shoot(self, forceAngle=None):
		'''forceAngle allows a custom firing angle.'''
		if forceAngle is None:
			forceAngle = self.shooter.theta
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
				angle = forceAngle + self.spread*adj
				self.makeBullet(angle)
		else:
			self.makeBullet(forceAngle)
		#reset cooldown
		self.cooldown = self.refire_rate


	def makeBullet(self, angle):
		tempbullet = Bullet(angle, self.shooter.rect.centerx+self.offset[0],\
			self.shooter.rect.centery+self.offset[1], self.shooter)
		#Set bullet attributes
		tempbullet.speed = self.bullet_speed
		tempbullet.setColor(self.bullet_color)
		tempbullet.timeToLive = self.bullet_lifespan
		#Add bullet to the sprite groups
		globalvars.tangibles.add(tempbullet)



class HitBoxTesterGun():
	def __init__(self, shooter, name='default'):
		self.name='HitBoxTesterGun'
		self.cooldown=0 #How long until next shot
		self.bullet_speed=5
		self.refire_rate=10 #Fires once every refire_rate frames
		self.bullet_lifespan=150 #How long the bullet lasts before expiring
		self.bullet_color=colors.yellow
		self.shooter = shooter

	def cool(self):
		if self.cooldown > 0:
			self.cooldown -= 1

	def shoot(self):
		self.makeBullet(self.shooter.theta)
		#reset cooldown
		self.cooldown = self.refire_rate


	def makeBullet(self, angle):
		tempbullet = HitBoxTestBullet(angle, self.shooter.rect.centerx,\
			self.shooter.rect.centery, self.shooter)
		#Set bullet attributes
		tempbullet.speed = self.bullet_speed
		tempbullet.setColor(self.bullet_color)
		tempbullet.timeToLive = self.bullet_lifespan
		#Add bullet to the sprite groups
		globalvars.tangibles.add(tempbullet)



class MissileLauncher():
	def __init__(self, shooter, name='default'):
		self.name=name
		self.refire_rate=120 #Fires once every refire_rate frames
		self.cooldown=0 #How long until next shot
		self.shooter = shooter
		self.attack_angle = 10 #if within this angle to target, can shoot at target
		self.weapon_range = 700

	def cool(self):
		if self.cooldown > 0:
			self.cooldown -= 1

	def shoot(self):
		tempmissile = Missile(self.shooter)
		#Add missile to the sprite groups
		globalvars.tangibles.add(tempmissile)
		self.cooldown=self.refire_rate



class MineLayer():
	def __init__(self, shooter, name='default'):
		self.name=name
		self.refire_rate=10 #Fires once every refire_rate frames
		self.cooldown=0 #How long until next shot
		self.shooter = shooter
		self.attack_angle = 10 #if within this angle to target, can shoot at target
		self.weapon_range = 700

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



def getWeapon(profile, weaponOwner):
	weapon = Weapon(weaponOwner)
	if profile == 'mk0':
		weapon.name='Laser Mk0'
		weapon.refire_rate=100*globalvars.FPS #Fires once every seconds
		weapon.bullet_speed=0 #speed in pixels per second
		weapon.bullet_lifespan=0 #How long the bullet lasts in seconds before expiring
		weapon.bullet_num=0 #number of bullets fired at a time
		weapon.spread=0 #spread of bullets fired
		weapon.attack_angle = 0
		weapon.bullet_color=colors.pink
	elif profile == 'mk1':
		weapon.name='Laser Mk1'
		weapon.refire_rate=1*globalvars.FPS #Fires once every refire_rate seconds
		weapon.bullet_speed=400./float(globalvars.FPS) #speed in pixels per second
		weapon.bullet_lifespan=2*globalvars.FPS #How long the bullet lasts in seconds before expiring
		weapon.bullet_num=1 #number of bullets fired at a time
		weapon.spread=0 #spread of bullets fired
		weapon.attack_angle = 3
		weapon.bullet_color=colors.pink
	elif profile == 'mk2':
		weapon.name='Laser Mk2'
		weapon.refire_rate=int(0.5*globalvars.FPS) #Fires once every refire_rate seconds
		weapon.bullet_speed=500./float(globalvars.FPS) #speed in pixels per second
		weapon.bullet_lifespan=int(2.5*globalvars.FPS) #How long the bullet lasts in seconds before expiring
		weapon.bullet_num=1 #number of bullets fired at a time
		weapon.spread=0 #spread of bullets fired
		weapon.attack_angle = 3
		weapon.bullet_color=colors.pink
	elif profile == 'spread_mk2':
		weapon.name='Spread Shot Laser Mk2'
		weapon.refire_rate=int(0.5*globalvars.FPS) #Fires once every refire_rate seconds
		weapon.bullet_speed=500./float(globalvars.FPS) #speed in pixels per second
		weapon.bullet_lifespan=int(2.5*globalvars.FPS) #How long the bullet lasts in seconds before expiring
		weapon.bullet_num=2 #number of bullets fired at a time
		weapon.spread=10 #spread of bullets fired
		weapon.attack_angle = 3
		weapon.bullet_color=colors.pink
	elif profile == 'spread_mk3':
		weapon.name='Spread Shot Laser Mk3'
		weapon.refire_rate=int(0.2*globalvars.FPS) #Fires once every refire_rate seconds
		weapon.bullet_speed=650./float(globalvars.FPS) #speed in pixels per second
		weapon.bullet_lifespan=int(2.5*globalvars.FPS) #How long the bullet lasts in seconds before expiring
		weapon.bullet_num=3 #number of bullets fired at a time
		weapon.spread=10 #spread of bullets fired
		weapon.attack_angle = 3
		weapon.bullet_color=colors.pink
	elif profile == 'missile_mk1':
		weapon = MissileLauncher(weaponOwner, name='Missile Mk1')
		weapon.refire_rate=3*globalvars.FPS #Fires once every refire_rate seconds
	elif profile == 'mine':
		weapon = MineLayer(weaponOwner, name='Mine Mk1')
		weapon.refire_rate=1*globalvars.FPS #Fires once every refire_rate seconds
	elif profile == 'hit_box_test':
		weapon = HitBoxTesterGun(weaponOwner)
		weapon.refire_rate=int(0.2*globalvars.FPS) #Fires once every refire_rate seconds
		weapon.bullet_speed=650./float(globalvars.FPS) #speed in pixels per second
		weapon.bullet_lifespan=int(2.5*globalvars.FPS) #How long the bullet lasts in seconds before expiring
	return weapon


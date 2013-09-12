import colors
import game
import random as rd
import bullet

def inSights(shooter, target_loc, weapon_range, angle_min):
	'''Pre: shooter is a ship. target_loc is a tuple x,y. weapon_range is an int or float.
	angle_min is a float or int representing the minimal angle to the target.
	Post: returns true it the target is roughly in the sights of the shooter.
	TODO this method should probably be moved elsewhere.'''
	angle = shooter.getAngleToTarget(target=target_loc)
	#Check angle to target.
	#Also check that the target is roughly within this weapon's range.
	return abs(angle) < angle_min and \
	shooter.distanceToDestination(dest=target_loc) < weapon_range

def clearLineOfSight(seer, sight_range, angle_min):
	'''Pre: Seer is a ship. Sight_range is an int or float.
	Post: Returns true if there are no whiskerables in the line of sight of this ship.
	Useful for avoiding friendly fire.'''
	for w in game.whiskerables:
		center = w.getCenter()
		dist = seer.distanceToDestination(dest=center)
		if dist < sight_range and dist > 0 and\
		abs(seer.getAngleToTarget(center)) < angle_min:
			return False
	return True


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

	def cool(self):
		if self.cooldown > 0:
			self.cooldown -= 1

	def maybeShoot(self, shooter, force_shot=False):
		'''Player will fire when able using force_shot. NPC's will fire 
		when their gun is in range.'''
		if self.cooldown == 0:
			if force_shot:
				self.shoot(shooter)
			else:
				angle = shooter.getAngleToTarget()
				#Decide whether or not we can shoot
				if inSights(shooter, shooter.destination, \
				self.weapon_range, self.attack_angle) and\
				clearLineOfSight(shooter, self.weapon_range, self.attack_angle):
					for _ in range(self.bullet_num):
						self.shoot(shooter)

	def shoot(self, shooter):
		#Set bullet direction and starting location
		angle = shooter.theta
		if self.spread > 0:
			angle += rd.randint(-self.spread, self.spread)
		tempbullet = bullet.Bullet(angle, shooter.rect.centery,\
			shooter.rect.centerx, shooter)
		#Set bullet attributes
		tempbullet.speed = self.bullet_speed
		tempbullet.setColor(self.bullet_color)
		tempbullet.timeToLive = self.bullet_lifespan
		#Add bullet to the sprite groups
		game.tangibles.add(tempbullet)
		#reset cooldown
		self.cooldown = self.refire_rate


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


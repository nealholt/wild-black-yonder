import colors
import game
import random as rd
import bullet

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

	def maybeShoot(self, shooter, force_shot=False):
		'''Player will fire when able using force_shot. NPC's will fire 
		when their gun is in range.'''
		if self.cooldown > 0:
			self.cooldown -= 1
		else:
			if force_shot:
				self.shoot(shooter, is_player=True)
			else:
				angle = shooter.getAngleToTarget()
				#Decide whether or not we can shoot
				if abs(angle) < self.attack_angle:
					for _ in range(self.bullet_num):
						self.shoot(shooter)

	def shoot(self, shooter, is_player=False):
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
		game.allSprites.add(tempbullet)
		if is_player:
			game.playerSprites.add(tempbullet)
		else:
			game.enemySprites.add(tempbullet)
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


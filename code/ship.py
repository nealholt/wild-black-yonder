import pygame
import physicalObject
import profiles
import game
import colors
import explosion
import healthBar

class Ship(physicalObject.PhysicalObject):
	def __init__(self, top=0, left=0, image_name='default'):

		physicalObject.PhysicalObject.__init__(self, top=top, left=left,\
						image_name=image_name)

		self.name='default'
		self.weapons=[]
		self.engine=None

		self.health=50
		self.maxhealth=50

		profiles.shipProfile(self, profile='mk0')
		self.setProfile()

		self.myHealthBar = healthBar.HealthBar(width=20, height=10, ship=self, vertical=False, 
			current=self.health, total=self.maxhealth)
		game.intangibles.add(self.myHealthBar)

		self.is_a = game.SHIP


	def setProfile(self):
		#TODO shouldn't there be a better way to do this?
		self.maxSpeed = self.engine.maxSpeed
		self.dv = self.engine.dv
		self.dthea = self.engine.dtheta


	def takeDamage(self):
		self.health -= 10

	def isDead(self):
		return self.health <= 0


	def shoot(self, force_shot=False):
		#Force shot tells this to shoot even if a target 
		#is not obviously in view. NPC's will not take such wild shots.
		for w in self.weapons:
			w.maybeShoot(self, force_shot=force_shot)


	def update(self, offset):
		#for now we assume that every ship is hostile to the player
		self.setDestination(game.player.getCenter())

		#Turn towards target
		self.turnTowards()

		d = self.distanceToDestination()
		#If target is far, increase goal speed.
		if d > 200:
			self.targetSpeed = self.maxSpeed
		#If target is near, decrease goal speed.
		elif d < 120:
			self.targetSpeed = 0
		else:
			self.targetSpeed = self.maxSpeed/2

		#Check for firing solutions
		self.shoot()

		#modify speed
		self.approachSpeed()

		#move
		self.move()

		#draw
		x,y = self.getCenter()
		pos = x - offset[0], y - offset[1]
		self.drawAt(pos)


	def handleCollisionWith(self, other_sprite):
		'''For now ships take damage regardless of what they hit.'''
		died = False
		#Check for collisions with one's own bullets.
		#Don't respond to such collisions.
		if other_sprite.is_a == game.BULLET:
			if other_sprite.dontClipMe == self:
				return died
		elif other_sprite.is_a == game.SHIP:
			#Check for bounce off
			#For now, area stands in for mass and only the
			#less massive object bounces off
			if other_sprite.getArea() >= self.getArea():
				self.bounceOff(other_sprite)
		self.takeDamage()
		if self.isDead():
			game.intangibles.add(explosion.Explosion(self.getY(),self.getX()))
			#kill removes the calling sprite from all sprite groups
			self.kill()
			self.myHealthBar.kill()
			died = True
		return died


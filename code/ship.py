import pygame
import physicalObject
import profiles
import game
import colors
import explosion

class Ship(physicalObject.PhysicalObject):
	def __init__(self, top=0, left=0, image_name='default'):

		physicalObject.PhysicalObject.__init__(self, top=top, left=left,\
						image_name=image_name)

		self.name='default'
		self.weapons=[]
		self.engine=None

		self.health=50
		self.maxhealth=50

		self.healthBarWidth = 20
		self.healthBarHeight = 10

		profiles.shipProfile(self, profile='mk0')
		self.setProfile()

		#step 33: figure out how to only draw ship healthbars when on the screen: ship creates a physical object healthbar, and adds it to the intangibles, and maintains a pointer to it. ship doesn't draw it, but updates its location when the ship's update function is called. Might, probably want a healthbar object. Maybe it keeps track of the ship rather than the other way around. TODO LEFT OFF HERE. healthBar.py was created to keep track of healthbars and progress bars in general.
		#step 34: test healthbars

		self.is_a = game.SHIP


	def setProfile(self):
		#TODO shouldn't there be a better way to do this?
		self.maxSpeed = self.engine.maxSpeed
		self.dv = self.engine.dv
		self.dthea = self.engine.dtheta


	def drawHealthBarAt(self, offset):
		'''Draw health bars'''
		healthx = offset[0] - self.healthBarWidth/2
		healthy = offset[1] - self.healthBarHeight - self.rect.height/2

		tempRect = pygame.Rect(healthx, healthy, self.healthBarWidth, self.healthBarHeight)
		pygame.draw.rect(game.screen, colors.red, tempRect, 0)

		width = self.health/float(self.maxhealth)*self.healthBarWidth
		tempRect = pygame.Rect(healthx, healthy, width, self.healthBarHeight)
		pygame.draw.rect(game.screen, colors.green, tempRect, 0)

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
		self.drawHealthBarAt(pos)
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
			#step 23: this should be done to intangible_sprites
			game.allSprites.add(explosion.Explosion(self.getY(),self.getX()))
			#kill removes the calling sprite from all sprite groups
			self.kill()
			died = True
		return died


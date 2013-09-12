import pygame
import physicalObject
import profiles
import game
import colors

class Ship(physicalObject.PhysicalObject):
	def __init__(self, top=0, left=0, image_name='default'):

		physicalObject.PhysicalObject.__init__(self, top=top, left=left,\
						image_name=image_name)

		self.name='default'
		self.weapons=[]
		self.engine=None

		self.is_player=False

		self.health=50
		self.maxhealth=50

		self.healthBarWidth = 20
		self.healthBarHeight = 10

		profiles.shipProfile(self, profile='mk0')
		self.setProfile()


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


	def shoot(self):
		for w in self.weapons:
			w.maybeShoot(self, force_shot=self.is_player)


	def update(self, offset):
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


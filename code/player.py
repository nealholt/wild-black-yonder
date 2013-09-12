#TODO this is getting mighty similar to enemy. May be time to consolidate into one object

import pygame
import physicalObject
import bullet

class Player(physicalObject.PhysicalObject):
	def __init__(self, game):

		left = 100
		top = 100
		width = 10
		height = 10
		physicalObject.PhysicalObject.__init__(self, game, top, left, width, height)

		#Go to max speed immediately.
		self.targetSpeed = self.maxSpeed

	def shoot(self):
		tempbullet = bullet.Bullet(self.game, self.theta, self.rect.centery, self.rect.centerx, self)
		self.game.allSprites.add(tempbullet)
		self.game.playerSprites.add(tempbullet)

	def update(self):
		self.draw()

		#check if the object is due for an update
		if pygame.time.get_ticks() < self.lastUpdate + self.interval:
			return True
		self.lastUpdate += self.interval

		#Turn towards target
		self.turnTowards()

		#Approach target speed
		self.approachSpeed()

		self.move()



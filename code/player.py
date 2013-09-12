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

		#List of things not to collide with
		self.noClipList = pygame.sprite.Group()


	def shoot(self):
		tempbullet = bullet.Bullet(self.game, self.theta, self.rect.centery, self.rect.centerx, self)
		self.game.spritegroup.add(tempbullet)
		self.noClipList.add(tempbullet)

	def update(self):
		#Turn towards target
		self.turnTowards()

		#Approach target speed
		self.approachSpeed()

		self.move()
		self.draw()

	def noClipWith(self, other):
		return self.noClipList.has(other)

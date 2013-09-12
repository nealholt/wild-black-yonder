import physicalObject
import random as rd
import pygame

#Just flash some red and orange circles on the screen and throw out some debris.

class Explosion(physicalObject.PhysicalObject):
	def __init__(self, game, top, left):

		width = height = 0
		physicalObject.PhysicalObject.__init__(self, game, top, left, width, height)

		#How long this object will live
		self.timeToLive = 7

	def update(self):
		if self.timeToLive <= 0:
			self.kill() #http://pygame.org/docs/ref/sprite.html#Sprite.kill
			return True
		self.timeToLive -= 1

		self.game.allSprites.add(Flash(self.game,self.rect.centery,self.rect.centerx))
		self.game.allSprites.add(Debris(self.game,self.rect.centery,self.rect.centerx))



class Flash(physicalObject.PhysicalObject):
	def __init__(self, game, top, left):
		flashCenterRadius = 20
		flashRadiusMin = 20
		flashRadiusMax = 50
		flashMinTimeToLive = 8
		flashMaxTimeToLive = 17

		top += rd.randint(-flashCenterRadius,flashCenterRadius)
		left += rd.randint(-flashCenterRadius,flashCenterRadius)

		width = height = 0

		physicalObject.PhysicalObject.__init__(self, game, top, left, width, height)

		self.timeToLive = rd.randint(flashMinTimeToLive, flashMaxTimeToLive)
		color = self.randHotColor()
		radius = rd.randint(flashRadiusMin, flashRadiusMax)

		self.rect = pygame.draw.circle(self.game.screen, color, (left, top), radius, 0)

	def randHotColor(self):
		return (rd.randint(100, 155), rd.randint(000, 100), rd.randint(0, 20))

	def update(self):
		if self.timeToLive <= 0:
			self.kill() #http://pygame.org/docs/ref/sprite.html#Sprite.kill
			return True
		self.timeToLive -= 1
		self.draw()


class Debris(physicalObject.PhysicalObject):
	def __init__(self, game, top, left):
		width = 4
		height = 4
		self.timeToLive = rd.randint(10, 24)

		physicalObject.PhysicalObject.__init__(self, game, top, left, width, height)
		self.theta = rd.randint(0, 359)
		self.speed = rd.randint(7.0, 30.0)

	def update(self):
		if self.timeToLive <= 0:
			self.kill() #http://pygame.org/docs/ref/sprite.html#Sprite.kill
			return True
		self.timeToLive -= 1

		self.move()
		self.draw()


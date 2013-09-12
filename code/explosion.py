import physicalObject
import random as rd
import pygame

#Just flash some red and orange circles on the screen and throw out some randomly shaped debris.
	#TODO randomly shaped debris:
		#http://www.pygame.org/docs/ref/draw.html#pygame.draw.polygon
		#pygame.draw.polygon(Surface, color, pointlist, width=0)

class Explosion(physicalObject.PhysicalObject):
	def __init__(self, game, top, left):

		physicalObject.PhysicalObject.__init__(self, game, top, left, 1, 1)

		#How long this object will live in intervals
		self.timeToLive = 7

	def update(self):
		if self.timeToLive <= 0:
			self.kill() #http://pygame.org/docs/ref/sprite.html#Sprite.kill
			return True
		self.timeToLive -= 1

		self.game.spritegroup.add(Flash(self.game,self.rect.centery,self.rect.centerx))
		self.game.spritegroup.add(Debris(self.game,self.rect.centery,self.rect.centerx))


	def noClipWith(self, other):
		'''Don't clip with anything.'''
		return True


class Flash(physicalObject.PhysicalObject):
	def __init__(self, game, top, left):
		top += rd.randint(-20,20)
		left += rd.randint(-20,20)

		physicalObject.PhysicalObject.__init__(self, game, top, left, 0, 0)

		self.timeToLive = rd.randint(8, 15)
		color = (rd.randint(100, 155), rd.randint(000, 100), rd.randint(0, 20))
		#self.setColor(color)
		radius = rd.randint(20, 30)

		self.rect = pygame.draw.circle(self.game.screen, color, (left, top), radius, 0)

	def update(self):
		if self.timeToLive <= 0:
			self.kill() #http://pygame.org/docs/ref/sprite.html#Sprite.kill
			return True
		self.timeToLive -= 1
		self.draw()

	def noClipWith(self, other):
		'''Don't clip with anything.'''
		return True


class Debris(physicalObject.PhysicalObject):
	def __init__(self, game, top, left):
		width = 4
		height = 4
		self.timeToLive = rd.randint(10, 24)
		physicalObject.PhysicalObject.__init__(self, game, top, left, width, height)
		self.theta = rd.randint(0, 359)
		self.speed = rd.randint(70.0, 300.0) * self.interval

	def update(self):
		if self.timeToLive <= 0:
			self.kill() #http://pygame.org/docs/ref/sprite.html#Sprite.kill
			return True
		self.timeToLive -= 1
		self.move()
		self.draw()

	def noClipWith(self, other):
		'''Don't clip with anything.'''
		return True


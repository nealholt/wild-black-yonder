import physicalObject
import random as rd
import pygame
import game
import colors

#Just flash some red and orange circles on the screen and throw out some debris.

class Explosion(physicalObject.PhysicalObject):
	def __init__(self, top, left):

		physicalObject.PhysicalObject.__init__(self, top=top, left=left)

		#How long this object will live
		self.timeToLive = 7


	def update(self, offset):
		if self.timeToLive <= 0:
			self.kill() #http://pygame.org/docs/ref/sprite.html#Sprite.kill
			return True
		self.timeToLive -= 1

		#I have not a sweet fucking clue why the flash requires this adjustment 
		#but debris requires lack of an adjustment. It makes no sense to me.
		#I have tried very hard to figure this out and have spent much time on it.
		#I am unwilling to spend any more time. DO NOT go down this hole.
		top = self.rect.centery-offset[1]
		left = self.rect.centerx-offset[0]
		game.allSprites.add(Flash(top, left))
		game.allSprites.add(Debris(self.rect.centery, self.rect.centerx))



class Flash(physicalObject.PhysicalObject):
	def __init__(self, top, left):
		flashCenterRadius = 20
		flashRadiusMin = 20
		flashRadiusMax = 50
		flashMinTimeToLive = 8
		flashMaxTimeToLive = 17

		top += rd.randint(-flashCenterRadius,flashCenterRadius)
		left += rd.randint(-flashCenterRadius,flashCenterRadius)

		physicalObject.PhysicalObject.__init__(self, top=top, left=left)

		self.timeToLive = rd.randint(flashMinTimeToLive, flashMaxTimeToLive)
		color = colors.getRandHotColor()
		radius = rd.randint(flashRadiusMin, flashRadiusMax)

		self.rect = pygame.draw.circle(game.screen, color, (left, top), radius, 0)

	def update(self, offset):
		if self.timeToLive <= 0:
			self.kill() #http://pygame.org/docs/ref/sprite.html#Sprite.kill
			return True
		self.timeToLive -= 1
		self.draw(offset)


class Debris(physicalObject.PhysicalObject):
	def __init__(self, top, left):
		self.timeToLive = rd.randint(10, 24)

		physicalObject.PhysicalObject.__init__(self, top=top, left=left,\
						width=4, height=4)
		self.theta = rd.randint(-179, 180)
		self.speed = rd.randint(7.0, 30.0)

 	def update(self, offset):
		if self.timeToLive <= 0:
			self.kill() #http://pygame.org/docs/ref/sprite.html#Sprite.kill
			return True
		self.timeToLive -= 1
		#print 'START\nbefore move'+str(self.rect.topleft)
		self.move()
		#print 'after move'+str(self.rect.topleft)
		self.draw(offset)
		#print 'after draw'+str(self.rect.topleft)


class FixedBody(physicalObject.PhysicalObject):
	'''A motionless body created for testing purposes.'''
	def __init__(self, top, left):
		physicalObject.PhysicalObject.__init__(self, top=top, left=left,\
						width=40, height=40)

	def update(self, offset):
		self.draw(offset)


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
			#kill removes the calling sprite from all sprite groups
			self.kill() #http://pygame.org/docs/ref/sprite.html#Sprite.kill
			return True
		self.timeToLive -= 1

		#I have not a sweet fucking clue why the flash requires this adjustment 
		#but debris requires lack of an adjustment. It makes no sense to me.
		#I have tried very hard to figure this out and have spent much time on it.
		#I am unwilling to spend any more time. DO NOT go down this hole.
		top = self.rect.centery-offset[1]
		left = self.rect.centerx-offset[0]

		game.intangibles.add(Flash(top, left))
		game.intangibles.add(Debris(self.rect.centery, self.rect.centerx))



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
			#kill removes the calling sprite from all sprite groups
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
			#kill removes the calling sprite from all sprite groups
			self.kill() #http://pygame.org/docs/ref/sprite.html#Sprite.kill
			return True
		self.timeToLive -= 1
		self.move()
		self.draw(offset)


class FixedBody(physicalObject.PhysicalObject):
	'''A motionless body created for testing purposes.'''
	def __init__(self, top, left, image_name=None):
		physicalObject.PhysicalObject.__init__(self, top=top, left=left,\
						width=40, height=40, image_name=image_name)
		self.is_a = game.FIXEDBODY

	def update(self, offset):
		self.draw(offset)


class HealthKit(physicalObject.PhysicalObject):
	'''A motionless body created for testing purposes.'''
	def __init__(self, top, left):
		physicalObject.PhysicalObject.__init__(self, top=top, left=left,
						image_name='images/health')
		self.is_a = game.HEALTH
		self.health_amt = 10
		self.picked_up = False
		self.timeToLive = 30 #Time to live after being picked up.

	def update(self, offset):
		if not self.picked_up:
			self.draw(offset)
		elif self.timeToLive <=0:
			#kill removes the calling sprite from all sprite groups
			self.kill() #http://pygame.org/docs/ref/sprite.html#Sprite.kill
		else:
			self.timeToLive -= 1
			#TODO the following drawing of text will not work with some camera modes. You probably want to make this something more like a generic method for text drawing.
			#Display the amount of health that was here.
			pos = self.rect.topleft[0] - offset[0], \
				self.rect.topleft[1] - offset[1]
			game.writeTextToScreen(string='+'+str(self.health_amt), \
				font_size=36, color=colors.green, pos=pos)

	def handleCollisionWith(self, other_sprite):
		'''React to a collision with other_sprite.'''
		died = False
		if not self.picked_up and other_sprite.is_a == game.SHIP:
			self.picked_up = True
			other_sprite.gainHealth(self.health_amt)
		return died


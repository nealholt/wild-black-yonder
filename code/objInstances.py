import physicalObject
import random as rd
import pygame
import game
import colors


class Bullet(physicalObject.PhysicalObject):
	def __init__(self, direction, top, left, dontClipMe, width=5, height=5):

		physicalObject.PhysicalObject.__init__(self, top, left, width, height)

		self.theta = direction

		#How long this object will live. Unit is... frames?
		self.timeToLive = 50

		#dontClipMe is almost certainly the shooter of this bullet.
		#This is important because bullets usually start out at a 
		#location that is immediately clipping the shooter but we 
		#don't want ships to blow themselves up.
		self.dontClipMe = dontClipMe

		self.is_a = game.BULLET

		#A brief invulnerability is necessary so that spread shot 
		#bullets don't collide with each other immediately and
		#disappear. This might make self.dontClipMe redundant, but
		#I don't care about such minor efficiency gains as removing 
		#self.dontClipMe. At least not yet.
		self.briefinvulnerability = 10


	def update(self, offset):
		if self.timeToLive <= 0:
			#kill removes the calling sprite from all sprite groups
			self.kill() #http://pygame.org/docs/ref/sprite.html#Sprite.kill
			return True

		self.timeToLive -= 1

		self.move()

		self.draw(offset)


	def handleCollisionWith(self, other_sprite):
		'''For now bullets die immediately regardless of what they hit.'''
		died = False
		if self.briefinvulnerability > 0:
			self.briefinvulnerability -= 1
			return died

		#self.dontClipMe is usually the shooter of the bullet who would 
		#otherwise immediately collide with it.
		#For now, shoot through health packs with no effect.
		if other_sprite != self.dontClipMe and not other_sprite.is_a == game.HEALTH:
			died = True
			#kill removes the calling sprite from all sprite groups
			self.kill()
		return died


class Explosion(physicalObject.PhysicalObject):
	'''Just flash some red and orange circles on the screen and throw out some debris.'''
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


class HealthBar(physicalObject.PhysicalObject):
	def __init__(self, width=0, height=0, ship=None, vertical=False, current=100, total=100):
		self.ship = ship

		physicalObject.PhysicalObject.__init__(self, top=0, left=0)

		#Boolean for whether to draw the healthbar horizontally or vertically.
		self.vertical = vertical

		#Current and total health or progress or whatever the bar is measuring
		self.health = current
		self.maxHealth = total

		self.healthBarWidth = width
		self.healthBarHeight = height


	def update(self, offset):
		heightAdjust = 0
		if self.ship is None:
			x,y = self.rect.topleft
		else:
			x,y = self.ship.rect.center
			heightAdjust = self.ship.rect.height
			self.health = self.ship.health
		pos = x - offset[0], y - offset[1]

		healthx = pos[0] - self.healthBarWidth/2
		healthy = pos[1] - self.healthBarHeight - heightAdjust/2

		tempRect = pygame.Rect(healthx, healthy, \
			self.healthBarWidth, self.healthBarHeight)
		pygame.draw.rect(game.screen, colors.red, tempRect, 0)

		width = (self.health/float(self.maxHealth))*self.healthBarWidth
		tempRect = pygame.Rect(healthx, healthy, width, self.healthBarHeight)
		pygame.draw.rect(game.screen, colors.green, tempRect, 0)

		self.drawAt(pos)


	def draw(self):
		pass


class Follower(physicalObject.PhysicalObject):
	def __init__(self, top, left):
		'''This is the object that invisibly follows the player and the 
		screen centers on it.
		This mechanism was intended to give a sense of speed and direction.'''
		physicalObject.PhysicalObject.__init__(self, top,left,10,10)

		self.setColor((155,155,0))
		self.maxSpeed = 10.0
		self.dv = 0.5 #acceleration
		#Turn rate:
		self.dtheta = 10.0

	def update(self, offset=(0,0)):
		#Turn towards target
		self.turnTowards()

		#slow down if near target
		if not self.park():
			#Approach target speed
			self.targetSpeed = self.maxSpeed
			self.approachSpeed()

		self.move()


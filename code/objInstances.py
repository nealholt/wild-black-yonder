import physicalObject
import random as rd
import pygame
import colors
from geometry import translate
import globalvars
from misc import writeTextToScreen

class Bullet(physicalObject.PhysicalObject):
	def __init__(self, direction, x, y, dontClipMe, width=5, height=5):

		physicalObject.PhysicalObject.__init__(self, centerx=x, centery=y,\
			width=width, height=height)

		self.theta = direction

		#How long this object will live. Unit is... frames?
		self.timeToLive = 50

		#dontClipMe is almost certainly the shooter of this bullet.
		#This is important because bullets usually start out at a 
		#location that is immediately clipping the shooter but we 
		#don't want ships to blow themselves up.
		self.dontClipMe = dontClipMe

		self.is_a = globalvars.BULLET

		#A brief invulnerability is necessary so that spread shot 
		#bullets don't collide with each other immediately and
		#disappear. This is only a bullet-on-bullet invulnerability
		self.briefinvulnerability = 5

	def update(self):
		if self.timeToLive <= 0:
			#kill removes the calling sprite from all sprite groups
			self.kill() #http://pygame.org/docs/ref/sprite.html#Sprite.kill
			return True
		if self.briefinvulnerability > 0:
			self.briefinvulnerability -= 1
		self.timeToLive -= 1
		self.move()

	def handleCollisionWith(self, other_sprite):
		'''For now bullets die immediately regardless of what they hit.'''
		died = False
		if other_sprite.is_a == globalvars.BULLET and self.briefinvulnerability > 0:
			return died

		#self.dontClipMe is usually the shooter of the bullet who would 
		#otherwise immediately collide with it.
		#For now, shoot through health packs with no effect.
		if other_sprite != self.dontClipMe and not other_sprite.is_a == globalvars.HEALTH:
			died = True
			#kill removes the calling sprite from all sprite groups
			self.kill()
		return died


class Explosion(physicalObject.PhysicalObject):
	'''Just flash some red and orange circles on the screen and throw out some debris.'''
	def __init__(self, x=0, y=0):
		physicalObject.PhysicalObject.__init__(self, centerx=x, centery=y)

		#How long this object will live
		self.timeToLive = 7

	def update(self):
		'''Return true to be removed from intangibles. Return False othewise.'''
		if self.timeToLive <= 0:
			#kill removes the calling sprite from all sprite groups
			self.kill() #http://pygame.org/docs/ref/sprite.html#Sprite.kill
			return True
		self.timeToLive -= 1

		globalvars.intangibles.append(Flash(x=self.rect.centerx, y=self.rect.centery))
		globalvars.intangibles.append(Debris(x=self.rect.centerx, y=self.rect.centery))
		return False

	def draw(self, offset):
		'''Explosion objects aren't drawn. They create other objects to draw.'''
		pass


flashCenterRadius = 20
flashRadiusMin = 20
flashRadiusMax = 50
flashMinTimeToLive = 8
flashMaxTimeToLive = 17
class Flash(physicalObject.PhysicalObject):
	def __init__(self, x=0, y=0):
		y += rd.randint(-flashCenterRadius,flashCenterRadius)
		x += rd.randint(-flashCenterRadius,flashCenterRadius)

		physicalObject.PhysicalObject.__init__(self, centerx=x, centery=y)

		self.timeToLive = rd.randint(flashMinTimeToLive, flashMaxTimeToLive)
		self.color = colors.getRandHotColor()
		self.radius = rd.randint(flashRadiusMin, flashRadiusMax)

	def update(self):
		'''Return true to be removed from intangibles. Return False othewise.'''
		if self.timeToLive <= 0:
			#kill removes the calling sprite from all sprite groups
			self.kill() #http://pygame.org/docs/ref/sprite.html#Sprite.kill
			return True
		self.timeToLive -= 1
		return False

	def draw(self, offset):
		x,y = self.rect.topleft
		pos = x - offset[0], y - offset[1]
		pygame.draw.circle(globalvars.screen, self.color, pos, self.radius, 0)


class Debris(physicalObject.PhysicalObject):
	def __init__(self, x=0, y=0):
		physicalObject.PhysicalObject.__init__(self, \
			centerx=x, centery=y, width=4, height=4)
		self.timeToLive = rd.randint(10, 24)
		self.theta = rd.randint(-179, 180)
		self.speed = rd.randint(7.0, 30.0)

 	def update(self):
		'''Return true to be removed from intangibles. Return False othewise.'''
		if self.timeToLive <= 0:
			#kill removes the calling sprite from all sprite groups
			self.kill() #http://pygame.org/docs/ref/sprite.html#Sprite.kill
			return True
		self.timeToLive -= 1
		self.move()
		return False


class FixedBody(physicalObject.PhysicalObject):
	'''A motionless body created for testing purposes.'''
	def __init__(self, x=0, y=0, width=40, height=40, image_name=None, color=colors.white):
		physicalObject.PhysicalObject.__init__(self, centerx=x, centery=y,\
						width=width, height=height, \
						image_name=image_name, color=color)
		self.is_a = globalvars.FIXEDBODY


class FixedCircle(physicalObject.PhysicalObject):
	'''A motionless colored circle currently used to show the edges of the arena.'''
	def __init__(self, x=0, y=0, radius=10, color=colors.white):
		physicalObject.PhysicalObject.__init__(self, centerx=x, centery=y)
		self.color = color
		self.radius = radius
		#Override the parent class with the following so that we make sure the 
		#circle is drawn correctly when only drawing objects that actually 
		#appear on screen.
		self.rect.width = self.radius*2
		self.rect.height = self.radius*2
		self.rect.center = x,y

	def draw(self, offset):
		pos = self.rect.centerx - offset[0], \
			self.rect.centery - offset[1]
		pygame.draw.circle(globalvars.screen, self.color, \
			pos, self.radius, 0)


#When a rock is blown up, what comes out?
subrocks = dict()
subrocks['images/asteroidBigRoundTidied'] = ('asteroidWild2', 4)
subrocks['images/asteroidWild2'] = ('asteroidTempel', 4)
subrocks['images/asteroidTempel'] = ('debris', 10)
subrocks['images/Sikhote_small'] = ('gem',1)
subrocks['images/bournonite_30percent'] = ('gem', 3)
def splitRock(image_name, centerx=0, centery=0):
	new_image, count = subrocks[image_name]
	if new_image == 'gem':
		for _ in range(count):
			temp = Gem(x=centerx, y=centery)
			globalvars.tangibles.add(temp)
			globalvars.whiskerables.add(temp)
	elif new_image == 'debris':
		for _ in range(count):
			temp = Debris(x=centerx, y=centery)
			globalvars.intangibles.append(temp)
	else:
		for _ in range(count):
			temp = Asteroid(x=centerx, y=centery,
				image_name='images/'+new_image)
			globalvars.tangibles.add(temp)
			globalvars.whiskerables.add(temp)


class Asteroid(physicalObject.PhysicalObject):
	'''An object that moves in only one direction, independent of rotation.
	It takes damage from bullets, collides with ships, but does not 
	collide with anything else.'''
	def __init__(self, x=0, y=0, image_name='', speed_min=1.0, speed_max=5.0):
		physicalObject.PhysicalObject.__init__(self, \
			centerx=x, centery=y, image_name=image_name)
		self.is_a = globalvars.ASTEROID
		self.health_amt = 100
		#Choose a random rotation
		#self.dtheta = rd.randint(-2, 2) #TODO temporarily remove rotation because it gums up the hit box and causes us to drop frames when there are a lot of objects.
		#Choose a random direction. This is different from theta 
		#which will only determine image rotation.
		self.direction = rd.randint(-179, 180)
		#Choose a random speed
		self.speed = rd.randint(speed_min, speed_max)

	def update(self):
		'''Return true to be removed. Return False othewise.'''
		#Rotate
		#if self.dtheta != 0: self.turn(self.dtheta) #TODO temporarily remove rotation because it gums up the hit box and causes us to drop frames when there are a lot of objects.
		#Move in a direction independent of rotation
		self.loc = translate(self.loc, self.direction, self.speed)
		self.rect.centerx = self.loc[0]
		self.rect.centery = self.loc[1]
		return False

	def handleCollisionWith(self, other_sprite):
		'''React to a collision with other_sprite.'''
		#print 'asteroid collision '+str(other_sprite.is_a)
		#print self.speed
		died = False
		if other_sprite.is_a == globalvars.BULLET:
			self.health_amt -= 10
			if self.health_amt < 0:
				#die. spawn mini asteroids
				self.kill()
				died = True
				splitRock(self.image_name,\
					centerx=self.rect.centerx,\
					centery=self.rect.centery)
		#The following was added to automatically nudge apart any colliding asteroids, but populate space has been debugged so I feel that this is no longer needed at this time.
		#elif other_sprite.is_a == globalvars.ASTEROID and self.speed == 0:
		#	magnitude = max(self.radius, other_sprite.radius)
		#	angle = self.getAngleToTarget(target=other_sprite)
		#	other_sprite.translate(angle, magnitude)
		return died


class Gem(physicalObject.PhysicalObject):
	'''A valuable gem.'''
	def __init__(self, x=0, y=0, speed_min=1.0, speed_max=5.0):
		physicalObject.PhysicalObject.__init__(self, centerx=x, centery=y,
						image_name='images/TyDfN_tiny')
		self.is_a = globalvars.GEM
		#Choose a random rotation
		self.dtheta = rd.randint(-5, 5)
		#Choose a random direction. This is different from theta 
		#which will only determine image rotation.
		self.direction = rd.randint(-179, 180)
		#Choose a random speed
		self.speed = rd.randint(speed_min, speed_max)
		#Gems can be picked up
		self.picked_up = False
		self.timeToLive = 30 #Time to live after being picked up.
		self.points = 10

	def update(self):
		'''Return true to be removed. Return False othewise.'''
		if not self.picked_up:
			#Rotate
			self.turn(self.dtheta)
			#Move in a direction independent of rotation
			self.loc = translate(self.loc, \
				self.direction, self.speed)
			self.rect.center = self.loc[0], self.loc[1]
		elif self.timeToLive <=0:
			#kill removes the calling sprite from all sprite groups
			self.kill() #http://pygame.org/docs/ref/sprite.html#Sprite.kill
			return True
		else:
			self.timeToLive -= 1
		return False

	def draw(self, offset):
		if not self.picked_up:
			#Call parent's draw class
			physicalObject.PhysicalObject.draw(self, offset)
		else:
			#Display the amount of health that was here.
			pos = self.rect.left - offset[0], \
				self.rect.top - offset[1]
			writeTextToScreen(string='+'+str(self.points), \
				font_size=36, color=colors.blue, pos=pos)

	def handleCollisionWith(self, other_sprite):
		'''React to a collision with other_sprite.'''
		died = False
		if not self.picked_up and other_sprite.is_a == globalvars.SHIP:
			self.picked_up = True
			#give money to the ship
			#Not all game huds are equipped to handle points yet so we use this try catch.
			#http://stackoverflow.com/questions/610883/how-to-know-if-an-object-has-an-attribute-in-python/610923#610923
			try:
				globalvars.hud_helper.points += self.points
			except AttributeError:
				pass
		return died


class HealthKit(physicalObject.PhysicalObject):
	'''A motionless body created for testing purposes.'''
	def __init__(self, x=0, y=0):
		physicalObject.PhysicalObject.__init__(self, centerx=x, centery=y,
						image_name='images/health')
		self.is_a = globalvars.HEALTH
		self.health_amt = 10
		self.picked_up = False
		self.timeToLive = 30 #Time to live after being picked up.

	def update(self):
		'''Return true to be removed. Return False othewise.'''
		if not self.picked_up:
			pass
		elif self.timeToLive <=0:
			#kill removes the calling sprite from all sprite groups
			self.kill() #http://pygame.org/docs/ref/sprite.html#Sprite.kill
			return True
		else:
			self.timeToLive -= 1
		return False

	def draw(self, offset):
		if not self.picked_up:
			#Call parent's draw class
			physicalObject.PhysicalObject.draw(self, offset)
		else:
			#Display the amount of health that was here.
			pos = self.rect.left - offset[0], \
				self.rect.top - offset[1]
			writeTextToScreen(string='+'+str(self.health_amt), \
				font_size=36, color=colors.green, pos=pos)

	def handleCollisionWith(self, other_sprite):
		'''React to a collision with other_sprite.'''
		died = False
		if not self.picked_up and other_sprite.is_a == globalvars.SHIP:
			self.picked_up = True
			other_sprite.gainHealth(self.health_amt)
		return died


class HealthBar(physicalObject.PhysicalObject):
	def __init__(self, width=0, height=0, ship=None, vertical=False, current=100, total=100):
		self.ship = ship

		physicalObject.PhysicalObject.__init__(self)

		#Boolean for whether to draw the healthbar horizontally or vertically.
		self.vertical = vertical

		#Current and total health or progress or whatever the bar is measuring
		self.health = current
		self.maxHealth = total

		self.healthBarWidth = width
		self.healthBarHeight = height

		self.heightAdjust = 0
		if not self.ship is None:
			self.heightAdjust = self.ship.rect.height

	def update(self):
		if not self.ship is None:
			self.rect.center = self.ship.rect.center
			self.health = self.ship.health

	def draw(self, offset):
		pos = self.rect.centerx - offset[0], self.rect.centery - offset[1]

		healthx = pos[0] - self.healthBarWidth/2
		healthy = pos[1] - self.healthBarHeight - self.heightAdjust/2

		tempRect = pygame.Rect(healthx, healthy, \
			self.healthBarWidth, self.healthBarHeight)
		pygame.draw.rect(globalvars.screen, colors.red, tempRect, 0)

		width = (self.health/float(self.maxHealth))*self.healthBarWidth
		tempRect = pygame.Rect(healthx, healthy, width, self.healthBarHeight)
		pygame.draw.rect(globalvars.screen, colors.green, tempRect, 0)

		self.drawAt(pos)



class Follower(physicalObject.PhysicalObject):
	def __init__(self, x=0, y=0):
		'''This is the object that invisibly follows the player and the 
		screen centers on it.
		This mechanism was intended to give a sense of speed and direction.'''
		physicalObject.PhysicalObject.__init__(self, centerx=x, centery=y,\
			width=10,height=10)

		self.setColor((155,155,0))
		self.maxSpeed = 10.0
		self.dv = 0.5 #acceleration
		#Turn rate:
		self.dtheta = 10.0

	def update(self):
		#Turn towards target
		self.turnTowards()

		#slow down if near target
		if not self.park():
			#Approach target speed
			self.targetSpeed = self.maxSpeed
			self.approachSpeed()

		self.move()


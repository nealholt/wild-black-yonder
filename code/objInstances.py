import physicalObject
import random as rd
import pygame
import colors
from geometry import translate, distance, rotateAngle
import globalvars
from displayUtilities import writeTextToScreen, TemporaryText
from time import sleep

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


class Missile(physicalObject.PhysicalObject):
	'''missile - new object that seeks nearest enemy target, damage and explosion on impact. 
	initial direction is same as firer. initial speed is firer plus some amount. 
	will not impact firer.'''
	def __init__(self, shooter):

		physicalObject.PhysicalObject.__init__(self, \
			centerx=shooter.rect.centerx, \
			centery=shooter.rect.centery,\
			width=10, height=10)

		self.theta = 135./float(globalvars.FPS)
		self.targetSpeed = 250.0/float(globalvars.FPS)
		#The missile assumes the shooter's direction and gets the shooter's 
		#speed plus its own speed before settling down to its target velocity.
		#Missile actually starts out faster and slows down.
		self.speed = self.targetSpeed + shooter.speed
		self.dv = self.targetSpeed/float(globalvars.FPS*3.0) #missile gets to target speed in 3 seconds

		#dontClipMe is almost certainly the shooter of this missile.
		#This is important because bullets usually start out at a 
		#location that is immediately clipping the shooter but we 
		#don't want ships to blow themselves up.
		self.dontClipMe = shooter

		self.is_a = globalvars.BULLET

		#Find nearest enemy ship and set it as target.
		self.target = None
		if shooter.isPlayer:
			#Search through globalvars.whiskerables
			closest = 999999.
			for w in globalvars.whiskerables:
				d = distance(w.rect.center, self.rect.center)
				print d
				if d < closest and w.is_a == globalvars.SHIP:
					print 'nearer target found'
					print closest
					print d
					self.target = w
					closest = d
		else:
			self.target = globalvars.player

	def update(self):
		#TODO seek target like an npc ship does
		'''The following code is mostly duplicated in the ship's update function. Eventually I'd like to break this out as a more general seeking behavior.'''
		#If the missile has no target, it will just kill itself and effectively not fire. Later, it might be cooler to have the missile just dumbfire and explode after a timeout.
		if self.target is None:
			print 'Missile has no target. Aborting firing sequence.'
			self.kill()

		self.setDestination(self.target.rect.center)

		#Turn towards target
		self.turnTowards()

		#modify speed
		self.approachSpeed()

		#move
		self.move()



	def handleCollisionWith(self, other_sprite):
		'''For now missiles die immediately regardless of what they hit.'''
		died = False
		#self.dontClipMe is usually the shooter of the bullet who would 
		#otherwise immediately collide with it.
		#For now, shoot through health packs with no effect.
		if other_sprite != self.dontClipMe and not other_sprite.is_a == globalvars.HEALTH:
			#explode
			globalvars.intangibles_bottom.add(Explosion(\
				x=self.rect.centerx,y=self.rect.centery))
			died = True
			#kill removes the calling sprite from all sprite groups
			self.kill()
		return died



class Mine(physicalObject.PhysicalObject):
	'''mine - new object does not move. collides with nothing until short timer elapses. 
	on contact explodes and causes damage. enemy will avoid it.'''
	def __init__(self, shooter):

		physicalObject.PhysicalObject.__init__(self, \
			centerx=shooter.rect.centerx, \
			centery=shooter.rect.centery,\
			width=10, height=10,\
			color=colors.orange)

		self.theta = 0.
		self.speed = 0.
		self.targetSpeed = 0.
		self.dv = 0.0

		#This is needed so that the shooter doesn't immediately take damage
		#from his own mine.
		self.dontClipMe = shooter

		self.is_a = globalvars.BULLET

		#A timer. This mine will explode on contact after this many seconds.
		self.explodeAfter = 4*globalvars.FPS

	def update(self):
		''' '''
		if self.explodeAfter > 0:
			self.explodeAfter -= 1
			#Now make the mine dangerous to everyone, including the person who laid it.
			if self.explodeAfter == 0:
				self.dontClipMe = None

	def handleCollisionWith(self, other_sprite):
		'''For now mines die immediately regardless of what they hit.'''
		died = False
		if self.explodeAfter == 0 or other_sprite.is_a == globalvars.BULLET:
			#explode
			globalvars.intangibles_bottom.add(Explosion(\
				x=self.rect.centerx,y=self.rect.centery))
			died = True
			#kill removes the calling sprite from all sprite groups
			self.kill()
		return died


class Explosion(physicalObject.PhysicalObject):
	'''Just flash some red and orange circles on the screen and throw out some debris.
	xMinAdj, xMaxAdj, yMinAdj, and yMaxAdj are used to spread explosions around the screen.
	Time to live is in seconds.'''
	def __init__(self, x=0, y=0, xMinAdj=0, xMaxAdj=0, yMinAdj=0, yMaxAdj=0, ttl=0.5):
		physicalObject.PhysicalObject.__init__(self, centerx=x, centery=y)

		self.xMinAdj=xMinAdj
		self.xMaxAdj=xMaxAdj
		self.yMinAdj=yMinAdj
		self.yMaxAdj=yMaxAdj
		#How long this object will live
		self.timeToLive = int(ttl*globalvars.FPS)

	def update(self):
		'''Return true to be removed from intangibles. Return False othewise.'''
		if self.timeToLive <= 0:
			self.kill()
		self.timeToLive -= 1

		x = rd.randint(self.xMinAdj, self.xMaxAdj) + self.rect.centerx
		y = rd.randint(self.yMinAdj, self.yMaxAdj) + self.rect.centery

		globalvars.intangibles_top.add(Flash(x=x, y=y))
		globalvars.intangibles_bottom.add(Debris(x=x, y=y))

	def draw(self, offset):
		'''Explosion objects aren't drawn. They create other objects to draw.'''
		pass

	def isOnScreen(self, _): return False


class Flash(physicalObject.PhysicalObject):
	'''There are lots of default values for a basic flash. It can be fun to modify these.
	Time to live is in seconds.'''
	def __init__(self, x=0, y=0, flashCenterRadius = 20, flashRadiusMin = 20, flashRadiusMax = 50, flashMinTimeToLive = 0.3, flashMaxTimeToLive =0.8):

		y += rd.randint(-flashCenterRadius,flashCenterRadius)
		x += rd.randint(-flashCenterRadius,flashCenterRadius)
		self.radius = rd.randint(flashRadiusMin, flashRadiusMax)

		physicalObject.PhysicalObject.__init__(self, centerx=x, centery=y, 
			width=self.radius*2, height=self.radius*2)

		self.timeToLive = int((flashMinTimeToLive + 
			rd.random()*(flashMaxTimeToLive-flashMinTimeToLive)
			)*globalvars.FPS)
		self.color = colors.getRandHotColor()
		self.rect.topleft = (x-self.radius, y-self.radius)

	def update(self):
		'''Return true to be removed from intangibles. Return False othewise.'''
		if self.timeToLive <= 0:
			self.kill()
		self.timeToLive -= 1

	def draw(self, offset):
		x,y = self.rect.center
		pos = x - offset[0], y - offset[1]
		pygame.draw.circle(globalvars.screen, self.color, pos, self.radius, 0)


class Debris(physicalObject.PhysicalObject):
	'''TTL is in seconds.
	Speeds are in pixels per second.'''
	def __init__(self, x=0, y=0, minTTL=0.5, maxTTL=1.5, minSpeed=300, maxSpeed=500, minTheta=-179, maxTheta=180):
		physicalObject.PhysicalObject.__init__(self, \
			centerx=x, centery=y, width=4, height=4)
		self.timeToLive = int((minTTL + rd.random()*(maxTTL-minTTL))*globalvars.FPS)
		self.theta = rd.randint(minTheta, maxTheta)
		self.speed = float(rd.randint(minSpeed, maxSpeed))/float(globalvars.FPS)

 	def update(self):
		'''Return true to be removed from intangibles. Return False othewise.'''
		if self.timeToLive <= 0:
			self.kill()
		self.timeToLive -= 1
		self.move()


class Dust(physicalObject.PhysicalObject):
	'''Useful for giving player a sense of motion.'''
	def __init__(self, x=0, y=0, width=2, height=2, image_name=None, color=colors.white):
		physicalObject.PhysicalObject.__init__(self, centerx=x, centery=y,\
						width=width, height=height, \
						image_name=image_name, color=color)
		self.is_a = globalvars.DUST

	def update(self):
		'''For each dust particle,
		If the dust is too far from the player then move it to a location
		offscreen, but in the direction that the player is moving.
		Otherwise, just draw the dust with the update function.'''
		#left, top = offset
		dist = distance(self.rect.center, globalvars.player.rect.center)
		if dist > globalvars.WIDTH:
			magnitude = rd.randint(globalvars.CENTERX, globalvars.WIDTH)
			rotation = rd.randint(-70, 70)
			self.rect.center = translate(globalvars.player.rect.center,\
				rotateAngle(globalvars.player.theta, rotation),\
				magnitude)


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
subrocks['bigrock'] = ('medrock', 4)
subrocks['medrock'] = ('smallrock', 4)
subrocks['smallrock'] = ('debris', 10)
subrocks['gold'] = ('gem',1)
subrocks['silver'] = ('gem', 3)
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
			globalvars.intangibles_bottom.add(temp)
	else:
		for _ in range(count):
			temp = Asteroid(x=centerx, y=centery,
				image_name=new_image)
			globalvars.tangibles.add(temp)
			globalvars.whiskerables.add(temp)


class Asteroid(physicalObject.PhysicalObject):
	'''An object that moves in only one direction, independent of rotation.
	It takes damage from bullets, collides with ships, but does not 
	collide with anything else.
	Speed is in pixels per second.'''
	def __init__(self, x=0, y=0, image_name='', speed_min=50, speed_max=220):
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
		self.speed = float(rd.randint(speed_min, speed_max))/float(globalvars.FPS)

	def update(self):
		'''Return true to be removed. Return False othewise.'''
		#Rotate
		#if self.dtheta != 0: self.turn(self.dtheta) #TODO temporarily remove rotation because it gums up the hit box and causes us to drop frames when there are a lot of objects.
		#Move in a direction independent of rotation
		self.loc = translate(self.loc, self.direction, self.speed)
		self.rect.centerx = self.loc[0]
		self.rect.centery = self.loc[1]

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
	def __init__(self, x=0, y=0, speed_min=50, speed_max=250):
		physicalObject.PhysicalObject.__init__(self, centerx=x, centery=y,
						image_name='gem')
		self.is_a = globalvars.GEM
		#Choose a random rotation
		self.dtheta = float(rd.randint(-30, 30))/float(globalvars.FPS)
		#Choose a random direction. This is different from theta 
		#which will only determine image rotation.
		self.direction = rd.randint(-179, 180)
		#Choose a random speed
		self.speed = float(rd.randint(speed_min, speed_max))/float(globalvars.FPS)
		self.points = 10

	def update(self):
		'''Return true to be removed. Return False othewise.'''
		#Rotate
		self.turn(self.dtheta)
		#Move in a direction independent of rotation
		self.loc = translate(self.loc, \
			self.direction, self.speed)
		self.rect.center = self.loc[0], self.loc[1]

	def handleCollisionWith(self, other_sprite):
		'''React to a collision with other_sprite.'''
		if other_sprite.is_a == globalvars.SHIP:
			#give money to the ship. This might not be the ideal way to do this.
			#Look for the object in globalvars.intangibles_top that has attribute 
			#'points' and add the points to it. This object should 
			#be a displayUtilities.TimeLimitDisplay
			for it in globalvars.intangibles_top:
				if hasattr(it, 'points'):
					it.points += self.points
					break
			announcement = TemporaryText(
				x=self.rect.left, y=self.rect.top, 
				text='+'+str(self.points), color=colors.blue,
				ttl=3.0, fontSize=36, useOffset=True)
			globalvars.intangibles_top.add(announcement)
			self.kill()
		return False


class HealthKit(physicalObject.PhysicalObject):
	'''A motionless body created for testing purposes.'''
	def __init__(self, x=0, y=0):
		physicalObject.PhysicalObject.__init__(self, centerx=x, centery=y,
						image_name='health')
		self.is_a = globalvars.HEALTH
		self.health_amt = 10

	def handleCollisionWith(self, other_sprite):
		'''React to a collision with other_sprite.'''
		if other_sprite.is_a == globalvars.SHIP:
			other_sprite.gainHealth(self.health_amt)
			announcement = TemporaryText(
				x=self.rect.left, y=self.rect.top, 
				text='+'+str(self.health_amt), color=colors.green,
				ttl=3.0, fontSize=36, useOffset=True)
			globalvars.intangibles_top.add(announcement)
			self.kill()
		return False


class HealthBar(physicalObject.PhysicalObject):
	def __init__(self, width=40, height=40):
		physicalObject.PhysicalObject.__init__(self, width=width, height=height)
		self.is_a = globalvars.OTHER
		#To prevent smearing, we need to keep a separate width variable.
		self.new_width = self.rect.width
		self.red_bar = pygame.Surface([self.rect.width, self.rect.height])
		self.red_bar.fill(colors.red)

	def draw(self, offset):
		x,y = self.rect.topleft
		pos = x - offset[0], y - offset[1]

		globalvars.screen.blit(self.red_bar, pos)

		image = pygame.Surface([self.new_width, self.rect.height])
		image.fill(colors.green)
		globalvars.screen.blit(image, pos)



class WarpPortal(physicalObject.PhysicalObject):
	def __init__(self, x=0.0, y=0.0, destinationNode=0, method=None):
		physicalObject.PhysicalObject.__init__(self, centerx=x, centery=y, image_name='warp')
		self.destinationNode = destinationNode
		self.is_a = globalvars.OTHER
		#self.method will almost invariably be set to a call to scenarios.goToInfiniteSpace
		#This is done because if obj_instances imported scenarios then there would be
		#an import loop because scenarios imports from obj_instances.
		#I'm not sure if there is a better way to do this, but it works just fine.
		self.method = method

	def handleCollisionWith(self, other_sprite):
		'''React to a collision with other_sprite.'''
		#If other sprite is playership and this portal is the destination...
		if other_sprite.is_a == globalvars.SHIP and other_sprite.isPlayer\
		and globalvars.player.destinationNode == self.destinationNode:
			#Make sure the method is not none.
			if not self.method is None:
				#Call scenarios.goToInfiniteSpace
				self.method(self.destinationNode)
			else:
				print 'WARNING: WarpPortal method set to None. This may have been done in error.'
		return False


class Follower(physicalObject.PhysicalObject):
	def __init__(self, x=0, y=0):
		'''This is the object that invisibly follows the player and the 
		screen centers on it.
		This mechanism was intended to give a sense of speed and direction.'''
		physicalObject.PhysicalObject.__init__(self, centerx=x, centery=y,\
			width=10,height=10)

		self.setColor((155,155,0))
		self.maxSpeed = 300.0/float(globalvars.FPS)
		self.dv = engine.maxSpeed/float(globalvars.FPS*4.0) #acceleration
		#Turn rate:
		self.dtheta = 180./float(globalvars.FPS)

	def update(self):
		#Turn towards target
		self.turnTowards()

		#slow down if near target
		if not self.park():
			#Approach target speed
			self.targetSpeed = self.maxSpeed
			self.approachSpeed()

		self.move()


class FinishBullsEye(physicalObject.PhysicalObject):
	'''Paints a bullseye at the finish line.'''
        def __init__(self, target):
		physicalObject.PhysicalObject.__init__(self, \
			centerx=target[0], \
			centery=target[1],\
			width=100, height=100)
		self.is_a = globalvars.OTHER
		self.target = target #A location
		self.dtt = 0.0 #Distance to target
		self.update() #Set dtt
		self.finish_reached = False
		#Whether to offset this object's location based on the camera.
		#Text does not useOffset because we want to only position it relative to 0,0
		self.useOffset = True

	def update(self):
		''' '''
		#Distance to target
		self.dtt = distance(globalvars.player.rect.center, self.target)

	def draw(self, offset):
		#Draw a bulls eye (multiple overlapping red and white 
		#circles centered at the destination point.
		target = (self.target[0] - offset[0], self.target[1] - offset[1])
		pygame.draw.circle(globalvars.screen, colors.red, target, 50, 0)
		pygame.draw.circle(globalvars.screen, colors.white, target, 40, 0)
		pygame.draw.circle(globalvars.screen, colors.red, target, 30, 0)
		pygame.draw.circle(globalvars.screen, colors.white, target, 20, 0)
		pygame.draw.circle(globalvars.screen, colors.red, target, 10, 0)

		if self.finish_reached: return True

		#Check if the player has reached the destination.
		if self.dtt < 40:
			#If so, end the race.
			self.finish_reached = True
			writeTextToScreen(string='TIME TRIAL COMPLETED',\
				fontSize=64,pos=(globalvars.WIDTH/3, globalvars.HEIGHT/2))
			pygame.display.flip()
			sleep(2) #Sleep for 2 seconds.


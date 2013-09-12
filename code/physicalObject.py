import pygame
import math
import game

def centerAtLocWithDimensions(to_move, loc, width, height):
	'''Move the given image so that it is centered at the given location.'''
	x,y = loc
	to_move.move(x - width/2, y - height/2)



class PhysicalObject(pygame.sprite.Sprite):
	def __init__(self, top, left, width, height):

		#Sprite tutorial being used is here:
		# http://kai.vm.bytemark.co.uk/~piman/writing/sprite-tutorial.shtml
		#Sprite class:
		# http://pygame.org/docs/ref/sprite.html
		pygame.sprite.Sprite.__init__(self)
		#There is nothing particularly special about any of the following default values.

		#speed. All speeds will be in pixels per second.
		self.speed = 0.0
		self.targetSpeed = 0.0
		self.maxSpeed = 5.0
		#Acceleration in pixels per second squared. 
		#Each second the speed goes up by this amount.
		self.dv = 1.0

		#Rotation. All rotations are in degrees
		self.theta = 0.0
		self.dtheta = 3.0
		self.ddtheta = 1.0
		self.maxdtheta = 9.0

		self.acceptableError = 0.5 #you can be within this many degrees of the target

		self.destination = (0.0, 0.0)

		self.image = pygame.Surface([width, height])
	        self.image.fill((100,255,100)) #Randomly chosen default color
		self.base_image = self.image

		self.rect = self.image.get_rect()

		self.rect.topleft = (left, top)

	def updateImageAngle(self):
		#Update display. Specifically, the angle of the ship.
		#START: copied from stardog spaceship.py in draw function
		#prew = self.image.get_width()
		#preh = self.image.get_height()
		#print 'before:'
		#print self.image.get_width()
		#print self.image.get_height()
		self.image = pygame.transform.rotate(self.base_image, -self.theta).convert_alpha()

		#print 'after:'
		#print self.image.get_width()
		#print self.image.get_height()

		#Move slightly to account for the padding from rotation
		#self.rect = self.rect.move(prew - self.image.get_width(), preh - self.image.get_height())

		#I tried the following instead under the hypothesis that just re-centering the image on the player's location rather then calculating offset would get rid of the wobble, but this doesn't seem to be any better.
		centerAtLocWithDimensions(self.rect, self.getCenter(), self.image.get_width(), self.image.get_height())

		#The following is definitely worse than the previous, but it's still not perfect.
		#self.rect = self.rect.move(self.image.get_width()-prew, self.image.get_height()-preh)

		#imageOffset compensates for the extra padding from the rotation.
		#imageOffset = [- self.image.get_width() / 2,\
		#		- self.image.get_height() / 2]
		#print imageOffset
		#self.rect = self.rect.move(imageOffset[0], imageOffset[1])
		#offset is where on the input surface to blit the ship.
		#if offset:
		#	pos =[self.x  - offset[0] + pos[0] + imageOffset[0], \
		#		self.y  - offset[1] + pos[1] + imageOffset[1]]

		#draw to buffer:
		#surface.blit(self.image, pos)

		#draw to input surface:
		#pos[0] += - imageOffset[0] - self.radius
		#pos[1] += - imageOffset[1] - self.radius
		#surface.blit(buffer, pos) 
		#END: copied from stardog spaceship.py in draw function

	def getCenter(self):
		return self.rect.center

	def getX(self):
		return self.rect.centerx

	def getY(self):
		return self.rect.centery

	def noClipWith(self,other):
		'''Everything defaults to clipping.'''
		return False

	def setColor(self, color):
	        self.image.fill(color)

	def turnShallower(self):
		#Ease out of the turn
		if self.dtheta > 0:
			self.dtheta -= self.ddtheta
		else:
			self.dtheta += self.ddtheta

	def turnSharper(self, clockwise=True):
		#Increase the amount of turn in the desired direction
		if clockwise:
			self.dtheta = max(self.dtheta - self.ddtheta, -self.maxdtheta)
		else:
			self.dtheta = min(self.dtheta + self.ddtheta, self.maxdtheta)

	def turnCounterClockwise(self, delta=None):
		'''Turn in the desired direction.
		I'm using an angle system like stardog uses such that 
		east=0, north=-90, west=180, south=90'''
		if delta is None: delta = self.dtheta
		self.theta -= delta
		if self.theta < -180: self.theta += 360
		self.updateImageAngle()

	def turnClockwise(self, delta=None):
		'''Turn in the desired direction
		I'm using an angle system like stardog uses such that 
		east=0, north=-90, west=180, south=90'''
		if delta is None: delta = self.dtheta
		self.theta += delta
		if self.theta > 180: self.theta -= 360
		self.updateImageAngle()

	def turn(self, delta):
		'''I'm using an angle system like stardog uses such that 
		east=0, north=-90, west=180, south=90'''
		self.theta += delta
		if self.theta > 180: self.theta -= 360
		elif self.theta < -180: self.theta += 360
		self.updateImageAngle()

	def park(self):
		'''Slow to a stop near target destination.'''
		itersToStop = self.speed / self.dv
		if not self.speed == 0 and \
		itersToStop >= self.distanceToDestination() / self.speed:
			self.decelerate()
			self.targetSpeed = self.speed
			return True
		return False

	def approachSpeed(self):
		'''Modify this object's speed to approach the 
		goal speed (aka targetSpeed).'''
		if abs(self.speed - self.targetSpeed) < self.dv:
			self.speed = self.targetSpeed
		elif self.speed < self.targetSpeed:
				self.accelerate()
		else:
			self.decelerate()

	def accelerate(self):
		self.speed = min(self.maxSpeed, self.speed + self.dv)

	def decelerate(self):
		self.speed = max(0, self.speed - self.dv)

	def distanceToDestination(self):
		x,y = self.destination
		return math.sqrt( (self.rect.centerx-x)**2 + (self.rect.centery-y)**2 )

	def setDestination(self,point):
		'''Pre: point must be a tuple of integers or floats.'''
		self.destination = point

	def killDestination(self):
		self.destination = None

	def getShorterTurnDirection(self, target_angle):
		'''Given a target angle, calculate the shorter direction to turn 
		and how many degrees to turn in that direction.
		Figuring out how to calculate this was a little tricky for me.
		Drawing helped. The idea is that there are two different
		distances between points when those points are on a ring.
		True = clockwise
		False = counterclockwise
		'''
		a = self.theta
		b = target_angle
		self_is_a = True
		if b < a: #Ensure that a is the smaller of the two values.
			a = target_angle
			b = self.theta
			self_is_a = False
		dist1 = b-a
		dist2 = (a+180)+(180-b) #a+180 is actually a - -180
		if dist1 < dist2:
			if self_is_a:
				return True
			else:
				return False
		else:
			if self_is_a:
				return False
			else:
				return True

	def getAngleToTarget(self):
		'''This is a major departure from the old implementation. 
		THIS will pretend that up is positive Y values and down is 
		negative Y values as is standard in math, but not computer 
		science.
		SHIT. It's still not working. I haven't wrapped my head around why.'''
		x,y = self.destination
		rise = y - self.rect.centery
		run = x - self.rect.centerx
		#As I understand it, this ought to return one angle to the target,
		#though not necessarily the shortest angle.
		#Range of arctan is negative pi to pi and the world is upside down
		#because down is positive in the y direction.
		#See testAngleToTarget.py in backups for some examples.
		angle_to_target = math.degrees(math.atan2(rise, run)) - self.theta
		if angle_to_target < -180: angle_to_target += 360
		if angle_to_target > 180: angle_to_target -= 360
		return angle_to_target

	def turnTowards(self, angleOffset = 0):
		"""This was copied out of scripts.py in stardog and modified slightly. """
		angleToTarget = self.getAngleToTarget()
		#turnClockwise = self.getShorterTurnDirection(self, target_angle)
		#print angleToTarget
		if abs(angleToTarget) > self.acceptableError:
			#Get the amount to turn. It may be less than the total amount we can turn.
			if abs(angleToTarget) < self.dtheta:
				self.turn(angleToTarget)
			elif angleToTarget < 0:
				self.turnCounterClockwise()
			else:
				self.turnClockwise()


	def move(self):
		#Get new vector
		vectx = math.cos(math.radians(self.theta))
		vecty = math.sin(math.radians(self.theta))

		self.rect = self.rect.move(vectx*self.speed, vecty*self.speed)


	def draw(self, offset=(0,0)):
		pos = self.rect.centerx - offset[0], self.rect.centery - offset[1]
		game.screen.blit(self.image, pos)

	def drawAt(self, position=(0,0)):
		pos = position[0] - self.rect.width/2, position[1] - self.rect.height/2
		game.screen.blit(self.image, pos)

		#TODO TESTING
		#Draw an extra little image at top left and bottom left of this image
		#image = pygame.Surface([5,5])
	        #image.fill((200,100,100))
		#x1, y1 = position
		#x2, y2 = self.rect.topleft
		#game.screen.blit(image, (x1-x2, y1-y2))




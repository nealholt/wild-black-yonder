import pygame
import math
import game

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
		#Acceleration in pixels per second squared. So each second the speed goes up by this amount.
		self.dv = 1.0

		#Rotation. All rotations are in degrees
		self.theta = 0.0
		self.dtheta = 3.0
		self.ddtheta = 1.0
		self.maxdtheta = 9.0

		self.acceptableError = 2.0 #you can be within this many degrees of the target

		#Destination
		self.destx = 0.0
		self.desty = 0.0

		self.image = pygame.Surface([width, height])
	        self.image.fill((100,255,100)) #Random default color

		self.rect = self.image.get_rect()

		self.rect.topleft = (left, top)


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

	def turnCounterClockwise(self):
		#Turn in the desired direction
		self.theta = (self.theta + self.dtheta) % 360

	def turnClockwise(self):
		#Turn in the desired direction
		self.theta = self.theta - self.dtheta
		if self.theta < 0:
			self.theta += 360

	def park(self):
		'''Slow to a stop near target destination.'''
		itersToStop = self.speed / self.dv
		if not self.speed == 0 and itersToStop >= self.distanceTo(self.destx,self.desty) / self.speed:
			self.decelerate()
			self.targetSpeed = self.speed
			return True
		return False

	def approachSpeed(self):
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

	def distanceTo(self, x,y):
		return math.sqrt( (self.rect.centerx-x)**2 + (self.rect.centery-y)**2 )

	def setDestination(self,x,y):
		self.destx = x
		self.desty = y

	def getAngleToTarget(self):
		'''This is a major departure from the old implementation. 
		THIS will pretend that up is positive Y values and down is 
		negative Y values as is standard in math, but not computer 
		science.
		SHIT. It's still not working. I haven't wrapped my head around why.'''
		rise = self.desty - self.rect.centery
		run = self.destx - self.rect.centerx
		#As I understand it, this ought to return one angle to the target,
		#though not necessarily the shortest angle.
		#Range of arctan is negative pi to pi and the world is upside down
		#because down is positive in the y direction.
		#See testAngleToTarget.py in backups for some examples.
		return math.degrees(math.atan2(rise, run)) - self.theta

	def turnTowards(self, angleOffset = 0):
		"""This was copied out of scripts.py in stardog and modified slightly. """
		angleToTarget = (self.getAngleToTarget() + 180) % 360

		if not (-self.acceptableError < (angleToTarget-self.theta) < self.acceptableError):
			#old way start
			if angleToTarget > 180:
		#If outside an acceptable accuracy, turn more towards the target.
		#if abs(angleToTarget) > self.acceptableError:
		#	if angleToTarget > 0:
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
		game.screen.blit(self.image, position)


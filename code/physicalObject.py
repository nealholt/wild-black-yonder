import pygame
import math

class PhysicalObject:
	def __init__(self, game, top, left, width, height):
		#There is nothing particularly special about any of the following default values.

		#update move every tenth of a second and no sooner.
		#This means that all speeds will be in pixels per tenth of a
		#second unless modified. They will be modified here.
		self.interval = 0.1
		self.lastUpdate = pygame.time.get_ticks()

		#speed. All speeds will be in pixels per second.
		self.speed = 0.0
		self.maxSpeed = 50.0 * self.interval
		#Acceleration in pixels per second squared. So each second the speed goes up by this amount.
		self.dv = 1.0 * self.interval

		#Rotation. All rotations are in degrees
		self.theta = 0.0
		self.dtheta = 30.0 * self.interval #rotation per second #TODO TESTING. fixing this value for now for testing.
		self.ddtheta = 10.0 * self.interval #change in rotation per second squared
		self.maxdtheta = 90.0 * self.interval

		self.acceptableError = 2.0 #you can be within this many degrees of the target

		#Destination
		self.destx = 500.0
		self.desty = 100.0

		self.game = game

		self.color = (100,255,100)
		self.rect = pygame.Rect(left, top, width, height)


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
		#self.theta = (self.theta + min(self.dtheta,atMost)) % 360 #TODO TESTING. This failed to solve the problem where atmost was the angle to the target passed as an argument.
		self.theta = (self.theta + self.dtheta) % 360

	def turnClockwise(self):
		#Turn in the desired direction
		#self.theta = self.theta - min(self.dtheta,atMost) #TODO TESTING. This failed to solve the problem where atmost was the angle to the target passed as an argument.
		self.theta = self.theta - self.dtheta
		if self.theta < 0:
			self.theta += 360

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
		rise = self.desty - self.rect.centery
		run = self.destx - self.rect.centerx
		#As I understand it, this ought to return one angle to the target, though not necessarily the shortest angle.
		#Range of arctan is negative pi to pi and the world is upside down because down is positive in the y direction.
		#return math.degrees(math.atan2(rise, run))
		#TODO TESTING
		angleToTarget = math.degrees(math.atan2(rise, run)) - self.theta
		#print angleToTarget
		return (angleToTarget + 180) % 360

	#TODO this needs simplified. Turn towards should be separate from turn sharper or shallower.
	def turnTowards(self, angleOffset = 0):
		"""This was copied out of scripts.py in stardog and modified slightly. """
		angleToTarget = self.getAngleToTarget()

		#print 'to target '+str(angleToTarget)+'. curretn angle '+str(self.theta)

		#convert my angle to the range -180 to 180
		#myangle = self.theta
		#if myangle > 180:
		#	myangle = 360 - myangle
		#preDirection = self.theta

		#Ease out of the turn gradually so as not to overshoot
		#TODO TESTING. Cut out for simplicity.
		#turnMore = True
		#if abs(angleToTarget-180) < abs(self.dtheta):
		#	self.turnShallower()
		#	turnMore = False

		#If outside an acceptable accuracy, turn more towards the target.
		#old way: if not (-self.acceptableError < (angleToTarget-180) < self.acceptableError):
		if not (-self.acceptableError < (angleToTarget-self.theta) < self.acceptableError):
			#old way start
			if angleToTarget > 180:
				#if turnMore: self.turnSharper(False) #TODO TESTING
				self.turnCounterClockwise()
			else:
				#if turnMore: self.turnSharper(True) #TODO TESTING
				self.turnClockwise()
			#old way end

			#diff = abs(angleToTarget - myangle)
			#if angleToTarget < myangle:
			#	if diff < 180 - diff:
			#		self.turnClockwise()
			#	else:
			#		self.turnCounterClockwise()
			#else:
			#	if diff < 180 - diff:
			#		self.turnCounterClockwise()
			#	else:
			#		self.turnClockwise()



		#postAngle = self.getAngleToTarget()
		#if angleToTarget < postAngle:
		#	print 'Pre: '+str(angleToTarget)+'. Post: '+str(postAngle)
		#	#print 'Old theta: '+str(preDirection)+'. New theta: '+str(self.theta) #TODO TESTING
		#	#Undo the turn
		#	self.theta = preDirection
		#Even this doesn't work!


	def move(self):
		#check if the object is due for an update
		if pygame.time.get_ticks() < self.lastUpdate + self.interval:
			return True
		self.lastUpdate += self.interval

		#Get new vector
		vectx = math.cos(math.radians(self.theta))
		vecty = math.sin(math.radians(self.theta))

		self.rect = self.rect.move(vectx*self.speed, vecty*self.speed)


	def draw(self):
		pygame.draw.rect(self.game.screen, self.color, self.rect)


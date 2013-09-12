import pygame
import math


def clamp(x,a,b):
	return min(max(x,a),b)


def dist(x1,y1, x2,y2):
	return math.sqrt( (x1-x2)**2 + (y1-y2)**2 )


def dotProduct(x1,y1, x2,y2):
	return x1*x2 + y1*y2




class Player:
	def __init__(self, game):

		#update move every tenth of a second and no sooner.
		#This means that all speeds will be in pixels per tenth of a
		#second unless modified. They will be modified here.
		self.interval = 0.1
		self.lastUpdate = pygame.time.get_ticks()

		#speed. All speeds will be in pixels per second.
		self.speed = 0.0
		self.maxSpeed = 25.0 * self.interval
		#Acceleration in pixels per second squared. So each second the speed goes up by this amount.
		self.dv = 1.0 * self.interval

		#Rotation. All rotations are in degrees
		self.theta = 0.0
		self.dtheta = 0.0 #rotation per second
		self.ddtheta = 10.0 * self.interval #change in rotation per second squared
		self.maxdtheta = 30.0 * self.interval

		self.acceptableError = 5.0 #you can be within this many degrees of the target

		#Destination
		self.destx = 500.0
		self.desty = 100.0

		self.game = game

		self.color = (100,255,100)

		left = 100
		top = 100
		width = 10
		height = 10
		self.rect = pygame.Rect(left, top, width, height)

	def turnSharper(self):
		self.dtheta = min(self.dtheta + self.ddtheta, self.maxdtheta)
		#self.dtheta = self.dtheta + self.ddtheta

	def turnShallower(self):
		self.dtheta = max(0, self.dtheta - self.ddtheta)
		#self.dtheta = self.dtheta - self.ddtheta

	def turnCounterClockwise(self):
		#print 'theta pre '+str(self.theta)
		#self.theta = (self.theta + self.dtheta) % (2*math.pi)
		self.theta = (self.theta + self.dtheta) % 360
		#self.theta = self.theta + self.dtheta
		#print 'theta post '+str(self.theta)+'\nself dtheta '+str(self.dtheta)

	def turnClockwise(self):
		#print 'theta pre '+str(self.theta)
		#self.theta = self.theta - self.dtheta
		#if self.theta < 0:
		#	self.theta += 360
		#self.theta = self.theta - self.dtheta % (2*math.pi)
		self.theta = self.theta - self.dtheta
		if self.theta < 0:
			self.theta += 360
		#print 'theta post '+str(self.theta)+'\nself dtheta '+str(self.dtheta)

	def accelerate(self):
		self.speed = min(self.maxSpeed, self.speed + self.dv)

	def decelerate(self):
		self.speed = max(0, self.speed - self.dv)

	def distanceTo(self, x,y):
		return math.sqrt( (self.rect.centerx-x)**2 + (self.rect.centery-y)**2 )

	def unitVector(self, x,y):
		#vectx = x-self.rect.centerx
		#vecty = y-self.rect.centery

		vectLength = max(1, self.distanceTo(x,y))
	
		#return (float(vectx)/vectLength, float(vecty)/vectLength)
		return (x/vectLength, y/vectLength)

	def setDestination(self,x,y):
		self.destx = x
		self.desty = y

	def turnTowards(self, angleOffset = 0):
		"""This was copied out of scripts.py in stardog. """
		#angleToTarget = atan2(self.desty - self.rect.centery, self.destx - self.rect.centerx) - self.theta
		#angleToTarget = math.degrees(-math.atan2(self.desty - self.rect.centery, self.destx - self.rect.centerx)) - self.theta
		angleToTarget = math.degrees(math.atan2(self.desty - self.rect.centery, self.destx - self.rect.centerx)) - self.theta

		#print 'testing:'+str(math.atan2(self.desty - self.rect.centery, self.destx - self.rect.centerx))

		#print '\nAngle to target: '+str(angleToTarget)

		#angleToTarget = (angleToTarget - angleOffset + 180) % 360 - 180
		angleToTarget = (angleToTarget + 180) % 360

		#print 'testing angle to target:'+str(angleToTarget)

		if angleToTarget > 180:
			self.turnCounterClockwise()
		else:
			self.turnClockwise()
		#if not (-self.acceptableError < angleToTarget < self.acceptableError):
		#	if angleToTarget < 0:
		#		self.turnCounterClockwise()
		#	elif angleToTarget > 0:
		#		self.turnClockwise()
		#return -self.acceptableError < angleToTarget < self.acceptableError

	def move(self):
		#check if the object is due for an update
		if pygame.time.get_ticks() < self.lastUpdate + self.interval:
			return True

		#print '\n'+str(self.destx)+', '+str(self.desty)

		self.lastUpdate += self.interval

		#x = self.rect.centerx
		#y = self.rect.centery
		#First get angle to destination.
		#rise = y - self.desty
		#run = max(x - self.destx, 0.0000001)
		#angle = math.tan(rise/run) #Converted to radians

		#length1 = max(dotProduct(self.destx,self.desty,self.destx,self.desty), 0.0000001)
		#vect1x = self.destx/length1
		#vect1y = self.desty/length1

		#length2 = max(dotProduct(x,y,x,y), 0.0000001)
		#vect2x = x/length2
		#vect2y = y/length2

		#tester = dotProduct(vect1x,vect1y,vect1x,vect1y)
		#if tester != 1:
		#	print 'vect 1 x is wrong length: '+str(tester)
		#	exit()
		#tester = dotProduct(vect2x,vect2y,vect2x,vect2y)
		#if tester != 1:
		#	print 'vect 2 x is wrong length: '+str(tester)
		#	exit()


		#temp = clamp(dotProduct(vect1x,vect1y,vect2x,vect2y), -1.0, 1.0)
		#print temp
		#angle = math.acos(temp)

		#Slow down or speed up rotation
		#if(abs(self.theta - angle) < self.dtheta):
		#	#print 'turn shallower'
		#	self.turnShallower()
		#else:
		#	#print 'turn sharper'
		#	self.turnSharper()
		self.turnSharper()

		self.turnTowards()

		#vectx, vecty = self.unitVector(self.destx+math.cos(self.theta), self.desty+math.sin(self.theta))
		#vectx, vecty = self.unitVector(math.cos(self.theta), math.sin(self.theta))
		vectx = math.cos(math.radians(self.theta))
		vecty = math.sin(math.radians(self.theta))

		#print '\nx: '+str(vectx)+'\ny: '+str(vecty)+'\ncos theta: '+str(math.cos(math.radians(self.theta)))+'\nsin theta: '+str(math.sin(math.radians(self.theta)))+'\ntheta: '+str(self.theta)+'\ntheta radians: '+str(math.radians(self.theta))
		#print '\nx: '+str(vectx)+'\ny: '+str(vecty)+'\ntheta: '+str(self.theta)+'\ntheta radians: '+str(math.radians(self.theta))

		#Change speed
		#Calculate how long it will take to stop.
		#itersToStop = self.speed / self.dv
		#if not self.speed == 0 and itersToStop <= self.distanceTo(self.destx,self.desty) / self.speed:
		#	self.decelerate()
		#else:
		#	self.accelerate()
		self.accelerate()

		self.rect = self.rect.move(vectx*self.speed, vecty*self.speed)

		#print 'move '+str(vectx*self.speed)+', '+str(vecty*self.speed)


	def draw(self):
		pygame.draw.rect(self.game.screen, self.color, self.rect)


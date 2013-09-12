

import physicalObject
import bullet
import profiles
import random as rd
import game

class Ship(physicalObject.PhysicalObject):
	def __init__(self, top=0, left=0, width=20, height=20):

		physicalObject.PhysicalObject.__init__(self, top, left, width, height)

		self.name='default'
		self.weapons=[]
		self.engine=None
		self.health=10
		self.maxhealth=10

		profiles.enemyProfile(self)

		#self.attackAngle determines the number of degrees that is "close enough" for attack.
		self.attackAngle = 10.0


	def update(self, offset):
		#Turn towards target
		self.turnTowards()

		d = self.distanceToDestination()
		#If target is far, increase goal speed.
		if d > 200:
			self.targetSpeed = self.maxSpeed
		#If target is near, decrease goal speed.
		elif d < 120:
			self.targetSpeed = 0
		else:
			self.targetSpeed = self.maxSpeed/2

		#Check for firing solutions
		for w in self.weapons:
			w.maybeShoot(self) 

		#modify speed
		self.approachSpeed()

		#move
		self.move()

		#draw
		self.draw(offset)


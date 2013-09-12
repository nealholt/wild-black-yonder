import physicalObject
import bullet
import profiles
import random as rd
import game

class Enemy(physicalObject.PhysicalObject):
	def __init__(self, top, left):

		width = 20
		height = 20
		physicalObject.PhysicalObject.__init__(self, top, left, width, height)

		profiles.enemyProfile(self)

		#self.attackAngle determines the number of degrees that is "close enough" for attack.
		self.attackAngle = 20.0

	def maybeShoot(self):
		#This works, but fuck me I have no clue why.
		angle = self.getAngleToTarget() % 360
		#print angle
		if abs(360-angle) < self.attackAngle or angle < self.attackAngle:
			#print 'Angle to target: '+str(self.getAngleToTarget())+'  Theta: '+str(self.theta) #TESTING
			tempbullet = bullet.Bullet(self.theta, self.rect.centery, self.rect.centerx, self)
			game.allSprites.add(tempbullet)
			game.enemySprites.add(tempbullet)

	def update(self, offset):
		#Turn towards target
		self.turnTowards()

		#TODO use this hack to control rate of fire for now.
		if rd.random() < 0.15: self.maybeShoot()

		#Approach target speed
		self.approachSpeed()

		self.move()

		self.draw(offset)


import pygame
import physicalObject
import bullet

class Enemy(physicalObject.PhysicalObject):
	def __init__(self, game, top, left):

		width = 20
		height = 20
		physicalObject.PhysicalObject.__init__(self, game, top, left, width, height)
		self.setColor((100,255,255))

		#Go to max speed immediately.
		self.targetSpeed = self.maxSpeed

		#Give enemy reduced max speed relative to player
		self.maxSpeed = 20.0 * self.interval
		self.maxdtheta = 30.0 * self.interval

		#self.attackAngle determines the number of degrees that is "close enough" for attack.
		self.attackAngle = 5.0

	def maybeShoot(self):
		#TODO I still don't trust that this is working correctly.
		if abs(self.getAngleToTarget()-self.theta) < self.attackAngle:
			print 'Angle to target: '+str(self.getAngleToTarget())+'  Theta: '+str(self.theta) #TESTING
			tempbullet = bullet.Bullet(self.game, self.theta, self.rect.centery, self.rect.centerx, self)
			self.game.allSprites.add(tempbullet)
			self.game.enemySprites.add(tempbullet)

	def update(self):
		self.draw()

		#check if the object is due for an update
		if pygame.time.get_ticks() < self.lastUpdate + self.interval:
			return True
		self.lastUpdate += self.interval

		#Turn towards target
		self.turnTowards()

		self.maybeShoot()

		#Approach target speed
		self.approachSpeed()

		self.move()



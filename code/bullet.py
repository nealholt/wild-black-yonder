import pygame
import physicalObject

class Bullet(physicalObject.PhysicalObject):
	def __init__(self, game, direction, top, left, dontClipMe):

		width = 5
		height = 5
		physicalObject.PhysicalObject.__init__(self, game, top, left, width, height)

		self.speed = 100.0 * self.interval
		self.theta = direction
		self.setColor((255,100,100))

		#How long this object will live in intervals
		self.timeToLive = 50


	def update(self):
		if self.timeToLive <= 0:
			self.kill() #http://pygame.org/docs/ref/sprite.html#Sprite.kill
			return True

		self.timeToLive -= 1

		self.draw()

		#check if the object is due for an update
		if pygame.time.get_ticks() < self.lastUpdate + self.interval:
			return True
		self.lastUpdate += self.interval

		self.move()



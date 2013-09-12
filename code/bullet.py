import physicalObject
import profiles

class Bullet(physicalObject.PhysicalObject):
	def __init__(self, direction, top, left, dontClipMe, width=5, height=5):

		physicalObject.PhysicalObject.__init__(self, top, left, width, height)

		self.theta = direction

		#How long this object will live. Unit is... frames?
		self.timeToLive = 50


	def update(self, offset):
		if self.timeToLive <= 0:
			self.kill() #http://pygame.org/docs/ref/sprite.html#Sprite.kill
			return True

		self.timeToLive -= 1

		self.move()

		self.draw(offset)



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

		#Don't clip this thing. Used to prevent bullet from clipping with its own shooter
		self.dontClipMe = dontClipMe


	def update(self):
		if self.timeToLive <= 0:
			self.kill() #http://pygame.org/docs/ref/sprite.html#Sprite.kill
			return True

		self.timeToLive -= 1

		self.move()
		self.draw()

	def noClipWith(self, other):
		return self.dontClipMe == other

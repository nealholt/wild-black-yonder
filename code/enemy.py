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

	def update(self):
		self.draw()


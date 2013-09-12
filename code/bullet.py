import physicalObject

class Bullet:
	def __init__(self, game, direction, top, left):

		self.game = game

		width = 5
		height = 5
		self.po = physicalObject.PhysicalObject(game, top, left, width, height)
		self.po.speed = 100.0 * self.po.interval
		self.po.theta = direction
		self.po.color = (255,100,100)

		#How long this object will live in intervals
		self.timeToLive = 30


	def update(self):
		if self.timeToLive <= 0:
			self.game.triggers.remove(self)
			return True

		self.timeToLive -= 1

		self.po.move()
		self.po.draw()


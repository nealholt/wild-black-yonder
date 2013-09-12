import physicalObject
import profiles
import game
import colors

class HealthBar(physicalObject.PhysicalObject):
	def __init__(self, top, left, width, height, ship=None, vertical=False, current=100, total=100):
		physicalObject.PhysicalObject.__init__(self, top, left, width, height)

		self.ship = ship
		self.vertical = vertical

		#Current and total health or progress or whatever the bar is measuring
		self.health = current
		self.maxHealth = total


	def update(self, offset):
		if self.ship is None:
			x,y = self.rect.topleft
		else:
			x,y = self.ship.getCenter()
		pos = x - offset[0], y - offset[1]

		healthx = pos[0] - self.healthBarWidth/2
		healthy = pos[1] - self.healthBarHeight - self.rect.height/2

		tempRect = pygame.Rect(healthx, healthy, \
			self.healthBarWidth, self.healthBarHeight)
		pygame.draw.rect(game.screen, colors.red, tempRect, 0)

		width = self.health/float(self.maxhealth)*self.healthBarWidth
		tempRect = pygame.Rect(healthx, healthy, width, self.healthBarHeight)
		pygame.draw.rect(game.screen, colors.green, tempRect, 0)

		self.drawAt(pos)



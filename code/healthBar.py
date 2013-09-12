import physicalObject
import pygame
import game
import colors

class HealthBar(physicalObject.PhysicalObject):
	def __init__(self, width=0, height=0, ship=None, vertical=False, current=100, total=100):
		self.ship = ship

		physicalObject.PhysicalObject.__init__(self, top=0, left=0)

		#Boolean for whether to draw the healthbar horizontally or vertically.
		self.vertical = vertical

		#Current and total health or progress or whatever the bar is measuring
		self.health = current
		self.maxHealth = total

		self.healthBarWidth = width
		self.healthBarHeight = height


	def update(self, offset):
		heightAdjust = 0
		if self.ship is None:
			x,y = self.rect.topleft
		else:
			x,y = self.ship.getCenter()
			heightAdjust = self.ship.rect.height
			self.health = self.ship.health
		pos = x - offset[0], y - offset[1]

		healthx = pos[0] - self.healthBarWidth/2
		healthy = pos[1] - self.healthBarHeight - heightAdjust/2

		tempRect = pygame.Rect(healthx, healthy, \
			self.healthBarWidth, self.healthBarHeight)
		pygame.draw.rect(game.screen, colors.red, tempRect, 0)

		width = (self.health/float(self.maxHealth))*self.healthBarWidth
		tempRect = pygame.Rect(healthx, healthy, width, self.healthBarHeight)
		pygame.draw.rect(game.screen, colors.green, tempRect, 0)

		self.drawAt(pos)


	def draw(self):
		pass


import physicalObject
import bullet

class Enemy:
	def __init__(self, game):

		left = 500
		top = 500
		width = 10
		height = 10
		self.po = physicalObject.PhysicalObject(game, top, left, width, height)
		self.po.color = (100,255,255)

		self.game = game


	def shoot(self):
		self.game.triggers.append(bullet.Bullet(self.game, self.po.theta, self.po.rect.centery, self.po.rect.centerx))


	def setDestination(self,x,y):
		self.po.setDestination(x,y)


	def update(self):
		self.po.draw()


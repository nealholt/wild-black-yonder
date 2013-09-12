import physicalObject
import bullet

class Player:
	def __init__(self, game):

		left = 100
		top = 100
		width = 10
		height = 10
		self.po = physicalObject.PhysicalObject(game, top, left, width, height)
		self.po.color = (100,255,100)

		self.game = game


	def shoot(self):
		self.game.triggers.append(bullet.Bullet(self.game, self.po.theta, self.po.rect.centery, self.po.rect.centerx))


	def setDestination(self,x,y):
		self.po.setDestination(x,y)


	def update(self):
		#Turn towards target
		self.po.turnTowards()

		#TODO can you fix this next bit to be a method in po?
		#Change speed
		#Calculate how long it will take to stop.
		itersToStop = self.po.speed / self.po.dv
		if not self.po.speed == 0 and itersToStop >= self.po.distanceTo(self.po.destx,self.po.desty) / self.po.speed:
			self.po.decelerate()
		else:
			self.po.accelerate()

		self.po.move()
		self.po.draw()


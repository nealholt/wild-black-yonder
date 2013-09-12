import physicalObject
import game

class HitBoxTester(physicalObject.PhysicalObject):
	'''Like a bullet, but these hit box testers will fly in from all angles and freeze on the screen where they collide with the player. this will reveal the true hit box so I can start to figure out why it isn't where I expect it to be.'''
	def __init__(self, top=0, left=0, destination=(0,0)):

		physicalObject.PhysicalObject.__init__(self, top, left, width=5, height=5)
		self.destination = destination
		self.theta = self.getAngleToTarget(target=self.destination)
		self.speed = 3
		self.stopped = False
		self.isHitBoxTester = True

	def update(self, offset):
		if not self.stopped:
			self.move()

		self.draw(offset)

	def handleCollisionWith(self, other_sprite):
		self.stopped = True
		died = True
		return died




def hitBoxTest(c):
	#shoot a bunch of hit box testers 
	#in towards the player
	h=HitBoxTester(top=c[1]+50, left=c[0]+50, destination=c)
	game.tangibles.add(h)
	h=HitBoxTester(top=c[1]+50, left=c[0]-50, destination=c)
	game.tangibles.add(h)
	h=HitBoxTester(top=c[1]+50, left=c[0], destination=c)
	game.tangibles.add(h)
	h=HitBoxTester(top=c[1]-50, left=c[0]+50, destination=c)
	game.tangibles.add(h)
	h=HitBoxTester(top=c[1]-50, left=c[0]-50, destination=c)
	game.tangibles.add(h)
	h=HitBoxTester(top=c[1]-50, left=c[0], destination=c)
	game.tangibles.add(h)
	h=HitBoxTester(top=c[1], left=c[0]+50, destination=c)
	game.tangibles.add(h)
	h=HitBoxTester(top=c[1], left=c[0]-50, destination=c)
	game.tangibles.add(h)



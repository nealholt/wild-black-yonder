import physicalObject
import globalvars

class HitBoxTester(physicalObject.PhysicalObject):
	'''Like a bullet, but these hit box testers freeze on the screen where they collide 
	with anything. this will reveal the true hit box of an object.'''
	def __init__(self, top=0, left=0, destination=(0,0)):

		physicalObject.PhysicalObject.__init__(self, top, left, width=5, height=5)
		self.destination = destination
		self.theta = self.getAngleToTarget(target=self.destination)
		self.speed = 3
		self.stopped = False
		self.isHitBoxTester = True

	def update(self):
		if not self.stopped: self.move()

	def handleCollisionWith(self, other_sprite):
		self.stopped = True
		died = True
		return died



class HitBoxTestBullet(physicalObject.PhysicalObject):
	'''Like a bullet, but these hit box testers freeze on the screen where they collide 
	with anything. this will reveal the true hit box of an object.'''
	def __init__(self, direction, x, y, dontClipMe, width=5, height=5):
		physicalObject.PhysicalObject.__init__(self, centerx=x, centery=y,\
			width=width, height=height)
		self.theta = direction
		self.dontClipMe = dontClipMe
		self.speed = 3
		self.stopped = False
		self.isHitBoxTester = True

	def update(self):
		if not self.stopped: self.move()

	def handleCollisionWith(self, other_sprite):
		died = False
		if other_sprite != self.dontClipMe:
			self.stopped = True
			died = True
		return died



def hitBoxTest(c, startdist=50):
	'''shoot a bunch of hit box testers 
	in towards the location c
	start from startdist pixels away.'''
	h=HitBoxTester(top=c[1]+startdist, left=c[0]+startdist, destination=c)
	globalvars.tangibles.add(h)
	h=HitBoxTester(top=c[1]+startdist, left=c[0]-startdist, destination=c)
	globalvars.tangibles.add(h)
	h=HitBoxTester(top=c[1]+startdist, left=c[0], destination=c)
	globalvars.tangibles.add(h)
	h=HitBoxTester(top=c[1]-startdist, left=c[0]+startdist, destination=c)
	globalvars.tangibles.add(h)
	h=HitBoxTester(top=c[1]-startdist, left=c[0]-startdist, destination=c)
	globalvars.tangibles.add(h)
	h=HitBoxTester(top=c[1]-startdist, left=c[0], destination=c)
	globalvars.tangibles.add(h)
	h=HitBoxTester(top=c[1], left=c[0]+startdist, destination=c)
	globalvars.tangibles.add(h)
	h=HitBoxTester(top=c[1], left=c[0]-startdist, destination=c)
	globalvars.tangibles.add(h)



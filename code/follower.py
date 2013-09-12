import physicalObject
import profiles

class Follower(physicalObject.PhysicalObject):
	def __init__(self, top, left):

		physicalObject.PhysicalObject.__init__(self, top,left,10,10) #TODO temporarily make visible for testing.

		profiles.followerProfile(self)

	def update(self, offset=(0,0)):
		#Turn towards target
		self.turnTowards()

		#slow down if near target
		if not self.park():
			#Approach target speed
			self.targetSpeed = self.maxSpeed
			self.approachSpeed()

		self.move()
		#self.draw() #TODO temporarily draw for testing purposes.

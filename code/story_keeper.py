import globalvars
import physicalObject


class StoryKeeper(physicalObject.PhysicalObject):
	def __init__(self, name='default'):
		physicalObject.PhysicalObject.__init__(self)
		self.is_a = globalvars.OTHER
		self.progress = 0
		#Only update this object once per second
		self.delay = globalvars.FPS
		self.update_countdown = self.delay

	def update(self):
		self.update_countdown -= 1
		if self.update_countdown < 0:
			self.update_countdown = self.delay
			#Perform update
		pass

	def isOnScreen(self, _):
		return False

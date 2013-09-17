#So far, this is just a stripped down ship object that doesn't move or do anything else.
import physicalObject
import globalvars

class CapitalShip(physicalObject.PhysicalObject):
	def __init__(self, centerx=0, centery=0, image_name='default'):

		#Capital ship uses custom collision dimensions
		#Original dimensions: 990 x 280
		#collisiontopleft is the inset.
		#collisionwidth and collisionheight are the width and height from the inset.
		physicalObject.PhysicalObject.__init__(self, centerx=centerx,\
			centery=centery, image_name=image_name,\
			collisiontopleft=(100,120), collisionwidth=890,  collisionheight=140)

		self.weapons=[]
		self.engine=None

		self.health=50
		self.maxhealth=50

		self.is_a = globalvars.SHIP
		self.isPlayer = False

		#Use rectangular (as opposed to circular) collision detection.
		self.useRectangular = True


	def update(self):
		pass

	def draw(self, offset):
		x,y = self.rect.center
		pos = x - offset[0], y - offset[1]
		self.drawAt(pos)



#So far, this is just a stripped down ship object that doesn't move or do anything else.
import physicalObject
import globalvars
import objInstances

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

	def handleCollisionWith(self, other_sprite):
		''' '''
		died = False
		#Check for collisions with one's own bullets.
		#Don't respond to such collisions.
		if other_sprite.is_a == globalvars.BULLET:
			if other_sprite.dontClipMe == self:
				return died
			else:
				self.health -= 5
		if self.health <= 0: #if capital ship is dead.
			globalvars.intangibles.append(objInstances.Explosion(\
				x=self.rect.centerx,y=self.rect.centery))
			#kill removes the calling sprite from all sprite groups
			self.kill()
			died = True
		return died

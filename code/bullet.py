import physicalObject
import profiles
import game

class Bullet(physicalObject.PhysicalObject):
	def __init__(self, direction, top, left, dontClipMe, width=5, height=5):

		physicalObject.PhysicalObject.__init__(self, top, left, width, height)

		self.theta = direction

		#How long this object will live. Unit is... frames?
		self.timeToLive = 50

		#dontClipMe is almost certainly the shooter of this bullet.
		#This is important because bullets usually start out at a 
		#location that is immediately clipping the shooter but we 
		#don't want ships to blow themselves up.
		self.dontClipMe = dontClipMe

		self.is_a = game.BULLET


	def update(self, offset):
		if self.timeToLive <= 0:
			#kill removes the calling sprite from all sprite groups
			self.kill() #http://pygame.org/docs/ref/sprite.html#Sprite.kill
			return True

		self.timeToLive -= 1

		self.move()

		self.draw(offset)


	def handleCollisionWith(self, other_sprite):
		'''For now bullets die immediately regardless of what they hit.'''
		died = False
		#self.dontClipMe is usually the shooter of the bullet who would 
		#otherwise immediately collide with it.
		#For now, shoot through health packs with no effect.
		if other_sprite != self.dontClipMe and not other_sprite.is_a == game.HEALTH:
			died = True
			#kill removes the calling sprite from all sprite groups
			self.kill()
		return died

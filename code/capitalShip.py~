#So far, this is just a stripped down ship object that doesn't move or do anything else.
import physicalObject
import globalvars
import objInstances
import weapon
from geometry import distance, angleFromPosition

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
		#Load some weapons on the capital ship
		#Initially 3 basic lasers
		self.weapons = [weapon.getWeapon('mk1', self),
				weapon.getWeapon('mk1', self),
				weapon.getWeapon('mk1', self)]
		#Gun locations for the capital ship
		self.myTop = self.rect.topleft[1]+self.collisiontopleft[1]
		self.myLeft = self.rect.topleft[0]+self.collisiontopleft[0]
		self.myBottom = self.rect.topleft[1]+self.collisiontopleft[1]+self.collisionheight
		self.gunlocs = [(self.rect.centerx, self.myTop), #top
			(self.myLeft, self.rect.centery), #left
			(self.rect.centerx, self.myBottom)] #bottom
		#Set the weapon offsets
		self.weapons[0].offset = (0, self.collisionheight/-2) #top
		self.weapons[1].offset = (self.collisionwidth/-2, 0) #left
		self.weapons[2].offset = (0, self.collisionheight/2) #bottom

		self.engine=None

		self.health=50
		self.maxhealth=50

		self.is_a = globalvars.SHIP
		self.isPlayer = False

		#Use rectangular (as opposed to circular) collision detection.
		self.useRectangular = True


	def shoot(self, force_shot=False):
		#Force shot tells this to shoot even if a target 
		#is not obviously in view. NPC's will not take such wild shots.
		#Capital ship initially has 3 guns. one on top, one in front, and one on bottom.

		#Top
		#If weapon is cool, player is above ship and in range, then fire.
		if self.weapons[0].cooldown == 0 and \
		self.destination[1] < self.myTop and \
		distance(self.gunlocs[0], self.destination) < self.weapons[0].weapon_range:
			angle = angleFromPosition(self.gunlocs[0], self.destination)
			self.weapons[0].shoot(angle)
		#Front
		#If weapon is cool, player is in front of ship and in range, then fire.
		if self.weapons[1].cooldown == 0 and \
		self.destination[0] < self.myLeft and \
		distance(self.gunlocs[1], self.destination) < self.weapons[1].weapon_range:
			angle = angleFromPosition(self.gunlocs[1], self.destination)
			self.weapons[1].shoot(angle)
		#Bottom
		#If weapon is cool, player is under ship and in range, then fire.
		if self.weapons[2].cooldown == 0 and \
		self.destination[1] > self.myBottom and \
		distance(self.gunlocs[2], self.destination) < self.weapons[2].weapon_range:
			angle = angleFromPosition(self.gunlocs[2], self.destination)
			self.weapons[2].shoot(angle)


	def cooldown(self):
		'''Cool all our weapons'''
		for w in self.weapons:
			w.cool()

	def update(self):
		#for now we assume that every ship is hostile to the player
		self.setDestination(globalvars.player.rect.center)
		#cooldown all the weapons
		self.cooldown()
		#Check for firing solutions
		self.shoot()

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
				#Spawn explosion at point of impact
				globalvars.intangibles.append(objInstances.Explosion(\
					x=other_sprite.rect.centerx,y=other_sprite.rect.centery))
		if self.health <= 0: #if capital ship is dead.
			globalvars.intangibles.append(objInstances.Explosion(\
				x=self.rect.centerx,y=self.rect.centery,\
				xMinAdj=self.collisionwidth/-2, xMaxAdj=self.collisionwidth/2,\
				yMinAdj=self.collisionheight/-2, yMaxAdj=self.collisionheight/2,\
				ttl=3))
			#kill removes the calling sprite from all sprite groups
			self.kill()
			died = True
		return died


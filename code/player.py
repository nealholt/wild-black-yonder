import pygame
import physicalObject
import bullet
import profiles
import game
import colors

#START: copied from stardog utils.py
#THIS WILL GO HERE FOR TEMPORARY TESTING PURPOSES ONLY
#setup images
#if there is extended image support, load .gifs, otherwise load .bmps.
#.bmps do not support transparency, so there might be black clipping.
if pygame.image.get_extended():
	ext = ".gif"
else:
	ext = ".bmp"

def loadImage(filename, colorkey=colors.black):
	try:
		image = pygame.image.load(filename).convert()
		image.set_colorkey(colorkey)
	except pygame.error:
		image = pygame.image.load("images/default" + ext).convert()
		image.set_colorkey(colors.white)
	return image
#END: copied from stardog utils.py


class Player(physicalObject.PhysicalObject):
	def __init__(self, image_name):

		left = 100
		top = 100
		width = 30
		height = 19
		physicalObject.PhysicalObject.__init__(self, top, left, width, height)

		profiles.playerProfile(self)

		self.health = 100.0
		self.maxHealth = 100.0
		self.healthBarWidth = 20
		self.healthBarHeight = 10

		self.parkAtDestination = False

		#START: copied from stardog floaters.py
		self.base_image = loadImage(image_name + ext)
		#rotate() takes a counter-clockwise angle. 
		#self.image = pygame.transform.rotate(image, -self.dir).convert() #NEAL COMMENTED
		self.image = pygame.transform.rotate(self.base_image, -self.theta).convert() #NEAL ADDED
		#self.image.set_colorkey((0,0,0))
		self.rect = self.image.get_rect()
		#END: copied from stardog floaters.py


	def parkingBrake(self):
		'''Change the truth value of park.'''
		self.parkAtDestination = not self.parkAtDestination

	def shoot(self):
		tempbullet = bullet.Bullet(self.theta, self.rect.centery, self.rect.centerx, self)
		game.allSprites.add(tempbullet)
		game.playerSprites.add(tempbullet)

	def takeDamage(self):
		self.health -= 10

	def isDead(self):
		return self.health <= 0

	def drawHealthBarAt(self, x, y):
		#Draw health bars
		healthx = x-(self.rect.width+self.healthBarWidth)/2
		healthy = y-self.rect.height-self.healthBarHeight

		tempRect = pygame.Rect(healthx, healthy, self.healthBarWidth, self.healthBarHeight)
		pygame.draw.rect(game.screen, colors.red, tempRect, 0)

		width = (self.health/self.maxHealth)*self.healthBarWidth
		tempRect = pygame.Rect(healthx, healthy, width, self.healthBarHeight)
		pygame.draw.rect(game.screen, colors.green, tempRect, 0)


	def update(self, offset=(0,0)):
		if not self.destination is None:
			#Turn towards target
			self.turnTowards()

			if self.parkAtDestination:
				self.park()
			else:
				#Approach target speed
				self.approachSpeed()
		else:
			#Approach target speed
			self.approachSpeed()

		self.move()


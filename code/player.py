import pygame
import physicalObject
import bullet
import profiles
import game

#START: copied from stardog utils.py
#THIS WILL GO HERE FOR TEMPORARY TESTING PURPOSES ONLY
#setup images
#if there is extended image support, load .gifs, otherwise load .bmps.
#.bmps do not support transparency, so there might be black clipping.
if pygame.image.get_extended():
	ext = ".gif"
else:
	ext = ".bmp"

def loadImage(filename, colorkey=(0,0,0)):
	try:
		image = pygame.image.load(filename).convert()
		image.set_colorkey(colorkey)
	except pygame.error:
		image = pygame.image.load("images/default" + ext).convert()
		image.set_colorkey((255,255,255))
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

		#START: copied from stardog floaters.py
		image = loadImage(image_name + ext)
		#rotate() takes a counter-clockwise angle. 
		#self.image = pygame.transform.rotate(image, -self.dir).convert() #NEAL COMMENTED
		self.image = pygame.transform.rotate(image, -self.theta).convert() #NEAL ADDED
		#self.image.set_colorkey((0,0,0))
		self.rect = self.image.get_rect()
		#END: copied from stardog floaters.py


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
		healthx = x-self.rect.width
		healthy = y-self.rect.height-self.healthBarHeight

		tempRect = pygame.Rect(healthx, healthy, self.healthBarWidth, self.healthBarHeight)
		pygame.draw.rect(game.screen, (255,36,0), tempRect, 0) #Color red

		width = (self.health/self.maxHealth)*self.healthBarWidth
		tempRect = pygame.Rect(healthx, healthy, width, self.healthBarHeight)
		pygame.draw.rect(game.screen, (0,64,0), tempRect, 0) #Color green


	def update(self, offset=(0,0)):
		#Turn towards target
		self.turnTowards()

		#Approach target speed
		self.approachSpeed()

		self.move()



import pygame
import physicalObject
import bullet
import profiles
import game

class Player(physicalObject.PhysicalObject):
	def __init__(self):

		left = 100
		top = 100
		width = 10
		height = 10
		physicalObject.PhysicalObject.__init__(self, top, left, width, height)

		profiles.playerProfile(self)

		self.health = 100.0
		self.maxHealth = 100.0
		self.healthBarWidth = 20
		self.healthBarHeight = 10

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



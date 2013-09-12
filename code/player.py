import pygame
import physicalObject
import bullet
import profiles

class Player(physicalObject.PhysicalObject):
	def __init__(self, game):

		left = 100
		top = 100
		width = 10
		height = 10
		physicalObject.PhysicalObject.__init__(self, game, top, left, width, height)

		profiles.playerProfile(self)

		self.health = 100.0
		self.maxHealth = 100.0
		self.healthBarWidth = 20
		self.healthBarHeight = 10

	def shoot(self):
		tempbullet = bullet.Bullet(self.game, self.theta, self.rect.centery, self.rect.centerx, self)
		self.game.allSprites.add(tempbullet)
		self.game.playerSprites.add(tempbullet)

	def takeDamage(self):
		self.health -= 10

	def isDead(self):
		return self.health <= 0

	def update(self):
		#Turn towards target
		self.turnTowards()

		#Approach target speed
		self.approachSpeed()

		self.move()

		self.draw()

		#Draw health bars
		healthx = self.getX()-self.rect.width
		healthy = self.getY()-self.rect.height-self.healthBarHeight

		tempRect = pygame.Rect(healthx, healthy, self.healthBarWidth, self.healthBarHeight)
		pygame.draw.rect(self.game.screen, (255,36,0), tempRect, 0) #Color red

		width = (self.health/self.maxHealth)*self.healthBarWidth
		tempRect = pygame.Rect(healthx, healthy, width, self.healthBarHeight)
		pygame.draw.rect(self.game.screen, (0,64,0), tempRect, 0) #Color green



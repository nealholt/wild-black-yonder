#Major help on this file from:
#http://pygame.org/docs/tut/chimp/ChimpLineByLine.html
# and there is still more to learn from that webpage.
import os, sys
import pygame
from pygame.locals import *


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


class Player:
	def __init__(self, game):
		self.direction = 0 #360 degrees

		self.game = game

		self.image, self.rect = load_image('ship090.jpg')
		self.original,_ = load_image('ship090.jpg')
		#This is a good idea for any image that will be repeatedly blitted.
		#http://www.pygame.org/docs/ref/surface.html#Surface.convert
		self.image = self.image.convert()


	def turnLeft(self):
		#TODO redundant and ugly. Fix it.
		center = self.rect.center
		#Reset image
		if self.direction < 360 and self.direction+15 >= 360:
			self.image = self.original
			self.direction = (self.direction+15) % 360
			self.image = pygame.transform.rotate(self.image, self.direction) #Where 15 is the angle.
		        self.rect = self.image.get_rect(center=center)
		else:
			self.direction = (self.direction+15) % 360
			self.image = pygame.transform.rotate(self.image, 15) #Where 15 is the angle.
		        self.rect = self.image.get_rect(center=center)



	def turnRight(self):
		center = self.rect.center
		self.direction = (self.direction-15) % 360
		self.image = pygame.transform.rotate(self.image, -15) #Where 15 is the angle.
	        self.rect = self.image.get_rect(center=center)

	def draw(self):
		self.game.screen.blit(self.image, self.rect)

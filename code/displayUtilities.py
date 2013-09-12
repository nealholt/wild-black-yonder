import pygame
import game
import colors

#copied from stardog utils.py
#setup images
#if there is extended image support, load .gifs, otherwise load .bmps.
#.bmps do not support transparency, so there might be black clipping.
ext = ".bmp"
if pygame.image.get_extended():
	ext = ".gif"


def loadImage(filename):
	'''copied from stardog utils.py '''
	try:
		image = pygame.image.load(filename).convert()
		#colorkey tells pygame what color to make transparent.
		#We assume that the upper left most pixel's color is the color to make transparent.
		colorkey = image.get_at((0,0))
		image.set_colorkey(colorkey)
	except pygame.error:
		image = pygame.image.load("images/default" + ext).convert()
		image.set_colorkey(colors.white)
	return image


def writeTextToScreen(string='', font_size=12, color=colors.white, pos=(0,0)):
	font = pygame.font.Font(None, font_size)
	text = font.render(string, 1, color)
	textpos = text.get_rect(center=pos)
	game.screen.blit(text, textpos)


def displayShipLoc(ship):
	string = "Player X,Y: "+str(ship.getX())+','+str(ship.getY())+\
		'. Speed: '+str(ship.speed)+'. MaxSpeed: '+str(ship.maxSpeed)
	writeTextToScreen(string=string, font_size=36, color=colors.white, pos=(400,10))



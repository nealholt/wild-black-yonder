import pygame
import colors
import time
from geometry import *
import globalvars
from misc import writeTextToScreen


#copied from stardog utils.py
#setup images
#if there is extended image support, load .gifs, otherwise load .bmps.
#.bmps do not support transparency, so there might be black clipping.
ext = ".bmp"
if pygame.image.get_extended(): ext = ".gif"

def preLoadImage(filename, transparency=True):
	'''copied from stardog utils.py. Heavily modified.
	transparency tells the method whether or not to set a transparent color.'''
	#try:
	image = pygame.image.load(filename).convert()
	if transparency:
		#colorkey tells pygame what color to make transparent.
		#We assume that the upper left most pixel's color is the color to make transparent.
		colorkey = image.get_at((0,0))
		image.set_colorkey(colorkey)
	#except pygame.error as e:
	#	image = pygame.image.load("images/default" + ext).convert()
	#	if transparency:
	#		image.set_colorkey(colors.white)
	return image


#Keep a list of preloaded images
'''In theory, preloading the images and then getting copies of them when needed with the convert() method will be faster and more efficient than loading the image anew each time.
According to 
http://www.pygame.org/docs/ref/image.html
"The returned Surface will contain the same color format, colorkey and alpha transparency as the file it came from. You will often want to call Surface.convert() with no arguments, to create a copy that will draw more quickly on the screen."
I tested this. It is WAAAAY faster.'''
image_list = dict()
image_list['bigrock'] = preLoadImage('images/asteroidBigRoundTidied'+ext) #large asteroid
image_list['medrock'] = preLoadImage('images/asteroidWild2'+ext) #medium asteroid
image_list['smallrock'] = preLoadImage('images/asteroidTempel'+ext) #small asteroid
image_list['gold'] = preLoadImage('images/Sikhote_small'+ext) #gold asteroid
image_list['silver'] = preLoadImage('images/bournonite_30percent'+ext) #silver asteroid
image_list['ship'] = preLoadImage('images/ship'+ext) #smallest ship
image_list['destroyer'] = preLoadImage('images/destroyer'+ext) #small ship
image_list['health'] = preLoadImage('images/health'+ext) #health kit
image_list['gem'] = preLoadImage('images/TyDfN_tiny'+ext) #gem
image_list['bgjupiter'] = preLoadImage('images/ioOverJupiter'+ext, transparency=False) #background jupiter
image_list['bggalaxies'] = preLoadImage('images/galaxyLenses'+ext, transparency=False) #background galaxies
image_list['bigShip'] = preLoadImage('images/bigShip'+ext) #capital ship
image_list['warp'] = preLoadImage('images/warpPortal'+ext) #warp portal



def trunc(f, n):
	'''Truncates/pads a float f to n decimal places without rounding.
	Source: http://stackoverflow.com/questions/783897/truncating-floats-in-python '''
	slen = len('%.*f' % (n, f))
	return str(f)[:slen]


def displayShipLoc(ship):
	#if ship is None: return True
	string = "Player X,Y: "+trunc(ship.rect.centerx, 0)+','+trunc(ship.rect.centery,0)+\
		'. Speed: '+trunc(ship.speed,0)+'. MaxSpeed: '+str(trunc(ship.maxSpeed,0))
	writeTextToScreen(string=string, fontSize=36, color=colors.white, pos=(400,10))


def formatTime(seconds):
	minutes = str(int(seconds/60))
	sec = str(int(seconds%60))
	if len(sec) == 1: sec = '0'+sec
	return minutes+':'+sec


def drawArrowAtTarget(target):
	'''Pre: target is a location (x,y).
	Post: Draws an arrow towards the target.'''
	#Get player's angle to target regardless of current player orientation.
	att = angleFromPosition(globalvars.player.rect.center, target)
	#Get a point radius distance from the player in the 
	#direction of the target, centered on the screen.
	#This will form the tip of the arrow
	tip = translate((globalvars.CENTERX, globalvars.CENTERY), att, globalvars.SCREENRADIUS)
	#Get a point radius-20 distance from the player in the 
	#direction of the target
	#This will be used to build the base of the triangle.
	base = translate((globalvars.CENTERX, globalvars.CENTERY), att, globalvars.SCREENRADIUS-20)
	#get angles + and - 90 degrees from the angle to the target
	leftwing = rotateAngle(att, -90)
	rightwing = rotateAngle(att, 90) 
	#Use these angles and the point closer to the player to 
	#get points for the "wings" of the triangle that forms 
	#the head of the arrow.
	leftwingtip = translate(base, leftwing, 10)
	rightwingtip = translate(base, rightwing, 10)
	#Draw a filled in polygon for the arrow head.
	pygame.draw.polygon(globalvars.screen, colors.yellow, \
		[leftwingtip, tip, rightwingtip])
	#Get a point radius-50 distance from the player in the 
	#direction of the target.
	#This will be used to draw the line part of the arrow.
	linestart = translate((globalvars.CENTERX, globalvars.CENTERY), att, globalvars.SCREENRADIUS-50)
	#Draw a 20 pixel thick line for the body of the arrow.
	pygame.draw.line(globalvars.screen, colors.yellow, linestart, base, 10)




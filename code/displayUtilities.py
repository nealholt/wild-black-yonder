import pygame
import colors
import time
from geometry import *
import globalvars


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


def writeTextToScreen(string='', fontSize=12, color=colors.white, pos=(0,0)):
	'''Returns the rectangle of the given text.'''
	font = pygame.font.Font(None, fontSize)
	text = font.render(string, 1, color)
	textpos = text.get_rect(center=pos)
	globalvars.screen.blit(text, textpos)
	return textpos


class TemporaryText(pygame.sprite.Sprite):
	'''Specify the position of the text, contents, whether or not the
	text should flash and how fast it should do so in seconds, and the 
	time for the text to live in seconds.
	Font size and color can also be specified'''
        def __init__(self, x=0, y=0, text=None, timeOn=0, timeOff=0, ttl=0, fontSize=12, color=colors.white):
		pygame.sprite.Sprite.__init__(self)
		self.is_a = globalvars.OTHER
		font = pygame.font.Font(None, fontSize)
		self.texts = []
		self.positions = []
		maxWidth=0
		maxHeight=0
		leftmost = globalvars.WIDTH
		topmost = globalvars.HEIGHT
		for t in text:
			self.texts.append(font.render(t, 1, color))
			textpos = self.texts[-1].get_rect(center=(x, y+maxHeight))
			self.positions.append(textpos)
			maxWidth = max(textpos.width, maxWidth)
			maxHeight += fontSize
			leftmost = min(textpos.left, leftmost)
			topmost = min(textpos.top, topmost)
		self.rect = pygame.Rect(leftmost, topmost, maxWidth, maxHeight)
		self.timeOn = timeOn * globalvars.FPS
		self.timeOff = timeOff * globalvars.FPS
		self.ttl = ttl * globalvars.FPS
		#Whether to offset this object's location based on the camera.
		#Text does not useOffset because we want to only position it relative to 0,0
		self.useOffset = False
		#Attributes for flashing:
		self.showing = True
		self.countdown = self.timeOn

	def update(self):
		'''Return true to be removed from intangibles. Return False otherwise.'''
		if self.countdown <= 0:
			#Reset countdown and invert showing
			if self.showing:
				self.countdown = self.timeOff
			else:
				self.countdown = self.timeOn
			self.showing = not self.showing
		if self.showing and self.timeOff > 0:
				self.countdown -= 1
		else:
			self.countdown -= 1
		self.ttl -= 1
		return self.ttl <= 0

	def draw(self, _):
		for i in range(len(self.texts)):
			globalvars.screen.blit(self.texts[i], self.positions[i])
		
	def isOnScreen(self, _):
		return self.showing



class ShipStatsText(pygame.sprite.Sprite):
	'''Display ship stats at the top of the screen. '''
        def __init__(self, x=0, y=0, text=None, fontSize=36, color=colors.white):
		pygame.sprite.Sprite.__init__(self)
		self.is_a = globalvars.OTHER
		self.color = color
		self.font = pygame.font.Font(None, fontSize)
		#Whether to offset this object's location based on the camera.
		#Text does not useOffset because we want to only position it relative to 0,0
		self.useOffset = False
		#Create the rect and draw once to properly initialize it.
		self.rect = None
		self.draw((0,0))

	def update(self):
		'''Return true to be removed from intangibles. Return False otherwise.'''
		return False

	def draw(self, _):
		string = 'Player X,Y: '+trunc(globalvars.player.rect.centerx, 0)+\
			','+trunc(globalvars.player.rect.centery,0)+\
			'. Speed: '+trunc(globalvars.player.speed,0)+\
			'. MaxSpeed: '+str(trunc(globalvars.player.maxSpeed,0))
		text = self.font.render(string, 1, self.color)
		self.rect = text.get_rect()
		self.rect.topleft = (250,10)
		globalvars.screen.blit(text, self.rect.topleft)

	def isOnScreen(self, _): return True



class TimerDisplay(pygame.sprite.Sprite):
	'''Counts down time remaining in race.'''
        def __init__(self, target, fontSize=36):
		pygame.sprite.Sprite.__init__(self)
		self.is_a = globalvars.OTHER
		self.font = pygame.font.Font(None, fontSize)
		self.target = target #A location
		#Track time in seconds
		self.start_time = time.time()
		#Whether to offset this object's location based on the camera.
		#Text does not useOffset because we want to only position it relative to 0,0
		self.useOffset = False
		#Create the rect and draw once to properly initialize it.
		self.rect = None
		self.draw((0,0))

	def update(self):
		'''Return true to be removed from intangibles. Return False otherwise.'''
		return False

	def draw(self, _):
		#elapsed time
		elapsed = time.time() - self.start_time
		#Distance to target
		dtt = distance(globalvars.player.rect.center, self.target)
		#Write the elapsed time to the top of the screen.
		string = 'Time: '+formatTime(elapsed)+\
				'. Distance: '+trunc(dtt,0)
		text = self.font.render(string, 1, colors.white)
		self.rect = text.get_rect()
		self.rect.topleft = (250,10)
		globalvars.screen.blit(text, self.rect.topleft)

	def isOnScreen(self, _): return True




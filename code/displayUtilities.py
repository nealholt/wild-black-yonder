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



def loadImage(imagename):
	'''In theory, preloading the images and then getting copies of them when needed with the convert() method will be faster and more efficient than loading the image anew each time.
	According to 
	http://www.pygame.org/docs/ref/image.html
	"The returned Surface will contain the same color format, colorkey and alpha transparency as the file it came from. You will often want to call Surface.convert() with no arguments, to create a copy that will draw more quickly on the screen."
	'''
	return image_list[imagename].convert()


def trunc(f, n):
	'''Truncates/pads a float f to n decimal places without rounding.
	Source: http://stackoverflow.com/questions/783897/truncating-floats-in-python '''
	slen = len('%.*f' % (n, f))
	return str(f)[:slen]


def displayShipLoc(ship):
	#if ship is None: return True
	string = "Player X,Y: "+trunc(ship.rect.centerx, 0)+','+trunc(ship.rect.centery,0)+\
		'. Speed: '+trunc(ship.speed,0)+'. MaxSpeed: '+str(ship.maxSpeed)
	writeTextToScreen(string=string, font_size=36, \
			       color=colors.white, pos=(400,10))


class PlayerInfoDisplayer():
	'''I have a hunch that this is not the best way to do this,
	but it will work for now.
	Displays player information at the top of the screen.'''
        def __init__(self):
		pass

	def update(self, _):
		displayShipLoc(globalvars.player)


def formatTime(seconds):
	minutes = str(int(seconds/60))
	sec = str(int(seconds%60))
	if len(sec) == 1: sec = '0'+sec
	return minutes+':'+sec


class TimeTrialAssistant():
	'''Displays an arrow pointing towards the destination
	and counts down time remaining in race.'''
        def __init__(self, target):
		self.target = target #A location
		self.radius = min(globalvars.WIDTH, globalvars.HEIGHT)/2
		#Track time in seconds
		self.start_time = time.time()
		self.finish_reached = False

	def update(self, offset):
		#Draw a bulls eye (multiple overlapping red and white 
		#circles centered at the destination point.
		target = (self.target[0] - offset[0], self.target[1] - offset[1])
		pygame.draw.circle(globalvars.screen, colors.red, target, 50, 0)
		pygame.draw.circle(globalvars.screen, colors.white, target, 40, 0)
		pygame.draw.circle(globalvars.screen, colors.red, target, 30, 0)
		pygame.draw.circle(globalvars.screen, colors.white, target, 20, 0)
		pygame.draw.circle(globalvars.screen, colors.red, target, 10, 0)

		if self.finish_reached: return True

		#Distance to target
		dtt = distance(globalvars.player.rect.center, self.target)

		#elapsed time
		elapsed = time.time() - self.start_time
		#Write the elapsed time to the top of the screen.
		string = 'Time: '+formatTime(elapsed)+'. Distance: '+trunc(dtt,0)
		writeTextToScreen(string=string, font_size=36,\
				       color=colors.white, pos=(400,10))

		#Only display the guiding arrow if player is too far away to see the target
		if dtt > self.radius:
			#Get player's angle to target regardless of current player orientation.
			att = angleFromPosition(globalvars.player.rect.center, self.target)
			#Get a point radius distance from the player in the 
			#direction of the target, centered on the screen.
			#This will form the tip of the arrow
			tip = translate((globalvars.CENTERX, globalvars.CENTERY), att, self.radius)
			#Get a point radius-20 distance from the player in the 
			#direction of the target
			#This will be used to build the base of the triangle.
			base = translate((globalvars.CENTERX, globalvars.CENTERY), att, self.radius-20)
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
			linestart = translate((globalvars.CENTERX, globalvars.CENTERY), att, self.radius-50)
			#Draw a 20 pixel thick line for the body of the arrow.
			pygame.draw.line(globalvars.screen, colors.yellow, linestart, base, 10)
		#Check if the player has reached the destination.
		if dtt < 40:
			#If so, end the race.
			self.finish_reached = True
			writeTextToScreen(string='TIME TRIAL COMPLETED',\
				font_size=64,pos=(globalvars.WIDTH/3, globalvars.HEIGHT/2))
			pygame.display.flip()
			time.sleep(2) #Sleep for 2 seconds.
		pass


class TimeLimit():
	'''Initially to be used for the gem wild scenario in 
	which the player has a limited amount of time to 
	grab as many gems as possible.'''
        def __init__(self, time_limit=0):
		self.points = 0
		self.time_limit = time_limit #in seconds
		#Track time in seconds
		self.start_time = time.time()
		self.finish_reached = False

	def update(self, offset):
		if self.finish_reached: return True

		#Update elapsed time
		elapsed = time.time() - self.start_time
		#Write the elapsed time to the top of the screen.
		string = 'Time: '+formatTime(elapsed)+\
			' Points:'+str(self.points)
		writeTextToScreen(string=string, font_size=36,\
				       color=colors.white, pos=(400,10))

		#Check to see if time has run out.
		if elapsed >= self.time_limit:
			#If so, end the scenario.
			self.finish_reached = True
			writeTextToScreen(string='GEM WILD COMPLETED',\
				font_size=64,pos=(globalvars.WIDTH/3, globalvars.HEIGHT/2))
			pygame.display.flip()
			time.sleep(2) #Sleep for 2 seconds.
			#Wipe out all the gems:
			for t in globalvars.tangibles:
				if t.is_a == globalvars.GEM: t.kill()
		pass


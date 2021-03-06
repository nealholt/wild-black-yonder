import pygame
import colors
import time
from geometry import *
import globalvars
import sys
sys.path.append('code/cython-'+str(sys.platform)) #Import from a system-specific cython folder
#Because cython files only work on the system they were compiled on.
import cygeometry
import physicalObject
import drawable


def trunc(f, n):
	'''Truncates/pads a float f to n decimal places without rounding.
	Source: http://stackoverflow.com/questions/783897/truncating-floats-in-python '''
	slen = len('%.*f' % (n, f))
	return str(f)[:slen]


def formatTime(seconds):
	minutes = str(int(seconds/60))
	sec = str(int(seconds%60))
	if len(sec) == 1: sec = '0'+sec
	return minutes+':'+sec


def drawArrowAtTarget(target):
	'''Pre: target is a location (x,y).
	Post: Draws an arrow towards the target.
	Returns a rect that encompasses the arrow drawn.'''
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
	polyrect = pygame.draw.polygon(globalvars.screen, colors.yellow, \
		[leftwingtip, tip, rightwingtip])
	#Get a point radius-50 distance from the player in the 
	#direction of the target.
	#This will be used to draw the line part of the arrow.
	linestart = translate((globalvars.CENTERX, globalvars.CENTERY), att, globalvars.SCREENRADIUS-50)
	#Draw a 20 pixel thick line for the body of the arrow.
	linerect = pygame.draw.line(globalvars.screen, colors.yellow, linestart, base, 10)
	#Calculate and return the encompassing rect
	return pygame.Rect(min(polyrect.left, linerect.left),
		min(polyrect.top, linerect.top),
		max(polyrect.right, linerect.right),
		max(polyrect.bottom, linerect.bottom))


def writeTextToScreen(string='', fontSize=12, color=colors.white, pos=(0,0)):
	'''Returns the rectangle of the given text.'''
	font = pygame.font.Font(None, fontSize)
	text = font.render(string, 1, color)
	textpos = text.get_rect(center=pos)
	globalvars.screen.blit(text, textpos)
	return textpos


class TemporaryText(physicalObject.PhysicalObject):
	'''Specify the position of the text, contents, whether or not the
	text should flash and how fast it should do so in seconds, and the 
	time for the text to live in seconds.
	Font size and color can also be specified.'''
        def __init__(self, x=0, y=0, text='', timeOn=1, timeOff=0, ttl=0, fontSize=12, color=colors.white, useOffset=False):
		physicalObject.PhysicalObject.__init__(self)
		self.is_a = globalvars.OTHER
		font = pygame.font.Font(None, fontSize)
		self.text = font.render(text, 1, color)
		self.rect = self.text.get_rect(center=(x, y))
		self.timeOn = timeOn * globalvars.FPS
		self.timeOff = timeOff * globalvars.FPS
		self.ttl = int(ttl * globalvars.FPS)
		#Whether to offset this object's location based on the camera.
		#Text does not typically useOffset because we want to position it relative to 0,0
		#Exceptions include +10 from gems and health pickups.
		self.useOffset = useOffset
		#Attributes for flashing:
		self.showing = True
		self.countdown = self.timeOn

	def update(self):
		''' '''
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
		if self.ttl <= 0: self.kill()

	def draw(self, offset):
		pos = self.rect.topleft
		if self.useOffset:
			pos = pos[0]-offset[0], pos[1]-offset[1]
		globalvars.screen.blit(self.text, pos)
		
	def isOnScreen(self, offset):
		if self.useOffset:
			return self.showing
		else:
			#Call parent's method
			physicalObject.PhysicalObject.isOnScreen(self, offset)


class SpeechBubble(physicalObject.PhysicalObject):
	'''Text is an array of text'''
        def __init__(self, speaker=None, text='', ttl=0, width=0, height=0, fontSize=12, color=colors.black, bgcolor=colors.white):
		physicalObject.PhysicalObject.__init__(self, width=width, height=height)
		self.speaker = speaker
		self.width = width
		self.height = height
		self.is_a = globalvars.OTHER
		font = pygame.font.Font(None, fontSize)
		self.text = font.render(text, 1, color)
		self.ttl = ttl
		self.color = color
		self.bgcolor = bgcolor
		self.drawable_rect = drawable.Rectangle(x1=0, y1=0, width=self.width, height=self.height, color=self.bgcolor, thickness=0)
		self.rect = self.drawable_rect.rect


	def update(self):
		''' '''
		angle = angleFromPosition(self.speaker.rect.center, globalvars.player.rect.center)
		magnitude = 30
		new_point = translate(self.speaker.rect.center, angle, magnitude)
		self.rect = pygame.Rect(new_point[0], new_point[1], self.width, self.height)
		self.ttl -= 1
		if self.ttl < 0: self.kill()


	def draw(self, offset):
		pos = self.rect.topleft[0]-offset[0], self.rect.topleft[1]-offset[1]
		self.drawable_rect.rect = pygame.Rect(pos[0], pos[1], self.width, self.height)
		self.drawable_rect.draw()
		globalvars.screen.blit(self.text, pos)



class ShipStatsText(physicalObject.PhysicalObject):
	'''Display ship stats at the top of the screen. '''
        def __init__(self, x=0, y=0, text=None, fontSize=36, color=colors.white):
		physicalObject.PhysicalObject.__init__(self, color=color)
		self.is_a = globalvars.OTHER
		self.font = pygame.font.Font(None, fontSize)
		#Whether to offset this object's location based on the camera.
		#Text does not useOffset because we want to only position it relative to 0,0
		self.useOffset = False
		#Create draw once to properly initialize the rectangle.
		self.draw((0,0))

	def draw(self, _):
		string = 'Fuel: '+str(globalvars.player.fuel/1000)+\
			'. Speed: '+trunc(globalvars.player.speed,0)+\
			'. MaxSpeed: '+str(trunc(globalvars.player.maxSpeed,0))+\
			'. Player X,Y: '+trunc(globalvars.player.rect.centerx, 0)+','+\
			trunc(globalvars.player.rect.centery,0)
		text = self.font.render(string, 1, self.color)
		self.rect = text.get_rect()
		self.rect.topleft = (150,10)
		globalvars.screen.blit(text, self.rect.topleft)

	def isOnScreen(self, _): return True


class TimerDisplay(physicalObject.PhysicalObject):
	'''Counts down time remaining in race.'''
        def __init__(self, target, fontSize=36):
		physicalObject.PhysicalObject.__init__(self)
		self.is_a = globalvars.OTHER
		self.font = pygame.font.Font(None, fontSize)
		self.target = target #A location
		#Track time in seconds
		self.start_time = time.time()
		#Whether to offset this object's location based on the camera.
		#Text does not useOffset because we want to only position it relative to 0,0
		self.useOffset = False
		#Draw once to properly initialize the rectangle.
		self.draw((0,0))

	def draw(self, _):
		#elapsed time
		elapsed = time.time() - self.start_time
		#Distance to target
		dtt = cygeometry.distance(globalvars.player.rect.center, self.target)
		#Write the elapsed time to the top of the screen.
		string = 'Time: '+formatTime(elapsed)+\
				'. Distance: '+trunc(dtt,0)
		text = self.font.render(string, 1, colors.white)
		self.rect = text.get_rect()
		self.rect.topleft = (250,10)
		globalvars.screen.blit(text, self.rect.topleft)

	def isOnScreen(self, _): return True


class TimeLimitDisplay(physicalObject.PhysicalObject):
	'''Initially to be used for the gem wild scenario in 
	which the player has a limited amount of time to 
	grab as many gems as possible.
	Text is the message to display to the user when the minigame completes.
	points_to_win is the number of points at which the scenario is considered won.
	If time runs out before the amount of points is acquired then the player loses.'''
        def __init__(self, text, time_limit=0, points_to_win=1, fontSize=36, display_points=True, mission=None):
		physicalObject.PhysicalObject.__init__(self)
		self.is_a = globalvars.TIMELIMITDISPLAY
		self.text = text
		self.points_to_win = points_to_win
		self.display_points = display_points
		self.mission = mission
		self.font = pygame.font.Font(None, fontSize)
		self.points = 0
		self.time_limit = time_limit #in seconds
		#Track time in seconds
		self.start_time = time.time()
		#Whether to offset this object's location based on the camera.
		#Text does not useOffset because we want to only position it relative to 0,0
		self.useOffset = False
		#Draw once to properly initialize the rectangle.
		self.draw((0,0))

	def draw(self, _):
		#Update elapsed time
		elapsed = time.time() - self.start_time
		#Write the elapsed time to the top of the screen.
		string = 'Time: '+formatTime(self.time_limit-elapsed)
		if self.display_points:
			string += ' Points:'+str(self.points)
		text = self.font.render(string, 1, colors.white)
		self.rect = text.get_rect()
		self.rect.topleft = (250,10)
		globalvars.screen.blit(text, self.rect.topleft)
		#Check to see if the player won the minigame
		if self.points >= self.points_to_win:
			self.winMission()
		#Check to see if time has run out.
		elif elapsed >= self.time_limit:
			self.loseMission()

	def loseMission(self, suppress_menu=False):
			self.text.append('You lost.')
			self.mission.executeConsequences(self.mission.consequences_fail)
			self.text.append('Results of the mission: '+self.mission.failure_description)
			#Reset mission faction and node to None.
			self.mission.faction = None
			self.mission.node = None
			globalvars.disable_menu = False
			if not suppress_menu:
				#Display completed mission text.
				globalvars.menu.setEndMinigamePanel(self.text)

	def winMission(self):
			self.text.append('You Won!')
			self.mission.executeConsequences(self.mission.consequences_win)
			if self.display_points:
				self.text.append('You acquired '+str(self.points)+' points.')
			self.text.append('Results of the mission: '+self.mission.success_description)
			#Reset mission faction and node to None.
			self.mission.faction = None
			self.mission.node = None
			globalvars.disable_menu = False
			#Display completed mission text.
			globalvars.menu.setEndMinigamePanel(self.text)

	def isOnScreen(self, _): return True


class ArrowToDestination(physicalObject.PhysicalObject):
	'''Paints a yellow arrow pointing to the given target.'''
        def __init__(self, target):
		physicalObject.PhysicalObject.__init__(self)
		self.is_a = globalvars.ARROW
		self.target = target #An object with a rect
		self.dtt = 0.0 #Distance to target
		#Whether to offset this object's location based on the camera.
		#Text does not useOffset because we want to only position it relative to 0,0
		self.useOffset = False
		#Draw once to properly initialize the rectangle.
		self.draw((0,0))

	def update(self):
		''' '''
		#Distance to target
		self.dtt = cygeometry.distance(globalvars.player.rect.center, self.target.rect.center)

	def draw(self, _):
		self.rect = drawArrowAtTarget(self.target.rect.center)

	def isOnScreen(self, _):
		#Only display the guiding arrow if player is too far away to see the target
		return self.dtt > globalvars.SCREENRADIUS


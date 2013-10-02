import pygame
import globalvars
from colors import *

def trunc(f, n):
	'''Truncates/pads a float f to n decimal places without rounding.
	Source: http://stackoverflow.com/questions/783897/truncating-floats-in-python '''
	slen = len('%.*f' % (n, f))
	return str(f)[:slen]

def writeTextToScreen(string='', fontSize=12, color=white, pos=(0,0)):
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
        def __init__(self, x=0, y=0, text=None, timeOn=0, timeOff=0, ttl=0, fontSize=12, color=white):
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
        def __init__(self, x=0, y=0, text=None, fontSize=36, color=white):
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


import pygame.font
import globalvars
from colors import *

def writeTextToScreen(string='', fontSize=12, color=white, pos=(0,0)):
	'''Returns the rectangle of the given text.'''
	font = pygame.font.Font(None, fontSize)
	text = font.render(string, 1, color)
	textpos = text.get_rect(center=pos)
	globalvars.screen.blit(text, textpos)
	return textpos


class TemporaryText():
	'''Specify the position of the text, contents, whether or not the
	text should flash and how fast it should do so in seconds, and the 
	time for the text to live in seconds.
	Font size and color can also be specified'''
        def __init__(self, x=0, y=0, text=None, timeOn=0, timeOff=0, ttl=0, fontSize=12, color=white):
		self.pos = (x,y)
		self.text = text #An array of text to print one on top of the next.
		self.timeOn = timeOn * globalvars.FPS
		self.timeOff = timeOff * globalvars.FPS
		self.ttl = ttl * globalvars.FPS
		self.fontSize = fontSize
		self.color = color
		self.rect = None
		#Attributes for flashing:
		self.showing = True
		self.countdown = self.timeOn

	def update(self):
		'''Return true to be removed from intangibles. Return False othewise.'''
		if self.countdown <= 0:
			#Reset countdown and invert showing
			if self.showing:
				self.countdown = self.timeOff
			else:
				self.countdown = self.timeOn
			self.showing = not self.showing
		if self.showing:
			for i in range(len(self.text)):
				x,y = self.pos
				y += i*self.fontSize
				self.rect = writeTextToScreen(string=self.text[i],\
					fontSize=self.fontSize,\
					color=self.color, pos=(x,y))
			if self.timeOff > 0:
				self.countdown -= 1
		else:
			self.countdown -= 1
		self.ttl -= 1
		return self.ttl <= 0


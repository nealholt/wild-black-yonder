import pygame.font
import globalvars
from colors import *

def writeTextToScreen(string='', fontSize=12, color=white, pos=(0,0)):
	font = pygame.font.Font(None, fontSize)
	text = font.render(string, 1, color)
	textpos = text.get_rect(center=pos)
	globalvars.screen.blit(text, textpos)


class TemporaryText():
	'''Specify the position of the text, contents, whether or not the
	text should flash and how fast it should do so in seconds, and the 
	time for the text to live in seconds.
	Font size and color can also be specified'''
        def __init__(self, x=0, y=0, text='', flashInterval=0, ttl=0, fontSize=12, color=white):
		self.pos = (x,y)
		self.text = text
		self.flashInterval = flashInterval * globalvars.FPS
		self.ttl = ttl * globalvars.FPS
		self.fontSize = fontSize
		self.color = color
		#Attributes for flashing:
		self.showing = True
		self.countdown = self.flashInterval

	def update(self):
		'''Return true to be removed from intangibles. Return False othewise.'''
		if self.countdown <= 0:
			#Reset countdown and invert showing
			self.countdown = self.flashInterval
			self.showing = not self.showing
		if self.showing:
			writeTextToScreen(string=self.text, fontSize=self.fontSize,\
				color=self.color, pos=self.pos)
		if self.flashInterval > 0:
			self.countdown -= 1
		self.ttl -= 1
		return self.ttl <= 0


import pygame
import game
#stardog in menuElements.py has a panel class. Initially, I'll base my panels and menus off that.


class Panel:
	"""Panel(mouse, rect) -> new Panel. 
	The basic building block of the menu system. """
	color = (100, 200, 100)
	image = None
	drawBorder = True
	bgColor = None
	def __init__(self, left=0, top=0, width=0, height=0):
		self.rect = pygame.Rect(left, top, width, height)
		self.panels = []

	def click(self, button, pos):
		"""called when this panel is clicked on."""
		#pass the click on to first colliding child:
		for panel in self.panels:
			if panel.rect.collidepoint(pos):
				if panel.click(button, pos):
					return True

	def handleEvent(self, event):
		if self.rect.collidepoint(event.pos):
			print 'EVENT DETECTED in panel!'
		else:
			print 'outside panel.'

	def draw(self, offset=(0,0)):
		"""draws this panel on the surface."""
		if not self.bgColor is None:
			pygame.draw.rect(game.screen, self.bgColor, self.rect, 0)
		elif self.drawBorder:
			pygame.draw.rect(game.screen, self.color, self.rect, 1)
		elif not self.image is None:
			game.screen.blit(self.image, self.rect.topleft, \
					(0, 0, self.rect.width, self.rect.height))
		for panel in self.panels:
			panel.draw(offset=offset)



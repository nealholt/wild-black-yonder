import drawable
import pygame
import colors
import scenarios
import globalvars

class Panel:
	"""The basic building block of the menu system. """
	def __init__(self):
		self.panels = []
		self.drawables = []
		self.method = None #Invoke this when the panel is clicked on.
		self.alt_color = colors.green #Use this alternate color upon mouseover
		self.use_alt = False

	def addDrawable(self, drawable):
		self.drawables.append(drawable)

	def addPanel(self, panel):
		self.panels.append(panel)

	def highlight(self):
		'''This function is called in response to mouse over events.'''
		self.use_alt = True

	def anySelected(self, pos):
		for d in self.drawables:
			if d.rect.collidepoint(pos):
				return True
		return False

	def handleEvent(self, event):
		if not self.method is None:
			self.use_alt = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				#Not all event types have positions so we check this inside the other guard.
				if self.anySelected(event.pos):
					self.method()
			elif event.type == pygame.MOUSEMOTION:
				#Not all event types have positions so we check this inside the other guard.
				if self.anySelected(event.pos):
					self.highlight()
		#Pass event down to sub panels
		for panel in self.panels:
			panel.handleEvent(event)

	def draw(self):
		"""draws this panel on the surface."""
		for d in self.drawables:
			if self.use_alt:
				d.draw(use_color=self.alt_color)
			else:
				d.draw()
		for panel in self.panels:
			panel.draw()



def getTestingPanel():
	border_padding = 100
	top = border_padding
	left = border_padding
	height = globalvars.HEIGHT-2*border_padding
	width = globalvars.WIDTH-2*border_padding

	menu = Panel()

	#First draw a white frame around the menu.
	temp = drawable.Rectangle(x1=left, y1=top, width=width, height=height, \
		color=colors.white, thickness=3)
	menu.addDrawable(temp)

	#Then draw the background for the menu
	temp = drawable.Rectangle(x1=left, y1=top, width=width, height=height, \
		color=colors.reddishgray)
	menu.addDrawable(temp)

	#Then draw the contents of the menu
	horiz_space = 200
	vert_space = 100
	x1, y1 = horiz_space, globalvars.HEIGHT/2
	radius = 10
	#panel made of a circle centered at start
	subpanel = Panel()
	subpanel.method = scenarios.testScenario00
	temp = drawable.Circle(x1=x1, y1=y1, radius=radius, color=colors.yellow)
	subpanel.addDrawable(temp)
	menu.addPanel(subpanel)

	texts = ['Asteroids', 'Gem Wild', 'Race', 'Furball', 'Infinite space']
	methods = [scenarios.asteroids, scenarios.gemWild, scenarios.race, scenarios.furball, scenarios.infiniteSpace]

	x2 = horiz_space*2
	for i in range(5):
		j = i-2
		y2 = globalvars.HEIGHT/2+vert_space*j

		subpanel = Panel()
		#http://www.secnetix.de/olli/Python/lambda_functions.hawk
		subpanel.method = methods[i]
		temp = drawable.Circle(x1=x2, y1=y2, radius=radius, color=colors.yellow)
		subpanel.addDrawable(temp)
		temp = drawable.Text(x1=(x2+2*radius), y1=y2, string=texts[i],\
			font_size=24, color=colors.white)
		subpanel.addDrawable(temp)
		menu.addPanel(subpanel)

		temp = drawable.Line(x1=x1, y1=y1, x2=x2, y2=y2)
		menu.addDrawable(temp)

	return menu


def getRestartPanel():
	border_padding = 100
	top = border_padding
	left = border_padding
	height = globalvars.HEIGHT-2*border_padding
	width = globalvars.WIDTH-2*border_padding

	menu = Panel()

	#First draw a white frame around the menu.
	temp = drawable.Rectangle(x1=left, y1=top, width=width, height=height, \
		color=colors.white, thickness=3)
	menu.addDrawable(temp)

	#Then draw the background for the menu
	temp = drawable.Rectangle(x1=left, y1=top, width=width, height=height, \
		color=colors.reddishgray)
	menu.addDrawable(temp)

	#Then draw the contents of the menu
	#Display text explaining that player died.
	temp = drawable.Text(x1=globalvars.WIDTH/2-100, y1=200, string='You have died',\
		font_size=24, color=colors.white)
	menu.addDrawable(temp)
	#Display button allowing player to restart.
	subpanel = Panel()
	subpanel.method = scenarios.restart
	temp = drawable.Rectangle(x1=globalvars.WIDTH/2-75, y1=300, width=200, height=50, \
		color=colors.blue)
	subpanel.addDrawable(temp)
	temp = drawable.Text(x1=globalvars.WIDTH/2, y1=340, string='Restart',\
		font_size=32, color=colors.white)
	subpanel.addDrawable(temp)
	menu.addPanel(subpanel)

	return menu



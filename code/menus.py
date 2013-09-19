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
		self.argument = None #This is useful if the method of the panel takes an argument.

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

	def setMethod(self, method):
		self.method = method

	def handleEvent(self, event):
		if not self.method is None:
			self.use_alt = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				#Not all event types have positions so we check this inside the other guard.
				if self.anySelected(event.pos):
					if self.argument is None:
						self.method()
					else:
						self.method(self.argument)
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


#There was a lot of duplicate code so I moved some of it out.
border_padding = 100
top = border_padding
left = border_padding
height = globalvars.HEIGHT-2*border_padding
width = globalvars.WIDTH-2*border_padding
def getStandardMenu():
	'''There was a lot of code duplication so I stuck it in a method all its own.'''
	menu = Panel()

	#First draw a white frame around the menu.
	temp = drawable.Rectangle(x1=left, y1=top, width=width, height=height, \
		color=colors.white, thickness=3)
	menu.addDrawable(temp)

	#Then draw the background for the menu
	temp = drawable.Rectangle(x1=left, y1=top, width=width, height=height, \
		color=colors.reddishgray)
	menu.addDrawable(temp)

	return menu


def getTestingPanel():
	menu = getStandardMenu()

	#Then draw the contents of the menu
	horiz_space = 200
	vert_space = 70
	x1, y1 = horiz_space, globalvars.HEIGHT/2
	radius = 10
	#panel made of a circle centered at start
	subpanel = Panel()
	subpanel.setMethod(scenarios.testScenario00)
	temp = drawable.Circle(x1=x1, y1=y1, radius=radius, color=colors.yellow)
	subpanel.addDrawable(temp)
	menu.addPanel(subpanel)

	texts = ['Asteroids', 'Gem Wild', 'Race', 'Furball', 'Infinite space', 'Capital ship']
	methods = [scenarios.asteroids, scenarios.gemWild, scenarios.race, scenarios.furball, scenarios.infiniteSpace, scenarios.capitalShipScenario]

	x2 = horiz_space*2
	methodLength = len(methods)
	for i in range(methodLength):
		j = i-methodLength/2
		y2 = globalvars.HEIGHT/2+vert_space*j

		subpanel = Panel()
		#http://www.secnetix.de/olli/Python/lambda_functions.hawk
		subpanel.setMethod(methods[i])
		temp = drawable.Circle(x1=x2, y1=y2, radius=radius, color=colors.yellow)
		subpanel.addDrawable(temp)
		temp = drawable.Text(x1=(x2+2*radius), y1=y2, string=texts[i],\
			font_size=24, color=colors.white)
		subpanel.addDrawable(temp)
		menu.addPanel(subpanel)

		temp = drawable.Line(x1=x1, y1=y1, x2=x2, y2=y2)
		menu.addDrawable(temp)

	#Add a "tab" up at the top that switches to weapon selection
	subpanel = Panel()
	temp = drawable.Rectangle(x1=(left+30), y1=(top+5), width=100, height=20, \
		color=colors.yellow, thickness=2)
	subpanel.addDrawable(temp)
	#Add text
	temp = drawable.Text(x1=(left+30+5), y1=(top+5+5), string='Weapons', font_size=24, color=colors.white)
	subpanel.addDrawable(temp)
	#This will be the panel that allows the user to change weapons.
	subpanel.setMethod(setWeaponsPanel)
	menu.addPanel(subpanel)

	return menu


def getGalaxyPanel(localSystem):
	'''Pre: localSystem is a NodeManager object that has been initialized.'''
	menu = getStandardMenu()
	radius = 10
	for n in localSystem.nodes:
		subpanel = Panel()
		temp = drawable.Circle(x1=n.x, y1=n.y, radius=radius, color=colors.yellow)
		subpanel.addDrawable(temp)
		menu.addPanel(subpanel)
	for c in localSystem.connections:
		temp = drawable.Line(x1=c[0], y1=c[1], x2=c[2], y2=c[3])
		menu.addDrawable(temp)
	return menu


def getRestartPanel():
	menu = getStandardMenu()

	#Then draw the contents of the menu
	#Display text explaining that player died.
	temp = drawable.Text(x1=globalvars.WIDTH/2-100, y1=200, string='You have died',\
		font_size=24, color=colors.white)
	menu.addDrawable(temp)
	#Display button allowing player to restart.
	subpanel = Panel()
	subpanel.setMethod(scenarios.restart)
	temp = drawable.Rectangle(x1=globalvars.WIDTH/2-75, y1=300, width=200, height=50, \
		color=colors.blue)
	subpanel.addDrawable(temp)
	temp = drawable.Text(x1=globalvars.WIDTH/2, y1=340, string='Restart',\
		font_size=32, color=colors.white)
	subpanel.addDrawable(temp)
	menu.addPanel(subpanel)

	return menu



weaponsList = ['mk0', 'mk1', 'mk2', 'spread_mk2', 'spread_mk3', 'missile_mk1', 'mine', 'hit_box_test']
def setWeaponsPanel():
	'''Creates the weapon panel and sets the current panel to be the weapon panel.'''
	menu = getStandardMenu()
	#Then draw the contents of the menu
	for i in xrange(len(weaponsList)):
		subpanel = Panel()
		temp = drawable.Text(x1=globalvars.WIDTH/2-100, y1=(40*i+150), \
			string=weaponsList[i], font_size=24, color=colors.white)
		subpanel.addDrawable(temp)
		#The following commented code does not work so I created an argument attribute for the panel object.
		#subpanel.setMethod(lambda: globalvars.player.setWeapon(weaponsList[i]))
		subpanel.setMethod(globalvars.player.setWeapon)
		subpanel.argument = weaponsList[i]
		menu.addPanel(subpanel)
	globalvars.panel = menu


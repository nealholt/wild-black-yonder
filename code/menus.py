class Panel:
	"""The basic building block of the menu system. """
	def __init__(self, rect):
		self.rect = rect
		self.panels = []
		self.drawables = []

	def addDrawable(self, drawable):
		self.drawables.append(drawable)

	def addPanel(self, panel):
		self.panels.append(panel)

	def handleEvent(self, event):
		if self.rect.collidepoint(event.pos):
			print 'EVENT DETECTED in panel!'
		else:
			print 'outside panel.'

	def draw(self):
		"""draws this panel on the surface."""
		for d in self.drawables:
			d.draw()
		for panel in self.panels:
			panel.draw()


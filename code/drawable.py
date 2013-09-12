import pygame
import game
from colors import *

class Drawable:
	def __init__(self, x1=0, y1=0, color=white):
		self.x1, self.y1 = x1, y1
		self.color = color

	def draw(self):
		pass


class Rectangle(Drawable):
	def __init__(self, x1=0, y1=0, width=0, height=0, color=white, thickness=0):
		Drawable.__init__(self, x1=x1, y1=y1, color=color)
		self.width = width
		self.height = height
		self.rect = pygame.Rect(self.x1, self.y1, self.width, self.height)
		self.thickness = thickness

	def draw(self):
		pygame.draw.rect(game.screen, self.color, \
			self.rect, self.thickness)


class Circle(Drawable):
	def __init__(self, x1=0, y1=0, radius=0, color=white):
		Drawable.__init__(self, x1=x1, y1=y1, color=color)
		self.radius = radius

	def draw(self):
		pygame.draw.circle(game.screen, self.color, \
			(self.x1, self.y1), self.radius)


class Line(Drawable):
	def __init__(self, x1=0, y1=0, x2=0, y2=0, color=white):
		Drawable.__init__(self, x1=x1, y1=y1, color=color)
		self.p2 = x2, y2

	def draw(self):
		pygame.draw.line(game.screen, self.color, \
			(self.x1, self.y1), self.p2)

class Text(Drawable):
	def __init__(self, x1=0, y1=0, string='', font_size=12, color=white):
		Drawable.__init__(self, x1=x1, y1=y1, color=color)

		font = pygame.font.Font(None, font_size)
		self.text = font.render(string, 1, self.color)
		self.textpos = self.text.get_rect(center=(self.x1, self.y1))

	def draw(self):
		game.screen.blit(self.text, self.textpos)


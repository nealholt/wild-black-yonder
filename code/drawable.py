import pygame
import game
from colors import *

class Drawable:
	def __init__(self, x1=0, y1=0, color=white):
		self.x1, self.y1 = x1, y1
		self.color = color
		self.rect = None

	def draw(self):
		pass


class Rectangle(Drawable):
	def __init__(self, x1=0, y1=0, width=0, height=0, color=white, thickness=0):
		Drawable.__init__(self, x1=x1, y1=y1, color=color)
		self.width = width
		self.height = height
		self.rect = pygame.Rect(self.x1, self.y1, self.width, self.height)
		self.thickness = thickness

	def draw(self, use_color=None):
		color_to_use = self.color
		if not use_color is None:
			color_to_use = use_color
		pygame.draw.rect(game.screen, color_to_use, \
			self.rect, self.thickness)


class Circle(Drawable):
	def __init__(self, x1=0, y1=0, radius=0, color=white):
		Drawable.__init__(self, x1=x1, y1=y1, color=color)
		self.radius = radius

	def draw(self, use_color=None):
		color_to_use = self.color
		if not use_color is None:
			color_to_use = use_color
		self.rect = pygame.draw.circle(game.screen, color_to_use, \
			(self.x1, self.y1), self.radius)


class Line(Drawable):
	def __init__(self, x1=0, y1=0, x2=0, y2=0, color=white):
		Drawable.__init__(self, x1=x1, y1=y1, color=color)
		self.p2 = x2, y2

	def draw(self, use_color=None):
		color_to_use = self.color
		if not use_color is None:
			color_to_use = use_color
		self.rect = pygame.draw.line(game.screen, color_to_use, \
			(self.x1, self.y1), self.p2)

class Text(Drawable):
	def __init__(self, x1=0, y1=0, string='', font_size=12, color=white):
		Drawable.__init__(self, x1=x1, y1=y1, color=color)
		self.font_size = font_size
		self.string = string

	def draw(self, use_color=None):
		color_to_use = self.color
		if not use_color is None:
			color_to_use = use_color
		font = pygame.font.Font(None, self.font_size)
		text = font.render(self.string, 1, color_to_use)
		self.rect = text.get_rect(center=(self.x1, self.y1))
		self.rect.left += self.rect.width/2 #Shift the text right by half its own width.
		game.screen.blit(text, self.rect)


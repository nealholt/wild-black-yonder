

import pygame
#from pygame.locals import *
import sys
sys.path.append('code')
import game

WIDTH = 900
HEIGHT = 700

black = (0,0,0)

if __name__=="__main__":
	#set up the disply:
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	screen.fill(black)
	game = game.Game(screen)
	game.run()

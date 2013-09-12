

import pygame
#from pygame.locals import *
import sys
sys.path.append('code')
import game

WIDTH = 900
HEIGHT = 700

black = (0,0,0)

if __name__=="__main__":
	print 'Camera options include:\n'+\
	'   python playGame.py -camera 0 #for fixed view\n'+\
	'   python playGame.py -camera 1 #for view centered on player\n'+\
	'   python playGame.py -camera 2 #for view that follows player\n'

	camera_type = 2
	if '-camera' in sys.argv:
		camera_type = int(sys.argv[ sys.argv.index('-camera') + 1 ])
	if camera_type < 0 or camera_type > 2:
		print 'ERROR INVALID camera type. Valid input is 0, 1, or 2. Exiting.'
		exit()
	print 'You chose camera type: '+str(camera_type)

	print 'INSTRUCTIONS: Press space bar to shoot.\nPress escape to quit.\nStarship will move towards the mouse.\n'

	#set up the display:
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	screen.fill(black)
	game = game.Game(screen, camera=camera_type)
	game.run()

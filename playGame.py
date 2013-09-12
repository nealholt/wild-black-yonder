import sys
sys.path.append('code')
import game

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


	print 'FPS can be set with -fps #. For example:\n'+\
	'   python playGame.py -fps 30 #default value\n'
	if '-fps' in sys.argv:
		game.FPS = int(sys.argv[ sys.argv.index('-fps')+1])


	print 'INSTRUCTIONS: Press space bar to shoot.\n'+\
	'Press "/" or "?" to query game state. Currently this just prints the player\'s destination.\n'+\
	'Press escape to quit.\n'+\
	'Press "e" to create an enemy ship that will attack the player.\n'+\
	'Press up arrow to increase player speed by one quarter of max up to max.\n'+\
	'Press down arrow to decrease player speed by one quarter of max down to zero.\n'+\
	'Press left arrow to turn counter-clockwise 30 degrees.\n'+\
	'Press right arrow to turn clockwise 30 degrees.\n'+\
	'Click on the screen to tell the starship to move towards the clicked point.\n'+\
	'Press "p" to slow down and park at destination.\n'+\
	'Press "q" to remove destination and simply fly in current direction.\n'

	game = game.Game(camera=camera_type)
	game.run()

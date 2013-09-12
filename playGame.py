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

	print 'INSTRUCTIONS: Press space bar to shoot.\n'+\
	'Press escape to quit.\n'+\
	'Press "e" to create an enemy ship that will attack the player.\n'+\
	'Starship will move towards the mouse.\n'

	game = game.Game(camera=camera_type)
	game.run()

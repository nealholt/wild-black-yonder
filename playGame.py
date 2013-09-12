import sys
sys.path.append('code')
import game
from scenarios import testScenario00
if __name__=="__main__":
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
	'Press "m" to display a panel. m is for menu in this case. TESTING.\n'+\
	'Press "p" to slow down and park at destination.\n'+\
	'Press "s" to pause/unpause the game.\n'+\
	'Press "q" to remove destination and simply fly in current direction.\n'

	#Initial test scenario
	testScenario00()

	game.game_obj.run()


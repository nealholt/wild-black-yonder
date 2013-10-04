import sys
sys.path.append('code')
import game
from scenarios import testScenario00
if __name__=="__main__":
	print 'FPS can be set with -fps #. For example:\n'+\
	'   python playGame.py -fps 60 #default value\n'
	if '-fps' in sys.argv:
		game.FPS = int(sys.argv[ sys.argv.index('-fps')+1])

	#Initial test scenario
	testScenario00()

	game.run()


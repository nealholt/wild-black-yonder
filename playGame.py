import sys
sys.path.append('code')
import game
if __name__=="__main__":
	print 'Using flip instead of dirty rectangles can be set with -flip. For example:\n'+\
		'   python playGame.py -flip\n'+\
		'The default value is to use dirty.\n'
	if '-flip' in sys.argv:
		game.useDirty = False

	#Send player to node 0 in infinite space
	game.globalvars.scenario_manager.goToInfiniteSpace(0)

	game.run()


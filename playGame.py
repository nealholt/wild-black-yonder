import sys
sys.path.append('code')
import game
if __name__=="__main__":
	print 'Using flip to update the whole display can be set with -flip. For example:\n'+\
		'   python playGame.py -flip\n'+\
 		'Using dirty rectangles to update the display can be set with -dirty. For example:\n'+\
		'   python playGame.py -dirty\n'+\
		'The default value is to use a dynamic combination of both.\n'
	if '-flip' in sys.argv:
		game.update_mechanism = game.FLIP
	if '-dirty' in sys.argv:
		game.update_mechanism = game.DIRTY

	#Send player to node 0 in infinite space
	game.globalvars.scenario_manager.goToInfiniteSpace(0)

	game.run()


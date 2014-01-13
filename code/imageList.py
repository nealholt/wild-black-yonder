import pygame

#copied from stardog utils.py
#setup images
#if there is extended image support, load .gifs, otherwise load .bmps.
#.bmps do not support transparency, so there might be black clipping.
ext = ".bmp"
if pygame.image.get_extended(): ext = ".gif"

def preLoadImage(filename, transparency=True):
	'''copied from stardog utils.py. Heavily modified.
	transparency tells the method whether or not to set a transparent color.'''
	#try:
	image = pygame.image.load(filename).convert()
	if transparency:
		#colorkey tells pygame what color to make transparent.
		#We assume that the upper left most pixel's color is the color to make transparent.
		colorkey = image.get_at((0,0))
		image.set_colorkey(colorkey)
	#except pygame.error as e:
	#	image = pygame.image.load("images/default" + ext).convert()
	#	if transparency:
	#		image.set_colorkey(colors.white)
	return image


#Keep a list of preloaded images
'''In theory, preloading the images and then getting copies of them when needed with the convert() method will be faster and more efficient than loading the image anew each time.
According to 
http://www.pygame.org/docs/ref/image.html
"The returned Surface will contain the same color format, colorkey and alpha transparency as the file it came from. You will often want to call Surface.convert() with no arguments, to create a copy that will draw more quickly on the screen."
I tested this. It is WAAAAY faster.'''
image_list = dict()
image_list['default'] = preLoadImage('images/default'+ext) #A default image used as a placeholder.
image_list['bigrock'] = preLoadImage('images/asteroidBigRoundTidied'+ext) #large asteroid
image_list['medrock'] = preLoadImage('images/asteroidWild2'+ext) #medium asteroid
image_list['smallrock'] = preLoadImage('images/asteroidTempel'+ext) #small asteroid
image_list['gold'] = preLoadImage('images/Sikhote_small'+ext) #gold asteroid
image_list['silver'] = preLoadImage('images/bournonite_30percent'+ext) #silver asteroid
image_list['ship'] = preLoadImage('images/ship'+ext) #smallest ship
image_list['destroyer'] = preLoadImage('images/destroyer'+ext) #small ship
image_list['health'] = preLoadImage('images/health'+ext) #health kit
image_list['gem'] = preLoadImage('images/TyDfN_tiny'+ext) #gem
image_list['bgjupiter'] = preLoadImage('images/ioOverJupiter'+ext, transparency=False) #background jupiter
image_list['bggalaxies'] = preLoadImage('images/galaxyLenses'+ext, transparency=False) #background galaxies
image_list['bigShip'] = preLoadImage('images/bigShip'+ext) #capital ship
image_list['warp'] = preLoadImage('images/warpPortal'+ext) #warp portal
image_list['shipoutline'] = preLoadImage('images/space-ship-sm'+ext) #ship outline
image_list['gas'] = preLoadImage('images/fuel_can'+ext) #gas can
image_list['flag00'] = preLoadImage('images/flag00'+ext, transparency=False) #faction flag
image_list['flag01'] = preLoadImage('images/flag01'+ext, transparency=False) #faction flag
image_list['flag02'] = preLoadImage('images/flag02'+ext, transparency=False) #faction flag
image_list['planet'] = preLoadImage('images/titan-lakes-full-131023'+ext) #planet for resource trading


DEBUG = True

FPS = 30 #frames per second

WIDTH = 900
HEIGHT = 700

CENTERX = WIDTH / 2
CENTERY = HEIGHT / 2

#Used by physicalObject to define what each physicalObject is.
BULLET = 0
OTHER = 1
SHIP = 2
FIXEDBODY = 3
HEALTH = 4
ASTEROID = 5

#The least distance to check for a collision. Might need adjusted if we start using really big objects.
MINSAFEDIST = 1024

BGCOLOR = (0,0,0) #Black. I would have imported colors but I want globalvars to import absolutely nothing so there are no loops in the graph of my imports.
BGIMAGE = None

#instantiate sprite groups
tangibles = None
intangibles = None
#This last group will contain any sprites that will tickle whiskers
whiskerables = None
#An array of fixed-location, white specks designed to reveal player motion by their relative movement.
dust = []

#set up the display:
screen = None
#Player must be created before scenario is called.
player = None

#An object that displays scenario-specific hud stuff.
hud_helper = None

#If arena is set to anything other than zero, then the player will be forced to stay inside the arena and all other objects will also be pointed roughly in the direction of the center of the arena. This is used for 
arena = 0

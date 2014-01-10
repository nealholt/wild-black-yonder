DEBUG = True

FPS = 60 #frames per second

NUMBEROFNODES = 200

WIDTH = 900
HEIGHT = 700

CENTERX = WIDTH / 2
CENTERY = HEIGHT / 2
#Radius of a circle that just barely fits inside the screen:
SCREENRADIUS = min(WIDTH, HEIGHT)/2

MENU_BORDER_PADDING = 50
MENU_PADDING = 25

#Used by physicalObject to define what each physicalObject is.
temp = 0
BULLET = temp; temp+=1
OTHER = temp; temp+=1
SHIP = temp; temp+=1
CAPITALSHIP = temp; temp+=1
FIXEDBODY = temp; temp+=1
HEALTH = temp; temp+=1
ASTEROID = temp; temp+=1
GEM = temp; temp+=1
DUST = temp; temp+=1
ARROW = temp; temp+=1
TRADEGOOD = temp; temp+=1
TIMELIMITDISPLAY = temp; temp+=1

#The least distance to check for a collision. Might need adjusted if we start using really big objects.
MINSAFEDIST = 1024

BGCOLOR = (0,0,0) #Black. I would have imported colors but I want globalvars to import absolutely nothing so there are no loops in the graph of my imports.
BGIMAGE = None

#instantiate sprite groups
tangibles = None
intangibles_bottom = None #Display beneath all other things
intangibles_top = None #Display above all other things
#This last group will contain any sprites that will tickle whiskers. NPCs have whiskers for collision avoidance.
whiskerables = None

#set up the display:
screen = None
#Player must be created before scenario is called.
player = None

#If arena is set to anything other than zero, then the player will be forced to stay inside the arena and all other objects will also be pointed roughly in the direction of the center of the arena. This is used for 
arena = 0

#Display menus and the like on the panel.
menu = None

#How many seconds to continue displaying while the player is dead before kicking him back to the restart menu.
deathcountdown = 3 * FPS

#Local system of nodes
galaxy = None

#List of all the factions and object to manage them:
factions = None

#Track score and time limit in minigames
score_keeper = None

scenario_manager = None

mission_manager = None

#Store indices of node attributes so you can refer to them more easily.
temp = 0
node_debris_index = temp; temp+=1
node_wealth_index = temp; temp+=1
node_production_index = temp; temp+=1
#Store indices of faction attributes so you can refer to them more easily.
temp = 0
faction_relationship_index = temp; temp+=1
faction_weapon_tech_index = temp; temp+=1
faction_missile_tech_index = temp; temp+=1
faction_mine_tech_index = temp; temp+=1
faction_ship_tech_index = temp; temp+=1
faction_engine_tech_index = temp; temp+=1

#Set to true in order to disable any menu access except for pause.
disable_menu = False

#There will be two sprite groups into which ships go. Ships in separate groups will be enemies.
RED_TEAM = None
BLUE_TEAM = None
REDTEAM = 0
BLUETEAM = 1

story_keeper = None

#The following are for gathering efficiency data
time_lapses = None
dirty_rect_size = None


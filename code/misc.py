import pygame.font
import globalvars
from colors import *

def writeTextToScreen(string='', font_size=12, color=white, pos=(0,0)):
	global screen
	font = pygame.font.Font(None, font_size)
	text = font.render(string, 1, color)
	textpos = text.get_rect(center=pos)
	globalvars.screen.blit(text, textpos)


def wipeOldScenario():
	for sprt in globalvars.tangibles: sprt.kill()
	for sprt in globalvars.intangibles: sprt.kill()
	globalvars.intangibles = []
	for sprt in globalvars.whiskerables: sprt.kill()

	globalvars.BGCOLOR = black
	globalvars.BGIMAGE = None

	#Add the player back in.
	globalvars.tangibles.add(globalvars.player)
	globalvars.player.setHealthBar()

	#Immediately clear the panel
	globalvars.panel = None

	#Reset the hud_helper
	globalvars.hud_helper = None

	#Reset the arena
	globalvars.arena = 0



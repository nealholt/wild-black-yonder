from mover import *

while not finished:
	screen.blit(BGIMAGE, (0,0))
	for m in messages:
		finished = True
		if not m.finished:
			m.move()
			finished = False

	pygame.time.wait(wait_time)
	pygame.display.flip()
	clock.tick(120)

for event in pygame.event.get():
	if event.type == pygame.QUIT:
		running = False


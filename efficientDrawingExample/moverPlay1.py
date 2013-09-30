from mover import *

while not finished:
	dirty_rects = []
	for m in messages:
		finished = True
		if not m.finished:
			m_rect = (m.x, m.y, envelope_width, envelope_height)
			# - Blit a piece of the background over the sprite's current location, erasing it.
			screen.blit(BGIMAGE, (m.x,m.y), area=m_rect)
			# - Append the sprite's current location rectangle to a list called dirty_rects.
			dirty_rects.append(m_rect)
			# - Move the sprite.
			# - Draw the sprite at it's new location.
			m.move()
			finished = False
			# - Append the sprite's new location to my dirty_rects list.
			dirty_rects.append((m.x, m.y, envelope_width, envelope_height))
	# - Call display.update(dirty_rects)
	pygame.display.update(dirty_rects)

	pygame.time.wait(wait_time)
	clock.tick(120)

for event in pygame.event.get():
	if event.type == pygame.QUIT:
		running = False

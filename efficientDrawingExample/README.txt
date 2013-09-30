
moverPlay1 is more complicated and uses dirty rects and no call to flip.
moverPlay2 is less complicated and flips the entire screen.

moverPlay2 is slower than moverPlay2, which can be seen by running the following:

python -m cProfile -s cumulative moverPlay1.py > deleteme1.txt

python -m cProfile -s cumulative moverPlay2.py > deleteme2.txt

This efficiency gain was recommended by:
http://www.pygame.org/docs/tut/newbieguide.html

Author of the newbieguide argues you should not use pygame.display.update(). Instead do things in the following much more efficient manner.
 - Blit a piece of the background over the sprite’s current location, erasing it.
 - Append the sprite's current location rectangle to a list called dirty_rects.
 - Move the sprite.
 - Draw the sprite at it's new location.
 - Append the sprite’s new location to my dirty_rects list.
 - Call display.update(dirty_rects)
The difference in speed is astonishing. Consider that Solarwolf has dozens of constantly moving sprites updating smoothly, and still has enough time left over to display a parallax starfield in the background, and update that too.


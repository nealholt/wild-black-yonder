
YOU DON'T ACTUALLY HAVE TO WORRY ABOUT TRANSPARENT COLORS!
PYGAME TAKES CARE OF THAT FOR YOU!


INSTRUCTIONS FOR CUTTING OUT AN IMAGE:

Open Gimp.
Use the scissors select tool.
Turn antialiasing on.
  Experiment with the other options. I don't understand them even after reading documentation.
Cut out the image.
Create new.
Paste into the new screen.
Image menu -> autocrop
Layer menu -> anchor layer, to deselect the selection.
Select the paint bucket tool
I set the threshold to between 50-70 to get a nice fill around my initial object.
Fill in the background.
Save in gimp format.
Save in gif format.
Save in bmp format.

DONE. IF YOU REALLY NEED A TRANSPARENT IMAGE, CONTINUE READING.


The script for giving a gif a transparent color came from here:
http://www.mit.edu/people/nocturne/transparent.html
http://www.mit.edu/people/nocturne/etc/trans.transgif.html

./transgif.pl -000000 cutoutBig3Black.gif > cutoutBig3Blacktransparent.gif


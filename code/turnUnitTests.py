import math


def turnTowards(x1,y1,x2,y2,dir):
	angleToTarget = math.degrees(math.atan2(y1-y2, x1-x2)) - dir

	print math.degrees(math.atan2(y1-y2, x1-x2))

	#angleToTarget = (angleToTarget + 180) % 360 - 180
	angleToTarget = (angleToTarget + 180) % 360
	if angleToTarget > 180:
		print 'turn left'
	else:
		print 'turn right'



direction = 90
x1 = 0
y1 = 0
targetx = 1
targety = 0

print '\nCorrect answer is turn right: '
turnTowards(targetx,targety,x1,y1,direction)

targetx = -1
targety = 0

print '\nCorrect answer is turn left: '
turnTowards(targetx,targety,x1,y1,direction)

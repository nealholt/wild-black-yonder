import math
import random as rd

def distance(p1, p2):
	'''Returns distance between two points.'''
	return math.sqrt( (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 )


adjustments = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,-1)]
def getCoordsNearLoc(loc, mindist, maxdist):
	'''Returns random coordinates with maxdistx in the x direction
	and within maxdisty in the y direction of the location, loc, 
	but not within bufferdist of the loc.'''
	x = rd.randint(-maxdist, maxdist)+loc[0]
	y = rd.randint(-maxdist, maxdist)+loc[1]
	adjust = adjustments[ rd.randint(0,len(adjustments)-1) ]
	while distance((x,y), loc) < mindist:
		x = x+adjust[0]
		y = y+adjust[1]
	return x,y


def inSights(shooter, target_loc, weapon_range, angle_min):
	'''Pre: shooter is a ship. target_loc is a tuple x,y. weapon_range is an int or float.
	angle_min is a float or int representing the minimal angle to the target.
	Post: returns true it the target is roughly in the sights of the shooter.'''
	angle = shooter.getAngleToTarget(target=target_loc)
	#Check angle to target.
	#Also check that the target is roughly within this weapon's range.
	return abs(angle) < angle_min and \
	distance(shooter.rect.center, target_loc) < weapon_range


def angleToSlope(angle):
	'''Convert the given angle to a slope.'''
	run = math.cos(math.radians(angle))
	rise = math.sin(math.radians(angle))
	return rise/run


def rotateAngle(angle, rotation):
	'''I'm using an angle system like stardog uses such that 
	east=0, north=-90, west=180, south=90'''
	angle += rotation
	if angle > 180: angle -= 360
	elif angle < -180: angle += 360
	return angle


def angleFromPosition(start, end):
	'''Get the angle from the start to the end.
	This is taken from physicalObject's getAngleToTarget function.'''
	rise = end[1] - start[1]
	run = end[0] - start[0]
	#As I understand it, this ought to return one angle to the target,
	#though not necessarily the shortest angle.
	#Range of arctan is negative pi to pi and the world is upside down
	#because down is positive in the y direction.
	#See testAngleToTarget.py in backups for some examples.
	angle_to_target = math.degrees(math.atan2(rise, run))
	if angle_to_target < -180: angle_to_target += 360
	if angle_to_target > 180: angle_to_target -= 360
	return angle_to_target


def lineIntersectsCircle(m, b, h, k, r):
	'''Circle: (x-h)^2+(y-k)^2=r^2
	Line: y=mx+b
	Plug in the line for y in the circle
	then convert it to a quadratic of x equal to zero.
	If b^2-4ac, the part under the square root in the quadratic formula,
	is greater than zero, then the line and the circle intersect.

	Circle: (x-h)**2+(y-k)**2=r**2
	Line: y=mx+b
	(x-h)**2+(mx+b-k)**2=r**2
	x**2-2xh+h**2+m**2x**2+2mx(b-k)+(b-k)**2=r**2
	x**2+m**2x**2-2xh+2mx(b-k)+(b-k)**2+h**2-r**2=0
	(1+m**2) x**2 + (-2h+2m(b-k)) x + (b-k)**2+h**2-r**2=0
	(1+m**2) x**2 + (2*m*(b-k)-2*h) x + (b-k)**2+h**2-r**2=0

	a = 1+m**2
	b = 2*m*(b-k)-2*h
	c = (b-k)**2+h**2-r**2

	b^2-4ac

	(2*m*(b-k)-2*h)**2 - 4 * (1+m**2) * ((b-k)**2+h**2-r**2)
	'''
	return 0 <= (2*m*(b-k)-2*h)**2 - 4 * (1+m**2) * ((b-k)**2+h**2-r**2)


def translate(location, angle, magnitude):
	'''This is very similar to the PhysicalObject.move function.'''
	vectx = math.cos(math.radians(angle))
	vecty = math.sin(math.radians(angle))
	x,y = location
	return x+vectx*magnitude, y+vecty*magnitude


def getShorterTurnDirection(self, target_angle):
	'''TODO: I'm not 100% sure this works. In any case, no one is using it right now.
	Given a target angle, calculate the shorter direction to turn 
	and how many degrees to turn in that direction.
	Figuring out how to calculate this was a little tricky for me.
	Drawing helped. The idea is that there are two different
	distances between points when those points are on a ring.
	True = clockwise
	False = counterclockwise
	'''
	a = self.theta
	b = target_angle
	self_is_a = True
	if b < a: #Ensure that a is the smaller of the two values.
		a = target_angle
		b = self.theta
		self_is_a = False
	dist1 = b-a
	dist2 = (a+180)+(180-b) #a+180 is actually a - -180
	if dist1 < dist2:
		return self_is_a
	else:
		return not self_is_a


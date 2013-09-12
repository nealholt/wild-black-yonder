#unit test angle to target


import math

print "\n"


#Current implementation
def getAngleToTarget0(meX, meY, meDirection, targetX, targetY):
	rise = targetY - meY
	run = targetX - meX
	angleToTarget = math.degrees(math.atan2(rise, run)) - meDirection
	return (angleToTarget + 180) % 360

print 'East '+str(getAngleToTarget0(0,0,0,1,0)) #due east
print 'North '+str(getAngleToTarget0(0,0,0,0,1)) #due north
print 'West '+str(getAngleToTarget0(0,0,0,-1,0)) #due west
print 'South '+str(getAngleToTarget0(0,0,0,0,-1)) #due south

print "\n\n"

def getAngleToTarget1(meX, meY, meDirection, targetX, targetY):
	rise = targetY - meY
	run = targetX - meX
	angleToTarget = math.degrees(math.atan2(rise, run)) - meDirection
	return angleToTarget + 180

print 'East '+str(getAngleToTarget1(0,0,0,1,0)) #due east
print 'North '+str(getAngleToTarget1(0,0,0,0,1)) #due north
print 'West '+str(getAngleToTarget1(0,0,0,-1,0)) #due west
print 'South '+str(getAngleToTarget1(0,0,0,0,-1)) #due south

print "\n\n"

def getAngleToTarget2(meX, meY, meDirection, targetX, targetY):
	rise = targetY - meY
	run = targetX - meX
	return math.degrees(math.atan2(rise, run)) - meDirection

print 'East '+str(getAngleToTarget2(0,0,0,1,0)) #due east
print 'North '+str(getAngleToTarget2(0,0,0,0,1)) #due north
print 'West '+str(getAngleToTarget2(0,0,0,-1,0)) #due west
print 'South '+str(getAngleToTarget2(0,0,0,0,-1)) #due south

print "\n\n"

def getAngleToTarget3(meX, meY, meDirection, targetX, targetY):
	rise = targetY - meY
	run = targetX - meX
	return math.degrees(math.atan2(rise, run))

print 'East '+str(getAngleToTarget3(0,0,0,1,0)) #due east
print 'North '+str(getAngleToTarget3(0,0,0,0,1)) #due north
print 'West '+str(getAngleToTarget3(0,0,0,-1,0)) #due west
print 'South '+str(getAngleToTarget3(0,0,0,0,-1)) #due south

print "\n\n"

#Test at 45 degree angle

print 'East '+str(getAngleToTarget0(0,0,45,1,0)) #due east
print 'North '+str(getAngleToTarget0(0,0,45,0,1)) #due north
print 'West '+str(getAngleToTarget0(0,0,45,-1,0)) #due west
print 'South '+str(getAngleToTarget0(0,0,45,0,-1)) #due south

print "\n\n"

#Test at 45 degree angle

print 'East '+str(getAngleToTarget2(0,0,45,1,0)) #due east
print 'North '+str(getAngleToTarget2(0,0,45,0,1)) #due north
print 'West '+str(getAngleToTarget2(0,0,45,-1,0)) #due west
print 'South '+str(getAngleToTarget2(0,0,45,0,-1)) #due south

print "\n\n"


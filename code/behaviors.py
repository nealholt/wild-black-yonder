import game
from geometry import distance

def setClosestSprites():
	'''Pre:
	Post: For all ships in the whiskerables sprite list, the closest sprite 
	and the distance to that sprite is set. This is used for helping NPC 
	ships avoid collisions.'''
	#Get all the whiskerable sprites in an array
	sprite_list = game.whiskerables.sprites()
	#TODO I'd like to make use of sorting like I do for collision checking with this, but recently it was gumming up the works, so I'm simplifying it for now.
	#Sort them by their top point as is done when checking for collisions.
	#sprite_list = sorted(sprite_list, \
	#	key=lambda c: c.rect.topleft[1]+c.rect.height,\
	#	reverse=True)
	#For each sprite...
	for i in xrange(len(sprite_list)):
		#Get the next sprite to deal with.
		A = sprite_list[i]
		#only ships can avoid objects.
		if A.is_a != game.SHIP: #TODO this could be more efficient by keeping another group that is just ships. Of course there is a cost there. It might be worth profiling at some point to see if this is better or another group that is just non-player ships is better.
			continue
		#Reset closest sprite and the distance to that sprite. Sprites 
		#further than this distance will be ignored.
		closest_sprite = None
		least_dist = game.MINSAFEDIST
		#search for too close sprites
		for j in xrange(len(sprite_list)):
			if j != i:
				B = sprite_list[j]
				dist = distance(A.rect.center, B.rect.center) - B.radius - A.radius
				if dist < least_dist:
					least_dist = dist
					closest_sprite = B
		'''#TODO this is the old way it was done when the sprite list was sorted, but I was accidentally missing checks on certain sprites so I simplified it for the time being.
		#search forward for too close sprites
		for j in xrange(i+1, len(sprite_list)):
			B = sprite_list[j]
			dist = distance(A.rect.center, B.rect.center) - B.radius - A.radius
			if dist < least_dist:
				least_dist = dist
				closest_sprite = B
				#break #TODO TESTING
			#TODO TESTING
			#elif abs(A.rect.centerx - B.rect.centerx) > least_dist:
			#	break
		#search backward for too close sprites
		count_back = []
		if i > 0:
			count_back = range(0, i-1)
			count_back.reverse()
		for j in count_back:
			B = sprite_list[j]
			dist = distance(A.rect.center, B.rect.center) - B.radius - A.radius
			if dist < least_dist:
				least_dist = dist
				closest_sprite = B
				#break #TODO TESTING
			#TODO TESTING
			#elif abs(A.rect.centerx - B.rect.centerx) > least_dist:
			#	break'''
		#Set sprite A's closest sprite and the distance to that sprite.
		#if not closest_sprite is None: print closest_sprite.image_name+' at '+str(least_dist) #TODO TESTING
		A.setClosest(closest_sprite, least_dist)


def collisionHandling():
	'''The following function comes from pseudo code from
	 axisAlignedRectangleCollision.txt that has been modified.'''
	#Get a list of all the sprites
	sprite_list = game.tangibles.sprites()
	#sort the list in descending order based on each 
	#sprite's y coordinate (aka top) plus height.
	#Remember that larger y coordinates indicate further down
	#on the screen.
	#Reverse tells sorted to be descending.
	#rect.topleft[1] gets the y coordinate, top.
	sprite_list = sorted(sprite_list, \
		key=lambda c: c.rect.topleft[1]+c.rect.height,\
		reverse=True)
	#iterate over the sprite list
	for i in xrange(len(sprite_list)):
		A = sprite_list[i]
		for j in xrange(i+1, len(sprite_list)):
			B = sprite_list[j]
			#if A's least y coord (A's top) is > B's
			#largest y coord (B's bottom)
			#then they don't overlap and none of the following
			#sprites overlap A either becuase the list is sorted
			#by bottom y coordinates.
			#We therefore skip the rest of the sprites in the list.
			if A.rect.topleft[1] > B.rect.topleft[1]+B.rect.height:
				break
			else:
				#Otherwise, we need to see if they overlap
				#in the x direction.
				#if A's greatest x coord is < B's least x coord
				#or B's greatest x coord is < A's least x coord
				#then they don't overlap, but one of the following 
				#sprites might still overlap so we move to the
				#next sprite in the list.
				#OLD WAY based on rectangles:
				#if A.rect.topleft[0]+A.rect.width < B.rect.topleft[0]\
				#or B.rect.topleft[0]+B.rect.width < A.rect.topleft[0]:
				#NEW WAY based on circles:
				#If the distance between our centers is larger than are 
				#summed radii, then we have not collided.
				if distance(A.rect.center, B.rect.center) > A.radius+B.radius:
					pass
				else:
					#they overlap. They should handle 
					#collisions with each other.
					A_died = A.handleCollisionWith(B)
					B.handleCollisionWith(A)
					#If A has died, then don't worry about A
					#colliding with anything else.
					if A_died:
						break




################################## IMPORTING LIBRARIES ####################################

from __future__ import print_function
import time
from sr.robot import *

a_th = 2.3
d_th = 0.4
R = Robot()
gold_th=1.1
silver_th=1

################################### DEFINING FUNCTIONS #####################################
			
def drive(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

###########################################################################################

def turn(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

############################################################################################

def find_silver_token():
    dist=3
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER and -70<token.rot_y<70:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==3:
	return -1, -1
    else:
   	return dist, rot_y

############################################################################################

def find_golden_token():
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -40<token.rot_y<40:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	return -1, -1
    else:
   	return dist, rot_y

############################################################################################

def find_golden_token_left():

    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -105<token.rot_y<-75:
            dist=token.dist
    if dist==100:
	return -1
    else:
   	return dist

############################################################################################

def find_golden_token_right():

    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and 75<token.rot_y<105:
            dist=token.dist
    if dist==100:
	return -1
    else:
   	return dist

############################################################################################

def grab_it():

	if R.grab():
	    	print("Gotcha!")
	    	turn(44, 2)
	    	drive(20, 0.9)
	    	R.release()
	    	drive(-20,0.9)
		turn(-44,2)

################################### DEFINING MAIN FUNCTION ##################################
# I decided to make a main() function where to code, I could do it even without implementing it.

def main():
	
	# We want to loop the program to move the robot endlessy.
	
	while 1:
		
		# The following 4 lines are needed in order to update the informations of the tokens, either gold or silver,
		# the while loop updates the infos reading the lines.

		dist_silver, rot_silver = find_silver_token()
		dist_gold, rot_gold =find_golden_token()
		left_dist=find_golden_token_left()
		right_dist=find_golden_token_right()
		
		# If we are away from the gold and silver tokens we keep driving straight the robot so we can get closer to
		# gold or silver boxes. We want to use a small amount of time in the function drive() so we can avoid problems
		# related to getting to close to the walls.
		
		if (dist_gold>gold_th and dist_silver>silver_th) or (dist_gold>gold_th and dist_silver==-1):
			drive(130,0.1)
		
		# If we are close to silver boxes we use a different control which makes us able to get close to the silver 
		# token without pushing it. This kind of control let us get to the silver token whenever we are silver_th (1.5)
		# away from the silver token, then we get closer to it by using the three elifs so we can grab it with the
		# first if.
		
		if dist_silver<silver_th and dist_silver!=-1:
			print("Silver is really close")
			if dist_silver < d_th:
				print("Found it!")
				grab_it()
	    		elif -a_th<=rot_silver<=a_th:
	    			drive(40, 0.1)
	    			print("Ah, that'll do.")
		    	elif rot_silver < -a_th:
				print("Left a bit...")
				turn(-10, 0.1)
			elif rot_silver > a_th:
				print("Right a bit...")
				turn(10, 0.1)
		
		# If the robot is too close to the golden wall we stop the robot and depending to the distance of the golden
		# tokens on the right or on the left it turns in one direction. Then when the distance detected by the 
		# find_golden_token() function will be higher than gold_th it will drive straight.
		
		if dist_gold<gold_th and dist_gold!=-1:
		
			print("Wait a minute, where's the wall?")
			
			if left_dist>right_dist:
				turn(-35, 0.1)
				print("Wall on the right "+ str(right_dist)+ ", the distance on the left is: "+str(left_dist))		
			elif right_dist>left_dist:
				turn(35, 0.1)
				print("Wall on the left "+ str(left_dist)+ ", the distance on the right is: "+str(right_dist))
			else:
				print("sinistra e destra circa uguali")
				print("destra: "+ str(right_dist))
				print("sinistra: "+str(left_dist))

############################################################################################

main()



############################################################################################

from __future__ import print_function
import time
from sr.robot import *

a_th = 2.3
d_th = 0.4
R = Robot()
gold_th=1
silver_th=1.5

############################################################################################

def drive(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

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
   	
def grab_silver(rot_silver):
	print("Go grab silver")
	if R.grab(): # if we grab the token....
		print("Gotcha!")
		turn(20, 3.2)
		R.release()
		turn(-20,3.2)
    	elif -a_th<=rot_silver<=a_th:
    		drive(40, 0.5) 
    		print("Ah, that'll do.")
	elif rot_silver < -a_th: 
		print("Left a bit...")
		turn(-5, 0.3)
	elif rot_silver > a_th:
		print("Right a bit...")
		turn(+5, 0.3)
   	
############################################################################################

def main():

	while 1:
	
		dist_silver, rot_silver = find_silver_token()
		dist_gold, rot_gold =find_golden_token()
		left_dist=find_golden_token_left()
		right_dist=find_golden_token_right()
									
		if (dist_gold>gold_th and dist_silver>silver_th) or (dist_gold>gold_th and dist_silver==-1):
			print("Vado dritto")
			drive(70,0.5)		
						
		elif dist_gold<gold_th and dist_gold!=-1:
			print("Fermati, dov'e` il muro?")
			if left_dist>right_dist:
				turn(-25, 0.1)
				print("Muro a destra "+ str(right_dist)+ ", la somma a sinistra invece e': "+str(left_dist))		
			elif right_dist>left_dist:
				turn(25, 0.1)
				print("Muro a sinistra "+ str(left_dist)+ ", la somma a destra invece e': "+str(right_dist))
			else:
				print("sinistra e destra circa uguali")
				print("destra: "+ str(right_dist))
				print("sinistra: "+str(left_dist))
				

		if dist_silver<silver_th and dist_silver!=-1: 
			print("Silver is close")
			if dist_silver < d_th: 
				print("Found it!")
				#grab_silver(rot_silver)
				if R.grab(): # if we grab the token....
				    	print("Gotcha!")
				    	turn(20, 3)
				    	drive(20, 0.8)
				    	R.release()
				    	drive(-20,0.8)
					turn(-20,3)
	    		elif -a_th<=rot_silver<=a_th:
	    			drive(40, 0.5) 
	    			print("Ah, that'll do.")
		    	elif rot_silver < -a_th: 
				print("Left a bit...")
				turn(-10, 0.1)
			elif rot_silver > a_th:
				print("Right a bit...")
				turn(10, 0.1)
				
main()


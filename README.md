First assignment of Research Track 1 <img src="https://raw.githubusercontent.com/jmnote/z-icons/master/svg/python.svg" width="30" height="30">
================================

This is a simple, portable robot simulator developed by [Student Robotics](https://studentrobotics.org). Our professor, throught the help of this simulator, gave us an assignment regarding the coding of the movement of the robot inside the enviroment. Before starting, if you need a specific information, I recommend to use the table of contents on the up left corner!

Installing and running <img src="https://icon-library.com/images/loading-gif-icon/loading-gif-icon-14.jpg" width="15" height="15">
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).
To install the libraries up here, here's some commands for the linux shell:

```bash
$ sudo apt-get install python-dev python-pip python-pygame python-yaml`
```

``` bash
$ sudo pip install pypybox2d`
```

Once the dependencies are installed, get inside the directory on the shell. To run the game, run the command:

```bash
$ python2 run.py assignment.py`
```
## Troubleshooting <img src="https://cdn140.picsart.com/264247623010202.gif" width="20" height="20">

When running `python run.py <file>`, you may be presented with an error: `ImportError: No module named 'robot'`. This may be due to a conflict between sr.tools and sr.robot. To resolve, symlink simulator/sr/robot to the location of sr.tools.

On Ubuntu, this can be accomplished by:
* Find the location of srtools: `pip show sr.tools`
* Get the location. In my case this was `/usr/local/lib/python2.7/dist-packages`
* Create symlink: `ln -s path/to/simulator/sr/robot /usr/local/lib/python2.7/dist-packages/sr/`

Pygame, unfortunately, can be tricky (though [not impossible](http://askubuntu.com/q/312767)) to install in virtual environments. If you are using `pip`, you might try `pip install hg+https://bitbucket.org/pygame/pygame`, or you could use your operating system's package manager. Windows users could use [Portable Python](http://portablepython.com/). PyPyBox2D and PyYAML are more forgiving, and should install just fine using `pip` or `easy_install`.

Introduction <img src="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/298029cc-f5c6-4b7b-a146-ecdf85f98de0/dcf5a2t-a143285d-db85-4b8a-bfef-6cae76df284d.gif?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzI5ODAyOWNjLWY1YzYtNGI3Yi1hMTQ2LWVjZGY4NWY5OGRlMFwvZGNmNWEydC1hMTQzMjg1ZC1kYjg1LTRiOGEtYmZlZi02Y2FlNzZkZjI4NGQuZ2lmIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.ucsQuh7pcnByIslYFv1ETJ2Q8_V8N7wjKUkacaNwOB4" width="20" height="20">
----------------------
The aim of the project was to make the robot moving inside a maze made out of golden boxes. We can see the maze if we run the command:
```bash
$ python2 run.py empty.py`
```
<p align="center">
	<img src="https://github.com/LucaPreddi/RT1_Assignment_1/blob/main/pics%20and%20gifs/Maze.png">
</p>

We can see some silver boxes spread around the maze. Another aim of the project was not to avoid the silver boxes but to grab them and move them away the path the robot walks. Here's a gif to show the behaviour the robot must have when meeting a silver token:

<p align="center">
	<img src="https://github.com/LucaPreddi/RT1_Assignment_1/blob/main/pics%20and%20gifs/Grab.gif" height=226>
</p>

Professor asked us to let the robot move only counter clockwise, so we had to think how to make the robot turn always in the right direction. Here's shown the behaviour the robot must have when meeting a wall:

<p align="center">
	<img src="https://github.com/LucaPreddi/RT1_Assignment_1/blob/main/pics%20and%20gifs/Hit.gif" height=226>
</p>

Using the libraries we downloaded and our brain we had to make it work! The following sections will explain step by step the code we developed, starting from the libraries, developing the functions we decided to use and ending with the main code.

How the robot interacts with the enviroment  <img src="https://images.squarespace-cdn.com/content/v1/5ba175f0a9e0286ef432a3bf/1545322611971-20CSVNUR4SEH7PO0BXK9/Full-Run-Turn.gif" width="40" height="40">
----------------------
The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

Functions <img src="https://c.tenor.com/y2JXkY1pXkwAAAAC/cat-computer.gif" width="20" height="20">
----------------------
In order to make the code lighter and tidy I implemented some functions, they're not diffult, but some of them need a bit more attention because they're crucial for the code and for the behaviour of the robot. I'm going to explain each of them, trying to explain them for the overall comprehension of the main function, which contains the whole instructions for the intelligence of the robot and it needs a whole section to be explained.

### drive() ###
The `drive()` function permits the movement of the robot using the robot libraries. If we want to go backwards, it only needs a negative speed parameter. Obviously both the motors should have the same amount of power in order to drive straight and not curving.
- Arguments 
  - `speed`, the amount of linear velocity that we want our robot to assume.
  - `seconds`, the amount of seconds we want out robot to drive.
- Returns
  - None.
- Code
```python
def drive(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
```
### turn() ###
The `turn()` functions permits the robot to turn where he is without having a linear velocity, indeed the robot is perfectly "stuck" in the point in the space he has even if he rotates.
- Arguments 
  - `speed`, the amount of angular velocity that we want our robot to assume.
  - `seconds`, the amount of seconds we want out robot to turn.
- Returns
  - None.
- Code
```python
def turn(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
```

### find_silver_token() ###
The `find_silver_token()` function is used to study all the silver tokens that are around the robot. The function checks all the tokens that the robot, we can say, sees thanks to `R.see()` method. The function only takes the tokens that are closer than 3 (which is pretty close inside the enviroment) and inside the angle `φ`, which is `-70°<φ<70°`. Obviously, as long as we want only silver tokens, we want to have as `marker_type` `MARKER_TOKEN_SILVER`, because it's what it differentiates it from the golden ones.
- Arguments 
  - None.
- Returns
  - Returns distance of the closest silver token and angle between the robot and the closest silver token (`dist`, `rot_y`).
- Code
```python
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
```
<p align="center">
	<img src="https://github.com/LucaPreddi/RT1Assignment1/blob/main/pics%20and%20gifs/Find_silver_token().jpg">
</p>

### find_golden_token() ###
The `find_golden_token()` function is crucial for the movement of the robot close to a wall. As the `find_silver_token()` function, it uses the same methods and code structure of it. We can underline the paramaters that change which are the dist which is going to be higher in order to always check where is the closest golden box (`dist=100`), the angle which is going to be more limited (`-40°<φ<40°`) because we want to check only the golden boxes in front of the robot, and, of course, the `marker_type` which is going to be `MARKER_TOKEN_GOLD`.
- Arguments 
  - None.
- Returns
  - Returns distance of the closest golden token and angle between the robot and the closest golden token (`dist`, `rot_y`).
- Code
```python
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

```
<p align="center">
	<img src="https://github.com/LucaPreddi/RT1Assignment1/blob/main/pics%20and%20gifs/Find_golden_token().jpg">
</p>

### find_golden_token_left() ###
The `find_golden_token_left()` function is used to check how far is the wall of golden boxes on the left, used with its sister, `find_golden_token_right()` we can check where do we have to turn when getting closer to a wall. Nothing is really new because again only one important parameter changes which is the angle, which now is `-105°<φ<-75°`, as the angle is negative on the left.
- Arguments 
  - None.
- Returns
  - Returns distance of the closest golden token on the left (`dist`).
- Code
```python
def find_golden_token_left():
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and -105<token.rot_y<-75:
            dist=token.dist
    if dist==100:
	return -1
    else:
   	return dist
```

### find_golden_token_right() ###
The `find_golden_token_right()` function is identical to the one just explained, it only changes the angle which is `75°<φ<105°`, as the angle is positive on the right.
- Arguments 
  - None.
- Returns
  - Returns distance of the closest golden token on the right (`dist`).
- Code
```python
def find_golden_token_right():

    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and 75<token.rot_y<105:
            dist=token.dist
    if dist==100:
	return -1
    else:
   	return dist
```
<p align="center">
	<img src="https://github.com/LucaPreddi/RT1Assignment1/blob/main/pics%20and%20gifs/Find_gold_token_left_right().jpg">
</p>

### grab_it() ###
The `grab_it()` function it's used to do a set of instructions which where inconvenient to put inside the code, as now the main() function feel more conceptual.
- Arguments 
  - None.
- Returns
  - None.
- Code
```python
def grab_it():
	if R.grab():
	    	print("Gotcha!")
	    	turn(20, 3)
	    	drive(20, 0.9)
	    	R.release()
	    	drive(-20,0.9)
		turn(-20,3)
```

Main function <img src="https://c.tenor.com/TyhWL7gJwPgAAAAj/peppo-dance.gif" width="20" height="20">
----------------------
The `main()` function contains all the functions that I developed during the coding part of the project. __What the `main()` really has is the conceptual part of the project that is the way the robot _thinks_ and how he reacts to the enviroment__. 
To have a clearer field of view I decided to write down a sort of __flowchart__, in order to have a tidy group of concepts inside the whole work I had to develop. Here's the flowchart:

![immagine](https://github.com/LucaPreddi/RT1Assignment1/blob/main/Flowchart_new.png)

As we want the robot do loop endlessy inside the maze we want to put the instructions inside a while loop which loops endlessy, updating every loop the informations. 

__IMPORTANT NOTE!__: in the code I uploaded you will see a lot of `print()` functions around the code, this helps you to understand where in the code you are running the program by reading the terminal. Feel free to erase them, for now I'm going to omit them for easier explanation.

```python
while(1):

	dist_silver, rot_silver = find_silver_token()
	dist_gold, rot_gold =find_golden_token()
	left_dist=find_golden_token_left()
	right_dist=find_golden_token_right()
```

Now, we want to cover the first two parts of the flowchart, using the functions we implemented. Now it is going to be really easy because ny implementing the functions I implemented in the functions section we have all the work more or less done. The first one is the one below.

![immagine](https://github.com/LucaPreddi/RT1Assignment1/blob/main/pics%20and%20gifs/Flowchart_2.png)

We do it by adding the last three instructions to the code, using a simple if statement. Thank's to these instructions our robot can move easily when he's away from a token and from a wall made of golden boxes. The variable `silver_th` is an int number which permits us to change the behaviour of the robot when is close to a silver token (`silver_th=1`).

```python
# Looping endlessy
while(1):

	# Updating informations.
	dist_silver, rot_silver = find_silver_token()
	dist_gold, rot_gold =find_golden_token()
	left_dist=find_golden_token_left()
	right_dist=find_golden_token_right()
	
	# First part of the flowchart.
	if (dist_gold>gold_th and dist_silver>silver_th) or (dist_gold>gold_th and dist_silver==-1):
			print("Drive straight 0.05 seconds")
			drive(100,0.05)
```

The second part we want to study is the one regarding the behaviour of the robot close to a wall, which is exactly this part of the flowchart.

![immagine](https://github.com/LucaPreddi/RT1Assignment1/blob/main/pics%20and%20gifs/Flowchart_1.png)

We solve this part by adding some lines using the two parameters `right_dist` and `left_dist`, which they can help us a lot, indeed studying the distance either in the left and in the right our robot will turn to the left or to the right!

```python
# Looping endlessy
while(1):

	# Updating informations.
	dist_silver, rot_silver = find_silver_token()
	dist_gold, rot_gold =find_golden_token()
	left_dist=find_golden_token_left()
	right_dist=find_golden_token_right()
	
	# First part of the flowchart.
	if (dist_gold>gold_th and dist_silver>silver_th) or (dist_gold>gold_th and dist_silver==-1):
			drive(100,0.05)
			
	# Second part of the flowchart.
	if dist_gold<gold_th and dist_gold!=-1:
			if left_dist>right_dist:
				turn(-25, 0.1)
			elif right_dist>left_dist:
				turn(25, 0.1)
```
Now we want to cover the last part of the flowchart, the part where the robot is really close to a silver token, and we want to start the routine that makes the robot getting closer to the silver token, adjusting the angle and the distancee and then grabs it. 

The part I'm talking about is the following.

![immagine](https://github.com/LucaPreddi/RT1Assignment1/blob/main/pics%20and%20gifs/Flowchart_3.png)

To develop the code, I decided to use again a really simple if statement, thanks to all the function and reasoning part I went through before starting coding the `main()` function part, at the end we want to call the function to make it all work.

The parameters `a_th`, `-a_th` and `d_th` are those thanks to them we can call the `R.grab()` method and grab the token. The angle and the distance of the robot from the token should be: __`-a_th<φ<a_th` and `d<d_th` with `a_th=2.3` and `d_th=0.4`__.

```python
# Looping endlessy
while(1):
	
	# Updating informations.
	dist_silver, rot_silver = find_silver_token()
	dist_gold, rot_gold =find_golden_token()
	left_dist=find_golden_token_left()
	right_dist=find_golden_token_right()
	
	# First part of the flowchart.
	if (dist_gold>gold_th and dist_silver>silver_th) or (dist_gold>gold_th and dist_silver==-1):
			drive(100,0.05)
			
	# Second part of the flowchart.
	if dist_gold<gold_th and dist_gold!=-1:
			if left_dist>right_dist:
				turn(-25, 0.1)
			elif right_dist>left_dist:
				turn(25, 0.1)
	
	# Third and last part of the flowchart.
	if dist_silver<silver_th and dist_silver!=-1:
			if dist_silver < d_th:
				grab_it()
	    		elif -a_th<=rot_silver<=a_th:
	    			drive(40, 0.1)
		    	elif rot_silver < -a_th:
				turn(-10, 0.1)
			elif rot_silver > a_th:
				turn(10, 0.1)
	
main()
```
__IMPORTANT NOTE__: if you need a better version of the code with more comments, you can open directly the assignment.py file, which contains a lot more comments to the code and all the code I just explained in the whole README.md file. Please feel free to contact me for more explanation and suggestings. Anyway I will show you my results and what can be improved more.

Results
----------------------

### Overall work ###

I am satisfied with the work I've done, I had the opportunity to get deeper into python functions even if the .py we developed is not that hard. Another remarkable part of the project was reasoning before starting coding, that was really important, because we gained a lot of time that we would've spent looking at the code without understanding. I worked a lot with my university colleagues and we were very satisfied for the code each of us developed, comparing every lines and trying to find out what was the best result. 

The overall comprehension of the code in python has to be connected with all the time paid understanding how Git works and all the consequences for each command that we run we will have (like committing before pulling!). This platform is really challenging and permits you to give value to your work.

As the job is (or at least seems) done here's the final result with a sped up video.

https://user-images.githubusercontent.com/85370395/138760348-266444a5-5395-4948-aeb4-d99ac111c672.mp4

### Possible improvements ###

I will try to explain with a list what can be improved in the code in order to have a cleaner movement of the robot. Again, if you have any suggestions feel free to contact me by the links you find in my personal [bio](https://github.com/LucaPreddi).

1. __Online control__, this came out from my friend [@Matteo](https://github.com/MatteoCarlone) and I minds. The aim of this idea is instead of letting the robot hit the wall, trying to always see where is the silver token and trying to mantain the centre of the line, this would make a way smoother movement of the robot.
2. __Adding more controls__, as you can see the code is pretty simple and for what the professor was asking, it satisfies the requests. But if we think the robot in another maze, maybe with some different shape walls (like zig-zag-ed or with a wave shape) we can have some problems when choosing the turning direction.

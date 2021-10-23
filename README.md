First assignment of Research Track 1
================================

This is a simple, portable robot simulator developed by [Student Robotics](https://studentrobotics.org). Our professor, throught the help of this simulator, gave us an assignment regarding the coding of the movement of the robot inside the enviroment.

Installing and running
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
## Troubleshooting

When running `python run.py <file>`, you may be presented with an error: `ImportError: No module named 'robot'`. This may be due to a conflict between sr.tools and sr.robot. To resolve, symlink simulator/sr/robot to the location of sr.tools.

On Ubuntu, this can be accomplished by:
* Find the location of srtools: `pip show sr.tools`
* Get the location. In my case this was `/usr/local/lib/python2.7/dist-packages`
* Create symlink: `ln -s path/to/simulator/sr/robot /usr/local/lib/python2.7/dist-packages/sr/`

Pygame, unfortunately, can be tricky (though [not impossible](http://askubuntu.com/q/312767)) to install in virtual environments. If you are using `pip`, you might try `pip install hg+https://bitbucket.org/pygame/pygame`, or you could use your operating system's package manager. Windows users could use [Portable Python](http://portablepython.com/). PyPyBox2D and PyYAML are more forgiving, and should install just fine using `pip` or `easy_install`.

Introduction
----------------------
The aim of the project was to make the robot moving inside a maze made out of golden boxes. We can see the maze if we run the command:
```bash
$ python2 run.py empty.py`
```

![immagine](https://github.com/LucaPreddi/RT1_Assignment_1/blob/main/pics%20and%20gifs/Maze.png)

We can see some silver boxes spread around the maze. Another aim of the project was not to avoid the silver boxes but to grab them and move them away the path the robot walks. Here's a gif to show the behaviour the robot must have when meeting a silver token:

![immagine](https://github.com/LucaPreddi/RT1_Assignment_1/blob/main/pics%20and%20gifs/Grab.gif)

Professor asked us to let the robot move only counter clockwise, so we had to think how to make the robot turn always in the right direction. Here's shown the behaviour the robot must have when meeting a wall:

![immagine](https://github.com/LucaPreddi/RT1_Assignment_1/blob/main/pics%20and%20gifs/Hit.gif)

Using the libraries we downloaded and our brain we had to make it work! The following sections will explain step by step the code we developed, starting from the libraries, developing the functions we decided to use and ending with the main code.

Small explanation of how the robot interacts with the enviroment
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

Functions
----------------------
In order to make the code lighter and tidy I implemented some functions, they're not diffult, but some of them need a bit more attention because they're crucial for the code and for the behaviour of the robot. I'm going to explain each of them, trying to explain them for the overall comprehension of the main function, which contains the whole instructions for the intelligence of the robot and it needs a whole section to be explained.

### Drive ###
The drive function permits the movement of the robot using the robot libraries. If we want to go backwards, it only needs a negative speed parameter. Obviously both the motors should have the same amount of power in order to drive straight and not curving.
- Parameters 
  - Speed, the amount of linear velocity that we want our robot to assume.
  - Seconds, the amount of seconds we want out robot to drive.
- Returns
  - none
- Code
```python
    def drive(speed, seconds):
      R.motors[0].m0.power = speed
      R.motors[0].m1.power = speed
      time.sleep(seconds)
      R.motors[0].m0.power = 0
      R.motors[0].m1.power = 0
```
### Turn ###
The turn functions permits the robot to turn where he is without having a linear velocity, indeed the robot is perfectly "stuck" in the point in the space he has even if he rotates.
- Parameters 
  - Speed, the amount of angular velocity that we want our robot to assume.
  - Seconds, the amount of seconds we want out robot to turn.
- Returns
  - none
- Code
```python
    def turn(speed, seconds):
      R.motors[0].m0.power = speed
      R.motors[0].m1.power = -speed
      time.sleep(seconds)
      R.motors[0].m0.power = 0
      R.motors[0].m1.power = 0
```

Main function
----------------------

Results
----------------------

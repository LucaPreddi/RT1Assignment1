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
The aim of the project was to make the robot moving inside a maze made out of golden boxes.

![immagine](https://github.com/LucaPreddi/RTAssignment1/blob/main/Maze.PNG)

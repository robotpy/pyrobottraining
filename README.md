pyrobottraining
===============

This is a repository that can be used as a tool to teach you about programming
an FRC robot using python and the RobotPy WPILib libraries.

Note: If you aren't very familiar with python programming, you may want to
complete  [pybasictraining](https://github.com/frc1418/pybasictraining) first,
which will teach you the basics of programming in python.

Preparation
===========

Install the requirements
------------------------

One of the really useful things about python is that you can write code that
behaves the same regardless of which platform you're running it on. As such,
the challenges should function the same regardless of whether you're using
Windows or OSX or Linux. However, each platform will require slightly different
steps to install the necessary requirements.

### OSX/Linux

You need to have the following things installed:

* [Python 3.5 or greater](https://www.python.org/downloads/release/python-350/)
  (this requires admin access)
* The `pyfrc` python module and its requirements
  * If you have admin access, install via `sudo pip3 install pyfrc`
  * If you don't, you can install via `pip3 install --user pyfrc`

### Windows

You need to have the following things installed:

* [Python 3.5 or greater](https://www.python.org/downloads/release/python-350/)
  (this requires admin access)
* The `pyfrc` python module and its requirements
  * At a command prompt, `py -3 -m pip install pyfrc`

Get the code
------------

You need to clone this git repository somewhere on your computer. You can use
eclipse to do this, or open up a terminal and run the following:

    git clone https://github.com/robotpy/pyrobottraining.git

About the challenges
--------------------

In [the challenges](#the-challenges) section, each bullet point is a challenge
you must complete. The name of the challenge is listed first, followed by the
description of the challenge.

All of the challenges will involve adding code to robot.py, which is a file
that could potentially be used to control a real FRC robot. You can also run
your code using the pyfrc robot simulator.

Please keep in mind that there are generally many different ways you can get
the challenge tests to pass, but typically each test is a simple step that
builds upon the knowledge/things done in previous tests. You are encouraged
to complete the tests in order.


Testing to see if you beat the challenges
-----------------------------------------

The challenges currently need to be run in the terminal/command line. This means
you need to open up a terminal or cmd and change directories to wherever you
checked out the code.

There are two ways to run the challenges. If you think your code can beat ALL
of the challenges, then you can run the tests the same way that you will run 
tests when you write real robot code (because this IS real robot code):

    OSX/Linux: ./robot.py test
    Windows:   py robot.py test

However, running all the challenges can be a bit confusing and give you a lot
of errors that you don't care about when concentrating on beating the current
challenge. To run a single challenge, do this instead:

    OSX/Linux: ./run_single.sh CHALLENGE
    Windows    run_single.bat CHALLENGE
  
So for example, to run challenge `v1` on OSX or Linux, you would do this:

    ./run_single.sh v1

Whereas on Windows you would do this:

    run_single.bat v1

Should be simple enough!

Documentation
-------------

Before you start creating code for the challenges, you may find it useful to
read through the following resources:

* [Anatomy of a Robot](http://robotpy.readthedocs.org/en/latest/guide/anatomy.html) -
  this is a python-focused guide for writing FRC Robot code, and tells you about
  each piece and how they fit together.
* [Python WPILib Documentation](http://robotpy.readthedocs.org/en/latest/wpilib.html) -
  contains information about using all the various pieces of WPILib

Challenges
==========

basics
------

At all times your robot code must pass all basic pyfrc tests, which ensure that
your robot can pass through all modes without crashing. Additionally, you must
document all methods and classes with docstrings.

The basic tests will only run when running all other tests, and not when running
single tests.

initialization
--------------

When initializing motors and sensors in your robot code, you should do it in
the `robotInit` method. These challenges will ask you to create a `robotInit`
method, and create various objects in it. You may find it convenient to add
additional initialization code to `robotInit` for other challenges.

* i1 - Create a `robotInit` method in the `MyRobot` class
* i2 - Create a Talon motor controller object that uses PWM channel 1 (`motor1`)
* i3 - Create a Talon motor controller object that uses PWM channel 2 (`motor2`)
* i4 - Create a Victor motor controller object that uses PWM channel 3 (`motor3`)
* i5 - Create a Victor motor controller object that uses PWM channel 4 (`motor4`)
* i6 - Create a digital input object on port 1 (`dio1`)
* i7 - Create an analog input object on port 5  (`analog5`)
* i8 - Create a joystick object on port 0, and assign it to an instance variable
  named `stick`
  
Motor control
-------------

These challenges will require you to create code that executes when the robot
is actually running -- in the `teleopPeriodic` method.

* m1 - Define a `teleopPeriodic` method
* m2 - During teleop, set the value of `motor1` to 1.0. When not in teleop, set 
  to 0
* m3 - During teleop, set the value of `motor2` to the value of the joystick's
  X axis. When not in teleop, set to 0
* m4 - During teleop, if `dio1` is on, then set the value of `motor3` to the
  value of the joystick's Y axis. If it is off, then set the motor to 0.

Simple state machines
---------------------

* s1 - If the robot's battery voltage drops below 9 volts, set motors 1-3 to
  0 until the voltage rises above 10 volts or the robot is disabled (you must
  have completed m1-m4)
* s2 - During teleop, set motor4 to 0. If the joystick trigger is pressed and
  released, set motor4 to the value of the joystick's Z axis until the joystick
  trigger is pressed and released again. If the robot enters disabled
  mode, when the robot enters teleop it should not turn motor4 back on until
  the trigger has been pressed and released again

Autonomous mode
---------------

TODO



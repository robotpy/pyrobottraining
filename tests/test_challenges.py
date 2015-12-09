#
# To legally & successfully complete the challenges, you MUST NOT change the
# contents of this file!
#

import random

import wpilib
import inspect

# Include basic pyfrc tests
include_pyfrc_tests = False
if include_pyfrc_tests:
    from pyfrc.tests import *
    from pyfrc.tests.docstring_test import test_docstrings
    import pyfrc.tests.docstring_test
    pyfrc.tests.docstring_test.pedantic_docstrings = False


def test_i1(robot):
    '''Create a `robotInit` method in the `MyRobot` class'''
    assert hasattr(robot, 'robotInit')
    assert inspect.ismethod(robot.robotInit)
    
    # If there's an error here, you didn't create a robotInit method
    assert inspect.getmodule(robot.robotInit) is not wpilib.iterativerobot
    
def test_i2(robot, hal_data):
    '''Create a Talon motor controller object that uses PWM channel 1 (`motor1`)'''
    assert hal_data['pwm'][1]['initialized'] == False # don't create the motor in the constructor!
    robot.robotInit()
    
    # Check that the correct port was used
    assert hal_data['pwm'][1]['initialized'] == True
    assert hal_data['pwm'][1]['type'] == 'talon'

def test_i3(robot, hal_data):
    '''Create a Talon motor controller object that uses PWM channel 2 (`motor2`)'''
    assert hal_data['pwm'][2]['initialized'] == False # don't create the motor in the constructor!
    robot.robotInit()
    
    # Check that the correct port was used
    assert hal_data['pwm'][2]['initialized'] == True
    assert hal_data['pwm'][2]['type'] == 'talon'

def test_i4(robot, hal_data):
    '''Create a Victor motor controller object that uses PWM channel 3 (`motor3`)'''
    assert hal_data['pwm'][3]['initialized'] == False # don't create the motor in the constructor!
    robot.robotInit()
    
    # Check that the correct port was used
    assert hal_data['pwm'][3]['initialized'] == True
    assert hal_data['pwm'][3]['type'] == 'victor'    

def test_i5(robot, hal_data):
    '''Create a Victor motor controller object that uses PWM channel 4 (`motor4`)'''
    assert hal_data['pwm'][4]['initialized'] == False # don't create the motor in the constructor!
    robot.robotInit()
    
    # Check that the correct port was used
    assert hal_data['pwm'][4]['initialized'] == True
    assert hal_data['pwm'][4]['type'] == 'victor'
    
def test_i6(robot, hal_data):
    '''Create a digital input object on port 1'''
    assert hal_data['dio'][1]['initialized'] == False   # Don't create in the constructor!
    robot.robotInit()
    
    assert hal_data['dio'][1]['initialized'] == True    # digital input 1 initialized?
    assert hal_data['dio'][1]['is_input'] == True       # is it an input?

def test_i7(robot, hal_data):
    '''Create an analog input object on port 5  (`analog5`)'''
    assert hal_data['analog_in'][5]['initialized'] == False
    robot.robotInit()
    assert hal_data['analog_in'][5]['initialized'] == True

def test_i8(robot):
    '''Create a joystick object on port 1, and assign it to an instance variable
  named `stick`'''
    assert not hasattr(robot, 'stick')
    robot.robotInit()
    
    assert hasattr(robot, 'stick')
    assert isinstance(robot.stick, wpilib.Joystick)
    assert robot.stick.port == 0



def test_m1(robot):
    '''Define a `teleopPeriodic` method'''
    assert hasattr(robot, 'teleopPeriodic')
    assert inspect.ismethod(robot.teleopPeriodic)
    
    # If there's an error here, you didn't create a teleopPeriodic method
    assert inspect.getmodule(robot.teleopPeriodic) is not wpilib.iterativerobot

class StepController(object):
    '''
        Robot test controller object that enable/disables the 
        robot every 10 steps (approx 200ms in fake time)
    '''
    
    def __init__(self, control, on_step, init_old=0):
        '''constructor'''
        self.control = control
        self.step = 0
        self._on_step = on_step
        self.default = init_old
        self.old = {}
        
    def __call__(self, tm):
        '''Called when a new robot DS packet is received'''
        self.step += 1
        if self.step % 10 == 0:
            enabled = int((self.step / 10) % 2) == 1
            self.control.set_operator_control(enabled=enabled)
        return self._on_step(tm, self.step)
    
    def swap(self, new, name='default'):
        '''
            When we modify a sensor's value, the robot code will not actually
            change the corresponding output until on_step returns, so we use
            this to store the next expected value, and retrieve the last value
            that we expected them to output.
        '''    
        old = self.old.get(name, self.default)
        self.old[name] = new
        return old

def test_m2(robot, hal_data, control):
    '''During teleop, set the value of `motor1` to 1.0. When not in teleop, set 
  to 0'''
    
    hal_data['power']['vin_voltage'] = 12.0
    
    def _on_step(tm, step):
        if step <= 10:
            assert hal_data['pwm'][1]['value'] == 0
        elif step <= 20:
            assert abs(hal_data['pwm'][1]['value'] - 1.0) < 0.01    # motor set to 1.0? 
        elif step <= 30:
            assert hal_data['pwm'][1]['value'] == 0
        elif step < 40:
            assert abs(hal_data['pwm'][1]['value'] - 1.0) < 0.01    # motor set to 1.0? 
        else:
            return False
        
        return True
    
    c = StepController(control, _on_step)
    control.run_test(c)
    assert c.step == 40
    
def test_m3(robot, hal_data, control):
    '''During teleop, set the value of `motor2` to the value of the joystick's
  X axis'''
    
    hal_data['power']['vin_voltage'] = 12.0
    
    def _on_step(tm, step):
        
        # The joystick value is a random number
        j = random.random()
        hal_data['joysticks'][0]['axes'][0] = j
        
        # for each of these assertions:
        #   the motor value is hal_data[]...
        #   the expected value is returned from c.swap(..)
        
        if step < 10: # robot disabled
            assert abs(hal_data['pwm'][2]['value'] - c.swap(0)) < 0.01
            
        elif step < 20: # enabled
            assert abs(hal_data['pwm'][2]['value'] - c.swap(j)) < 0.01
             
        elif step < 30: # disabled
            assert abs(hal_data['pwm'][2]['value'] - c.swap(0)) < 0.01
            
        elif step < 40: # enabled
            assert abs(hal_data['pwm'][2]['value'] - c.swap(j)) < 0.01
            
        else:
            return False
        
        return True
    
    c = StepController(control, _on_step)
    control.run_test(c)
    assert c.step == 40

def test_m4(robot, hal_data, control):
    '''During teleop, if `dio1` is on, then set the value of `motor3` to the
  value of the joystick's Y axis. If it is off, then set the motor to 0.'''
    
    hal_data['power']['vin_voltage'] = 12.0
    
    def _on_step(tm, step):
        
        # The joystick value is a random number
        j = random.random()
        hal_data['joysticks'][0]['axes'][1] = j
        
        # toggle the digital io frequently
        if (step % 10) < 3:
            ne = 0
            hal_data['dio'][1]['value'] = False
        else:
            hal_data['dio'][1]['value'] = True
            ne = j
        
        # for each of these assertions:
        #   the motor value is hal_data[]...
        #   the expected value is returned from c.swap(..)
        
        if step < 10: # robot disabled
            assert abs(hal_data['pwm'][3]['value'] - c.swap(0)) < 0.01
            
        elif step < 20: # enabled
            assert abs(hal_data['pwm'][3]['value'] - c.swap(ne)) < 0.01
             
        elif step < 30: # disabled
            assert abs(hal_data['pwm'][3]['value'] - c.swap(0)) < 0.01
            
        elif step < 40: # enabled
            assert abs(hal_data['pwm'][3]['value'] - c.swap(ne)) < 0.01
            
        else:
            return False
        
        return True
    
    c = StepController(control, _on_step)
    control.run_test(c)
    assert c.step == 40

def test_s1(robot, hal_data, control):
    '''If the robot's battery voltage drops below 9 volts, set motors 1-3 to
  0 until the voltage rises above 10 volts or the robot is disabled (you must
  have completed m1-m4)'''
    
    # TODO: technically, the user shouldn't be setting the motor
    #       value more than once during a call to teleopPeriodic,
    #       but that would be annoying to check...
    
    hal_data['power']['vin_voltage'] = 12.0
    hal_data['dio'][1]['value'] = True
    
    # The joystick value is a random number
    j = random.random()
    hal_data['joysticks'][0]['axes'][0] = j
    hal_data['joysticks'][0]['axes'][1] = j
    hal_data['joysticks'][0]['axes'][2] = j
    
    def _on_step(tm, step):
        
        nv1 = 1
        nv2 = j
        
        if step < 10: # robot disabled
            nv1 = nv2 = 0
        
        elif step < 20: # enabled -- test transitions
                
            if step < 12: # normal operation
                pass
            elif step < 16: # low voltage! oh noes!
                nv1 = nv2 = 0
                hal_data['power']['vin_voltage'] = 8.0
                
            else: # back to normal
                hal_data['power']['vin_voltage'] = 12.0
             
        elif step < 30: # disabled
            nv1 = nv2 = 0
            
        elif step < 40: # enabled: don't let the voltage back up until disabled
            
            if step == 39:
                # low voltage! oh noes!
                nv1 = nv2 = 0
                hal_data['power']['vin_voltage'] = 8.0
        
        elif step < 50: # disabled
            nv1 = nv2 = 0
            hal_data['power']['vin_voltage'] = 12.0
        
        elif step < 60: # enabled: check to see that the motors went back on
            pass
        
        else:
            return False
        
        # Check that the motor values match
        v1 = c.swap(nv1, 'v1')  # motor 1
        v2 = c.swap(nv2, 'v2')  # motor 2,3
        
        assert abs(hal_data['pwm'][1]['value'] - v1) < 0.01
        assert abs(hal_data['pwm'][2]['value'] - v2) < 0.01
        assert abs(hal_data['pwm'][3]['value'] - v2) < 0.01
        
        return True
    
    c = StepController(control, _on_step)
    control.run_test(c)
    assert c.step == 60
    
def test_s2(robot, hal_data, control):
    '''During teleop, set motor4 to 0. If the joystick trigger is pressed and
  released, set motor4 to the value of the joystick's Z axis until the joystick
  trigger is pressed and released again. If the robot enters disabled
  mode, when the robot enters teleop it should not turn motor4 back on until
  the trigger has been pressed and released again'''
    
    def _on_step(tm, step):
        
        # set z-axis to a random value
        j = random.random()
        hal_data['joysticks'][0]['axes'][2] = j
        
        v = 0
        trig = False
        
        if step < 10: # robot disabled
            pass
        
        elif step < 20: # robot enabled
            if step < 12:
                pass
            elif step < 14: # triggered
                trig = True
            elif step < 16: # active
                v = j
            elif step < 18: # triggered
                trig = True
                v = j
            else:   # inactive again
                pass
            
        elif step < 30: # robot disabled
            pass
            
        elif step < 40: # robot enabled
            
            if step < 36:
                pass
            elif step < 39:
                trig = True
            else:
                v = j
                
        elif step < 50: # disabled
            pass
        
        elif step < 60:
            
            if step < 52:
                pass
            elif step < 55: # triggered
                trig = True
            elif step < 56: # active
                v = j
            elif step < 57: # triggered
                trig = True
                v = j
            else:   # inactive again
                pass
            
        else:
            return False
    
        # set trigger
        hal_data['joysticks'][0]['buttons'][1] = trig
    
        # Check motor value
        assert abs(hal_data['pwm'][4]['value'] - c.swap(v)) < 0.01
        
        return True
    
    c = StepController(control, _on_step)
    control.run_test(c)
    assert c.step == 60

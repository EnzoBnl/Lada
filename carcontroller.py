import RPi.GPIO as GPIO 
import time
import sys

class CarController:
    KEYS_TO_ACTION = {'p': "forward", 'm': "backward", 'a':"left", 'z': "right"}
    def __init__(self):
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(31,GPIO.OUT)
        GPIO.setup(33,GPIO.OUT)
        GPIO.setup(35,GPIO.OUT)
        GPIO.setup(37,GPIO.OUT)
        self.pwm_f = GPIO.PWM(31, 5)
        self.pwm_b = GPIO.PWM(33, 5)
        self.state = [0,0,0,0,0]  # f, b, l, r, speed
        print(id(self), "created")

    def forward(self, speed=1):
        """
        :param speed: float in ]0.25, 1]
        """
        print("forward with speed %=", speed*100, "%")
        self.stop_backward(speed)
        GPIO.output(31,GPIO.HIGH)
        self.state[0], self.state[1], self.state[4] = 1, 0, speed
        if speed != 1:
            self.pwm_f.start(speed*100)
        
    def stop_forward(self, speed=None):
        print("stop_forward")
        GPIO.output(31,GPIO.LOW)
        self.state[0] = 0
        if speed != 1:
            self.pwm_f.stop()

    def backward(self, speed=1):
        """
        :param speed: float in ]0.25, 1]
        """
        print("backwardforward with speed %=", speed*100, "%")
        self.stop_forward(speed)
        GPIO.output(33,GPIO.HIGH)
        self.state[0], self.state[1], self.state[4] = 0, 1, speed
        if speed != 1:
            self.pwm_b.start(speed*100)
        
    def stop_backward(self, speed=None):
        print("stop_backward")
        GPIO.output(33,GPIO.LOW)
        self.state[1] = 0
        if speed != 1:
            self.pwm_b.stop()

    def left(self, _=None):
        print("left")
        self.stop_right()
        GPIO.output(35,GPIO.HIGH)
        self.state[2], self.state[3] = 1, 0
        
    def stop_left(self, _=None):
        print("stop_left")
        GPIO.output(35,GPIO.LOW)
        self.state[2] = 0

    def right(self, _=None):
        print("right")
        self.stop_left()
        GPIO.output(37,GPIO.HIGH)
        self.state[2], self.state[3] = 0, 1
        
    def stop_right(self, _=None):
        print("stop_right")
        GPIO.output(37,GPIO.LOW)
        self.state[3] = 0
        
    def stop(self):
        print("stop")
        self.stop_right()
        self.stop_left()
        self.stop_forward()
        self.stop_backward()
    
    def resume_from_state(self, state):
        if state[0] == 1:
            self.forward(state[4])
        elif state[1] == 1:
            self.backward(state[4])
        if state[2] == 1:
            self.left()
        elif state[3] == 1:
            self.right()
    
    def malus(self, seconds):
        state_before_malus = self.state[:]
        self.stop()
        time.sleep(seconds)
        self.resume_from_state(state_before_malus)
    
    def __del__(self):
        print("deleting", id(self))
        self.stop()
        GPIO.cleanup()
        print(id(self), "deleted")

    def __exit__(self):
        del self

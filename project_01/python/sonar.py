"""
--------------------------------------------------------------------------
Sonar
--------------------------------------------------------------------------
License:   
Copyright 2019 Theodore Hoisington

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

Uses the adafruit_hcsr04 library to measure distances with 
two HC-SR04 ultrasonic sensors

"""

import time
import board
from adafruit_hcsr04 import HCSR04
import Adafruit_BBIO.GPIO as GPIO
import display
import threading


BUTTON0 = "P2_3"

GPIO.setup(BUTTON0, GPIO.IN)


#HCSR04(trigger pin, echo pin)
sonar0 = HCSR04(board.P2_2, board.P2_4)
sonar1 = HCSR04(board.P2_6, board.P2_8)

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------

left_sonar = 0
right_sonar = 0
passed = True
#Value that is the max distance for the device.
running_average = 0
distance_buffer = 10
reset_distance = 3

#Initializing display values
num_inside = 0
total_entered = 0
total_exited = 0


def check_button():
    """
    On button press it resets the values on display.
    """
    global num_inside
    global total_entered
    global total_exited
    
    if GPIO.input(BUTTON0) == 0:
        
        num_inside = 0
        total_entered = 0
        total_exited = 0
        display.update_image()
        return True
    return False
    
#------------------------

count = 1
value_list = []
def keep_average():
    """Gets average distance of first 20 sensor readings"""
    global count
    global value_list
    global running_average
    total = 0
    while count < 20:
        value_list.append(sonar0.distance)
        time.sleep(.1)
        
        count += 1
    for num in value_list:
        total += num    
    running_average = total / len(value_list)
    print(running_average)
    
def ultrasonic():
    """Constantly updates left_sonar and right_sonar with sensor vales"""
    global left_sonar
    global right_sonar
    global running_average
    
    keep_average()
    
    try:
        while True:
            try:
                
                left_sonar = int(sonar0.distance)
                print("0:", left_sonar)
                
                time.sleep(.1)
                right_sonar = int(sonar1.distance)
                print("1:", right_sonar)
                
                time.sleep(.1)
                sonar_algorithm(left_sonar,right_sonar)
            except RuntimeError:
                pass
    except KeyboardInterrupt:
        pass

def exit():
    global passed
    while(True):
    
    
        while left_sonar < (running_average - 10) or right_sonar < (running_average - 10):
            passed == False
        passed = True
        #jingle()
        #print("passed")
       
        display.update_image()

def sonar_algorithm(left,right):
    """Checks to see which direction a person is entering from"""
    global num_inside
    global total_entered
    global total_exited
    global passed
    
    #The exit thread is constantly updating the values for passed
    if left < running_average - 10 and passed == True:
        print("entered left")
        passed = False
        total_entered += 1
        num_inside += 1
    elif right < running_average - 10 and passed == True:
        print("entered right")    
        passed = False
        total_exited += 1
        num_inside += -1
        

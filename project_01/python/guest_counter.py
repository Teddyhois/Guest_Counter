"""
--------------------------------------------------------------------------
Guest Counter
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

Uses Ultrasonic sensors to detect if a person has passed by the device.
When someone passes the device, a tone plays and the values on the OLED display
are updated to represent how many people are inside the room, have entered, and 
have exited.

"""
import display
import sonar
import time
import threading
import Adafruit_BBIO.PWM as PWM

#setup the speaker
piezo_pin = "P2_1"

#Piezo Note
NOTE_C5  = 523

def play_note(Note, Length):
    """
    Plays a given note for a given length.
    """
    PWM.start(piezo_pin, 50, Note)
    #time.sleep(Length)
    

    
    
#Creating Threads
#Thread for reading sensor values
readings = threading.Thread(name = 'reading',target = sonar.ultrasonic)
#Thread for checking if someone has passed through the device
exit = threading.Thread(name = 'exit',target = sonar.exit)
#Thread to initialize the screen and display the loading animation
screen_init = threading.Thread(name = 'init', target = display.init_file)
#Thread to play jingle

    
def main():
    #clear PWM
    PWM.stop(piezo_pin)
    PWM.cleanup()
    
    #initialize the screen and display the loading animation
    screen_init.start()
    #starts the ultrasonic readings
    readings.start()
    #sleeps the program for 10 seconds to allow the program to calculate the max distance/running average
    time.sleep(10)
    #Starts the function to check if someone is passed the sensors.
    exit.start()

    while(True):
        sonar.check_button()
        
        #If someone is in the sensors, the speaker will play tone
        if sonar.passed == False:
            play_note(NOTE_C5,.1)
        else:
            PWM.stop(piezo_pin)
            PWM.cleanup()
        pass
        
if __name__ == '__main__':
    main()









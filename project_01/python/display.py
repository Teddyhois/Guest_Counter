"""
--------------------------------------------------------------------------
Display
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

Uses the pillow library to create and save new images to send to the 
Mikroe OLED C Click board for display

"""
from PIL import Image, ImageDraw, ImageFont
import os
import time
import sonar


#Sets the screen to black initially
os.system("dd if=/dev/zero of=/dev/fb0 > /dev/null 2>&1")


local_num_inside = 0
local_total_entered = 0
local_total_exited = 0

num_inside_pos = (2, 25)
total_entered_pos = (2, 45)
total_exited_pos = (2, 65)

fontname = "arial.ttf"
txt = Image.new('RGB', (100,130), (255, 255, 255))
font = ImageFont.truetype(fontname, 17)
write = ImageDraw.Draw(txt)  

def new_PIL():
    """Resets txt which is the new image being written on"""
    global txt
    txt = Image.new('RGB', (100,130), (255, 255, 255))
    write = ImageDraw.Draw(txt)
    
def write_text(location, text):
    """Add string text to the image at the inputted location"""
    prefix = ""
    if location == num_inside_pos: 
        prefix = "Inside: "
    if location == total_entered_pos: 
        prefix = "Entered: "
    if location == total_exited_pos: 
        prefix = "Exited: "

    write = ImageDraw.Draw(txt)
    write.text(location, (prefix + text), font=font, fill = (0,0,0))
""" unused?
def write_other(location, text):
    """"""
    write.text(location, text, font=font, fill = (0,0,0))
   """ 
def setup_screen():
    """Creates initial image to be displayed on screen after loading"""
    write_text((2,0), "Guest Count")
    write_text(num_inside_pos, "0")
    write_text(total_entered_pos, "0")
    write_text(total_exited_pos, "0")


def load_screen(num):
    """Creates graphic for loading screen"""
    write_text((2,0), "Guest Count")
    write_text((2, 20*num), "LOADING")
    
def flip_image(image_path, saved_location):
    """
    Flip or mirror the image
 
    @param image_path: The path to the image to edit
    @param saved_location: Path to save the cropped image
    """
    image_obj = Image.open(image_path)
    rotated_image = image_obj.transpose(Image.FLIP_LEFT_RIGHT)
    rotated_image.save(saved_location)

def send_image():
    """Sends a completed image to the screen using terminal commands"""
    txt.save('img.png') 
    flip_image('img.png', 'flipped_img.jpg')
    os.system("sudo fbi -T 1 -a flipped_img.jpg")
    
def rewrite():
    """Update the counters"""
    write_text((2,0), "Guest Count")
    write_text(num_inside_pos, str(sonar.num_inside))
    write_text(total_entered_pos, str(sonar.total_entered))
    write_text(total_exited_pos, str(sonar.total_exited))
    
def update_image():
    """Checks if any of the numbers have changed, then rewrites and updates the image"""
    new_PIL()
    global local_num_inside
    global local_total_entered
    global local_total_exited
    new_image_bool = False
    if local_num_inside != sonar.num_inside:
        
        local_num_inside = int(sonar.num_inside)
        new_image_bool = True
    if local_total_entered != sonar.total_entered:
        
        local_total_entered = int(sonar.total_entered)
        new_image_bool = True
    if local_total_exited != sonar.total_exited:
     
        local_total_exited = int(sonar.total_exited)    
        new_image_bool = True
    if new_image_bool == True:
        rewrite()
        send_image()
        

def ready(): 
    """Screen following the Loading Screen"""
    new_PIL()
    #setup_screen()
    rewrite()
    send_image()
def init_file():
    """Initializes screens"""
    
    load_screen(1)
    send_image()
    time.sleep(3)
    load_screen(2)
    send_image()
    time.sleep(3)
    load_screen(3)
    send_image()
    time.sleep(3)
    load_screen(4)
    send_image()
    time.sleep(1)
    ready()
    







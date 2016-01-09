# OLEDclock.py

# This program interfaces with one of Adafruit's OLED displays and a Raspberry Pi (over SPI). It displays the current 
# date (Day, Month, Year) and then scrolls to the current time. The program waits for 2 seconds between scrolls.

# Example code from the py-gaugette library... Commented by The Raspberry Pi Guy

# Imports the necessary modules
import gaugette.ssd1306
import time
import sys
from PIL import Image

# Sets up our pins again
RESET_PIN = 15
DC_PIN    = 16
width = 128
height = 32

led = gaugette.ssd1306.SSD1306(reset_pin=RESET_PIN, dc_pin=DC_PIN)
led.begin()
led.clear_display()

offset = 0 # flips between 0 and 32 for double buffering

# While loop has bulk of the code in it!
image = Image.open("/home/torben/OLED/python-examples/fischer.png")
image_r = image.resize((width,height), Image.BICUBIC)
image_bw = image_r.convert("1")

var1 = True

while True:

    # write the current time to the display on every other cycle
    if offset == 0:
        if var1:
            text1 = "frisch,"
            led.draw_text2(0,0,text1,1)
            led.display()
            time.sleep(1)
            text2 = "frisch, frischer,"
            led.draw_text2(0,0,text2,1)
            led.display()
            time.sleep(1)
            text3 = "Fischer !!!"
            led.draw_text2(0,16,text3,2)
        else:
            text1 = "Immer frischer"
            led.draw_text2(0,0,text1,1)
            led.display()
            time.sleep(1)
            text2 = "Immer frischer beim"
            led.draw_text2(0,0,text2,1)
            led.display()
            time.sleep(1)
            text3 = "Fischer !!!"
            led.draw_text2(0,16,text3,2)
            
        led.display()
        
        #text = time.strftime("%A")
        #led.draw_text2(0,0,text,2)
        #text = time.strftime("%e %b %Y")
        #led.draw_text2(0,16,text,2)
        #text = time.strftime("%X")
        #led.display()
        time.sleep(2)
        led.clear_display()
    else:
        # Finally this bit maps each pixel (depending on whether it is black or white) to the display.
        # Note here we are not using the text command like in previous programs. We use led.draw_pixel:
        # That way we can individually address each pixel and tell it to be either on or off (on = white, off = black)
        for y in range(height):
            for x in range(width):
                led.draw_pixel(x,y+32,bool(int(image_bw.getpixel((x,y)))))
            led.display()
            time.sleep(0.1)

        time.sleep(2)
        var1 = not var1
        led.clear_display()

    # vertically scroll to switch between buffers
    for i in range(0,32):
        offset = (offset + 1) % 64
        led.command(led.SET_START_LINE | offset)
        #time.sleep(0.01)

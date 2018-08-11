import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

# Test the field loop
# This looks for a field pulse and flickers the LED at 25Hz
# if there is a video signal being input.
# You need to set up the video chips first using
# ./vbit-i2c.sh
# or
# python 7113.py 
# python 7120.py 

#define GPIO_FLD 3 -> Broadcom 22
#define GPIO_CSN 5 -> Broadcom 24
#define GPIO_MUX 6 -> Broadcom 25
#define GPIO_LED 7 -> Broadcom 4

# setup the I/O to VBIT
GPIO.setup(4, GPIO.OUT)
GPIO.setup(22, GPIO.IN)

try:
  while True:
    GPIO.wait_for_edge(22, GPIO.RISING) # Look for the field pulse
    GPIO.output(4, GPIO.HIGH) # blink the LED
    GPIO.wait_for_edge(22, GPIO.FALLING) # Look for the field pulse
    GPIO.output(4, GPIO.LOW) # blink the LED

except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
  print("Keyboard interrupt")    

except:
   print("some error") 

finally:
   print("clean up") 
   GPIO.cleanup() # cleanup all GPIO 

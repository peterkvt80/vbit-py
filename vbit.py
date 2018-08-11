#!/usr/bin/env python

# Teletext Stream to VBIT hardware
# Copyright (c) 2018 Peter Kwan
# MIT License.

import time
import RPi.GPIO as GPIO

from saa7120 import saa7120
from saa7113 import saa7113

GPIO.setmode(GPIO.BCM)

saa7120()
saa7113()

GPIO_FLD=22 #define GPIO_FLD 3 -> Broadcom 22
GPIO_CSN=24 #define GPIO_CSN 5 -> Broadcom 24
GPIO_MUX=25 #define GPIO_MUX 6 -> Broadcom 25
GPIO_LED=4 #define GPIO_LED 7 -> Broadcom 4

# setup the I/O to VBIT
GPIO.setup(4, GPIO.OUT)
GPIO.setup(22, GPIO.IN)

def fieldEdge(self):
  field= GPIO.input(GPIO_FLD)
  GPIO.output(GPIO_LED, field)

print 'System started'

#try:

GPIO.add_event_detect(GPIO_FLD, GPIO.BOTH, callback=fieldEdge) # Look for the field pulse

#except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
#  print("Keyboard interrupt")    

#except:
#   print("some error") 

#finally:
#   print("clean up") 
#   GPIO.cleanup() # cleanup all GPIO 

while True:
  time.sleep(5)

GPIO.cleanup()

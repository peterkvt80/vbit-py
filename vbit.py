#!/usr/bin/env python3

# Teletext Stream to VBIT hardware
# Copyright (c) 2018 Peter Kwan
# MIT License.

# Release 1.0.1

# System libraries
import sys
import time
import RPi.GPIO as GPIO

# Local libraries
from saa7120 import saa7120
from saa7113 import saa7113
from fifo import Fifo
from buffer import Buffer

# Use Broadcom pin numbering
GPIO.setmode(GPIO.BCM)

# Globals
packetSize=42 # The input stream packet size. Does not include CRI and FC

# Setup
saa7120()
saa7113()

# Objects
fifo=Fifo()

# buffer stuff
head=0
tail=0
BUFFERS = 2
buf = [0] * BUFFERS
for i in range(BUFFERS):
  buf[i]=Buffer()

countdown=BUFFERS-1
if countdown<1:
  countdown=1

GPIO_FLD=22 #define GPIO_FLD 3 -> Broadcom 22
GPIO_CSN=24 #define GPIO_CSN 5 -> Broadcom 24
GPIO_MUX=25 #define GPIO_MUX 6 -> Broadcom 25
GPIO_LED=4 #define GPIO_LED 7 -> Broadcom 4

# setup the I/O to VBIT
GPIO.setup(GPIO_LED, GPIO.OUT)
GPIO.setup(GPIO_FLD, GPIO.IN)

# This is the interrupt routine that triggers on each field
def fieldEdge(self):
  global buf
  global GPIO_LED
  global GPIO_FLD
  global tail
  global head
  GPIO.output(GPIO_LED, GPIO.HIGH)
  ##### Wait until the vbi has been transmitted #####
  time.sleep(0.0016) # Between Suspend while 1.6 ms
  # vbi is done. load the next field
  fifo.spiram.deselect()
  GPIO.output(GPIO_LED, GPIO.LOW)
  # we are done with the buffer
  if head == tail: # Source buffer was not ready. We're going to need a faster Pi.
    print ('?') 
  ##### Copy from the source buffer to the fifo #####
  fifo.fill()
  fifo.spiram.spi.writebytes(buf[tail].field)
  if len(buf[tail].field)!=720:    # The source buffer was not full. Did we run out of time?
    print ('x',len(buf[tail].field),end='') # If you see this, we have failed
  # Done with this buffer 
  tail=(tail+1)%BUFFERS
  # Get ready to transmit. Do it now while we have plenty of time
  fifo.transmit()

print ('vbit.py System started')

try:
  # This thread will be used to read the input stream into a field buffer
  while True:
    ###### Wait while the buffers are full ######
    while (head+1)%BUFFERS == tail:
      time.sleep(0.0001)
    ###### load the next buffer ######
    buf[head].clearBuffer()
    # load a field of 16 vbi lines
    for line in range(16):  
      # packet=file.read(packetSize) # file based version
      packet=sys.stdin.buffer.read(packetSize) # read binary from stdin
      buf[head].addPacket(packet)
      if packet == '':
        print ('really bad problem that needs fixing')      
    ##### step to the next buffer
    head=(head+1)%BUFFERS
    
    # Sequence the startup so we get fully buffered before we start transmitting
    if countdown==1: # now the buffer is full we can enable interrupts
      GPIO.add_event_detect(GPIO_FLD, GPIO.BOTH, callback=fieldEdge) # Look for the field pulse   
    if countdown>0:
      countdown-=1

except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
  print("Keyboard interrupt")    

except:
   print("some error") 

finally:
   print("clean up") 
   GPIO.cleanup() # cleanup all GPIO 

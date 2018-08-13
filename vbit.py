#!/usr/bin/env python3

# Teletext Stream to VBIT hardware
# Copyright (c) 2018 Peter Kwan
# MIT License.

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
vbiActive=False # True while the vbi is busy. The vbi is using the fifo
bufferReady=False # When a field is loaded this goes high. Set low when copied to fifo 
packetSize=42 # The input stream packet size. Does not include CRI and FC
oddField = True
countdown=2

# Setup
saa7120()
saa7113()

# Objects
fifo=Fifo()
bufOdd=Buffer()
bufEven=Buffer()

GPIO_FLD=22 #define GPIO_FLD 3 -> Broadcom 22
GPIO_CSN=24 #define GPIO_CSN 5 -> Broadcom 24
GPIO_MUX=25 #define GPIO_MUX 6 -> Broadcom 25
GPIO_LED=4 #define GPIO_LED 7 -> Broadcom 4

# setup the I/O to VBIT
GPIO.setup(GPIO_LED, GPIO.OUT)
GPIO.setup(GPIO_FLD, GPIO.IN)

# This is the interrupt routine that triggers on each field
def fieldEdge(self):
  global bufferReady
  global oddField
  global vbiActive
  global bufOdd
  global bufEven
  global GPIO_LED
  global GPIO_FLD

  oddField = GPIO.input(GPIO_FLD) # Use this to double buffer
  fifo.transmit(oddField)
  GPIO.output(GPIO_LED, GPIO.HIGH)
  vbiActive = True
  time.sleep(0.0016) # Between Suspend while 1.6 ms
  # VBIT should be ended now
  fifo.spiram.deselect()
  GPIO.output(GPIO_LED, GPIO.LOW)
  vbiActive = False
  # we are done with the buffer
  if bufferReady!=True: # @todo if the buffer is not ready, what can we do? Loop a bit?
    print ('?') 
  # fill the other field in the fifo
  fifo.fill(oddField)
  if oddField:
    if len(bufEven.field)==720:
      fifo.spiram.spi.writebytes(bufEven.field)
    else:
      print ('o',end='') # If you see this, we have failed
  else:
    if len(bufOdd.field)==720:
      fifo.spiram.spi.writebytes(bufOdd.field)
    else:
      print ('e',end='')
  fifo.spiram.deselect()
  # Done with this buffer 
  bufferReady = False

print ('vbit.py System started')

#try:


#except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
#  print("Keyboard interrupt")    

#except:
#   print("some error") 

#finally:
#   print("clean up") 
#   GPIO.cleanup() # cleanup all GPIO 

# This thread will be used to read the input stream into a field buffer
counter = 0
while True:
  # Wait until the buffer has been used
  while bufferReady==True:
    time.sleep(0.0005)
  odd=oddField
  print ('.', end='') # for main loop
  counter+=1
  if (counter % 50) == 0:
    print()
  if odd:
    bufEven.clearBuffer()
  else:
    bufOdd.clearBuffer()
  # load a field of 16 vbi lines
  for line in range(16):  
    # packet=file.read(packetSize) # file based version
    packet=sys.stdin.buffer.read(packetSize) # read binary from stdin
    if odd:
      bufEven.addPacket(packet)
    else:
      bufOdd.addPacket(packet)
    if packet == '':
      break      
  # field is loaded
  bufferReady = True
  
  # Sequence the startup so we get fully buffered before we start transmitting
  if countdown==2: # Mark the buffer as not ready and load the other field
    bufferReady = False
    oddField = not oddField
  if countdown==1: # now the buffer is full we can enable interrupts
    GPIO.add_event_detect(GPIO_FLD, GPIO.BOTH, callback=fieldEdge) # Look for the field pulse   
  if countdown>0:
    countdown-=1

  # print ("*****FIELD******* size=",len(buf.field))
  #buf.printPacket()
  

GPIO.cleanup()

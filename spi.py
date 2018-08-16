#!/usr/bin/env python3

# SPI druver for Teletext Stream to VBIT hardware
# Copyright (c) 2018 Peter Kwan
# MIT License.

import spidev
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

class SPIRAM: # spiram is used as a hardware buffer  to play out the teletext packets.
  print ("SPIRAM created")
  # Instruction set of the spiram
  
  # modes
  READ	=	0x03
  WRITE = 0x02
  RDSR = 0x05
  WRSR	= 0x01
  
  # status
  MODE_BYTE = 0x00
  MODE_PAGE = 0x80
  MODE_SEQUENTIAL = 0x40
  
  def __init__(self, bus, device):
    GPIO.setup(24, GPIO.OUT) # GPIO_CSN. Chip select is bit banged because reasons
    self.deselect() # disable the SPIRAM
    self.bus = bus
    self.device = device
    self.spi=spidev.SpiDev()
    self.spi.open(bus, device)
    # speed depends on your cable. 
    # If you have data corruption due to a
    # long cable or ropey ribbon cable, try 122000
    # If you have a shorter cable you can go faster. 
    # More speeds at www.takaitra.com/posts/492
    self.spi.max_speed_hz=7800000 # normal speed
    # self.spi.max_speed_hz=488000 # slowest that will work

  # chip select
  def toggleCS(self): # /// Toggle the chip select prior to setting state
    # deselect and reselect the chip prior to setting it up
    GPIO.output(24, GPIO.HIGH) # CSN
    time.sleep(0.000110)
    GPIO.output(24, GPIO.LOW)
  def deselect(self):
    GPIO.output(24, GPIO.HIGH) # disable the spiram CSN
  # addressing
  # /// mode - A mode value SPIRAM_MODE_*
  # /// address - 0..32k assuming a 23K256 memory
  def setAddress(self, mode, address): #/// Set the read/write mode and address
    self.toggleCS()
    buf=[mode,(address>>8) & 0xff, address & 0xff]
    self.spi.writebytes(buf)
  def setStatus(self, status):
    self.toggleCS()
    buf=[SPIRAM.WRSR, status]
    self.spi.writebytes(buf)
    self.deselect()
 
#try:
  # exercise the interface 
#spiram=SPIRAM(0,0) # create an instance
#spiram.setStatus(SPIRAM.MODE_SEQUENTIAL) ## set the addressing mode

  # write a small block
#spiram.setAddress(SPIRAM.WRITE,0x100)
#b=[65,66,67,68,77,77,77,77,77,77,77,55,77,77,77]
#spiram.spi.writebytes(b)
#spiram.deselect()

  # read it back. It should match
#spiram.setAddress(SPIRAM.READ,0x100)
#print (spiram.spi.readbytes(len(b)))
#spiram.deselect()

#except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
#  print("Keyboard interrupt")    

#except:
   #print("some error") 

#finally:
   #print("clean up") 
   #GPIO.cleanup() # cleanup all GPIO 
   
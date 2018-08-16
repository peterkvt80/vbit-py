#!/usr/bin/env python3

# Buffering test vbit-test-py
# ../vbit2/vbit2 2> /dev/null | ./vbit-test.py
# Copyright (c) 2018 Peter Kwan
# MIT License.

import sys

def reverse(x):
  x = ((x & 0xF0) >> 4) | ((x & 0x0F) << 4)
  x = ((x & 0xCC) >> 2) | ((x & 0x33) << 2)
  x = ((x & 0xAA) >> 1) | ((x & 0x55) << 1)
  return x  

def reverseBuffer(buf):
  b=bytearray()
  for ch in buf:
    b.append(reverse(ch)) 
  return b

class Buffer:
  clockFrame = bytearray(b'\x55\x55\x27') # clock run-in and framing code
#  clockFrame = b'\xaa\xaa\xe4' # clock run-in and framing code (reversed?)
  print ('Buffer created')
  def __init__(self):
    self.field=bytearray()
    self.count = 0 # The packet count
  def addPacket(self,pkt):
  #horrible suspicion that all characters need to be endian reversed
    # could add test for 42 character packets
    # Append the new packet
 #   for i in range(len(Buffer.clockFrame)):
 #     self.field.extend(reverse(Buffer.clockFrame[i]))
 #   for i in range(len(pkt)):
 #     self.field.extend(reverse(pkt))
    self.field.extend(reverseBuffer(Buffer.clockFrame))
    self.field.extend(reverseBuffer(pkt))
    self.count+=1
  def clearBuffer(self):
    self.field=bytearray()
    self.count = 0 # The packet count
  def printPacket(self):
      print (self.field)
  def reverseBuffer(self,buf):
    print (type(buf))

# test for bit order reverse    
#buf=Buffer()
#reverseBuffer(Buffer.clockFrame)
 
      

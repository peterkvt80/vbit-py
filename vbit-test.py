#!/usr/bin/env python3

# Buffering test vbit-test-py
# ../vbit2/vbit2 2> /dev/null | ./vbit-test.py
# Copyright (c) 2018 Peter Kwan
# MIT License.

import sys

class Buffer:
  clockFrame = b'\x55\x55\x27' # clock run-in and framing code
  def __init__(self):
    self.field=bytearray()
    self.count = 0 # The packet count
  def addPacket(self,pkt):
    # could add test for 42 character packets
    # Append the new packet
    self.field.extend(Buffer.clockFrame)
    self.field.extend(pkt)
    self.count+=1
  def clearBuffer(self):
    self.field=bytearray()
    self.count = 0 # The packet count
  def printPacket(self):
      print (self.field)

#  main
packetSize=42
#filename='data.txt'
#file=open(filename, "rb")
buf = Buffer()
for field in range(4):
  for line in range(16):  
    # packet=file.read(packetSize)
    packet=sys.stdin.buffer.read(packetSize)
    print (packet)
    buf.addPacket(packet)
    if packet == '':
      break
  print ("*****FIELD*******")
  buf.printPacket()
  buf.clearBuffer()


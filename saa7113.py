#!/usr/bin/env python

import smbus

#define SLAVE_ADDRESS_7113    (0x4a >> 1)
#define SLAVE_ADDRESS_7121    (0x88 >> 1)
# Set up the registers of a vbit Pi saa7113 video decoder
# 
def saa7113():
  bus=smbus.SMBus(1)
  bus.write_byte_data(0x25, 0x01, 0x08) # 0x01,0x08, // increment delay - 0x08 recommended 
  bus.write_byte_data(0x25, 0x02, 0xc0) # 0x02,0xc0 # // analog control 1 - 0xc0 Mode 0 CVBS, input pin 4, 9 bit hyst off, amp and anti-alias active
  bus.write_byte_data(0x25, 0x03, 0x13) # 0x03,0x33, // analog control 2 - AGC fixed during video and  blanking. Probably NOT what we want!
  bus.write_byte_data(0x25, 0x04, 0x00) # 0x04,0x00, // analog control 3 - Static Gain set to 0. Channel 1
  bus.write_byte_data(0x25, 0x05, 0x00) # 0x05,0x00, // analog control 4 - Static Gain channel 2 (Don't care)
  bus.write_byte_data(0x25, 0x06, 0xe9) # 0x06,0xe9, // horiz sync start - e9 recommnded
  bus.write_byte_data(0x25, 0x07, 0x0d) # 0x07,0x0d, // horiz sync stop - 0d recommended
  bus.write_byte_data(0x25, 0x08, 0x98) # 0x08,0x98, // sync control - vertical noise=normal, PLL closed, Fast locking mode, field toggle on interlace, field detection AUFD 
  bus.write_byte_data(0x25, 0x09, 0x01) # 0x09,0x01, // luminance control - aperture factor = 0.25, update agc per line,active luma (correct?), bandpass 4MHz, prefilter bypassed, chroma trap set for CVBS
  bus.write_byte_data(0x25, 0x0a, 0x80) # 0x0a,0x80, // luminance brightness - Set to ITU level
  bus.write_byte_data(0x25, 0x0b, 0x47) # 0x0b,0x47, // luminance contrast - Set to ITU level
  bus.write_byte_data(0x25, 0x0c, 0x40) # 0x0c,0x40, // chrominance saturation - Set to ITU level
  bus.write_byte_data(0x25, 0x0d, 0x00) # 0x0d,0x00, // chrominance hue - Phase control
  bus.write_byte_data(0x25, 0x0e, 0x01) # 0x0e,0x01, // chrominance control - Normal bandwidth 800kHz, PAL
  bus.write_byte_data(0x25, 0x0f, 0x2a) # 0x0f,0x2a, // chrominance gain control ?
  bus.write_byte_data(0x25, 0x10, 0x00) # 0x10,0x00, // format/delay control - Mainly ITU 656
  bus.write_byte_data(0x25, 0x11, 0x0c) # 0x11,0x0c, // output control 1
  bus.write_byte_data(0x25, 0x12, 0xa1) # 0x12,0xa1, // output control 2 - Default 0x01. Controls RTS0 (don't care) and RTS1 - ODD/EVEN Field
  bus.write_byte_data(0x25, 0x13, 0x00) # 0x13,0x00, // output control 3 - Analog test select (don't care)

  bus.write_byte_data(0x25, 0x15, 0x00) # 0x15,0x00, // VGATE start - Probably don't care
  bus.write_byte_data(0x25, 0x16, 0x00) # 0x16,0x00, // VGATE stop - Probably don't care
  bus.write_byte_data(0x25, 0x17, 0x00) # 0x17,0x00, // MSBs for VGATE control - Probably don't care
  #// 0x1f,0x, decoder status byte. readonly
  bus.write_byte_data(0x25, 0x40, 0x02) # 0x40,0x02, // slicer control 1 - Probably don't care
  #// 0x41 to 0x57 // line control register 2 to 24  - Don't care
  bus.write_byte_data(0x25, 0x58, 0x00) # 0x58,0x00, // programmable framing code- Don't care
  bus.write_byte_data(0x25, 0x59, 0x54) # 0x59,0x54, // horizontal offset for slicer - don't care
  bus.write_byte_data(0x25, 0x5a, 0x07) # 0x5a,0x07, // vertical offset for slicer - Don't care
saa7113()
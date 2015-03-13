#!/usr/bin/python

# This is a library for providing access to Kwikset Smartcode Locks via UART
# The h/w interface is 3.3V 9600 baud 8N1 standard UART
# This is more  of a protocol encoder/decoder though

import kwikset_protocol
import serial
import os
import threading

ser = None

def setup_arduinobreakout_pins():
    # First let's make sure all the pins are exported for config
    os.system("echo 214 > /sys/class/gpio/export")
    os.system("echo 248 > /sys/class/gpio/export")
    os.system("echo 249 > /sys/class/gpio/export")
    os.system("echo 216 > /sys/class/gpio/export")
    os.system("echo 217 > /sys/class/gpio/export")
    # Shouldn't need this as serial port opening should take care of it
    #os.system("echo 130 > /sys/class/gpio/export")
    #os.system("echo 131 > /sys/class/gpio/export")
    # Next lets Tristate all the outputs
    os.system("echo low > /sys/class/gpio/gpio214/direction")
    # Next lets setup the buffer/level shifter I/O directions
    os.system("echo low > /sys/class/gpio/gpio248/direction")
    os.system("echo high > /sys/class/gpio/gpio249/direction")
    # Disable the external pull ups
    os.system("echo low > /sys/class/gpio/gpio216/direction")
    os.system("echo low > /sys/class/gpio/gpio217/direction")
    # Set Edison I/O directions (shouldn't be necessary, but here for posterity
    #os.system("echo in > /sys/class/gpio/gpio130/direction")
    #os.system("echo out > /sys/class/gpio/gpio131/direction")
    # Remove tristate 
    os.system("echo high > /sys/class/gpio/gpio214/direction")
    
def setup_serial():
    global ser
    # Initialize serial port
    ser = serial.Serial("/dev/ttyMFD1",9600,timeout=0)
    
def init_kwikset_lock():
    global ser
    if ser == None:
        print "Serial Port not setup"
        return False
    ser.write(kwikset_protocol.generate_init_packet())

def unlock():
    global ser
    if ser == None:
        print "Serial Port not setup"
        return False
    ser.write(kwikset_protocol.generate_unlock_packet())
    
def lock():
    global ser
    if ser == None:
        print "Serial Port not setup"
        return False
    ser.write(kwikset_protocol.generate_lock_packet())       
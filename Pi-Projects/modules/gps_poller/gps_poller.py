#! /usr/bin/python
# Written by Varun Verma 23 Aug 2018
# Reference to Dan Mandle http://dan.mandle.me September 2012
# License: GPL 2.0
 
from gps import *
import threading

class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self.gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
 
  def run(self):
    try:
      while self.running:
        self.current_value = self.gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
    except StopIteration:
      pass

  def get_current_value(self):
    return self.gpsd

  def stop_polling(self):
    self.running = False

  def get_polling_status(self):
    return self.running
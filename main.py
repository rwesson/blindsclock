#!/usr/bin/python

import datetime
import math
import random

from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import sp
from kivy.properties import NumericProperty,ObjectProperty,StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.stacklayout import StackLayout
from kivy.utils import platform
from kivy.app import App
from threading import Thread

Builder.load_file("kv.kv")
#Config.set('kivy', 'exit_on_escape', '0')

# set up platform-specific things

if platform=="android":
  from android.permissions import request_permissions, Permission
  from kivy.core.audio import audio_android
  request_permissions([Permission.READ_EXTERNAL_STORAGE,Permission.WRITE_EXTERNAL_STORAGE])

else:
  Window.size=(400,780)

def format_time(s,h=False):
  if h:
    return "%02d : %02d : %02d"%(math.floor(s/3600),math.floor(s%3600/60),s%60)
  return "%02d : %02d"%(math.floor(s/60),s%60)

class MainView(StackLayout):
  def __init__(self,*args,**kwargs):
    super().__init__(**kwargs)
# set up blinds, display initial values
    self.smallblinds=[ 25,50,100,150,200,300,400,500,600,800,1000,1500,2000,3000,4000,5000 ]

# set up trackers

    self.blindlevel=0
    self.blindsrunning=False
    self.blindsinterval=900
    self.gametime=0
    self.time=self.blindsinterval

# get time, set initial display
    self.ids.timeuntilnextblinds.text=format_time(self.blindsinterval)

# display blinds
    self.display_blinds()

# start clock
    Clock.schedule_interval(self.update_display,1)

  def display_blinds(self):
    self.ids.currentblinds.text=("%d / %d"%(self.smallblinds[self.blindlevel],self.smallblinds[self.blindlevel]*2))
    self.blindlevel=min(self.blindlevel,len(self.smallblinds)-1)
    if self.blindlevel+1<len(self.smallblinds):
      self.ids.nextblinds.text=("next blinds: %d / %d"%(self.smallblinds[self.blindlevel+1],self.smallblinds[self.blindlevel+1]*2))
    else:
      self.ids.nextblinds.text="NO MORE BLIND RAISES"

  def update_display(self,interval):
    if not self.blindsrunning:
      return

    self.ids.timeuntilnextblinds.text=format_time(self.time)
    self.ids.timeuntilnextblinds.bgwidth=(1-(self.time/self.blindsinterval))*self.ids.timeuntilnextblinds.width
    self.time-=1
    self.ids.gametime.text=format_time(self.gametime,True)
    self.gametime+=1

# handle timer getting to zero
    if self.time<0:
      self.time=self.blindsinterval
      self.blindlevel+=1
      self.ids.timeuntilnextblinds.bgwidth=0
      self.display_blinds()

  def start_blinds_timer(self):
    if self.ids.startstop.text=="start":
      self.blindsrunning=True
      self.ids.startstop.text="stop"
    else:
      self.blindsrunning=False
      self.ids.startstop.text="start"

  def blinds_control(self,opt):
    if opt=="prev":
      self.blindlevel=max(0,self.blindlevel-1)
    elif opt=="next":
      self.blindlevel=min(len(self.smallblinds)-1,self.blindlevel+1)
    elif opt=="reset":
      self.blindlevel=0
      self.blindsrunning=False

    self.time=self.blindsinterval
    self.ids.timeuntilnextblinds.text=format_time(self.time)
    self.display_blinds()

class BlindsTimer(App):
  def build(self):
    self.width = Window.width
    self.height = Window.height
    return MainView()

if __name__ == '__main__':
    BlindsTimer().run()

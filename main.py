#!/usr/bin/python

import datetime
import json
import math
import os
import random

from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import sp
from kivy.properties import BooleanProperty,NumericProperty,StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
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
  Window.size=(400,780) # mobile gives 1080,2116

from kivy.core.audio import SoundLoader

# game speeds
gamespeeds={
 "slow":      [ 20,20,20,20,20,20,20,20,20,20,20,20,20,20,20 ],
 "standard":  [ 20,20,20,15,15,15,10,10,10,10,10,10,10,10,10 ],
 "fast":      [ 10,10,10,7.5,7.5,7.5, 5, 5, 5, 5, 5, 5, 5, 5, 5 ],
 "very fast": [  5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5 ]
}

gamespeed="standard"

def format_time(s,h=False):
  if h:
    return "%02d : %02d : %02d"%(math.floor(s/3600),math.floor(s%3600/60),s%60)
  return "%02d : %02d"%(math.floor(s/60),s%60)

class ConfirmReset(Popup):
  def __init__(self,*args,**kwargs):
    super().__init__(**kwargs)
    self.title="sure?"
    self.confirmed=BooleanProperty()

  def confirm(self,msg):
    if msg=="yeah":
      self.confirmed=True
    else:
      self.confirmed=False

    self.dismiss()

class BlindsStructure(Popup):
  def __init__(self,*args,**kwargs):
    super().__init__(**kwargs)
    self.title="Blinds structure"

  def load_blinds_display(self,blinds,intervals,currentlevel):
    data=[]
    for i,b in enumerate(blinds):
      highlight=i==currentlevel
      altrow=i%2==0
      row=BlindsDisplayRow(text="%d: %d / %d (%s)"%(i+1,b,b*2,format_time(intervals[i])),highlight=highlight,altrow=altrow)
      self.ids.blindsstructure.add_widget(row)

class BlindsDisplayRow(Label):
  highlight=BooleanProperty()
  altrow=BooleanProperty()
  def __init__(self,*args,**kwargs):
    super().__init__(**kwargs)

class GameSpeedCheckBox(CheckBox):
  def __init__(self,*args,**kwargs):
    super().__init__(**kwargs)
    self.bind(active=self.select_game_speed)

  def select_game_speed(self,button,state):
    global gamespeed
    if self.active:
      gamespeed=self.parent.gamespeed

class BlindsSelectorRow(StackLayout):
  active=BooleanProperty(False)
  text=StringProperty()
  gamespeed=StringProperty()
  def __init__(self,*args,**kwargs):
    super().__init__(**kwargs)
    checkbox=GameSpeedCheckBox(active=self.active,group="gamespeed")
    self.add_widget(checkbox)
    self.add_widget(GameSpeedLabel(text=" "+self.text))

class BlindTimeHandler(Label):
  def __init__(self,*args,**kwargs):
    super().__init__(**kwargs)
  def on_touch_down(self,touch):
    if self.collide_point(*touch.pos) and touch.is_double_tap:
      ref=self.parent.parent
      newpos=(touch.pos[0])/self.width * ref.current_interval
      ref.time=ref.current_interval-newpos
      ref.ids.timeuntilnextblinds.text=format_time(ref.time)
      ref.ids.timeuntilnextblinds.bgwidth=(1-(ref.time/ref.current_interval))*ref.ids.timeuntilnextblinds.width

class MainView(StackLayout):
  def __init__(self,*args,**kwargs):
    super().__init__(**kwargs)
    current_interval=NumericProperty()
    self.initialise("standard")
    Clock.schedule_interval(self.update_display,1)

# set up blinds, display initial values
  def initialise(self,gamespeed="standard"):
    print("setting up %s game..."%gamespeed)
    print("game time approx. %d minutes"%sum(gamespeeds[gamespeed]))
    self.gamespeed=gamespeed
    self.smallblinds=[ 25,50,100,200,300,400,500,600,800,1000,2000,3000,4000,5000,6000 ]
    self.intervals=[ 60*x for x in gamespeeds[self.gamespeed]]
    self.ids.startstop.text="start"
    self.ids.timeuntilnextblinds.bgwidth=0

# set up trackers

    self.blindlevel=0
    self.blindsrunning=False
    self.current_interval=self.intervals[self.blindlevel]
    self.gametime=0
    self.time=self.current_interval

# get time, set initial display
    self.ids.timeuntilnextblinds.text=format_time(self.current_interval)

# display blinds
    self.display_blinds()

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

    if self.blindlevel+1<len(self.smallblinds):
      self.ids.timeuntilnextblinds.text=format_time(self.time)
      self.ids.timeuntilnextblinds.bgwidth=(1-(self.time/self.current_interval))*self.ids.timeuntilnextblinds.width
      self.time-=1
    else:
      self.ids.timeuntilnextblinds.text="-- : --"
      self.ids.timeuntilnextblinds.bgwidth=0

    self.ids.gametime.text=format_time(self.gametime,True)
    self.gametime+=1

# change text colour if less than 60s remaining
    self.ids.timeuntilnextblinds.color="red" if self.time<60 else "white"

# handle timer getting to zero
    if self.time<0:
      self.blindlevel+=1
      self.current_interval=self.intervals[self.blindlevel]
      self.ids.timeuntilnextblinds.bgwidth=0
      self.time=self.intervals[self.blindlevel]
      self.display_blinds()
      notification=SoundLoader.load("sounds/clip%d.mp3"%random.randrange(1,9))
      notification.play()

  def start_blinds_timer(self):
    if self.ids.startstop.text=="start":
      self.blindsrunning=True
      self.ids.startstop.text="stop"
    else:
      self.blindsrunning=False
      self.ids.startstop.text="start"

  def blinds_control(self,opt):
    if opt=="prev":
      if self.time>(self.current_interval-10):
        self.blindlevel=max(0,self.blindlevel-1)
    elif opt=="next":
      self.blindlevel=min(len(self.smallblinds)-1,self.blindlevel+1)

    self.current_interval=self.intervals[self.blindlevel]
    self.time=self.current_interval
    self.ids.timeuntilnextblinds.bgwidth=0
    self.ids.timeuntilnextblinds.text=format_time(self.time)
    self.display_blinds()

  def reset(self):
    self.popup=ConfirmReset(size_hint=(0.8,0.2))
    self.popup.bind(on_dismiss=self.confirm_reset)
    self.popup.open()

  def confirm_reset(self,arg2):
    if self.popup.confirmed==True:
# reset blinds
      self.blindlevel=0
      self.current_interval=self.intervals[self.blindlevel]
      self.blindsrunning=False
      self.time=self.current_interval
      self.ids.timeuntilnextblinds.bgwidth=0
      self.ids.timeuntilnextblinds.color="white"
# reset game time
      self.gametime=0
      self.ids.gametime.text=format_time(self.gametime,True)
# stop timers if they are running
      if self.ids.startstop.text=="stop":
        self.start_blinds_timer()
# update display
      self.ids.timeuntilnextblinds.text=format_time(self.time)
      self.display_blinds()
    else:
      pass

  def show_blind_structure(self):
    self.popup=BlindsStructure()
    self.popup.load_blinds_display(self.smallblinds,self.intervals,self.blindlevel)
    self.popup.open()

  def show_info(self):
    content=StackLayout(orientation="tb-lr")
    appinfo={
      "Version":version.version["revno"],
      "Last modified":version.version["revdate"],
    }
    content.add_widget(Label(size_hint=(1,0.05)))
    content.add_widget(InfoLabel(text="APP INFO"))

    for key,value in appinfo.items():
      content.add_widget(InfoLabel(text="   "+key+" "+value))

    content.add_widget(Label(size_hint=(1,0.05)))
    content.add_widget(InfoLabel(text="GAME SPEED"))

    for speed in ["Slow","Standard","Fast","Very fast"]:
      approxtime = round(2*sum([ x for x in gamespeeds[speed.lower()] ])/60)
      hourstring = "hr" if approxtime==2 else "hrs"
      timefmt = "%d" if approxtime%2==0 else "%3.1f"

      intervals = sorted(list(set(gamespeeds[speed.lower()])),reverse=True)
      intervalstext = " / ".join([str(x) for x in intervals] )
      timestring = "%s ("+intervalstext+" mins, ~ "+timefmt+" "+hourstring+" total)"
      labeltext = timestring%(speed,0.5*approxtime)
      active=speed.lower()==self.gamespeed
      content.add_widget(BlindsSelectorRow(gamespeed=speed.lower(),text=labeltext,active=active))

    confirmgamespeed = Button(text="set",size_hint=(1,0.05))
    confirmgamespeed.bind(on_press = self.set_game_speed)
    content.add_widget(confirmgamespeed)

    self.info=Popup(title="Info!",content=content)
    self.info.open()

  def set_game_speed(self,button):
    if gamespeed!=self.gamespeed:
      self.initialise(gamespeed)
    self.info.dismiss()

class Version:
  def __init__(self):
    if os.path.exists("local/version.json"):
      f=open("local/version.json")
      self.version=json.load(f)
      f.close()
    else:
      self.version={"revno": "--","revdate": "--"}


version=Version()

class BlindsTimer(App):
  def build(self):
    self.width = Window.width
    self.height = Window.height
    return MainView()

class InfoLabel(Label):
  def __init__(self,*args,**kwargs):
    super().__init__(**kwargs)

class GameSpeedLabel(Label):
  def __init__(self,*args,**kwargs):
    super().__init__(**kwargs)

if __name__ == '__main__':
    BlindsTimer().run()

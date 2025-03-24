#!/usr/bin/python

import datetime
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

class MainView(StackLayout):
  def __init__(self,*args,**kwargs):
    super().__init__(**kwargs)
# set up blinds, display initial values
    self.smallblinds=[ 25,50,100,150,200,300,400,500,600,800,1000,1500,2000,3000,4000,5000 ]
    self.ids.currentblinds.text=("%d / %d"%(self.smallblinds[0],self.smallblinds[0]*2))
    self.ids.nextblinds.text=("%d / %d"%(self.smallblinds[1],self.smallblinds[1]*2))

# get time, set initial display
    timenow=datetime.datetime.now()
    self.ids.time.text=timenow.strftime("%H:%M:%S")
    self.ids.timeuntilnextblinds.text="15:00"

# set up timer
    self.time=0

class BlindsTimer(App):
  def build(self):
    self.width = Window.width
    self.height = Window.height
    return MainView()

if __name__ == '__main__':
    BlindsTimer().run()

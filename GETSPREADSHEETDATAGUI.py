from __future__ import print_function
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
import calendar
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.actionbar import *
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.properties import NumericProperty, ReferenceListProperty
import kivy
from kivy.app import App
import datetime
import time
from kivy.uix.label import Label #widgets
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from KivyCalendar import DatePicker
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import gspread
import json
from datetime import date, timedelta
from functools import partial
import numpy as np
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds' , 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('SpreadSheetExample-3bca0af9d5d8.json', scope)
gc = gspread.authorize(credentials)
wks = gc.open('Docalendar').sheet1
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
class CreateAccountWindow(Screen):

    namee = ObjectProperty(None)
    def submit(self):
        try:
            global id
            data = wks.get_all_records()
            cell = wks.find(self.namee.text)
            values_list = wks.row_values(cell.row)
            id = values_list
            sm.current = "main"


        except gspread.CellNotFound:
            sm.current = "notfound"
class DOCalendar(Screen):
    n = ObjectProperty(None)
    b = ObjectProperty(None)
    t = ObjectProperty(None)
    def on_pre_enter(self):
        self.changen()
        self.changet()
        self.changeb()
        self.changea()
    def changen(self):
        self.ids.n.text = "Name: "+id[1]
    def changet(self):
        self.ids.t.text = "Phone: "+id[2]
    def changeb(self):
        self.ids.b.text = "Birthday: "+id[3]




class NotFound(Screen):
    na = ObjectProperty(None)

class Arrange(Screen):
    error = ObjectProperty(None)
    date = ObjectProperty(None)
    time = ObjectProperty(None)

    def getevents(self):
        creds = None
        global dategiven
        global eventsprint
        global datee
        global datee11
        global timegiven
        global service
        global dateendfinal
        global datefinal
        timegiven = self.time.text
        eventsprint = []
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        service = build('calendar', 'v3', credentials=creds)
        dategiven = self.date.text

        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        datee = datetime.datetime.strptime(dategiven, '%d-%m-%Y').strftime("%Y-%m-%d"+ "T" +"%H:%M:%S"+"+02:00")
        nextdaystr = self.date.text.split("-")[0]
        nextday = int(nextdaystr) +1

        datee1 = str(nextday) +"-"+ self.date.text.split("-")[1]+"-"+ self.date.text.split("-")[2]
        datee11 = datetime.datetime.strptime(datee1, '%d-%m-%Y').strftime("%Y-%m-%d"+ "T" +"%H:%M:%S"+"+02:00")
        events_result = service.events().list(calendarId='primary',timeMin =datee,timeMax = datee11,
                                            maxResults=24, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            eventsprint.append('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            eventsprint.append((start, event['summary']))
    def validatedate(self):
        try:
            self.ids.error.text =""
            if(datetime.datetime.strptime(self.date.text, '%d-%m-%Y')):
                self.getevents()
                self.manager.current = 'freedate'
            else:
                self.ids.error.text="Error give valid date!"
        except ValueError:
                self.ids.error.text="Error give valid date!"
    def validatetime(self):
        try:
                self.ids.error.text =""
                if (datetime.datetime.strptime(self.date.text, '%d-%m-%Y') and datetime.datetime.strptime(self.time.text, '%H:%M')):
                        self.getevents()
                        self.manager.current = 'add_appoint'

        except ValueError:
                self.ids.error.text="Error give valid date and time!"

class FreeDate(Screen):
        t0 = ObjectProperty(None)
        t1 = ObjectProperty(None)
        t2 = ObjectProperty(None)
        t3 = ObjectProperty(None)
        t4 = ObjectProperty(None)
        t5 = ObjectProperty(None)
        t6 = ObjectProperty(None)
        t7 = ObjectProperty(None)
        t8 = ObjectProperty(None)
        t9 = ObjectProperty(None)
        t10 = ObjectProperty(None)
        t11 = ObjectProperty(None)
        notfound = ObjectProperty(None)
        datetop = ObjectProperty(None)
        def changet(self,x):
            self.ids.datetop.text =   dategiven.split("-")[0] +" "+ calendar.month_name[int((dategiven).split("-")[1])] +" "+dategiven.split("-")[2]
            if(eventsprint[0]!="No upcoming events found."):
                self.ids.notfound.text = ""
                for i in range(x):
                    nm = "t"+str(i)
                    time = str(eventsprint[i]).split(",")[0]
                    datewithouttime = time.split("T")[0]
                    timewithoutdate = time.split("T")[1]
                    timefin = timewithoutdate.split("+")[0]
                    name = str(eventsprint[i]).split(",")[1]
                    name = name.replace("'", '')
                    name = name.replace(')', '')
                    if(nm == "t0"):
                        self.ids.t0.text = name +"\nat "+ timefin.split(":")[0]+":"+timefin.split(":")[1]
                    if(nm =="t1"):
                        self.ids.t1.text =name +"\nat "+ timefin.split(":")[0]+":"+timefin.split(":")[1]
                    if(nm == "t2"):
                        self.ids.t2.text =  name +"\nat "+ timefin.split(":")[0]+":"+timefin.split(":")[1]
                    if(nm == "t3"):
                        self.ids.t3.text = name +"\nat "+ timefin.split(":")[0]+":"+timefin.split(":")[1]
                    if(nm =="t4"):
                        self.ids.t4.text = name +"\nat "+ timefin.split(":")[0]+":"+timefin.split(":")[1]
                    if(nm == "t5"):
                        self.ids.t5.text =name +"\nat "+ timefin.split(":")[0]+":"+timefin.split(":")[1]
                    if(nm == "t6"):
                        self.ids.t6.text =name +"\nat "+ timefin.split(":")[0]+":"+timefin.split(":")[1]
                    if(nm =="t7"):
                        self.ids.t7.text = name +"\nat "+ timefin.split(":")[0]+":"+timefin.split(":")[1]
                    if(nm == "t8"):
                        self.ids.t8.text =  name +"\nat "+ timefin.split(":")[0]+":"+timefin.split(":")[1]
                    if(nm == "t9"):
                        self.ids.t9.text =  name +"\nat "+ timefin.split(":")[0]+":"+timefin.split(":")[1]
                    if(nm =="t10"):
                        self.ids.t10.text = name +"\nat "+ timefin.split(":")[0]+":"+timefin.split(":")[1]
                    if(nm == "t11"):
                        self.ids.t11.text =name +"\nat "+ timefin.split(":")[0]+":"+timefin.split(":")[1]


            else:
                self.ids.notfound.text = "No upcoming events found."
                self.ids.t0.text = ""
                self.ids.t1.text = ""
                self.ids.t2.text = ""
                self.ids.t3.text = ""
                self.ids.t4.text = ""
                self.ids.t5.text = ""
                self.ids.t6.text = ""
                self.ids.t7.text = ""
                self.ids.t8.text = ""
                self.ids.t9.text = ""
                self.ids.t10.text = ""
                self.ids.t11.text = ""
        def clear(self):
                self.ids.notfound.text=""
                self.ids.t0.text = ""
                self.ids.t1.text = ""
                self.ids.t2.text = ""
                self.ids.t3.text = ""
                self.ids.t4.text = ""
                self.ids.t5.text = ""
                self.ids.t6.text = ""
                self.ids.t7.text = ""
                self.ids.t8.text = ""
                self.ids.t9.text = ""
                self.ids.t10.text = ""
                self.ids.t11.text = ""
        def on_pre_enter(self):
                self.changet(len(eventsprint))
class AddAppoint(Screen):
    info = ObjectProperty(None)
    def changetext(self):
        self.ids.info.text = "Appointment "+ dategiven.split("-")[0] +" "+ calendar.month_name[int((dategiven).split("-")[1])] +" "+dategiven.split("-")[2]+" at " +timegiven + " with " + id[1]
    def addappointment(self):
        timegiven1 = timegiven
        datefinal = datee.split("T")[0] +"T"+ timegiven1+":00+02:00"
        timeend = str(int(timegiven.split(":")[0])+1)
        timeend = timeend + ":"+str(timegiven.split(":")[1])
        dateendfinal = datee.split("T")[0] +"T"+ timeend +":00+02:00"
        event = {
  'summary': 'Appointment with '+id[1],
  'description': '',
  'start': {
    'dateTime': datefinal ,
  },
  'end': {
    'dateTime':dateendfinal,
  },
  'attendees': [
    {'email': str(id[4])},
  ],
  }
        event = service.events().insert(calendarId='primary', body=event).execute()
        self.ids.added.text="Your Event has been added."
    def on_pre_enter(self):
        self.changetext()
        self.ids.added.text=""
class WindowManager(ScreenManager):
    pass
kv = Builder.load_file("DOCalendar.kv")

sm = WindowManager()

screens = [CreateAccountWindow(name="create"),DOCalendar(name="main"),NotFound(name="notfound"),Arrange(name="appoint"),FreeDate(name="freedate"),AddAppoint(name="add_appoint")]
for screen in screens:
    sm.add_widget(screen)


class DOCalendar(App):
    def build(self):
        self.icon = 'Calendar.ico'
        return sm



if __name__ == "__main__":
    DOCalendar().run()

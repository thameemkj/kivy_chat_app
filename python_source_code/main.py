from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.popup import Popup
from kivy.utils import get_color_from_hex as H

from chatlayout import ChatLayout

import socket
import threading

def reciever_thread(client_obj,chatlayout_obj):
    while(True):
        try:
            pkt=client_obj.recv(2**10).decode()
            if(pkt):
                pkt=pkt.split("\S")
                for i in range(1,len(pkt)-1,2):
                    username=pkt[i]
                    content=pkt[i+1]
                    chatlayout_obj.scrollview.msg_layout(username,content)
        except:
            Popup(title="Connection Error",content=Label(text="Connection lost. Please restart your application"),auto_dismiss=False,size_hint=(0.5,0.3)).open()
            break

class LoginButton(Button):
    pass
class SignupButton(Button):
    pass

class PopupBoxLayout(BoxLayout):
    def __init__(self,popup_obj,win_obj,label='',**kwargs):
        super(PopupBoxLayout,self).__init__(**kwargs)
        self.orientation="vertical"
        self.label=Label(text=label)
        self.add_widget(self.label)

        #BoxLayouts____________________________________________________
        self.buttonslayout=BoxLayout()

        #Buttons_______________________________________________________
        self.continuebutton=Button(text="Continue",on_release=popup_obj.dismiss)
        self.exitbutton=Button(text="EXIT",on_release=win_obj.stop)
        self.buttonslayout.add_widget(self.continuebutton)
        self.buttonslayout.add_widget(self.exitbutton)

        self.add_widget(self.buttonslayout)

    def change_label(self,label):
        self.label.text=label

class HeyBudLayout(FloatLayout):
    def __init__(self,**kwargs):
        super(HeyBudLayout,self).__init__(**kwargs)
        #Window.clearcolor=H("#000066")
        
        self.label=Label(text="Hey Bud",size_hint=(None,None),font_name="bellada.ttf",bold=True,font_size="50dp",color=H("#e6e6e6"),pos_hint={"center_x":0.5,"center_y":0.7})
        self.label.bind(texture_size=self.label.setter("size"))
        self.add_widget(self.label)
        
        self.username_textinput=TextInput(multiline=False,hint_text="Username",use_bubble=True,use_handles=True,size_hint=(None,None),height="30dp",width="300dp",pos_hint={"center_x":0.5,"center_y":0.58})
        self.add_widget(self.username_textinput)

        self.password_textinput=TextInput(multiline=False,hint_text="Address:Port",use_bubble=True,use_handles=True,password=False,size_hint=(None,None),height="30dp",width="300dp",pos_hint={"center_x":0.5,"center_y":0.533})
        self.add_widget(self.password_textinput)

        self.login_button=LoginButton(size_hint=(None,None),width="100dp",height="35dp",text="Login",font_size="15dp",bold=True,pos_hint={"center_x":0.35,"center_y":0.47})
        self.add_widget(self.login_button)
        
        self.signup_button=SignupButton(size_hint=(None,None),width="100dp",height="35dp",text="SignUp",font_size="15dp",bold=True,pos_hint={"center_x":0.65,"center_y":0.47})
        self.add_widget(self.signup_button)


client=socket.socket()
screenmanager=ScreenManager()
screenmanager.add_widget(Screen(name="heybud"))
screenmanager.add_widget(Screen(name="chatlayout"))
#chatlayout=ChatLayout(client)
#screenmanager.screens[1].add_widget(chatlayout)

class HeyBudApp(App):
    def build(self):
        Window.clearcolor=H("#000066")
        Window.softinput_mode="below_target"
        self.heybudlayout=HeyBudLayout()
        screenmanager.screens[0].add_widget(self.heybudlayout)
        screenmanager.current="heybud"
        #self.client=socket.socket()
        self.heybudlayout.login_button.bind(on_release=self.on_login)
        return screenmanager

    def on_login(self,instance):
        username=self.heybudlayout.username_textinput.text
        ip_addr=self.heybudlayout.password_textinput.text.split(":")

        chatlayout=ChatLayout(client,username)
        screenmanager.screens[1].add_widget(chatlayout)
        
        popup = Popup(title="Connection Status",size_hint=(0.5,0.25),disabled=False,auto_dismiss=False)
        popup.content=PopupBoxLayout(popup,self,"Connecting to server...")
        popup.open()

        try:
            client.connect((ip_addr[0],int(ip_addr[1])))
            thread1=threading.Thread(target=reciever_thread,daemon=True,args=(client,chatlayout,))
            thread1.start()
            #popup.content=PopupBoxLayout(popup,self,"Connection Successful")
            popup.dismiss()
            screenmanager.current="chatlayout"
            Window.clearcolor=H("#66c2ff")
        except:
            popup.content=PopupBoxLayout(popup,self,"Couldnt connect to server\nPlease re-run the application")

HeyBudApp().run()

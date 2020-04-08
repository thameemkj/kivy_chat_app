from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.core.window import Window,WindowBase
from kivy.utils import get_color_from_hex as H
import socket
import threading

class MyScrollView(ScrollView):
    def __init__(self,**kwargs):
        super(MyScrollView,self).__init__(**kwargs)
        self.layout=BoxLayout(orientation="vertical",pos_hint={"center_x":0.2,"center_y":0.5},size_hint=(None,None),spacing=30,width=300)
        self.layout.bind(minimum_height=self.layout.setter("height"))
        self.add_widget(self.layout)

    def msg_layout(self,username,content):

        #MainLayout___________________________________________________
        self.msglayout=BoxLayout(orientation="vertical",size_hint=(None,None),pos_hint={"center_x":0.7},spacing=5,width=300)
        self.msglayout.bind(minimum_height=self.msglayout.setter("height"))

        #UsernameLayout_______________________________________________
        a=Label(text=username,size_hint_y=None,color=H("ff0000"),bold=True)
        a.bind(width=lambda s,w:s.setter("text_size")(s,(w,None)))
        a.bind(texture_size=a.setter("size"))
        self.msglayout.add_widget(a)

        #MessageContentLayout_________________________________________
        l=Label(text=content,size_hint_y=None)
        l.bind(width=lambda s,w:s.setter("text_size")(s,(w,None)))
        l.bind(texture_size=l.setter("size"))
        self.msglayout.add_widget(l)
            
        self.layout.add_widget(self.msglayout)

class ChatLayout(FloatLayout):
    def __init__(self,client_obj,username,**kwargs):
        super(ChatLayout,self).__init__(**kwargs)
        self.client_obj=client_obj
        self.username=username

        #BoxLayouts()________________________________________________
        self.upperboxlayout=BoxLayout(size_hint_x=0.99,size_hint_y=0.08,pos_hint={"x":0.005,"y":0.92})
        self.scrollboxlayout=BoxLayout(size_hint_x=0.99,size_hint_y=0.78,pos_hint={"x":0.005,"y":0.12})
        self.bottomboxlayout=BoxLayout(size_hint_x=0.99,size_hint_y=0.07,pos_hint={"x":0.005,"y":0.04})

        #UpperLayout()_______________________________________________
        self.upperboxlayout.add_widget(Button(text="Upper BoxLayout"))
        self.add_widget(self.upperboxlayout)

        #ScrollView()________________________________________________
        self.scrollview=MyScrollView()
        self.scrollboxlayout.add_widget(self.scrollview)
        self.add_widget(self.scrollboxlayout)


        #BottomLayout()______________________________________________
        self.textinput=TextInput(hint_text="Type your message here",multiline=True,use_bubble=True,use_handles=True,cursor_width="2sp")
        self.bottomboxlayout.add_widget(self.textinput)
        self.sendbutton=Button(text="SEND",size_hint_x=0.2,on_release=self.on_send)
        self.bottomboxlayout.add_widget(self.sendbutton)
        self.add_widget(self.bottomboxlayout)

    def on_send(self,instance):
        msg=self.textinput.text
        msg="\S{}\S{}\S".format(self.username,msg)
        self.client_obj.send(msg.encode("ascii"))
        self.textinput.text=''

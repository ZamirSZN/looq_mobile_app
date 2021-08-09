from urllib.parse import unquote_plus, urlencode
from kivymd.app import MDApp
from kivy.uix.image import AsyncImage
from kivy.core.window import Window
from statusbarcolor import change_statusbar_color
from kivy.core.text import LabelBase
from kivy.clock import Clock
import webbrowser
from kivymd.toast import toast
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivy.factory import Factory
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.snackbar import Snackbar
from kivy.loader import Loader
from kivy.properties import StringProperty
import os
import random
from colors import *
from kivy.network.urlrequest import UrlRequest
import certifi
import gc

import ssl
ssl._create_default_https_context = ssl._create_unverified_context




#:import PostNewBox post_new.PostNewBox


Window.softinput_mode = "below_target"
Loader.loading_image = 'loader.gif'
Loader.error_image = 'error.gif'
Loader.num_workers=4

class ImageLoader(AsyncImage):
    anim_delay = .05


MONTSERRAT_FONTS=[
    {"name": "Montserrat","fn_regular": "fonts/Montserrat-Regular.ttf",},
    {"name": "Ubuntu","fn_regular": "fonts/Ubuntu-Regular.ttf",},]

for font in MONTSERRAT_FONTS:
    LabelBase.register(**font)

class ConfirmationLayout(BoxLayout):
    pass

class LooqDetail(BoxLayout):
    pass

class LooqWidget(ButtonBehavior,GridLayout):
    pass

class LooqApp(MDApp):
    version=1.0
    title='Looq'
    greeting=StringProperty('Hi there, Guest')
    store = JsonStore('looq.json')

    confirm_color=(0,1,0,1)
    confirm_image= StringProperty()
    confirm_text=StringProperty()

    USERNAME=''
    TOKEN=''
    LOGGED_IN=False

    DEBUG= False
    if DEBUG:
        server_url="http://127.0.0.1:8000/api/"
    else:
        server_url="https://looq.herokuapp.com/api/"
        
    looq_api_get= server_url+"all?format=json"
    looq_api_post= server_url+"post"
    looq_api_create_user= server_url+'create-user'
    looq_api_login_user= server_url+'login-user'
    looq_api_search=server_url+'all?search='
    looq_category_search=server_url+'category?search='
    looq_user_api=server_url+'user'

    def	confirm_bottomsheet(self,confirm_type,seconds):
        if confirm_type=='sent':
            self.confirm_color=YELLOW
            self.confirm_image='sent.gif'
            self.confirm_text="Your post has been sent !"
        elif confirm_type=='auth':
            self.confirm_color=AUTH_COLOR
            self.confirm_image='fingerprint.gif'
            self.confirm_text="You're now logged in !"
        else:
            pass

            
        self.confirmbottomsheet = MDCustomBottomSheet(
                                                screen=ConfirmationLayout(),
                                                radius=40,
                                                radius_from="top",)
        self.confirmbottomsheet.open()
        Clock.schedule_once(self.confirmbottomsheet.dismiss,seconds)

    def set_greeting(self):
        self.USERNAME=self.store.get('LooqUserProfile')['username']
        self.greeting='Hi there, %s' %self.USERNAME.capitalize()

    def user_api_response(self,req , result):
        username=result["username"]
        user_pk=result['pk']
        email=result['email']
        image=result['image']

        self.store.put('LooqUserDetail', email=email, user_pk=user_pk, image=image )
        self.root.ids.username_label.text=username
        self.root.ids.email_label.text=email
        self.root.ids.user_image.source=image

    def get_user_details(self):
        USERNAME=self.store.get('LooqUserProfile')['username']
        TOKEN=self.store.get('LooqUserProfile')['token']
        headers ={'username':USERNAME, 'Authorization': 'Token '+str(TOKEN)}
        UrlRequest(self.looq_user_api, req_headers=headers,  on_success=self.user_api_response,on_failure=self.on_failure,on_error=self.on_error)

    def show_last_looq_home_item(self, response):
        rndm=random.randrange(0,len(response))
        latest_item=response[rndm]
        object_name=latest_item["object_name"]		
        posted_on=latest_item['posted_on']
        description=latest_item["description"]
        image=latest_item["image"]

        looq_latest_widget=self.root.ids.looq_latest_widget
        looq_latest_widget.object_name=object_name
        looq_latest_widget.posted_on=posted_on
        looq_latest_widget.image=image
        looq_latest_widget.description=description
    
    

    def put_json_to_home_rv(self,req, response):
        all_looq_json_item=response
        looq_home_rv= self.root.ids.looq_home_rv
        looq_home_rv.data=[]
        
        for missing_object in all_looq_json_item:
            author=missing_object["author"]
            object_name=missing_object["object_name"]
            description=missing_object["description"]
            image=missing_object["image"]
            category=missing_object["category"]
            posted_on=missing_object['posted_on']
            
            looq_home_rv.data.append({
                "author":str(author),
                "object_name": str(object_name),
                "description": str(description),
                'image': str(image),
                "category": str(category),
                'posted_on':str(posted_on), })
        
        self.root.ids.looq_home_rv_spinner.active=False
        self.show_last_looq_home_item(response)


    def get_looq_objects_all(self, *args):
        gc.collect()
        UrlRequest(self.looq_api_get , on_success=self.put_json_to_home_rv,on_failure=self.on_failure,on_error=self.on_error)
        

    

    def on_failure(self, req, result):
        self.show_toast('Server Error !')
        print(result)
        
    def on_error(self, req, result):
        self.show_toast('Connection Error !')
        print(result)
       

        
    def home_rv_spinner_start(self):
        self.root.ids.looq_home_rv_spinner.active= True

    def home_rv_spinner_stop(self):
        self.root.ids.looq_home_rv_spinner.active= False
    
    
    def get_category(self,category):
        CATEGORY_CHOICES={
                    'General':1,
                    'Gadgets':2,
                    'Personal':3,
                    'Pets':4,
                    'Food':5,
                    'Stationary':6,
                    'Others':7 }
                
        self.root.ids.category_label.text=category
        _category=CATEGORY_CHOICES[category]
        
        UrlRequest(self.looq_category_search+str(_category) , on_success=self.put_json_to_category_rv,on_failure=self.on_failure,on_error=self.on_error)


        '''
        try:
            r=requests.get(self.looq_category_search+str(_category))
            if r.json()==[]:
                self.show_toast('No item in this category .')
                self.root.ids.looq_category_spinner.active=False
            else:
                self.put_json_to_category_rv(r.json())
        except:
            self.show_toast('Connection Failed !')
        '''

    def put_json_to_category_rv(self,req, result):
        if result==[]:
            self.show_toast('No item in this category')
            self.root.ids.looq_category_spinner.active=False
            return
        all_looq_json_item=result
        looq_category_rv= self.root.ids.looq_category_rv
        looq_category_rv.data=[]
        
        for missing_object in all_looq_json_item:
            author=missing_object["author"]
            object_name=missing_object["object_name"]
            description=missing_object["description"]
            image=missing_object["image"]
            category=missing_object["category"]
            posted_on=missing_object['posted_on']
            
            looq_category_rv.data.append({
                "author":str(author),
                "object_name": str(object_name),
                "description": str(description),
                'image': str(image),
                "category": str(category),
                'posted_on':str(posted_on),})
        
        self.root.ids.looq_category_spinner.active=False

    def save_user_data(self, username, token):
        self.store.put('LooqUserProfile', username=username, token=token, logged_in=True )
    
    #too lazy to find a workaround :(
    def check_logged_in_acccount(self):
        if not self.LOGGED_IN:
            self.goto_screen('looq-login', 'left')	
        if self.LOGGED_IN:
            self.goto_screen('looq-account', 'left')
            self.get_user_details()
            
    def check_logged_in(self,screen,direction):
        if not self.LOGGED_IN:
            self.goto_screen('looq-login', 'left')	
        if self.LOGGED_IN:
            self.goto_screen(screen, direction)
                
    def show_snackbar(self, text):
        Snackbar(text=text).show()
    
    def open_link(self, url):
        webbrowser.open(url)
    
    def light_mode(self):
        self.theme_cls.theme_style = 'Light'
        self.night_mode_bottom_sheet.dismiss()
        store=JsonStore("looq.json")
        store.put("theme",mode=self.theme_cls.theme_style)
        self.root.ids.toolbar.specific_text_color=(0,0,0,1)

    def reset(self):
        try:
            os.remove('looq.json')
        except:
            pass
        self.show_toast('Please restart the app')
        Clock.schedule_once(self.stop,2)

    def dark_mode(self):
        self.theme_cls.theme_style = 'Dark'
        self.night_mode_bottom_sheet.dismiss()
        store=JsonStore("looq.json")
        store.put("theme",mode=self.theme_cls.theme_style)

    def	reset_bottomsheet(self):
        self.resetbottomsheet = MDCustomBottomSheet(
                                                screen=Factory.ResetLayout(),
                                                radius=40,
                                                radius_from="top",)
        self.resetbottomsheet.open()	

    def nightmode_bottom_sheet(self):
        self.night_mode_bottom_sheet = MDCustomBottomSheet(
                                                screen=Factory.NightModeLayout(),
                                                radius=40,
                                                radius_from="top",)
        self.night_mode_bottom_sheet.open()
        
    def show_toast(self, text):
        toast(text)

    def detail_parameters(self, object_name, posted_on, category, description, author, image ):	
        self.root.ids.detail_image.source=image
        self.root.ids.looq_detail_widget.object_name=object_name
        self.root.ids.looq_detail_widget.posted_on=posted_on
        self.root.ids.looq_detail_widget.category=category
        self.root.ids.looq_detail_widget.description=description
        self.root.ids.looq_detail_widget.author=author
    
    def goto_screen(self, screen, direction):
        sm=self.root
        sm.current=screen
        sm.transition.direction=direction
    
    def load_user_profile(self):
        try:	
            self.theme_cls.theme_style=self.store.get('theme')['mode']
        except:
            pass
        #add auto darkmode in future versions

        try:
            self.USERNAME=self.store.get('LooqUserProfile')['username']
            self.TOKEN=self.store.get('LooqUserProfile')['token']
            self.LOGGED_IN=self.store.get('LooqUserProfile')['logged_in']
            self.greeting='Hi there, %s' %self.USERNAME.capitalize()
        except:
            print('No user yet')

    def request_android_permissions(self):
        from android.permissions import request_permissions, Permission

        def callback(permissions, results):

            if all([res for res in results]):
                # toast("All permitions granted.")
                self.permit = True
            else:
                toast("Permessions denied", True, 80)
                self.permit = False

        request_permissions([Permission.READ_EXTERNAL_STORAGE], callback)

    def build(self):
        if platform == "android":
            self.request_android_permissions()
        change_statusbar_color(PURPLE)
        self.load_user_profile()
        #self.root.current='looq-account'

        Clock.schedule_once(self.get_looq_objects_all)

if __name__=="__main__":
    from kivy.utils import platform
    if platform == 'win':
        Window.size = (340,660)

    LooqApp().run()

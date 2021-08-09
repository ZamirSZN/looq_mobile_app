from urllib.parse import urlencode
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDIconButton
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.app import App

from kivy.network.urlrequest import UrlRequest

app=App.get_running_app()


Builder.load_string('''

<TextLabel@ButtonBehavior+MDLabel>


<LoginBox>
	orientation:'vertical'
	spacing:dp(20)
	padding:dp(30)

	MDLabel:
		text:'Login to your account'
		theme_text_color:'Primary'
		font_name:'Montserrat'
		font_style:'H2'
		#pos_hint: {'center_x': .5, 'center_y':.9}
		size_hint_y:.08
	
	LooqTextField:
		hint_text:'Username'
		#mode: "rectangle"
		multiline: False
		max_text_length: 50
		id: username_field
		icon_right: 'account-circle'
		size_hint_y:.03
		on_text:self.check_length(self.text, self.max_text_length)

		

	LooqTextField:
		hint_text:'Password'
		password:True
		multiline: False
		max_text_length:50
		id:password_field
		icon_right: 'key'
		size_hint_y:.03
		on_text:self.check_length(self.text, self.max_text_length)


	
	
	TextLabel:
		text:'Dont have an account [color=#616cf0] Sign up[/color]'
		theme_text_color:'Primary'
		font_name:'Montserrat'
		markup:True
		#font_style:'H6'
		size_hint_y:.01
		on_release:
			app.goto_screen('looq-signup','right')
		
	GridLayout:
		cols:2
		size_hint_y:.01
		ShowPassword:
			id:show_password
			icon:'eye'
			#state:'normal'
			on_state:
				if self.state == 'down': show_password.icon='eye-off'; password_field.password=False
				else: show_password.icon='eye'; password_field.password=True
	  
		MDLabel:
			text:'Show password'
			theme_text_color:'Primary'
			font_name:'Montserrat'
			#font_style:'H2'
			#pos_hint: {'center_x': .5, 'center_y':.9}
			
	
	Widget:
		size_hint_y:.008
	
	
			
	SendButton:
		icon: 'check'
		text: '       Submit       '
		id:looq_login_button
		md_bg_color: get_color_from_hex("#e99c66" )
		font_name:'Montserrat'
		pos_hint: {'center_x': .5}
		on_press:
			root.login(username_field.text, password_field.text)
	Widget:
		size_hint_y:.03

''')



class ShowPassword(ToggleButtonBehavior, MDIconButton):
	pass

class LoginBox(BoxLayout):


	def login(self, username, password):
		global _username
		
		_username=username
		password=password
		params=urlencode({
			"username": username,   
			"password": password,})

		headers = {'Content-type': 'application/x-www-form-urlencoded',
		'Accept': 'application/json'}

		UrlRequest(app.looq_api_login_user, req_body=params, req_headers=headers, on_success=self.login_user,on_failure=app.on_failure,on_error=app.on_error)

	def login_user(self, req , result):
		token=result['token']
		app.save_user_data(_username, token)
		app.LOGGED_IN=True
		app.set_greeting()
		app.goto_screen('looq-home','right')
		app.confirm_bottomsheet('auth',7)
		app.get_user_details()

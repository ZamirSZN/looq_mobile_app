from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDIconButton
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.app import App
from login import LoginBox
from text_field import LooqTextField
from kivy.network.urlrequest import UrlRequest
from urllib.parse import urlencode



app=App.get_running_app()



Builder.load_string('''



<SignupBox>
	orientation:'vertical'
	spacing:dp(20)
	padding:dp(30)

	MDLabel:
		text:'Create a new account'
		theme_text_color:'Primary'
		font_name:'Montserrat'
		font_style:'H2'
		#pos_hint: {'center_x': .5, 'center_y':.9}
		size_hint_y:.05
		font_size:dp(43)
	
	LooqTextField:
		hint_text:'Username'
		id:username_field
		max_text_length: 50
		icon_right: 'account-circle'
		font_name:'Montserrat'
		size_hint_y:.03
		on_text:self.check_length(self.text, self.max_text_length)
		
	LooqTextField:
		hint_text:'Email'
		id:email_field
		max_text_length: 50
		icon_right: 'email'
		size_hint_y:.03
		on_text:self.check_length(self.text, self.max_text_length)

	LooqTextField:
		hint_text:'Password'
		password:True
		max_text_length:50
		icon_right: 'key'
		id:password1
		size_hint_y:.03
		on_text:self.check_length(self.text, self.max_text_length)

	LooqTextField:
		hint_text:'Password Confirmation'
		password:True
		max_text_length:50
		id:password2
		size_hint_y:.03
		on_text:self.check_length(self.text, self.max_text_length)

	TextLabel:
		text:'Dont have an account [color=#616cf0] Log in [/color]'
		theme_text_color:'Primary'
		font_name:'Montserrat'
		markup:True
		#font_style:'H6'
		size_hint_y:.01
		on_release:
			app.goto_screen('looq-login','right')
			
	GridLayout:
		cols:2
		size_hint_y:.01
		ShowPassword:
			id:show_password
			icon:'eye'
			#state:'normal'
			on_state:
				if self.state == 'down': show_password.icon='eye-off'; password1.password=False;password2.password=False
				else: show_password.icon='eye'; password1.password=True; password2.password=True

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
		md_bg_color: get_color_from_hex("#e99c66" )
		font_name:'Montserrat'
		pos_hint: {'center_x': .5}
		on_press:
			root.verify_signup_post_form(username_field.text, email_field.text, password1.text, password2.text)
	Widget:
		size_hint_y:.03

''')




class ShowPassword(ToggleButtonBehavior, MDIconButton):
	pass

class SignupBox(BoxLayout):

	#seriously i really wish i can reuse this function but im lazy :(

	#fuck it i found a way, i was too tired to think at first
	def check_username_field_length(self, text,max_text_length):
		if len(text) > max_text_length :
			self.ids.username_field.text=text[:max_text_length+1]
	
	def confirm_password(self, password1, password2):
		if password1 != password2:
			self.ids.password2.helper_text_mode="persistent"
			self.ids.password2.helper_text="Passwords do not match"
		elif password1== password2:
			self.ids.password2.helper_text_mode="persistent"
			self.ids.password2.helper_text="Passwords matches"
		else:
			pass

	

		'''
		
		r=requests.post(app.looq_api_login_user, data=data)
		if r.status_code==200:
			app.save_user_data(username, r.json())
			app.LOGGED_IN=True
			app.set_greeting()
			
			app.goto_screen('looq-home','right')
			app.confirm_bottomsheet('auth',7)
			app.get_user_details()
		else:
			error=next(iter(r.json().values()))
			app.show_snackbar(error)
		'''

	

	def signup_user(self, username_field, email_field, password2):
		global _password2, _username
		_password2=password2
		_username=username_field
		
		params=urlencode({
			"username": username_field,
			"email": email_field,  
			"password": password2,})

		headers = {'Content-type': 'application/x-www-form-urlencoded',
				'Accept': 'application/json'}
				
		UrlRequest(app.looq_api_create_user, req_body=params, req_headers=headers, on_success=self.call_login,on_failure=app.on_failure,on_error=app.on_error)
		

	def call_login(self, req, result):
		
		self.login(_username ,_password2)

	def login(self, username, password):
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
		

	def verify_signup_post_form(self, username_field, email_field, password1, password2):
		if len(username_field) < 1:
			app.show_snackbar('Username field cannot be empty !')
			return

		if len(email_field) < 1:
			app.show_snackbar('Email field cannot be empty !')
			return

		if len(password1) < 1:
			app.show_snackbar('Password field cannot be empty !')
			return

		if len(password2) < 1:
			app.show_snackbar('Please confirm the password !')
			return

		if password1 != password2:
			app.show_snackbar('Passwords do not match !')
			return
		
		if '@' not in email_field:
			app.show_snackbar('Please enter a valid email !')
			return

		self.signup_user(username_field, email_field, password2)

	


	
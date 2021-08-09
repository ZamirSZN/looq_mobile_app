from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.filemanager import MDFileManager
#from plyer import storagepath
import requests
from requests.exceptions import ConnectionError
from kivy.app import App
from threading import Thread
from kivy.storage.jsonstore import JsonStore
import time
from kivy.utils import platform
from text_field import LooqTextField



t=time.localtime()
app=App.get_running_app()

Builder.load_string('''
#:import LooqTextField text_field.LooqTextField
#:import PURPLE colors.PURPLE
#:import LIGHT_ORANGE colors.LIGHT_ORANGE
#:import ASH colors.ASH
#:import WHITE colors.WHITE
#:import LIGHT_PINK colors.LIGHT_PINK
#:import PINK colors.PINK
#:import DARK colors.DARK
#:import ORANGE colors.ORANGE



<PostNewBox>
	size_hint_y:1
	orientation:'vertical'
	spacing:dp(10)
	padding:dp(20)


	BoxLayout:
		size_hint_y:.5
		orientation:'vertical'
		spacing:dp(35)
		padding:dp(10)

		MDLabel:
			text:'Create a new post'
			theme_text_color:'Primary'
			font_name:'Montserrat'
			font_style:'H2'
			#pos_hint: {'center_x': .5, 'center_y':.9}
			size_hint_y:.08
				
		LooqTextField:
			hint_text:'Enter a name here'
			id:looq_name_field
			max_text_length: 50
			size_hint_y:.04
			on_text:self.check_length(self.text, self.max_text_length)


		LooqTextField:
			hint_text:'Please write a brief description'
			#multiline: True
			size_hint_y:.04
			max_text_length: 150
			id:looq_description_field
			on_text:self.check_length(self.text, self.max_text_length)


	BoxLayout:
		size_hint_y:.4
		orientation:'vertical'
		padding:dp(5)
		
		MDLabel:
			text:'Select a category'
			#font_size:dp(11)
			theme_text_color:'Hint'
			font_name:'Montserrat'
			#font_style:'H6'
			size_hint_y:.1
			id:looq_category_text
			
		ScrollView:
			do_scroll_y: False
			size_hint_y: .1
			bar_width:0
			
			BoxLayout:
				orientation: "vertical"
				size_hint_x: None
				width: self.minimum_width
				GridLayout:
					rows: 1
					size_hint_y: .4
					size_hint_x: None
					width: self.minimum_width
					spacing:dp(10)
					padding:dp(10)		
					CategoryButtonPost:
						icon: 'alpha-g-circle'
						text: 'General'
						md_bg_color: ASH
						on_press:
							looq_category_text.text=self.text
					CategoryButtonPost:
						icon: 'dog-side'
						text: 'Pets'
						md_bg_color: PINK
						on_press:
							looq_category_text.text=self.text
							
					CategoryButtonPost:
						icon: 'food'
						text: 'Food'
						md_bg_color: LIGHT_PINK
						on_press:
							looq_category_text.text=self.text
							

					CategoryButtonPost:
						icon: 'human'
						text: 'Personal'
						md_bg_color: DARK
						on_press:
							looq_category_text.text=self.text
							

					CategoryButtonPost:
						icon: 'monitor-cellphone'
						text: 'Gadgets'
						md_bg_color: ASH
						on_press:
							looq_category_text.text=self.text
							

					CategoryButtonPost:
						icon: 'bookshelf'
						text: 'Stationary'
						md_bg_color: PURPLE
						on_press:
							looq_category_text.text=self.text
							

					CategoryButtonPost:
						icon: 'tree'
						text: 'Others'
						md_bg_color: LIGHT_ORANGE
						on_press:
							looq_category_text.text=self.text
							

		GridLayout:
			size_hint_y:.08
			cols:2
			MDIconButton:
				icon:'file-image'
				on_release:
					#sm.current='looq_file_manager'
					#sm.transition.direction='left'
					root.open_looq_file_manager()
			MDLabel:
				text:'Pick an image'
				#font_size:dp(11)
				theme_text_color:'Hint'
				font_name:'Montserrat'
				#font_style:'H6'
				font_size:dp(13)
				#size_hint_y:.05
				id:looq_image_text
					
		
		
		Widget:
			size_hint_y:.008

		BoxLayout:
			orientation:'vertical'
			size_hint_y:.1
			
			
			MDFillRoundFlatIconButton:
				icon: 'check'
				text: '       Submit       '
				id:looq_post_send_button
				md_bg_color: get_color_from_hex("#e99c66" )
				font_name:'Montserrat'
				pos_hint: {'center_x': .5}
				on_press:
					root.verify_looq_post_form(looq_name_field.text, looq_description_field.text, looq_category_text.text ,looq_image_text.text)

			Widget:
				size_hint_y:.01

	Widget:
		size_hint_y:.1




''')


class PostNewBox(BoxLayout):
	manager_open = False
	file_manager = None

	def looq_post_request(self, object_name, description, category, looq_image):
		CATEGORY_CHOICES={

					'General':1,
					'Gadgets':2,
					'Personal':3,
					'Pets':4,
					'Food':5,
					'Stationary':6,
					'Others':7

							}
		_category=CATEGORY_CHOICES[category]

		store = JsonStore('looq.json')
		USERNAME=store.get('LooqUserProfile')['username']
		TOKEN=store.get('LooqUserProfile')['token']
		USER_PK=store.get('LooqUserDetail')['user_pk']


		img={
			"image": open(looq_image, 'rb') ,
			}

		headers ={'username':USERNAME, 'Authorization': 'Token '+str(TOKEN)}
		today=(str(t.tm_year)+'-'+str(t.tm_mon)+'-'+str(t.tm_mday))


		data={
			"author": USER_PK,	
			"object_name": object_name ,
			"description": description,
			"category": _category,
			"posted_on": today   
			}
		
	
		try:
			#use token instead
			r=requests.post(app.looq_api_post, files=img, data=data, headers=headers)
			if r.status_code==201:
				app.show_snackbar('Posted ! ')
				Thread(target=app.get_looq_objects_all).start()
				app.goto_screen('looq-home', 'right')

			else:
				app.show_snackbar('Error posting, please try again later ! ')
		except ConnectionError:
			app.show_toast('Connection Failed ! ')
		
	def verify_looq_post_form(self,looq_name_field,looq_description_field,looq_category_text,looq_image_text):


		if len(looq_name_field) < 1:
			app.show_snackbar('Name field cannot be empty !')
			return

		if len(looq_description_field) < 1:
			app.show_snackbar('Description field cannot be empty !')
			return
		
		if looq_category_text== 'Select a category' :
			app.show_snackbar('Please select a category !')
			return

		if looq_image_text == 'Pick an image' :
			app.show_snackbar('Please pick an image !')
			return
		Thread(target=self.looq_post_request(looq_name_field, looq_description_field, looq_category_text, looq_image_text)).start()


	def open_looq_file_manager(self):
		if platform=='android':
			from jnius import autoclass

			Environment = autoclass('android.os.Environment')
			Context = autoclass('android.content.Context')

			path=(Environment.getExternalStoragePublicDirectory(
						Environment.DIRECTORY_PICTURES).getAbsolutePath())
		else:
			#this path is just for debugging in order not to import the whole plyer module
			#therefore reducing the app size
			path='C:/Users/'
		self.file_manager = MDFileManager(exit_manager=self.exit_manager,
					select_path=self.select_path,previous=True,icon='check',ext=['jpg','img','png','jpeg',])
		self.file_manager.show(path)

	def select_path(self, path):    
		self.exit_manager()
		if type(path) == str:
			self.ids.looq_image_text.text=path
		else:
			self.ids.looq_image_text.text=(", ".join(path))

	def exit_manager(self, *args):
		self.manager_open = False
		self.file_manager.close()
		#self.root.current='looq-post'
		#self.root.transition.direction='right'

	def check_looq_name_length(self, text,max_text_length):
		if len(text) > max_text_length :
			self.ids.looq_name_field.text=text[:max_text_length+1]

	def check_looq_decription_length(self, text,max_text_length):
		if len(text) > max_text_length :
			self.ids.looq_description_field.text=text[:max_text_length+1]

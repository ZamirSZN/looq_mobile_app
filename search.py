from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.parser import global_idmap
from kivy.network.urlrequest import UrlRequest


app=App.get_running_app()


Builder.load_string('''

<LooqSearchRv@RecycleView>
    viewclass: 'LooqWidget'
    RecycleBoxLayout:
        orientation: 'vertical'
        size_hint: 1, None
        height: self.minimum_height
        default_size_hint: 1, None
        default_size: 0, dp(110)
		spacing:dp(15)


<SearchBox>
	orientation:'vertical'
	padding:dp(20)
	MDLabel:
		text:'Search'
		size_hint_y:.1
		font_style:'H4'
		font_name:'Montserrat'
		opposite_colors:False
		id:search_label
		theme_text_color:'Primary'
		halign:'left'
	
	GridLayout:
		cols:2
		size_hint_y:.12
		LooqTextField:
			hint_text:'Enter text here'
			id: looq_search_field
			max_text_length:50
			multiline:False
			size_hint_y:.04
			required:False
			on_text:self.check_length(self.text, self.max_text_length)

			on_text_validate:
				root.search(looq_search_field.text)

			
			
		MDIconButton:
			icon:"magnify"
			on_release:
				root.search(looq_search_field.text)
	
	
	LooqSearchRv:
		id:looq_search_rv
		size_hint_y:.7
	FloatLayout:
		size_hint_y:.2
		MDSpinner:
			size_hint:.08, 0.8
			pos_hint: {'center_x': .5, 'center_y': 1}
			active: False
			id:looq_search_rv_spinner
	

	
''')



class SearchBox(BoxLayout):
	def check_looq_search_length(self, text,max_text_length):
		if len(text) > max_text_length :
			self.ids.looq_search_field.text=text[:max_text_length+1]

	
	def put_json_to_home_rv(self, response):
		all_looq_json_item=response
		looq_search_rv= self.ids.looq_search_rv
		looq_search_rv.data=[]
		
		for missing_object in all_looq_json_item:
			author=missing_object["author"]
			object_name=missing_object["object_name"]
			description=missing_object["description"]
			image=missing_object["image"]
			category=missing_object["category"]
			posted_on=missing_object['posted_on']
			
			looq_search_rv.data.append({
				"author":str(author),
				"object_name": str(object_name),
				"description": str(description),
				'image': str(image),
				"category": str(category),
				'posted_on':str(posted_on),
			})
		
		
		self.ids.looq_search_rv_spinner.active=False

	
	def search(self, search_text):
		if len(search_text)>= 1:
			self.ids.looq_search_rv_spinner.active=True
			self.looq_search(app.looq_api_search+search_text)
		else:
			app.show_snackbar('Search field cannot be empty !')
			self.ids.looq_search_rv_spinner.active=False
	
	def check_result(self, req, result):
		if result==[]:
			app.show_toast('No items matches your search.!')
			self.ids.looq_search_rv_spinner.active=False
			self.ids.looq_search_rv.data=[]
			return
		self.put_json_to_home_rv(result)

	def looq_search(self, search_url):
		UrlRequest(search_url, on_success=self.check_result,on_failure=app.on_failure,on_error=app.on_error)
		

global_idmap['search_box'] = SearchBox()
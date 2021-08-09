
from kivy.lang import Builder

from kivymd.uix.textfield import MDTextField

Builder.load_string('''
<LooqTextField>
	font_name:'Montserrat'
	required:True
	multiline: False


''')


class LooqTextField(MDTextField):
	def check_length(self, text,max_text_length):
		if len(text) > max_text_length :
			self.text=text[:max_text_length+1]

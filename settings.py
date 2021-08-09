from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

Builder.load_string('''

#:import Clipboard kivy.core.clipboard.Clipboard

<SettingsBox>
    orientation:"vertical"
    padding:dp(20)

    MDLabel:
        text:'LOOQ'
        size_hint_y:.2
        font_style:'H1'
        font_name:'Montserrat'
        opposite_colors:False
        theme_text_color:'Primary'
        halign:'center'

    OneLineAvatarListItem:
        text: "Dark Mode"
        on_release:app.nightmode_bottom_sheet()
        IconLeftWidget:
            icon: "weather-night"



    TwoLineIconListItem:
        text: "Reset App"
        secondary_text: "Reset app preference and data"
        on_release:app.reset_bottomsheet()

        IconLeftWidget:
            icon: "delete-empty"

    OneLineIconListItem:
        text: "Source code"
        on_release:app.open_link("https://github.com/zamirszn/looq_mobile_app")	
        IconLeftWidget:
            icon: "github-circle"

    TwoLineIconListItem:
        text: "Dev"
        secondary_text: "@ZamirSZN"
        on_release:app.open_link("https://mubaraklawal.herokuapp.com")	
        IconLeftWidget:
            icon: "code-tags"
    TwoLineIconListItem:
        text: "Contact me , Report a bug"
        secondary_text: "mubaraklawal52@gmail.com"
        on_release:
            Clipboard.copy("https://mubaraklawal52@gmail.com")
            app.show_toast('Email copied')
        IconLeftWidget:
            icon: "gmail"
        
    Widget:
        size_hint_y: .1	

    


''')

class SettingsBox(BoxLayout):
    pass
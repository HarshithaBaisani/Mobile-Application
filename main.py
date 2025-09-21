from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarIconListItem, MDList
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.card import MDCard
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.uix.image import Image
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
from kivy.uix.screenmanager import SlideTransition
import random
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.floatlayout import FloatLayout
import webbrowser

class BaseScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg = Image(source=r"C:\Users\harsh\OneDrive\Desktop\FlutterApp\assets.jpg", allow_stretch=True, keep_ratio=False)
        self.add_widget(self.bg)
        self.base_layout = MDBoxLayout(orientation='vertical')
        self.add_widget(self.base_layout)
        header = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(56), padding=dp(8), spacing=dp(12))
        logo = Image(source=r"C:\Users\harsh\OneDrive\Desktop\FlutterApp\logo.jpg", size_hint=(None, 1), width=dp(70))
        header.add_widget(logo)
        header.add_widget(MDLabel(text="Calley", font_style="H6", valign="middle"))
        self.base_layout.add_widget(header)

USER_DATA = {}
TEST_LIST = [
    {"name": "Test 1", "status": "Pending", "total_calls": 5},
    {"name": "Test 2", "status": "Done", "total_calls": 10},
    {"name": "Test 3", "status": "Scheduled", "total_calls": 3},
]

class LanguageScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_language = "English"
        self.dialog = None
        from kivymd.uix.card import MDCard
        layout = MDBoxLayout(orientation="vertical", padding=dp(24), spacing=dp(16))
        self.base_layout.add_widget(layout)
        card = MDCard(orientation="vertical", padding=dp(18), size_hint=(0.95, None), height=dp(340), pos_hint={"center_x": 0.5}, elevation=8)
        card.add_widget(MDLabel(text="Choose Your Language", halign="center", font_style="H4", theme_text_color="Custom", text_color=(0.2,0.4,0.7,1)))
        scroll = ScrollView()
        lang_list = MDList()
        for lang in ["English", "Hindi", "Bengali", "Kannada", "Punjabi", "Tamil","Telugu"]:
            from kivymd.uix.selectioncontrol import MDCheckbox
            item = OneLineAvatarIconListItem(text=lang)
            lang_list.add_widget(item)
        scroll.add_widget(lang_list)
        card.add_widget(scroll)
        btn = MDRaisedButton(text="Continue", pos_hint={"center_x": 0.5}, md_bg_color=(0.2,0.5,0.8,1), elevation=6, on_release=self.next_screen)
        card.add_widget(btn)
        layout.add_widget(card)

    def set_language(self, lang, active):
        if active:
            self.selected_language = lang
            if self.dialog:
                self.dialog.dismiss()
            self.dialog = MDDialog(title="Choose Your Language", text=f"You have selected {lang}.")
            self.dialog.open()

    def next_screen(self, instance):
        USER_DATA["language"] = self.selected_language
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "registration"

class RegistrationScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDBoxLayout(orientation='vertical', padding=dp(16), spacing=dp(18))

        header = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(56), padding=dp(8), spacing=dp(12))
        logo = Image(source=r"C:\Users\harsh\OneDrive\Desktop\FlutterApp\logo.jpg", size_hint=(None, 1), width=dp(70))
        header.add_widget(logo)
        header.add_widget(MDLabel(text="Calley", font_style="H6", valign="middle"))
        layout.add_widget(header)

        layout.add_widget(MDLabel(text="Welcome", halign="center", font_style="H4"))
        layout.add_widget(MDLabel(text="Please register to continue", halign="center", font_style="Subtitle1"))

        signin_label = MDLabel(
            text='[color=000000]Already have an account?[/color] [ref=signin][color=2962FF]Sign in[/color][/ref]',
            halign='center',
            markup=True
        )
        signin_label.bind(on_ref_press=self.go_to_login)
        layout.add_widget(signin_label)

        self.name_input = MDTextField(hint_text="Full Name", mode="rectangle")
        self.email_input = MDTextField(hint_text="Email", mode="rectangle")
        self.password_input = MDTextField(hint_text="Password", password=True, mode="rectangle")
        self.mobile_input = MDTextField(hint_text="Mobile Number", mode="rectangle")
        layout.add_widget(self.name_input)
        layout.add_widget(self.email_input)
        layout.add_widget(self.password_input)
        layout.add_widget(self.mobile_input)

        terms_layout = MDBoxLayout(orientation='horizontal', spacing=dp(8), size_hint_y=None, height=dp(32), padding=(dp(8), 0, dp(8), 0))
        self.terms_checkbox = MDCheckbox(size_hint_x=None, width=dp(32))
        terms_label = MDLabel(text='I agree with terms and conditions', size_hint_x=1, halign='left', valign='middle', font_style="Caption")
        terms_layout.add_widget(self.terms_checkbox)
        terms_layout.add_widget(terms_label)
        layout.add_widget(terms_layout)

        self.register_btn = MDRaisedButton(text="Register", pos_hint={"center_x": 0.5})
        self.register_btn.bind(on_release=self.register)
        layout.add_widget(self.register_btn)

        self.base_layout.clear_widgets()
        self.base_layout.add_widget(layout)

    def register(self, instance):
        if not self.terms_checkbox.active:
            MDDialog(title="Error", text="You must agree to the terms and conditions").open()
            return

        name = self.name_input.text
        email = self.email_input.text
        password = self.password_input.text
        mobile = self.mobile_input.text

        if not (name and email and password and mobile):
            MDDialog(title="Error", text="Please fill all fields.").open()
            return

        USER_DATA['name'] = name
        USER_DATA['email'] = email
        USER_DATA['phone'] = mobile
        USER_DATA['password'] = password  

        MDDialog(title="Success", text=f"Registration successful! Proceed to OTP.").open()
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'otp'

    def go_to_login(self, *args):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'login'


OTP_STORAGE = {}

class OTPScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        layout.add_widget(MDLabel(text="Enter OTP sent to your phone", halign="center", font_style="H5"))

        self.otp_input = MDTextField(hint_text="OTP", size_hint_x=0.8, pos_hint={"center_x": 0.5})
        layout.add_widget(self.otp_input)

        send_btn = MDRaisedButton(text="Send OTP", pos_hint={"center_x": 0.5})
        send_btn.bind(on_release=self.send_otp)
        layout.add_widget(send_btn)

        verify_btn = MDRaisedButton(text="Verify OTP", pos_hint={"center_x": 0.5})
        verify_btn.bind(on_release=self.verify_otp)
        layout.add_widget(verify_btn)

        self.base_layout.add_widget(layout)

    def send_otp(self, instance):
        phone_number = USER_DATA.get('phone', '')  # Replace with actual phone number from your app
        otp = str(random.randint(100000, 999999))  # 6-digit OTP
        OTP_STORAGE[phone_number] = otp

        MDDialog(title="OTP Sent", text=f"Your OTP is: {otp}").open()
        print(f"OTP for {phone_number} is {otp}")  # Simulate sending to phone

    def verify_otp(self, instance):
        phone_number = USER_DATA.get('phone', '')
        entered_otp = self.otp_input.text.strip()

        if OTP_STORAGE.get(phone_number) == entered_otp:
            MDDialog(title="Success", text="OTP Verified!").open()
            self.manager.transition = SlideTransition(direction='left')
            self.manager.current = 'login'
        else:
            MDDialog(title="Error", text="Invalid OTP. Please try again.").open()


class LoginScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDBoxLayout(orientation='vertical', padding=dp(16), spacing=dp(18))

        header = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(56), padding=dp(8), spacing=dp(12))
        logo = Image(source=r"C:\Users\harsh\OneDrive\Desktop\FlutterApp\logo.jpg", size_hint=(None, 1), width=dp(70))
        header.add_widget(logo)
        header.add_widget(MDLabel(text="Calley", font_style="H6", valign="middle"))
        layout.add_widget(header)

        text_layout = MDBoxLayout(orientation='vertical', spacing=dp(8), size_hint_y=None)
        text_layout.height = dp(100)  # adjust height if needed

        welcome_label = MDLabel(text="Welcome", halign="center", font_style="H4")
        signin_msg = MDLabel(text="Please sign in to continue", halign="center", font_style="Subtitle1")
        signup_label = MDLabel(
            text='[color=000000]Don’t have an account?[/color] [ref=signup][color=2962FF]Sign up[/color][/ref]',
            halign='center',
            markup=True
        )
        signup_label.bind(on_ref_press=self.go_to_registration)

        text_layout.add_widget(welcome_label)
        text_layout.add_widget(signin_msg)
        text_layout.add_widget(signup_label)
        layout.add_widget(text_layout)

        self.email_input = MDTextField(hint_text="Email", mode="rectangle")
        self.password_input = MDTextField(hint_text="Password", password=True, mode="rectangle")
        layout.add_widget(self.email_input)
        layout.add_widget(self.password_input)

        forgot_label = MDLabel(
            text='[ref=forgot][color=2962FF]Forgot Password?[/color][/ref]',
            halign='right',
            markup=True
        )
        forgot_label.bind(on_ref_press=self.forgot_password)
        layout.add_widget(forgot_label)

        # Sign in button
        signin_btn = MDRaisedButton(text="Sign In", pos_hint={"center_x": 0.5})
        signin_btn.bind(on_release=self.login)
        layout.add_widget(signin_btn)

        # Clear base layout and add new layout
        self.base_layout.clear_widgets()
        self.base_layout.add_widget(layout)

    def login(self, instance):
        if not (self.email_input.text and self.password_input.text):
            MDDialog(title="Error", text="Fill all fields").open()
            return
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'dashboard'

    def go_to_registration(self, *args):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'registration'

    def forgot_password(self, *args):
        MDDialog(title="Info", text="Forgot Password clicked!").open()

class DashboardScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from kivymd.uix.toolbar import MDTopAppBar
        from kivymd.uix.card import MDCard
        from kivymd.uix.button import MDIconButton
        from kivy.uix.image import Image
        from kivy.uix.floatlayout import FloatLayout
        from kivy.uix.widget import Widget
        import webbrowser

        self.base_layout.clear_widgets()

        # 1️⃣ Top App Bar with Hamburger + Logo + Name
        top_bar = MDTopAppBar(
            title="Calley",
            pos_hint={"top": 1},
            elevation=8,
            left_action_items=[["menu", lambda x: self.open_menu()]],
        )
        self.base_layout.add_widget(top_bar)

        # 2️⃣ Main Layout
        main_layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(15),
        )


        # Spacer
        main_layout.add_widget(Widget(size_hint_y=None, height=dp(10)))

        # 3️⃣ Educational Video Card
        video_url = "https://www.youtube.com/watch?v=2vj37yeQQHg"
        video_card = MDCard(
            orientation="vertical",
            padding=dp(10),
            size_hint=(0.95, None),
            height=dp(220),
            pos_hint={"center_x": 0.5},
            elevation=12,
        )
        float_layout = FloatLayout(size_hint=(1, 1))

        video_thumbnail = Image(
            source=r"C:\Users\harsh\OneDrive\Desktop\FlutterApp\video_thumbnail.jpg",
            size_hint=(1, None),
            height=dp(160),
            allow_stretch=True,
        )
        float_layout.add_widget(video_thumbnail)

        play_btn = MDIconButton(
            icon="play-circle",
            icon_size="60sp",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            theme_text_color="Custom",
            text_color=(1, 0, 0, 1),
        )
        play_btn.bind(on_release=lambda x: webbrowser.open(video_url))
        float_layout.add_widget(play_btn)

        video_card.add_widget(float_layout)
        video_card.add_widget(
            MDLabel(
                text="Watch Educational Video",
                font_style="Subtitle1",
                halign="center",
                theme_text_color="Custom",
                text_color=(0.1, 0.3, 0.6, 1),
            )
        )
        main_layout.add_widget(video_card)

        # Add main layout above navigation
        self.base_layout.add_widget(main_layout)

        # 4️⃣ Bottom Navigation with Start Calling as tab
        from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem

        bottom_nav = MDBottomNavigation()

        bottom_nav.add_widget(
            MDBottomNavigationItem(
                name="home", text="Home", icon="home", on_tab_press=lambda x: self.goto_dashboard()
            )
        )
        bottom_nav.add_widget(
            MDBottomNavigationItem(
                name="calllist", text="Call List", icon="format-list-bulleted",
                on_tab_press=lambda x: self.goto_calllist(None)
            )
        )
        bottom_nav.add_widget(
            MDBottomNavigationItem(
                name="startcall", text="Start Calling", icon="phone",
                on_tab_press=lambda x: self.goto_calllist(None)
            )
        )
        bottom_nav.add_widget(
            MDBottomNavigationItem(
                name="register", text="Register Call", icon="phone-plus",
                on_tab_press=lambda x: self.goto_register()
            )
        )
        bottom_nav.add_widget(
            MDBottomNavigationItem(
                name="profile", text="Profile", icon="account",
                on_tab_press=lambda x: self.goto_profile()
            )
        )

        self.base_layout.add_widget(bottom_nav)

    # Helper methods for navigation
    def open_menu(self):
        print("Menu clicked!")

    def goto_dashboard(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "dashboard"

    def goto_calllist(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "testlist"

    def goto_register(self):
        print("Go to Call Register screen")

    def goto_profile(self):
        print("Go to Profile screen")



class TestListScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation="vertical", padding=dp(16), spacing=dp(18))
        card = MDCard(orientation="vertical", padding=dp(18), size_hint=(0.97, None), height=dp(320), pos_hint={"center_x": 0.5}, elevation=8)
        card.add_widget(MDLabel(text="Test List", font_style="H4", halign="center", theme_text_color="Custom", text_color=(0.2,0.5,0.8,1)))
        scroll = ScrollView()
        list_layout = MDList()
        for item in TEST_LIST:
            list_item = OneLineAvatarIconListItem(text=f"{item['name']} | {item['status']} | Calls: {item['total_calls']}")
            icon = MDIconButton(icon="phone", theme_text_color="Custom", text_color=(0.1,0.6,0.5,1))
            list_item.add_widget(icon)
            list_item.bind(on_release=self.goto_challenge)
            list_layout.add_widget(list_item)
        scroll.add_widget(list_layout)
        card.add_widget(scroll)
        layout.add_widget(card)
        self.base_layout.add_widget(layout)

    def goto_challenge(self, instance):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'challenge'

from kivy.core.image import Image as CoreImage
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.screen import MDScreen
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import SlideTransition
import matplotlib.pyplot as plt
import io

class ChallengeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Sample data
        self.call_data = {
            "Pending": 5,
            "Done": 8,
            "Scheduled": 3
        }

        main_layout = BoxLayout(orientation='vertical', padding=dp(16), spacing=dp(20))

        # Title
        main_layout.add_widget(MDLabel(
            text="Test Lists",
            font_style="H5",
            halign="center"
        ))

        # Pie chart
        pie_img = self.create_pie_chart()
        main_layout.add_widget(pie_img)

        # Summary below pie chart
        summary_layout = BoxLayout(orientation='horizontal', spacing=dp(20), size_hint_y=None, height=dp(40))
        for key, value in self.call_data.items():
            summary_layout.add_widget(MDLabel(
                text=f"{key}: {value}",
                halign="center",
                font_style="Subtitle1"
            ))
        main_layout.add_widget(summary_layout)

        # Spacer
        main_layout.add_widget(Widget(size_hint_y=None, height=dp(10)))

        # Start Calling Now button
        btn = MDRaisedButton(
            text="Start Calling Now",
            pos_hint={"center_x": 0.5},
            size_hint=(0.6, None),
            height=dp(45)
        )
        btn.bind(on_release=self.goto_calldetails)
        main_layout.add_widget(btn)

        self.add_widget(main_layout)

    def create_pie_chart(self):
        labels = list(self.call_data.keys())
        sizes = list(self.call_data.values())
        colors = ['#FF6B6B', '#4ECDC4', '#FFD93D']  # Pending=Red, Done=Greenish, Scheduled=Yellow

        fig, ax = plt.subplots(figsize=(3,3), dpi=80)
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.0f%%', startangle=90, colors=colors)
        ax.axis('equal')  # Equal aspect ratio ensures pie is circle

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
        buf.seek(0)
        img = CoreImage(buf, ext='png').texture
        buf.close()
        plt.close(fig)

        return Image(texture=img, size_hint=(1, None), height=dp(200))

    def goto_calldetails(self, instance):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'calldetails'


class CallDetailsScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation="vertical", padding=dp(16), spacing=dp(14))
        layout.add_widget(MDLabel(text="Call Details", font_style="H5", halign="center"))
        from kivymd.uix.card import MDCard
        for call in TEST_LIST:
            card = MDCard(size_hint=(0.9, None), height=dp(60), padding=dp(10), pos_hint={"center_x": 0.5})
            card.add_widget(MDLabel(text=f"{call['name']} - {call['status']} - Calls: {call['total_calls']}", halign="center"))
            layout.add_widget(card)
        self.base_layout.add_widget(layout)
class ProfileScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation="vertical", padding=dp(16), spacing=dp(18))
        layout.add_widget(MDLabel(text="Profile", font_style="H5", halign="center"))
        layout.add_widget(MDLabel(text=f"Name: {USER_DATA.get('name', '')}", halign="center"))
        layout.add_widget(MDLabel(text=f"Email: {USER_DATA.get('email', '')}", halign="center"))
        logout_btn = MDRaisedButton(text="Logout", pos_hint={"center_x": 0.5}, size_hint=(0.5, None), height=dp(45))
        logout_btn.bind(on_release=self.logout)
        layout.add_widget(logout_btn)
        self.base_layout.add_widget(layout)

    def logout(self, instance):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "login"

class CalleyApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        sm = ScreenManager()
        sm.add_widget(LanguageScreen(name="language"))
        sm.add_widget(RegistrationScreen(name="registration"))
        sm.add_widget(OTPScreen(name="otp"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(DashboardScreen(name="dashboard"))
        sm.add_widget(TestListScreen(name="testlist"))
        sm.add_widget(ChallengeScreen(name="challenge"))
        sm.add_widget(CallDetailsScreen(name="calldetails"))
        sm.add_widget(ProfileScreen(name="profile"))
        return sm

if __name__ == "__main__":
    CalleyApp().run()

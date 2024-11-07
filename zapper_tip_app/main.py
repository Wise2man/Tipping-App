import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from database import initialize_database
from ui_components import (
    RegisterScreen,
    LoginScreen,
    MainApp,
    PaymentHistoryScreen,
    ForgotPasswordScreen,
    SetNewPasswordScreen,
    AdminScreen,
    AdminPaymentHistoryScreen,
)

# Database setup
DATABASE_NAME = 'payfast_tip_app.db'

# Initialize the database
initialize_database()

class ZapperTipApp(App):
    def build(self):
        # Set up the main app layout
        self.root = BoxLayout(orientation='vertical')
        self.current_user = None
        self.is_admin = False
        self.user_email = None
        self.user_name_first = None
        self.show_login_screen()
        return self.root

    def show_main_app(self):
        # Show the main application screen
        self.root.clear_widgets()
        self.root.add_widget(MainApp(self))

    def show_login_screen(self):
        # Show the login screen
        self.root.clear_widgets()
        self.root.add_widget(LoginScreen(self))

    def show_register_screen(self):
        # Show the registration screen
        self.root.clear_widgets()
        self.root.add_widget(RegisterScreen(self))

    def show_payment_history_screen(self):
        # Show the payment history screen
        self.root.clear_widgets()
        self.root.add_widget(PaymentHistoryScreen(self))

    def show_forgot_password_screen(self):
        # Show the forgot password screen
        self.root.clear_widgets()
        self.root.add_widget(ForgotPasswordScreen(self))

    def show_set_new_password_screen(self, email):
        # Show the set new password screen
        self.root.clear_widgets()
        self.root.add_widget(SetNewPasswordScreen(self, email))

    def show_admin_screen(self):
        # Show the admin management screen
        self.root.clear_widgets()
        self.root.add_widget(AdminScreen(self))

    def show_admin_payment_history_screen(self):
        # Show the admin payment history screen
        self.root.clear_widgets()
        self.root.add_widget(AdminPaymentHistoryScreen(self))

    def logout(self):
        self.current_user = None
        self.is_admin = False
        self.user_email = None
        self.user_name_first = None
        self.show_login_screen()

if __name__ == '__main__':
    ZapperTipApp().run()
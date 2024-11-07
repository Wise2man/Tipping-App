from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from database import sqlite3, DATABASE_NAME, add_user, get_user, save_payment, get_payments, get_all_users, delete_user
from payfast import generate_payfast_url
from qr_code import generate_qr_code

class RegisterScreen(BoxLayout):
    def __init__(self, app, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        self.app = app
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        self.label = Label(text="Create Account")
        self.add_widget(self.label)
        self.username_input = TextInput(hint_text='Username', multiline=False)
        self.add_widget(self.username_input)
        self.password_input = TextInput(hint_text='Password', multiline=False, password=True)
        self.add_widget(self.password_input)
        self.email_input = TextInput(hint_text='Email', multiline=False)
        self.add_widget(self.email_input)
        self.name_first_input = TextInput(hint_text='First Name', multiline=False)
        self.add_widget(self.name_first_input)
        self.register_button = Button(text="Register")
        self.register_button.bind(on_press=self.register)
        self.add_widget(self.register_button)
        self.message_label = Label()
        self.add_widget(self.message_label)
        self.add_widget(Button(text="Back", on_press=lambda x: self.app.show_login_screen()))

    def register(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        email = self.email_input.text.strip()
        name_first = self.name_first_input.text.strip()
        if not username or not password or not email or not name_first:
            self.message_label.text = "All fields must be filled."
            return
        user = get_user(username, password)
        if user:
            self.message_label.text = "Username already exists. Redirecting to login."
            self.app.show_login_screen()
        else:
            add_user(username, password, email, name_first)
            self.message_label.text = "Account created! You can now log in."
            self.app.show_login_screen()

class LoginScreen(BoxLayout):
    def __init__(self, app, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.app = app
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        self.label = Label(text="Login")
        self.add_widget(self.label)
        self.username_input = TextInput(hint_text='Username', multiline=False)
        self.add_widget(self.username_input)
        self.password_input = TextInput(hint_text='Password', multiline=False, password=True)
        self.add_widget(self.password_input)
        self.login_button = Button(text="Login")
        self.login_button.bind(on_press=self.login)
        self.add_widget(self.login_button)
        self.register_button = Button(text="Create Account")
        self.register_button.bind(on_press=lambda x: self.app.show_register_screen())
        self.add_widget(self.register_button)
        self.forgot_password_button = Button(text="Forgot Password")
        self.forgot_password_button.bind(on_press=lambda x: self.app.show_forgot_password_screen())
        self.add_widget(self.forgot_password_button)
        self.message_label = Label()
        self.add_widget(self.message_label)

    def login(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        user = get_user(username, password)
        if user:
            self.app.current_user = username
            self.app.is_admin = user[4]
            self.app.user_email = user[2]
            self.app.user_name_first = user[3]
            if self.app.is_admin:
                self.app.show_admin_screen()
            else:
                self.app.show_main_app()
        else:
            self.message_label.text = "Invalid username or password."

class MainApp(BoxLayout):
    def __init__(self, app, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.app = app
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        if not self.app.is_admin:
            self.label = Label(text="Enter Tip Amount:")
            self.add_widget(self.label)
            self.amount_input = TextInput(hint_text='Amount', multiline=False)
            self.add_widget(self.amount_input)
            self.pay_button = Button(text="Pay Now")
            self.pay_button.bind(on_press=self.pay_now)
            self.add_widget(self.pay_button)
        else:
            self.label = Label(text="Welcome, Admin! You cannot make payments.")
            self.add_widget(self.label)
        self.history_button = Button(text="View Payment History")
        self.history_button.bind(on_press=self.show_payment_history)
        self.add_widget(self.history_button)
        self.add_widget(Button(text="Back", on_press=lambda x: self.app.show_login_screen()))
        self.add_widget(Button(text="Logout", on_press=self.logout))

    def pay_now(self, instance):
        try:
            amount = float(self.amount_input.text)
            username = self.app.current_user
            name_first = self.app.user_name_first
            email = self.app.user_email
            # Save payment to the database
            save_payment(username, amount)
            self.amount_input.text = ""
            # Generate PayFast URL
            payfast_url = generate_payfast_url(amount, username, name_first, email)
            # Generate QR code
            generate_qr_code(payfast_url)
            # Display QR code on the screen
            self.display_qr_code()
        except ValueError:
            self.label.text = "Please enter a valid amount."

    def display_qr_code(self):
        qr_image = Image(source='payfast_payment_qr.png')
        self.add_widget(qr_image)

    def show_payment_history(self, instance):
        self.app.show_payment_history_screen()

    def logout(self, instance):
        self.app.logout()

class PaymentHistoryScreen(BoxLayout):
    def __init__(self, app, **kwargs):
        super(PaymentHistoryScreen, self).__init__(**kwargs)
        self.app = app
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        self.label = Label(text="Payment History", font_size='20sp')
        self.add_widget(self.label)
        self.history_layout = GridLayout(cols=1, size_hint_y=None)
        self.history_layout.bind(minimum_height=self.history_layout.setter('height'))
        self.add_widget(self.history_layout)
        self.load_payment_history()
        self.back_button = Button(text="Back")
        self.back_button.bind(on_press=lambda x: self.app.show_main_app())
        self.add_widget(self.back_button)

    def load_payment_history(self):
        self.history_layout.clear_widgets()
        payments = get_payments(username=self.app.current_user)
        if payments:
            for amount, timestamp in payments:
                date, time = timestamp.split(" ")
                self.history_layout.add_widget(Label(text=f"You paid R{amount:.2f} on {date} at {time}", font_size='16sp'))
        else:
            self.history_layout.add_widget(Label(text="No payments found.", font_size='16sp'))

class ForgotPasswordScreen(BoxLayout):
    def __init__(self, app, **kwargs):
        super(ForgotPasswordScreen, self).__init__(**kwargs)
        self.app = app
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        self.label = Label(text="Forgot Password")
        self.add_widget(self.label)
        self.email_input = TextInput(hint_text='Enter your email', multiline=False)
        self.add_widget(self.email_input)
        self.reset_button = Button(text="Reset Password")
        self.reset_button.bind(on_press=self.reset_password)
        self.add_widget(self.reset_button)
        self.message_label = Label()
        self.add_widget(self.message_label)
        self.add_widget(Button(text="Back", on_press=lambda x: self.app.show_login_screen()))

    def reset_password(self, instance):
        email = self.email_input.text
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT username FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        if user:
            self.message_label.text = "Check your email for a reset link (simulated)."
            self.app.show_set_new_password_screen(email)
        else:
            self.message_label.text = "Email not found."
        conn.close()

class SetNewPasswordScreen(BoxLayout):
    def __init__(self, app, email, **kwargs):
        super(SetNewPasswordScreen, self).__init__(**kwargs)
        self.app = app
        self.email = email
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        self.label = Label(text="Set New Password")
        self.add_widget(self.label)
        self.new_password_input = TextInput(hint_text='New Password', multiline=False, password=True)
        self.add_widget(self.new_password_input)
        self.confirm_password_input = TextInput(hint_text='Confirm Password', multiline=False, password=True)
        self.add_widget(self.confirm_password_input)
        self.set_button = Button(text="Set Password")
        self.set_button.bind(on_press=self.set_password)
        self.add_widget(self.set_button)

    def set_password(self, instance):
        new_password = self.new_password_input.text
        confirm_password = self.confirm_password_input.text
        if new_password == confirm_password:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET password = ? WHERE email = ?', (new_password, self.email))
            conn.commit()
            conn.close()
            self.app.show_login_screen()
        else:
            self.label.text = "Passwords do not match."

class AdminScreen(BoxLayout):
    def __init__(self, app, **kwargs):
        super(AdminScreen, self).__init__(**kwargs)
        self.app = app
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        self.label = Label(text="Admin User Management", font_size='20sp')
        self.add_widget(self.label)
        self.user_list_layout = GridLayout(cols=1, size_hint_y=None)
        self.user_list_layout.bind(minimum_height=self.user_list_layout.setter('height'))
        self.add_widget(self.user_list_layout)
        self.load_users()
        self.username_input = TextInput(hint_text='Username', multiline=False)
        self.add_widget(self.username_input)
        self.password_input = TextInput(hint_text='Password', multiline=False)
        self.add_widget(self.password_input)
        self.email_input = TextInput(hint_text='Email', multiline=False)
        self.add_widget(self.email_input)
        self.name_first_input = TextInput(hint_text='First Name', multiline=False)
        self.add_widget(self.name_first_input)
        self.add_user_button = Button(text="Add User")
        self.add_user_button.bind(on_press=self.add_user)
        self.add_widget(self.add_user_button)
        self.delete_user_button = Button(text="Delete User")
        self.delete_user_button.bind(on_press=self.delete_user)
        self.add_widget(self.delete_user_button)
        self.payment_history_button = Button(text="View Payment History")
        self.payment_history_button.bind(on_press=lambda x: self.app.show_admin_payment_history_screen())
        self.add_widget(self.payment_history_button)
        self.back_button = Button(text="Back")
        self.back_button.bind(on_press=lambda x: self.app.logout())
        self.add_widget(self.back_button)

    def load_users(self):
        self.user_list_layout.clear_widgets()
        users = get_all_users()
        for username, email, name_first, is_admin in users:
            self.user_list_layout.add_widget(Label(text=f"Username: {username}, Email: {email}, Name: {name_first}, Admin: {bool(is_admin)}"))

    def add_user(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        email = self.email_input.text.strip()
        name_first = self.name_first_input.text.strip()
        if not username or not password or not email or not name_first:
            self.label.text = "All fields must be filled."
            return
        try:
            add_user(username, password, email, name_first)
            self.label.text = "User added successfully."
            self.load_users()
        except Exception as e:
            self.label.text = f"Error adding user: {e}"

    def delete_user(self, instance):
        username = self.username_input.text.strip()
        if not username:
            self.label.text = "Username must be provided."
            return
        try:
            delete_user(username)
            self.label.text = "User deleted successfully."
            self.load_users()
        except Exception as e:
            self.label.text = f"Error deleting user: {e}"

class AdminPaymentHistoryScreen(BoxLayout):
    def __init__(self, app, **kwargs):
        super(AdminPaymentHistoryScreen, self).__init__(**kwargs)
        self.app = app
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        self.label = Label(text="Admin Payment History", font_size='24sp', bold=True)
        self.add_widget(self.label)
        
        # Create a layout for the payment history
        self.history_layout = GridLayout(cols=4, size_hint_y=None)
        self.history_layout.bind(minimum_height=self.history_layout.setter('height'))
        self.history_layout.add_widget(Label(text="Username", bold=True, size_hint_y=None, height=40))
        self.history_layout.add_widget(Label(text="Amount (R)", bold=True, size_hint_y=None, height=40))
        self.history_layout.add_widget(Label(text="Date", bold=True, size_hint_y=None, height=40))
        self.history_layout.add_widget(Label(text="Time", bold=True, size_hint_y=None, height=40))
        self.add_widget(self.history_layout)
        
        # Pagination controls
        self.current_page = 0
        self.records_per_page = 5
        self.total_records = 0
        self.total_pages = 0
        
        # Navigation buttons
        self.navigation_layout = BoxLayout(size_hint_y=None, height=50)
        self.prev_button = Button(text="Previous")
        self.prev_button.bind(on_press=self.prev_page)
        self.navigation_layout.add_widget(self.prev_button)
        self.page_label = Label(text="")
        self.navigation_layout.add_widget(self.page_label)
        self.next_button = Button(text="Next")
        self.next_button.bind(on_press=self.next_page)
        self.navigation_layout.add_widget(self.next_button)
        self.add_widget(self.navigation_layout)
        
        # Total payments label
        self.total_label = Label(text="", size_hint_y=None, height=40)
        self.add_widget(self.total_label)
        
        # Load the payment history
        self.load_payment_history()
        
        # Back button
        self.back_button = Button(text="Back", size_hint_y=None, height=50)
        self.back_button.bind(on_press=lambda x: self.app.show_admin_screen())
        self.add_widget(self.back_button)

    def load_payment_history(self):
        self.history_layout.clear_widgets()
        payments = get_payments(username=None)
        
        # Calculate total records and pages
        self.total_records = len(payments)
        self.total_pages = (self.total_records // self.records_per_page) + (1 if self.total_records % self.records_per_page > 0 else 0)
        
        # Get the records for the current page
        start_index = self.current_page * self.records_per_page
        end_index = start_index + self.records_per_page
        current_payments = payments[start_index:end_index]
        
        # Calculate the overall total of all payments
        overall_total = sum(amount for _, amount, _ in payments)
        
        if current_payments:
            for username, amount, timestamp in current_payments:
                date, time = timestamp.split(" ")
                self.history_layout.add_widget(Label(text=username, size_hint_y=None, height=30))
                self.history_layout.add_widget(Label(text=f"R {amount:.2f}", size_hint_y=None, height=30))
                self.history_layout.add_widget(Label(text=date, size_hint_y=None, height=30))
                self.history_layout.add_widget(Label(text=time, size_hint_y=None, height=30))
            
            self.total_label.text = f"Total Payments: R {overall_total:.2f}"
        else:
            self.history_layout.add_widget(Label(text="No payments found.", font_size='16sp', size_hint_y=None, height=40))
            self.total_label.text = "Total Payments: R 0.00"
        
        self.update_page_label()

    def update_page_label(self):
        self.page_label.text = f"Page {self.current_page + 1} of {self.total_pages}"

    def prev_page(self, instance):
        if self.current_page > 0:
            self.current_page -= 1
            self.load_payment_history()

    def next_page(self, instance):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.load_payment_history()
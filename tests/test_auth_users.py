import os
import unittest
import json
from app import create_app, db
from database.db_models.user_models import User
import datetime


class AuthTestCase(unittest.TestCase):
    """Test case for the authenrication blueprint."""

    def setUp(self):
        """Set up test variables."""
        self.app = create_app(config_name="testing")
        # initialize the test client
        self.client = self.app.test_client
        # This is the user test json data with a predefined email and password
        self.user_data = {
            "email": "example1@mail.com",
            "password": "password",
            "username": "example1",
            "phone_number": "09067582433",
            "confirm_password": "password"
        }
        # This is the user test json data with a predefined email, password and confirmed = True
        self.confirmed_user_data = {
            "email": "example2@mail.com",
            "password": "password",
            "username": "example2",
            "phone_number": "09067582777",
            "confirm_password": "password"
        }

        with self.app.app_context():
            # Create all tables
            db.session.close()
            db.drop_all()
            db.create_all()
            user_1 = User(email="example3@mail.com", password="password", username="example3",
                          phone_number="09067582999", confirmed=False, firstname='', lastname='')
            user_2 = User(email="example2@mail.com", password="password", username="example2",
                          phone_number="09067582777", confirmed=True, firstname='', lastname='')

            user_1.save()
            user_2.save()

    def test_registration(self):
        """Test user registeration works correctly."""
        res = self.client().post('/api/auth/signup', data=self.user_data)
        # Get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains a success message and a 201 status code
        self.assertEqual(
            result['message'], "Registration Successful. An email has been sent to this email: %s. Please confirm your email to proceed." % (self.user_data['email']))
        self.assertEqual(res.status_code, 201)
        self.assertTrue(result['access_token'])

    def test_invalid_email_input(self):
        """Test for when user input a wrong email format."""
        self.user_data['email'] = 'example'
        res = self.client().post('/api/auth/signup', data=self.user_data)
        # Get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains a error message and a 400 status code
        self.assertEqual(result['message'], "Invalid Email Inputed")
        self.assertEqual(res.status_code, 400)

    def test_empty_email_input(self):
        """Test for when a user leave the email field empty."""
        self.user_data['email'] = ''
        res = self.client().post('/api/auth/signup', data=self.user_data)
        # Get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains a error message and a 400 status code
        self.assertEqual(result['message'], "This field is required.")
        self.assertEqual(res.status_code, 400)

    def test_invalid_password_input(self):
        """Test for when a user input a password lesser than 6 characters"""
        self.user_data['password'] = 'passw'
        self.user_data['confirm_password'] = 'passw'
        res = self.client().post('/api/auth/signup', data=self.user_data)
        # Get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains a error message and a 400 status code
        self.assertEqual(result['message'],
                         "Password should be greater than 6 characters")
        self.assertEqual(res.status_code, 400)

    def test_invalid_password_match(self):
        """Test for when a user input a password that does not match the confirm_password"""
        self.user_data['password'] = 'password222'
        res = self.client().post('/api/auth/signup', data=self.user_data)
        # Get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains a error message and a 400 status code
        self.assertEqual(result['message'],
                         "Oops! Sorry. The passwords you inputted are not the same.")
        self.assertEqual(res.status_code, 400)

    def test_invalid_phone_number_input(self):
        """Test for when a user input a phone_number lesser than 8 characters"""
        self.user_data['phone_number'] = '0802347'
        res = self.client().post('/api/auth/signup', data=self.user_data)
        # Get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains a error message and a 400 status code
        self.assertEqual(result['message'],
                         "Phone number should be greater than 8 characters")
        self.assertEqual(res.status_code, 400)

    def test_invalid_phone_number_input(self):
        """Test for when a user input a phone number that contains any other character apart from numbers """
        self.user_data['phone_number'] = 'this080347653'
        res = self.client().post('/api/auth/signup', data=self.user_data)
        # Get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains a error message and a 400 status code
        self.assertEqual(result['message'],
                         "Phone numbers must all contain numbers")
        self.assertEqual(res.status_code, 400)

    def test_invalid_username_input(self):
        """Test for when a user input a username lesser than 2 characters"""
        self.user_data['username'] = 'p'
        res = self.client().post('/api/auth/signup', data=self.user_data)
        # Get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains a error message and a 400 status code
        self.assertEqual(result['message'],
                         "Username should be greater than 2 characters")
        self.assertEqual(res.status_code, 400)

    def test_already_registered_user(self):
        """Test that a user cannot be registered twice."""
        res = self.client().post('/api/auth/signup', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        second_res = self.client().post('/api/auth/signup', data=self.user_data)
        self.assertEqual(second_res.status_code, 409)
        # get the results returned in json format
        result = json.loads(second_res.data.decode())
        self.assertEqual(
            result['message'], 'Email or phone number is already been used by an existing user. Please try again.')

    """ Test for LoginView Controller """

    def test_user_login(self):
        """Test registered user can login."""
        self.user_login_data = {
            'email': 'example3@mail.com',
            'password': 'password'
        }
        login_res = self.client().post('/api/auth/login', data=self.user_login_data)

        # get the results in json format
        result = json.loads(login_res.data.decode())

        # Test that the response contains success message
        self.assertEqual(result['message'], "Welcome! You are now logged in.")
        # Assert that the status code is equal to 200
        self.assertEqual(login_res.status_code, 200)
        self.assertTrue(result['access_token'])
    
    def test_invalid_email_input(self):
        """Test for when user input a wrong email format."""
        self.user_data['email'] = 'example@gmail.'
        res = self.client().post('/api/auth/login', data=self.user_data)
        # Get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains a error message and a 400 status code
        self.assertEqual(result['message'], "Invalid Email Inputed")
        self.assertEqual(res.status_code, 400)


    def test_invalid_user_login_input(self):
        """Test if email field is empty"""
        # res = self.client().post('/api/auth/signup', data=self.user_data)
        # self.assertEqual(res.status_code, 201)
        self.user_login_data = {
            'email': 'example3@mail.com',
            'password': 'password'
        }
        self.user_login_data['email'] = ''
        login_res = self.client().post('/api/auth/login', data=self.user_login_data)

        # get the results in json format
        result = json.loads(login_res.data.decode())
        # Test that the response contains success message
        self.assertEqual(result['message'], "This field is required.")
        # Assert that the status code is equal to 400
        self.assertEqual(login_res.status_code, 400)

    def test_non_registered_user_login(self):
        """Test non registered users cannot login."""
        # define a dictionary to represent an unregistered user
        self.not_a_user = {
            'email': 'not_a_user@example.com',
            'password': 'nopenotauser'
        }
        # send a POST request to /auth/login with the data above
        res = self.client().post('/api/auth/login', data=self.not_a_user)
        # get the result in json
        result = json.loads(res.data.decode())
        # assert that this response must contain an error message
        # and an error status code 401(Unauthorized)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(
            result['message'], "Invalid credentials, Please try again.")

    """ Test Email Confirmation View Controller """

    def test_email_confirmation_route_valid_token(self):
        """Test for email confirmation mail been sent"""
        self.email_user_data = {
            "email": "example@mail.com",
            "password": "password",
            "username": "example",
            "phone_number": "09067582555",
            "confirm_password": "password"
        }
        res = self.client().post('/api/auth/signup', data=self.email_user_data)

        email_token = User.generate_email_token(self, email='example@mail.com')

        email_res = self.client().get(
            '/api/auth/email-confirmation/?emailtoken='+email_token.decode())

        # Get the results returned in json format
        result = json.loads(email_res.data.decode())

        # assert that this response must contain an error message
        # and an error status code 200(Successful)
        self.assertEqual(
            result['message'], "Your have confirmed your accounts. Thanks!"
        )
        self.assertEqual(email_res.status_code, 200)

    def test_email_already_confirmed(self):
        """Test for email already confirmed by user"""
        email_token = User.generate_email_token(
            self, email='example2@mail.com')

        email_res = self.client().get(
            '/api/auth/email-confirmation/?emailtoken='+email_token.decode())

        # Get the results returned in json format
        result = json.loads(email_res.data.decode())
        # assert that this response must contain an error message
        # and an error status code 409(Conflit)
        self.assertEqual(
            result['message'], "This Account has already been confirmed."
        )
        self.assertEqual(email_res.status_code, 409)

    """ Test Re-verify Email Confirmation View Controller """

    def test_for_resend_email_confirm_link(self):
        """Test for resend email confirmation mail when user request for it"""
        self.user_data['email'] = 'example3@mail.com'
        res = self.client().post('/api/auth/reverify-email', data=self.user_data)
        email_token = User.generate_email_token(self, email=self.user_data)

        # Get the results returned in json format
        result = json.loads(res.data.decode())

        # assert that this response must contain an response
        # and a status code 200(Success)
        self.assertEqual(
            result['message'], 'An email confirmation link has been sent to this email: %s' % (
                "example3@mail.com")
        )
        self.assertEqual(res.status_code, 200)

    def test_for_non_existing_email(self):
        """Test for if email passed during requesting for re-verification link exist in the database"""
        self.user_data['email'] = 'emaildoes@notexist.com'
        res = self.client().post('/api/auth/reverify-email', data=self.user_data)

        # Get the results returned in json format
        result = json.loads(res.data.decode())

        # assert that this response must contain a error response
        # and an error status code 404(Resource not found)
        self.assertEqual(
            result['message'], "The email entered is not registered."
        )
        self.assertEqual(res.status_code, 404)

    def test_for_empty_email_input(self):
        """Test if email inputed by user is empty"""
        self.user_data['email'] = ''
        res = self.client().post('/api/auth/reverify-email', data=self.user_data)

        # Get the results returned in json format
        result = json.loads(res.data.decode())

        # assert that this response must contain a error response
        # and an error status code 400(Bad Request)
        self.assertEqual(
            result['message'], 'This field is required'
        )
        self.assertEqual(res.status_code, 400)

    def test_for_invalid_email_inputted(self):
        """Test if email inputted by user is a valid email address"""
        self.user_data['email'] = 'myinvalidemail@'
        res = self.client().post('/api/auth/reverify-email', data=self.user_data)

        # Get the results returned in json format
        result = json.loads(res.data.decode())

        # assert that this response must contain a error response
        # and an error status code 400(Bad Request)
        self.assertEqual(
            result['message'], 'Oops! You have inputed an invalid email.'
        )
        self.assertEqual(res.status_code, 400)

    def test_for_if_email_is_already_confirmed(self):
        """Test if user is already confirmed when user request for a re-verification email link"""
        res = self.client().post('/api/auth/reverify-email', data=self.confirmed_user_data)

        # Get the results returned in json format
        result = json.loads(res.data.decode())

        # assert that this response must contain a response
        # and an error status code 409(Conflit)
        self.assertEqual(
            result['message'], 'This email has already been verified.'
        )
        self.assertEqual(res.status_code, 409)

    """ Test forget password view controller """

    def test_for_empty_email_input(self):
        """Test for empty email input"""
        self.user_data['email'] = ''
        res = self.client().post('/api/auth/forget-password', data=self.user_data)

        # Get the results returned in json format
        result = json.loads(res.data.decode())

        # assert that this response must contain a response
        # and an error status code 409(Conflit)
        self.assertEqual(
            result['message'], 'This field is required'
        )
        self.assertEqual(res.status_code, 400)

    def test_for_invalid_email_inputted(self):
        """Test for invalid email input"""
        self.user_data['email'] = 'myinvalidemail@'
        res = self.client().post('/api/auth/forget-password', data=self.user_data)

        # Get the results returned in json format
        result = json.loads(res.data.decode())

        # assert that this response must contain a response
        # and an error status code 409(Conflit)
        self.assertEqual(
            result['message'], 'Oops! You have inputed an invalid email.'
        )
        self.assertEqual(res.status_code, 400)

    def test_for_non_existing_email(self):
        """Test for email that does not exist in the database"""
        self.user_data['email'] = 'non_existing@email.com'
        res = self.client().post('/api/auth/forget-password', data=self.user_data)

        # Get the results returned in json format
        result = json.loads(res.data.decode())

        # assert that this response must contain a response
        # and an error status code 409(Conflit)
        self.assertEqual(
            result['message'], 'This email is not registered.'
        )
        self.assertEqual(res.status_code, 404)

    def test_password_reset_link_sent(self):
        """Test for reset password link sent to user"""
        res = self.client().post('/api/auth/forget-password', data=self.confirmed_user_data)

        # Get the results returned in json format
        result = json.loads(res.data.decode())

        # assert that this response must contain a response
        # and an error status code 409(Conflit)
        self.assertEqual(
            result['message'], 'A password reset link has been sent to this email: %s' % (
                'example2@mail.com')
        )
        self.assertEqual(res.status_code, 200)

    """ Test for Reset password controller """

    def test_for_empty_password_field(self):
        """Test for empty password field."""
        self.user_data['password'] = ''
        res = self.client().post('/api/auth/reset-password/', data=self.user_data)

        # Get the results returned in json format
        result = json.loads(res.data.decode())

        # assert that this response must contain a response
        # and an error status code 409(Conflit)
        self.assertEqual(
            result['message'], 'This field is required.'
        )
        self.assertEqual(res.status_code, 400)

    def test_for_empty_confirm_password_field(self):
        """Test for empty confirm password input"""
        self.user_data['confirm_password'] = ''
        res = self.client().post('/api/auth/reset-password/', data=self.user_data)

        # Get the results returned in json format
        result = json.loads(res.data.decode())

        # assert that this response must contain a response
        # and an error status code 409(Conflit)
        self.assertEqual(
            result['message'], 'This field is required.'
        )
        self.assertEqual(res.status_code, 400)

    def test_for_password_match(self):
        """Test for incorrect password matching"""
        self.user_data['password'] = 'password2'
        res = self.client().post('/api/auth/reset-password/', data=self.user_data)

        # Get the results returned in json format
        result = json.loads(res.data.decode())

        # assert that this response must contain a response
        # and an error status code 409(Conflit)
        self.assertEqual(
            result['message'], 'Oops! Sorry. The passwords you inputted are not the same.'
        )
        self.assertEqual(res.status_code, 400)

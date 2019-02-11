import os
from flask import request, jsonify
from flask_restful import Resource
from validate_email import validate_email
from helpers.email import send_email
from helpers.email_template import email_template
from database.db_models.user_models import User


class RegistrationView(Resource):
    # This register a user
    def post(self):
        email_input = request.form.get('email').lstrip()
        email = email_input.lower()

        # Remove whitespaces from left and right
        username_input = request.form.get('username').lstrip()
        username = username_input.lower()

        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        phone_number = request.form.get('phone_number').lstrip()
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        confirmed = False

        # validate email as a valid email address without using regex
        is_valid = validate_email(email)

        # validate user inputs
        if email == '' or password == '' or phone_number == '' or username == '':
            response = jsonify({
                'message': 'This field is required.'
            })
            response.status_code = 400
            return response
        if len(password) < 6:
            response = jsonify({
                'message': 'Password should be greater than 6 characters'
            })
            response.status_code = 400
            return response
        if password != confirm_password:
            response = jsonify({
                'message': 'Oops! Sorry. The passwords you inputted are not the same.'
            })
            response.status_code = 400
            return response

        # This validate if what is inputed are all numbers
        if phone_number.isnumeric() == False:
            response = jsonify({
                'message': 'Phone numbers must all contain numbers'
            })
            response.status_code = 400
            return response
        if len(phone_number) < 8:
            response = jsonify({
                'message': 'Phone number should be greater than 8 characters'
            })
            response.status_code = 400
            return response
        if len(username) < 2:
            response = jsonify({
                'message': 'Username should be greater than 2 characters'
            })
            response.status_code = 400
            return response
        if is_valid == False:
            response = jsonify({
                'message': 'Invalid Email Inputed'
            })
            response.status_code = 400
            return response
        else:

            password_hash = User.generate_password_hash(self, password)

            # Find user email in the database
            user = User.query.filter_by(
                email=email, phone_number=phone_number).first()

            # If User is not found do this
            if user == None:
                try:
                    # Register the user
                    email = email
                    password = password_hash
                    phone_number = phone_number
                    firstname = firstname
                    lastname = lastname
                    confirmed = confirmed
                    user = User(
                        email=email,
                        password=password,
                        phone_number=phone_number, firstname=firstname, lastname=lastname,
                        username=username,
                        confirmed=confirmed
                    )
                    user.save()

                    # Generate Authentication token for the user using the user_id
                    access_token = user.generate_token(user.id)

                    auth_user_email = user.generate_email_token(user.email)

                    confirm_url = 'http://%s/api/auth/email-confirmation/?emailtoken=%s' % (os.getenv(
                        'HOST_URL'), auth_user_email.decode())

                    html = email_template(confirm_url)

                    subject = "Please confirm your mail"

                    send_email(user.email, subject, html)

                    response = jsonify({
                        'email': user.email,
                        'password': user.password,
                        'username': user.username,
                        'access_token': access_token.decode(),
                        'email_validation': user.confirmed,
                        'message': 'Registration Successful. An email has been sent to this email: ' + user.email + '. Please confirm your email to proceed.'
                    })

                    # return a response notifying the user that they registered
                    response.status_code = 201
                    return response

                except Exception as e:
                    # An error occured, therefore return a string message containing the error
                    response = jsonify({
                        'message': str(e),
                    })
                    response.status_code = 409
                    return response
            else:
                # There is an existing user. We don't want to register users twice
                # Return a message to the user telling them that the email, username or phone number is been used by another user
                response = jsonify({
                    'message': 'Email or phone number is already been used by an existing user. Please try again.'
                })

                response.status_code = 409
                return response

import os
from flask import request, jsonify
from flask_restful import Resource
from validate_email import validate_email
from helpers.email import send_email
from helpers.email_template import email_template
from database.db_models.user_models import User


class ReverifyEmailConfirmationView(Resource):
    def post(self):
        email_input = request.form.get('email').lstrip()
        email = email_input.lower()

        is_valid_email = validate_email(email)

        if email == '':
            response = jsonify({
                'message': 'This field is required'
            })
            response.status_code = 400
            return response
        if is_valid_email == False:
            response = jsonify({
                'message': 'Oops! You have inputed an invalid email.'
            })
            response.status_code = 400
            return response

        user = User.query.filter_by(email=email).first()

        if user == None:
            response = jsonify({
                'message': 'The email entered is not registered.'
            })
            response.status_code = 404
            return response
        elif user.confirmed == True:
            response = jsonify({
                'message': 'This email has already been verified.'
            })
            response.status_code = 409
            return response
        else:
            email_token = user.generate_email_token(user.email)

            confirm_url = 'http://%s/api/auth/email-confirmation/?emailtoken=%s' % (os.getenv(
                'HOST_URL'), email_token.decode())

            html = email_template(confirm_url)

            subject = "Please confirm your mail"

            send_email(user.email, subject, html)

            response = jsonify({
                'message': 'An email confirmation link has been sent to this email: %s' % (user.email)
            })
            response.status_code = 200
            return response

import os
from flask import request, jsonify
from flask_restful import Resource
from validate_email import validate_email
from helpers.email import send_email
from helpers.forget_password_template import forget_password_template
from database.db_models.user_models import User


class ForgetPasswordView(Resource):
    def post(self):
        # .lstrip() Removes all whitespaes
        email_input = request.form.get('email').lstrip()
        email = email_input.lower()

        is_valid_email = validate_email(email)

        # User input validations
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
                'message': 'This email is not registered.'
            })
            response.status_code = 404
            return response
        else:
            # Generate password token
            password_reset_token = user.generate_email_token(user.email)
            # Password Reset Link
            password_confirm_url = 'http://%s/api/auth/reset-password/?resettoken=%s' % (os.getenv(
                'HOST_URL'), password_reset_token.decode())
            # Password reset template
            password_template = forget_password_template(password_confirm_url)

            subject = "Password Reset Link"
            # Call the method that sends the mail inserting all arguments
            send_email(user.email, subject, password_template)

            response = jsonify({
                'message': 'A password reset link has been sent to this email: %s' % (user.email)
            })
            response.status_code = 200
            return response

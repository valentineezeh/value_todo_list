from flask import request, jsonify
from flask_restful import Resource
from datetime import datetime
from database.db_models.user_models import User


class ResetPasswordView(Resource):
    """This method handles the reset password functionality"""

    def post(self):
        # Get all required variables from the user
        password_token = request.args.get('resettoken')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validates User input
        if password == None or password == '':
            response = jsonify({
                'message': "This field is required."
            })
            response.status_code = 400
            return response
        if confirm_password == None or confirm_password == '':
            response = jsonify({
                'message': "This field is required."
            })
            response.status_code = 400
            return response

        if password != confirm_password:
            response = jsonify({
                'message': 'Oops! Sorry. The passwords you inputted are not the same.'
            })
            response.status_code = 400
            return response
        if password_token == None or password_token == '':
            response = jsonify({
                'message': 'You are not authorise to view this page.'
            })
            response.status_code = 403
            return response
        # Decode the token that is passed in the password reset link
        password_token_decode = User.decode_email_token(password_token)

        # Find user with the email in the database
        user = User.query.filter_by(email=password_token_decode).first()

        # Hash the new password gotten from user
        hash_password = user.generate_password_hash(password)

        # Check if the hash password is the same with password provided
        check_password_validity = user.check_password_validation(
            hash_password.decode(), password)

        if user and check_password_validity:
            # If all conditions are met update the user details with the new password
            user.password = hash_password.decode()
            user.save()
            # respond with a success message
            response = jsonify({
                'message': 'Password successfully updated, you can now login with your new password.'
            })
            response.status_code = 200
            return response
        else:
            # else return an error message
            response = jsonify({
                'message': 'Invalid Token.'
            })
            response.status_code = 500
            return response

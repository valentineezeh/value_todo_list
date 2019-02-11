from flask import request, jsonify
from flask_restful import Resource
from datetime import datetime
from database.db_models.user_models import User


class EmailConfirmationView(Resource):
    """This method handles the functionality that confirms the user email address"""

    def get(self):
        # Get token as params from the url
        token = request.args.get('emailtoken')
        # Decode the token by calling the decode_email_token method
        email = User.decode_email_token(token)
        # search through the database to find email
        user = User.query.filter_by(email=email).first()

        # If user is not yet confirm then confirm User
        if user.confirmed == False:
            try:
                user.confirmed = True
                user.confirmed_on_date = datetime.now()
                user.save()
                response = jsonify({
                    'message': 'Your have confirmed your accounts. Thanks!'
                })
                response.status_code = 200
                return response
            except Exception as e:
                # An error occured, therefore return a string message containing the error
                response = jsonify({
                    'message': str(e),
                })
                response.status_code = 500
                return response

        # If user is already confirmed return a message to the user
        else:
            response = jsonify({
                'message': 'This Account has already been confirmed.'
            })
            response.status_code = 409
            return response

from flask import Blueprint
from flask_restful import Api
from controllers.auth_controllers.Sign_up import RegistrationView
from controllers.auth_controllers.Sign_in import LoginView
from controllers.auth_controllers.Confirm_email import EmailConfirmationView
from controllers.auth_controllers.Reverify_email import ReverifyEmailConfirmationView
from controllers.auth_controllers.Forget_password import ForgetPasswordView
from controllers.auth_controllers.Reset_password import ResetPasswordView


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Routes
api.add_resource(RegistrationView, '/auth/signup')
api.add_resource(LoginView, '/auth/login')
api.add_resource(EmailConfirmationView, '/auth/email-confirmation/')
api.add_resource(ReverifyEmailConfirmationView, '/auth/reverify-email')
api.add_resource(ForgetPasswordView, '/auth/forget-password')
api.add_resource(ResetPasswordView, '/auth/reset-password/')

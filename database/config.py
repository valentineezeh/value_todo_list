# /instance/config.py

import os
from dotenv import load_dotenv

# Load up the dotenv in other to use env variables
App_Root = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(App_Root, '.env')
load_dotenv(dotenv_path)

# Main configuration


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL')

# Development database config


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL')

# Testing database config


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL')
    DEBUG = True

# Staging database config


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True

# Production database config


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}

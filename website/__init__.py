# Import necessary Flask modules and packages
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


# Initialize the SQLAlchemy database
db = SQLAlchemy()
DB_NAME = "database.db"

# Function to create the Flask application
def create_app():
    app = Flask(__name__)

    # Set the Flask application's secret key for security
    app.config['SECRET_KEY'] = 'how you doin keep it movin'

    # Configure the SQLAlchemy database URI to use SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # Import and register Blueprints for different parts of the application
    from .views import views
    from .auth import auth
    from .f1 import f1
    

    # Register the Blueprints with appropriate URL prefixes
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(f1, url_prefix='/f1')  # Register the F1 blueprint

    # Import the User model and create the database tables
    from .models import User
    with app.app_context():
        db.create_all()

    # Initialize the LoginManager for handling user sessions
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Function to load a user based on their ID
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# Function to create the database if it does not exist
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

from flask import Flask
from .config import Config 
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager 

db = SQLAlchemy() 
login = LoginManager() 
login.login_view = 'routes.login' 

from .models import User 

@login.user_loader
def load_user(id):
    return User.query.get(int(id)) 

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login.init_app(app)

    from . import models 
    
    from . import routes
    app.register_blueprint(routes.bp)

    with app.app_context():
        db.create_all() 
        
        from .dummy_data import insert_dummy_quiz_data
        insert_dummy_quiz_data()

    return app
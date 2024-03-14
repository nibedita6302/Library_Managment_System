import os
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from config import LocalDevelopmentConfig, StageConfig
from application.database import db
from flask_security import Security
from security import datastore
from application.jobs import workers
#from sqlalchemy.orm import scoped_session, sessionmaker
from flask_login import LoginManager
from flask_security import utils
from flask_sse import sse
from application.redis_cache import get_cache

app = None
api = None
celery = None
cache = None

def create_app():
    app = Flask(__name__)
    print(os.getenv('ENV', "development"))
    if os.getenv('ENV', "development") == "production":
      raise Exception("Currently no production config is setup.")
    elif os.getenv('ENV', "development") == "stage":
      print("Staring  Stage")
      app.config.from_object(StageConfig)
      print("pushed config")
    else:
      print("Staring Local Development")
      app.config.from_object(LocalDevelopmentConfig)
      print("pushed config")
    
    app.app_context().push()
    db.init_app(app)
    print("DB Init complete")
    
    app.app_context().push()
    
    login_manager.init_app(app)

    app.security = Security(app, datastore)   # setting up flask security for Users

    api = Api(app, prefix='/api')
    app.app_context().push()   
    CORS(app, supports_credentials=True)
    
    ## Create Celery instance
    celery = workers.celery

    celery.conf.update(                                       ## Update with configuration
        broker_url = app.config["CELERY_BROKER_URL"],
        result_backend = app.config["CELERY_RESULT_BACKEND"],
        timezone = 'Asia/Kolkata'
    )
    celery.Task = workers.ContextTask

    app.app_context().push()
    print('Celery Initiated...')

    cache = get_cache()     # setting up Cache
    cache.init_app(app)
    app.app_context().push()
    print('Cache Setup...')
    return app, api, celery

login_manager = LoginManager()

app ,api, celery= create_app()
print("Create app complete")

## Import models in main
from application.models.users import Users, Role, RoleUsers
from application.models.books import Books, Sections, Author, AuthorBook
from application.models.user_book_activity import UserBook, UserActivity
from application.models.reviews import Reviews
## Import controllers in main
from application.controller import login

from utils.default_data import create_default_data

with app.app_context():
    db.create_all()
    print('All models created.')
    # create default roles and librarian
    create_default_data(librarian_email='nibedita.6302@gmail.com', yourname='Nibedita C.')
    print('All default data created.')

@login_manager.user_loader
def load_user(user_id):
   return Users.query.get(int(user_id)) 

## Setup all APIs
from application.api.configure_routes import config_all_resource
config_all_resource(api) 

if __name__ == '__main__':
  # Run the Flask app
  app.run(host='localhost',port=8000, debug=True)
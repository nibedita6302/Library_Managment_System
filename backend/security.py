from flask_security import SQLAlchemySessionUserDatastore
from application.models.users import Users, Role
from application.database import db

# Setup Flask-Security
datastore = SQLAlchemySessionUserDatastore(db.session, Users, Role)


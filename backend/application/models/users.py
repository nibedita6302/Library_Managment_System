from ..database import db 
from .books import UserBook
from utils.credentials import check_password
from flask_security import UserMixin, RoleMixin
from sqlalchemy import Integer, String, Boolean, DateTime, Float, ForeignKey,  Column

RoleUsers = db.Table('role_user',
    Column('user_id', Integer(), ForeignKey('users.id'), primary_key=True), # users
    Column('role_id', Integer(), ForeignKey('role.id'), primary_key=True) # role
)

class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer(), autoincrement=True, primary_key=True)
    email = Column(String(), unique=True, nullable=False)
    name = Column(String(), nullable=False)
    password = Column(String(255), nullable=False)
    active = Column(Boolean, nullable=False, default=True) 
    fs_uniquifier = Column(String(255), unique=True) 
    #relationships
    roles = db.relationship('Role', secondary=RoleUsers, backref='assignedTo', cascade='all, delete')
    user_book = db.relationship('UserBook', back_populates='issuer', cascade='all, delete')
    
    def match_password(self, password):
        return  check_password(password, self.password)
    
class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(20), unique=True, nullable=False)
    description = Column(String(200))


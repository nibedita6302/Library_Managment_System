from flask_restful import Resource, fields, marshal, reqparse
from application.database import db
from security import datastore
from flask import request, jsonify
from flask_login import current_user
from flask_security import auth_required, roles_required

from application.models.users import Users, RoleUsers
from utils.credentials import *

class UserRegister(Resource):    
    ## Register new User
    def post(self): 
        jsonData = request.get_json()
        ## Check if all fields are filled
        if ('email' not in jsonData) or ('name' not in jsonData) or ('password' not in jsonData):
            return {'message': {'error': 'All fields are compulsory'}}, 400
        
        ## Check if email is NOT in Users database
        if not Users.query.filter_by(email=jsonData['email']).first():
            ## If NOT valid email (utils)
            if not validate_email(jsonData['email']):
                return {'message': {'error': 'Invalid Email'}}, 400
            ## If NOT valid password (utils)
            elif not validate_password(jsonData['password']):
                return {'message': {'error': 'Password must have atleast one Upper Case Letter,\
                                     Lower Case Letter, Special Character and a number.\
                                    Password must have 8 or more characters.'}}, 400
            else:
                user = datastore.create_user(email=jsonData['email'], name=jsonData['name'],
                                           password=hash_password(jsonData['password']))
                datastore.add_role_to_user(user, 'user')
                db.session.add(user)
                db.session.commit()
                return {'message': {'success': 'Registration Successfull, Login Now!'}}, 200
        # Email present in Users database
        return {'message': {'error': 'Email already exists.'}}, 400

## EXCEPT 'Librarian', for 'User' only!
class UserProfile(Resource):
    @auth_required('token')
    def get(self):     ## View user details
        user = Users.query.get(current_user.id)
        if user:
            if user.roles[0].name == 'librarian':
                return {'message': {'error': 'Confidential Information'}}, 401
            else:
                user_books = user.user_book
                current_issues, total_downloads = 0, 0
                for book in user_books:
                    if book.return_date is None:
                        current_issues+=1
                    if book.bought_price>0:
                        total_downloads+=1
                return {
                    'email': user.email,
                    'name': user.name,
                    'id': user.id,
                    'total_issues': len(user_books),
                    'current_issues': current_issues,
                    'total_downloads': total_downloads 
                }
            
        return {'message': {'error': 'User does not exists or not logged in.'}}, 400 

    @auth_required('token')
    @roles_required('user')
    def put(self):     ## Update existing user details
        user = Users.query.get(current_user.id)
        if user:
            if user.roles[0].name == 'librarian':
                return {'message': {'error': 'Unauthorized Access'}}, 401
            else:
                jsonData = request.get_json()
                if len(jsonData)>0:
                    if 'email' in jsonData:                                                     ## Check if email in form 
                        if Users.query.filter_by(email=jsonData['email']).first() is None:      ## Email is Unique
                            if validate_email(jsonData['email']):                               ## If valid email (utils)
                                user.email = jsonData['email']
                            else:
                                return {'message': {'error': 'Invalid Email'}}, 400
                        else:
                            return {'message': {'error': 'Email already exists'}}, 400          ## Check for name in form
                    if 'name' in jsonData and jsonData['name'].strip()!='':
                        user.name = jsonData['name']
                else:                                                                           ## All fields empty
                    return {'message': {'error': 'Atleast one field needs to be filled!'}}, 400        
            
            db.session.commit()
            return {'message': {'success': 'Successfull Update!'}}, 200
        
        return {'message': {'error': 'User does not exists or not logged in.'}}, 400 

    @auth_required('token')
    @roles_required('user')
    def delete(self, confirm):     ## Delete existing user 
        user = Users.query.get(current_user.id)
        if user:
            if user.roles[0].name == 'librarian':
                return {'message': {'error': 'Unauthorized Delete Operation'}}, 401
            elif confirm:
                user_role = db.session.query(RoleUsers).filter_by(user_id=current_user.id).first()
                print(user_role)
                db.session.delete(user)
                #db.session.delete(user_role)
                db.session.commit()
                return {'message': {'success': 'Deleted User'}}, 200
            else:
                return {'message': {'success': 'Canceled Delete'}}, 200
        
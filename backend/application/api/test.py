from flask_restful import Resource, fields, marshal, reqparse
from application.database import db
from security import datastore
from flask import request, jsonify
# from flask_login import login_user, logout_user, current_user
from flask_security import auth_required, roles_required

class Test(Resource):
    def get(self, num):
        return {'num':num}
    
    def get(self, num, add):
        return {'new num':num+add}
import os
from flask_restful import Resource, fields, marshal, reqparse
from application.database import db
from security import datastore
from flask import request, jsonify, current_app as app
from flask_login import current_user
from flask_security import auth_required, roles_required

from application.models.user_book_activity import UserBook, UserActivity
from application.models.books import *

class IssueBook(Resource):
    @auth_required('token')
    @roles_required('user')
    def post(self, book_id):        ## Request for book issue 
        pass

    @auth_required('token')
    @roles_required('user')
    def put(self, book_id):         ## Return book 
        pass

    @auth_required('token')
    @roles_required('user')
    def get(self, book_id):         ## Read Book Only
        pass


class UserStats(Resource):
    @auth_required('token')
    @roles_required('user')
    def get(self):
        ## Section Wise Distribution

        ## Favourite Author

        ## Ranking in different book reads
        pass